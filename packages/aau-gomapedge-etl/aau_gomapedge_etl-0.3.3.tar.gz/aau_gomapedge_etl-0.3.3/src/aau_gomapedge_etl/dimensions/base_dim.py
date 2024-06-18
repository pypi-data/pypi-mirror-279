from typing import Any

from simpleetl import Dimension

from aau_gomapedge_etl.model.settings import Settings, Table


class BaseDimension(Dimension):
    def __init__(self, table: Table, settings: Settings, integerkey=False):
        self._settings = settings
        schema = settings.dim_schema
        super().__init__(
            schema.name,
            table.name,
            table.key,
            self._row_expander,
            settings.cache_size,
            integerkey,
        )

    @property
    def key(self) -> str:
        return self._get_key()

    def _row_expander(self, row: dict[str, Any], namemapping: dict[str, str]):
        return row
