from pathlib import Path

from duckdb import DuckDBPyConnection, DuckDBPyRelation

from .protocol import Dataloader


class DefaultDataLoader(Dataloader):
    """
    This is the default loader which loads data from parquet files.
    Headings are expected to be in degrees and relative to the movement of the camera.
    """

    def __init__(
        self,
        con: DuckDBPyConnection,
        parquet: Path,
    ) -> None:
        super().__init__()
        self.__parquet = parquet
        self.__con = con

    def load(self) -> DuckDBPyRelation:
        self.__con.execute(
            """
CREATE TABLE detection AS
    SELECT id, 
           trip_no,
           img_seq_id,
           (heading + 180) % 360 AS heading,
           width,
           height,
           score,
           cls,
           ST_Point(lat, lng) AS location
    FROM read_parquet($parquet);
""",
            parameters={
                "parquet": self.__parquet.as_posix(),
            },
        )
        return self.__con.table("detection")
