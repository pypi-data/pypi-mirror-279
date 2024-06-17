from typing import Any

from simpleetl import datatypes

from aau_gomapedge_etl.model.settings import Settings

from .base_dim import BaseDimension


class DimClass(BaseDimension):
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.__table = settings.dim_schema.cls_table
        super().__init__(self.__table, settings, integerkey=True)
        self.add_lookupatt(
            "cls_name",
            datatypes.varchar(30),
            default_value=self._settings.null_string,
        )

    def _row_expander(self, row: dict[str, Any], namemapping: dict[str, str]):
        if row["cls_name"] == self._settings.null_string:
            row[self.key] = self._settings.null_row_no
        return row
