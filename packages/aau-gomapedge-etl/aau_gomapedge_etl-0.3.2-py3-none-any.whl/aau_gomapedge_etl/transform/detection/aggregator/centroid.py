from duckdb import DuckDBPyConnection, DuckDBPyRelation

from .protocol import Aggregator


class Centroid(Aggregator):
    def __init__(self, con: DuckDBPyConnection) -> None:
        self.__con = con

    def aggregate(self, tbl: DuckDBPyRelation) -> DuckDBPyRelation:
        return self.__con.query(
            """
SELECT cls,
       list(id ORDER BY id)                            AS ids,
       median(heading)                                 AS heading,
       median(score)                                   AS score,
       ST_Centroid(ST_Union_Agg(location ORDER BY id)) AS location
FROM tbl
GROUP BY cls, cid;
"""
        )
