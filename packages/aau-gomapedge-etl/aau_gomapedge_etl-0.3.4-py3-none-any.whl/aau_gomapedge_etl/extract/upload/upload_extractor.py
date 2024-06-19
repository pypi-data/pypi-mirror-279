import logging
from pathlib import Path

from duckdb import DuckDBPyConnection, DuckDBPyRelation
from yolonnx.services import Classifier

from aau_gomapedge_etl.model import ReverseGeocoder
from aau_gomapedge_etl.services.osrm_api import OSRM

from . import _addresses, _classification, _detections, _map_matching

logger = logging.getLogger("Extraction")


class UploadExtractorContext:
    def __init__(
        self,
        con: DuckDBPyConnection,
        geocoder: ReverseGeocoder,
        osrm: OSRM,
    ) -> None:
        self.__con = con
        self.__geocoder = geocoder
        self.__osrm = osrm

    def extract(
        self,
        trajectory: DuckDBPyRelation,
        detections: DuckDBPyRelation,
    ) -> None:
        if len(trajectory) == 0:
            logger.info("No trajectory data to extract")
            return

        logger.info(f"Extracting trajectory")
        self.__extract_trajectories(trajectory)
        logger.info(f"Extracting map matching")
        _map_matching.extract(self.__con, trajectory, self.__osrm)
        logger.info(f"Extracting addresses")
        _addresses.extract(self.__con, trajectory, self.__geocoder)
        if len(detections) > 0:
            logger.info(f"Extracting detections")
            _detections.extract(self.__con, detections)
            logger.info(f"Extracting classifications")
            _classification.extract(self.__con, detections)
        else:
            logger.info("No detections to extract")

    def __extract_trajectories(
        self,
        traj_tbl: DuckDBPyRelation,
    ):
        self.__con.execute(
            f"""
    INSERT INTO trajectory
        SELECT * FROM traj_tbl;
    """
        )


class UploadExtractor:
    def __init__(
        self,
        con: DuckDBPyConnection,
        users: DuckDBPyRelation,
        classifier: Classifier,
        geocoder: ReverseGeocoder,
        osrm: OSRM,
    ):
        self.__con = con
        self.__users = users
        self.__classifier = classifier
        self.__geocoder = geocoder
        self.__osrm = osrm

    def __enter__(self) -> UploadExtractorContext:
        return self.begin()

    def __exit__(self, exc_type, exc_val, exc_tb): ...

    def begin(self) -> UploadExtractorContext:
        self.__ensure_schema()

        logger.info(f"Extracting users")
        self.__extract_users()
        return UploadExtractorContext(self.__con, self.__geocoder, self.__osrm)

    def __ensure_schema(self):
        self.__con.install_extension("spatial")
        self.__con.load_extension("spatial")
        _classification.create_db_function(self.__con, self.__classifier)

        with Path(__file__).parents[2].joinpath("__sql", "extract.sql").open("rt") as f:
            self.__con.sql(f.read())

    def __extract_users(self):
        users = self.__users
        self.__con.execute(
            """
INSERT INTO user (id, creation_time, user_agent)
    SELECT * FROM users
    ON CONFLICT DO NOTHING;
"""
        )
