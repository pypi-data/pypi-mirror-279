from typing import Any
from uuid import UUID

from aau_gomapedge_etl.model import BYTEA
from aau_gomapedge_etl.model import UUID as UUID_TYPE
from aau_gomapedge_etl.model.settings import Settings

from .base_dim import BaseDimension


class DimObjImg(BaseDimension):
    def __init__(self, settings: Settings):
        table = settings.dim_schema.obj_img_table
        super().__init__(table, settings, integerkey=True)
        self.add_lookupatt(
            "hash",
            UUID_TYPE,
            default_value=UUID(int=0).hex,
        )
        self.add_att("img", BYTEA)

    def _row_expander(self, row: dict[str, Any], namemapping: dict[str, str]):
        if row["img"] is None:
            row[self.key] = self._settings.null_row_no

        return row
