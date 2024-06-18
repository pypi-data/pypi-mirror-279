from typing import Protocol, Sequence
from uuid import UUID

from duckdb import DuckDBPyRelation


class Trip(Protocol):
    id: int
    name: str
    trajectory: DuckDBPyRelation
    detections: DuckDBPyRelation
    is_processed: bool

    def mark_as_processed(self) -> None: ...


class User(Protocol):
    id: UUID
    trips: Sequence[Trip]


class ReverseGeocoder(Protocol):
    def reverse(self, location: tuple[float, float]) -> str: ...
