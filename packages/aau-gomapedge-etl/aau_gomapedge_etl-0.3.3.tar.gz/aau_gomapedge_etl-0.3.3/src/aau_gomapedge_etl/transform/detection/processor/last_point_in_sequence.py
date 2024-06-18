from duckdb import DuckDBPyConnection, DuckDBPyRelation

from .protocol import Processor


def group_by_threshold(distances: list[float | None], threshold: float) -> list[int]:
    last_key = 0
    rv = []
    for distance in distances:
        if distance is None:
            last_key = 1
        elif distance > threshold:
            last_key += 1
        rv.append(last_key)
    return rv


class LastPointInSequence(Processor):

    def __init__(self, con: DuckDBPyConnection) -> None:
        super().__init__()
        self.__con = con
        self.__con.create_function(
            "group_by_threshold", group_by_threshold, side_effects=True
        )

    def process(self, tbl: DuckDBPyRelation) -> DuckDBPyRelation:
        self.__con.execute(
            """
CREATE OR REPLACE TABLE detection AS
    WITH compare_to_prev AS (
        SELECT id,
               trip_no,
               img_seq_id,
               heading,
               width,
               height,
               score,
               cls,
               location,
               ST_Distance(location, lag(location) OVER w)   AS dist_diff,
               lag(width * height) OVER w / (width * height) AS size_diff_pct
        FROM tbl
        WINDOW w AS (PARTITION BY trip_no, cls ORDER BY trip_no, cls, img_seq_id, id) -- Maybe trip_no and cls can be removed
    ), diff_collection AS (
        SELECT list(id            ORDER BY trip_no, cls, img_seq_id, id) AS id_list,
               list(dist_diff     ORDER BY trip_no, cls, img_seq_id, id) AS dist_diff_list,
               list(size_diff_pct ORDER BY trip_no, cls, img_seq_id, id) AS size_diff_pct_list
        FROM compare_to_prev
    ), diff_key_collection AS (
        SELECT id_list,
               group_by_threshold(dist_diff_list, 50)       AS dist_grp_key_list,
               group_by_threshold(size_diff_pct_list, 0.85) AS size_grp_key_list,
        FROM diff_collection
    ), diff_key AS (
        SELECT UNNEST(id_list)           AS id,
               UNNEST(dist_grp_key_list) AS dist_grp_key,
               UNNEST(size_grp_key_list) AS size_grp_key
        FROM diff_key_collection
    ), last_location_collection AS (
        SELECT list(id)       AS id_list,
               last(location) AS last_location
        FROM tbl
            INNER JOIN diff_key USING (id)
        GROUP BY trip_no, cls, dist_grp_key, size_grp_key
    ), last_location AS (
        SELECT UNNEST(id_list) AS id,
           last_location
        FROM last_location_collection
    )
    SELECT id,
           trip_no,
           img_seq_id,
           heading,
           width,
           height,
           score,
           cls,
           last_location AS location
    FROM tbl
        INNER JOIN last_location USING (id);
""",
        )

        tbl = self.__con.table("detection")
        return tbl
