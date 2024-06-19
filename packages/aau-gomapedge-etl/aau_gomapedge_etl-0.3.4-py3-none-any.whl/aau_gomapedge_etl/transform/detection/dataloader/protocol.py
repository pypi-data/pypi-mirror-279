from typing import Protocol
from duckdb import DuckDBPyRelation


class Dataloader(Protocol):
    def load(self) -> DuckDBPyRelation: ...
