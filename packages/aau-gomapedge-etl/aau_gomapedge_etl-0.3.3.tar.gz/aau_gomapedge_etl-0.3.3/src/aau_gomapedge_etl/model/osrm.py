from typing import Literal

from geojson_pydantic import LineString
from pydantic import BaseModel

Profile = Literal["foot", "car", "bike"]
Gaps = Literal["split", "ignore"]


class RouteStep(BaseModel):
    geometry: str
    mode: str
    duration: float
    weight: float
    name: str
    distance: float


class RouteLeg(BaseModel):
    distance: float
    duration: float
    weight: float
    summary: str
    steps: list[RouteStep]


class Route(BaseModel):
    distance: float
    duration: float
    geometry: str | LineString
    weight: float
    weight_name: str
    legs: list[RouteLeg]


class RouteMatch(Route):
    confidence: float


class Waypoint(BaseModel):
    name: str
    location: tuple[float, float]
    distance: float
    hint: str


class WaypointMatch(Waypoint):
    matchings_index: int
    waypoint_index: int
    alternatives_count: int


class MatchResponse(BaseModel):
    code: str
    matchings: list[RouteMatch]
    tracepoints: list[WaypointMatch | None]
