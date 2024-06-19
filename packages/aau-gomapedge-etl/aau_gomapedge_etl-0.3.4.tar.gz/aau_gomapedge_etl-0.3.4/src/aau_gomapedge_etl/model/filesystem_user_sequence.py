import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, Sequence
from uuid import UUID

from duckdb import DuckDBPyConnection, DuckDBPyRelation

from aau_gomapedge_etl.utilities import uuid_utils

from .protocols import Trip, User

logger = logging.getLogger(__name__)


class FilesystemTrip(Trip):
    __processed_file_name = ".extracted"

    def __init__(
        self,
        con: DuckDBPyConnection,
        directory: Path,
        trip_id: int,
        user_id: UUID,
        separator: str = ",",
    ) -> None:
        self.__con = con
        self.__dir = directory
        self.__trip_id = trip_id
        self.__user_id = user_id
        self.__separator = separator

    @property
    def id(self) -> int:
        return self.__trip_id

    @property
    def name(self) -> str:
        return self.__dir.name

    @property
    def trajectory_file(self) -> Path:
        return self.__dir.joinpath("trajectory.csv")

    @property
    def detection_file(self) -> Path:
        return self.__dir.joinpath("detections.csv")

    @property
    def has_detections(self) -> bool:
        return self.detection_file.is_file()

    @property
    def trajectory(self):
        self.__con.load_extension("spatial")
        return self.__con.query(
            f"""
SELECT $trip_id                        AS trip_id,
       sequenceId                      AS img_seq_id,
       $user_id                        AS user,
       epoch_ms(timestamp)             AS timestamp,
       ST_POINT(longitude, latitude)   AS point,
       accuracy,
       altitude,
       altitudeAccuracy                AS altitude_accuracy,
       heading,
       speed
FROM read_csv(
    $path,
    delim = $sep,
    header = true
);
""",
            params={
                "trip_id": self.id,
                "path": self.trajectory_file.as_posix(),
                "sep": self.__separator,
                "user_id": self.__user_id,
            },
        )

    @property
    def detections(self) -> DuckDBPyRelation:
        if not self.has_detections:
            return self.__con.query("SELECT 'empty' WHERE 0=1;")

        staging_tbl = "staging_detections"
        self.__con.execute(
            f"""
CREATE OR REPLACE TEMPORARY TABLE {staging_tbl} AS
    SELECT $trip_id AS trip_id,
           $user_id AS user,
           import.* 
    FROM read_csv(
        $path,
        delim = $sep,
        header = true
    ) AS import;
""",
            parameters={
                "trip_id": self.id,
                "user_id": self.__user_id,
                "path": self.detection_file.as_posix(),
                "sep": self.__separator,
            },
        )

        self.__handle_missing_detection_columns(staging_tbl)
        return self.__con.table(staging_tbl).select(
            """
trip_id,
user,
sequenceId                                                  AS img_seq_id,
row_number() OVER (PARTITION BY sequenceId, trip_id)        AS obj_seq_id,
epoch_ms(timestamp)                                         AS timestamp,
x,
y,
width,
height,
imgWidth                                                    AS img_width,
imgHeight                                                   AS img_height,
classifier                                                  AS device_cls,
score                                                       AS device_score,
modelId                                                     AS model_id,
modelVersion                                                AS model_version,
modelSize                                                   AS model_size,
CASE WHEN crop IS NULL THEN NULL ELSE from_base64(crop) END AS img
"""
        )

    @property
    def is_processed(self) -> bool:
        return self.__dir.joinpath(self.__processed_file_name).is_file()

    def mark_as_processed(self) -> None:
        self.__dir.joinpath(self.__processed_file_name).touch()

    def __handle_missing_detection_columns(self, tbl: str):
        expected_columns = set(
            [
                "sequenceId",
                "timestamp",
                "x",
                "y",
                "width",
                "height",
                "imgWidth",
                "imgHeight",
                "classifier",
                "score",
                "modelId",
                "modelVersion",
                "modelSize",
                "crop",
            ]
        )

        col_diff = expected_columns.difference(self.__con.table(tbl).columns)

        if "crop" in col_diff:
            logger.warn(
                "No crop column found in csv file, adding column with NULL values"
            )
            self.__con.execute(
                f"ALTER TABLE {tbl} ADD COLUMN crop VARCHAR DEFAULT NULL;"
            )
            col_diff.remove("crop")  # Remove from col_diff since it was added
        if len(col_diff) > 0:
            # If we have any more columns missing we can't process the file
            raise ValueError(f"Mandatory column(s) not found in csv file: {col_diff}")


@dataclass
class FilesystemUser:
    id: UUID
    trips: Sequence[Trip]


class FilesystemUserSequence:
    def __init__(
        self,
        con: DuckDBPyConnection,
        root: Path,
        user_tbl: DuckDBPyRelation,
        include_extracted: bool,
        separator: str = ",",
    ) -> None:
        self.__con = con
        self.__root = root
        self.__user_tbl = user_tbl
        self.__include_extracted = include_extracted
        self.__separator = separator
        self.__trip_id = 1
        self.__users: Sequence[User] | None = None

    def __get_trips(self, directory: Path, user_id: UUID) -> Sequence[Trip]:
        trips: list[Trip] = []
        for directory in filter(lambda p: p.is_dir(), directory.iterdir()):
            trip = FilesystemTrip(
                self.__con,
                directory,
                self.__trip_id,
                user_id,
                self.__separator,
            )
            if not self.__include_extracted and trip.is_processed:
                continue

            if trip.has_detections:
                trips.append(trip)
                self.__trip_id += 1

        return trips

    def __get_users(self) -> Sequence[User]:
        if self.__users is None:
            user_ids: list[tuple[UUID]] = self.__user_tbl.select("id").fetchall()
            user_lookup: set[UUID] = set(cols[0] for cols in user_ids)

            users: list[User] = []

            for directory in filter(lambda p: p.is_dir(), self.__root.iterdir()):
                user_id = uuid_utils.parse_uuid(directory.name)
                if not user_id:
                    continue

                if user_id not in user_lookup:
                    logger.warning(
                        f"User '{user_id}' found in filesystem but not in the user database"
                    )
                    continue

                users.append(
                    FilesystemUser(user_id, self.__get_trips(directory, user_id))
                )
            self.__users = users
        return self.__users

    def __len__(self) -> int:
        return len(self.__get_users())

    def __getitem__(self, i: int) -> User:
        return self.__get_users()[i]

    def __iter__(self) -> Iterator[User]:
        return self.__get_users().__iter__()
