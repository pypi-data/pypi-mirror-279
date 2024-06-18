from duckdb import DuckDBPyConnection, DuckDBPyRelation

from aau_gomapedge_etl.services import AngleBalancingDBSCAN

from .protocol import Grouper


class ABDBSCAN(Grouper):
    __slots__ = ["__con", "__max_dist", "__max_angle", "__min_samples"]

    def __init__(
        self,
        con: DuckDBPyConnection,
        max_dist: float,
        max_angle: float,
        min_samples: int,
    ) -> None:
        self.__con = con
        self.__max_dist = max_dist
        self.__max_angle = max_angle
        self.__min_samples = min_samples
        con.create_function("ab_dbscan", self.__cluster)

    @property
    def max_dist(self) -> float:
        return self.__max_dist

    @property
    def max_angle(self) -> float:
        return self.__max_angle

    @property
    def min_samples(self) -> int:
        return self.__min_samples

    def __cluster(self, data: list[tuple[float, float, float]]) -> list[int]:
        cluster = AngleBalancingDBSCAN(
            self.max_dist, self.max_angle, self.min_samples, degrees=True
        )
        return cluster.fit_predict(data).tolist()

    def group(self, tbl: DuckDBPyRelation) -> DuckDBPyRelation:
        self.__con.execute(
            """
CREATE OR REPLACE TABLE detection AS
    WITH data_tbl AS (
        SELECT cls,
               list(id                                        ORDER BY id) AS ids,
               list([ST_X(location), ST_Y(location), heading] ORDER BY id) AS dimensions,
        FROM tbl
        GROUP BY cls
    ), cluster_tbl AS (
        SELECT unnest(ids)                   AS id,
               unnest(ab_dbscan(dimensions)) AS cid
        FROM data_tbl
    )
    SELECT id,
           cid,
           trip_no,
           img_seq_id,
           heading,
           width,
           height,
           score,
           cls,
           location
    FROM cluster_tbl
        INNER JOIN detection USING (id);
"""
        )
        return self.__con.table("detection")
