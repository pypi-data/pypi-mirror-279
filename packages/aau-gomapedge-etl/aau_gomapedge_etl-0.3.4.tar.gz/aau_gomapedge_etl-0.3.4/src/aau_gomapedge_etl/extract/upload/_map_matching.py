import logging
from typing import Any

from duckdb import DuckDBPyConnection, DuckDBPyRelation
from geojson_pydantic import LineString
from polars import DataFrame, Series

from aau_gomapedge_etl.model import RouteMatch, WaypointMatch
from aau_gomapedge_etl.services import OSRM

logger = logging.getLogger("Map Matching")


def __get_gps_data(con: DuckDBPyConnection, traj_tbl: DuckDBPyRelation) -> DataFrame:
    return con.query(
        """
SELECT img_seq_id,
       array_value(ST_X(point), ST_Y(point)) AS coords,
       accuracy,
       epoch(timestamp)::INTEGER AS timestamp
FROM traj_tbl
WHERE ST_X(point) IS NOT NULL and ST_Y(point) IS NOT NULL
ORDER BY timestamp;
"""
    ).pl()


def __insert_trip(con: DuckDBPyConnection, trip_id: int, matches: list[RouteMatch]):
    for i, match in enumerate(matches, 1):
        if not isinstance(match.geometry, LineString):
            logger.warning("Map match result is not a LineString")
            continue

        data = {
            "trip_id": trip_id,
            "trip_split_id": i,
            "confidence": match.confidence,
            "distance": match.distance,
            "duration": match.duration,
            "geojson": match.geometry.model_dump_json(),
        }

        con.execute(
            """
INSERT INTO trip (trip_id, trip_split_id, confidence, distance, duration, geom)
VALUES (
    $trip_id,
    $trip_split_id,
    $confidence,
    $distance,
    $duration,
    ST_GeomFromGeoJSON($geojson)
);""",
            data,
        )


def __insert_matched_points(
    con: DuckDBPyConnection,
    trip_id: int,
    img_seq_ids: Series,
    tracepoints: list[WaypointMatch | None],
):
    f: list[dict[str, Any]] = []
    for img_seq_id, tracepoint in zip(img_seq_ids, tracepoints):
        if tracepoint is None:
            continue

        location = tracepoint.location
        f.append(
            {
                "trip_id": trip_id,
                "img_seq_id": img_seq_id,
                "trip_split_id": tracepoint.matchings_index + 1,
                "distance": tracepoint.distance,
                "longitude": location[0],
                "latitude": location[1],
            }
        )

    df = DataFrame(f)
    con.sql(
        """
INSERT INTO match
    SELECT trip_id,
           img_seq_id,
           trip_split_id,
           distance                        AS distance_to_road,
           ST_POINT2D(longitude, latitude) AS match_point
    FROM df
"""
    )


def extract(con: DuckDBPyConnection, trajectory: DuckDBPyRelation, osrm: OSRM):
    gps_data = __get_gps_data(con, trajectory)
    trip_id_tuple = trajectory.first("trip_id").fetchone()
    if trip_id_tuple is None:
        return
    trip_id: int = trip_id_tuple[0]

    response = osrm.match(
        "car",
        gps_data["coords"],
        radiuses=gps_data["accuracy"],
        timestamps=gps_data["timestamp"],
        geometries="geojson",
        gaps="ignore",
    )
    __insert_trip(con, trip_id, response.matchings)
    __insert_matched_points(con, trip_id, gps_data["img_seq_id"], response.tracepoints)
