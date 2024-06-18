from typing import Any, cast

from duckdb import DuckDBPyConnection, DuckDBPyRelation
from geopy import Location
from polars import DataFrame

from aau_gomapedge_etl.model import ReverseGeocoder


def __get_addresses(
    trajectory: DuckDBPyRelation,
    geocoder: ReverseGeocoder,
) -> list[dict[str, Any]]:
    addresses: list[dict[str, Any]] = []
    rows = trajectory.select(
        """
trip_id,
img_seq_id,
ST_X(point) AS longitude,
ST_Y(point) AS latitude
"""
    )
    for row in rows.fetchall():
        longitude = row[2]
        latitude = row[3]
        if None in {longitude, latitude}:
            continue

        trip_id = row[0]
        seq_id = row[1]

        location = cast(
            Location | None,
            geocoder.reverse((latitude, longitude)),
        )

        address = dict[str, Any]()
        if location is not None:
            address: dict[str, Any] = location.raw["address"]

        addresses.append(
            {
                "trip_id": trip_id,
                "img_seq_id": seq_id,
                "country": address.get("country"),
                "country_code": address.get("country_code"),
                "region": address.get("region"),
                "state": address.get("state"),
                "state_district": address.get("state_district"),
                "county": address.get("county"),
                "municipality": address.get("municipality"),
                "city": address.get("city"),
                "town": address.get("town"),
                "village": address.get("village"),
                "suburb": address.get("house_number"),
                "house_number": address.get("house_number"),
                "road": address.get("road"),
                "postcode": address.get("postcode"),
            }
        )
    return addresses


def __insert(con: DuckDBPyConnection, addresses: list[dict[str, Any]]):
    df = DataFrame(
        addresses,
        schema={
            "trip_id": int,
            "img_seq_id": int,
            "country": str,
            "country_code": str,
            "region": str,
            "state": str,
            "state_district": str,
            "county": str,
            "municipality": str,
            "city": str,
            "town": str,
            "village": str,
            "suburb": str,
            "house_number": str,
            "road": str,
            "postcode": str,
        },
    )
    con.sql("INSERT INTO address FROM df")


def extract(
    con: DuckDBPyConnection,
    trajectory: DuckDBPyRelation,
    geocoder: ReverseGeocoder,
) -> None:
    addresses = __get_addresses(trajectory, geocoder)
    __insert(con, addresses)
