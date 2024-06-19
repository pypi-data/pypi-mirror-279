import uuid
from dataclasses import dataclass

from .db_types import (
    BYTEA,
    REAL,
    UUID,
    WKB_GEOGRAPHY_LINESTRING,
    WKB_GEOGRAPHY_POINT,
    WKB_GEOGRAPHY_POINT_NOT_NULL,
    WKT_GEOGRAPHY_POINT,
)
from .filesystem_user_sequence import FilesystemUserSequence
from .osrm import (
    Gaps,
    MatchResponse,
    Profile,
    Route,
    RouteLeg,
    RouteMatch,
    RouteStep,
    Waypoint,
    WaypointMatch,
)
from .protocols import ReverseGeocoder, Trip, User
from .settings import Settings


@dataclass
class DetectionAggMetadata:
    loader_name: str
    pre_name: str
    grp_name: str
    agg_name: str
    post_name: str
    src_fingerprint: uuid.UUID
    src_date_no: int
    src_time_no: int


__all__ = [
    "UUID",
    "BYTEA",
    "FilesystemUserSequence",
    "WKB_GEOGRAPHY_LINESTRING",
    "WKB_GEOGRAPHY_POINT",
    "WKB_GEOGRAPHY_POINT_NOT_NULL",
    "WKT_GEOGRAPHY_POINT",
    "REAL",
    "Settings",
    "MatchResponse",
    "Profile",
    "ReverseGeocoder",
    "Route",
    "RouteLeg",
    "RouteMatch",
    "RouteStep",
    "Trip",
    "User",
    "Waypoint",
    "WaypointMatch",
    "Gaps",
]
