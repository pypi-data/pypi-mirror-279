from duckdb import DuckDBPyConnection, DuckDBPyRelation

from .protocol import Aggregator


class LastPointInDirection(Aggregator):
    def __init__(self, con: DuckDBPyConnection) -> None:
        super().__init__()
        self.__con = con

    def aggregate(self, tbl: DuckDBPyRelation) -> DuckDBPyRelation:
        self.__con.execute(
            """
CREATE OR REPLACE TABLE aggregation AS
    with preprocess_heading AS (
        SELECT cls,
               cid,
               radians((median(heading) + 180) % 360) AS reversed_radian_heading
        FROM tbl
        GROUP BY cls, cid
    ), direction_vector_cte AS (
        SELECT cls,
               cid,
               [cos(reversed_radian_heading), sin(reversed_radian_heading)] AS direction_vector
        FROM preprocess_heading
    ), dot_product_cte AS (
        SELECT id,
               cls,
               cid,
               score,
               heading,
               location,
               list_dot_product(direction_vector, [ST_Y(location), ST_X(location)]) AS dot_product,
        FROM tbl
            INNER JOIN direction_vector_cte USING (cls, cid)
    )
    SELECT cls,
           list(id ORDER BY id)                                     AS ids,
           median(heading)                                          AS heading,
           median(score)                                            AS score,
           ST_GeomFromWKB(arg_max(ST_AsWKB(location), dot_product)) AS location
    FROM dot_product_cte
    GROUP BY cls, cid;
"""
        )

        return self.__con.table("aggregation")
