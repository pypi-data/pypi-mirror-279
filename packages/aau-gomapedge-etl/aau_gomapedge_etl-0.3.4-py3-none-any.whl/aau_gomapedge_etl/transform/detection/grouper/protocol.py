from typing import Protocol

from duckdb import DuckDBPyRelation


class Grouper(Protocol):
    def group(self, table: DuckDBPyRelation) -> DuckDBPyRelation: ...
