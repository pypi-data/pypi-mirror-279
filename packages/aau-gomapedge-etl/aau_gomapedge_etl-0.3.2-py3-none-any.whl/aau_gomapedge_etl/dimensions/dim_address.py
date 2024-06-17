from typing import Any

from simpleetl import datatypes

from aau_gomapedge_etl.model.settings import Settings

from .base_dim import BaseDimension


class DimAddress(BaseDimension):
    def __init__(self, settings: Settings):
        table = settings.dim_schema.address_table
        super().__init__(table, settings, integerkey=True)
        self.add_lookupatt("country", datatypes.varchar(56), self._settings.null_string)
        self.add_lookupatt(
            "country_code", datatypes.varchar(3), self._settings.null_string[0:3]
        )
        self.add_lookupatt("region", datatypes.varchar(30), self._settings.null_string)
        self.add_lookupatt("state", datatypes.varchar(30), self._settings.null_string)
        self.add_lookupatt(
            "state_district", datatypes.varchar(30), self._settings.null_string
        )
        self.add_lookupatt("county", datatypes.varchar(30), self._settings.null_string)
        self.add_lookupatt(
            "municipality", datatypes.varchar(30), self._settings.null_string
        )
        self.add_lookupatt("city", datatypes.varchar(30), self._settings.null_string)
        self.add_lookupatt("town", datatypes.varchar(30), self._settings.null_string)
        self.add_lookupatt("village", datatypes.varchar(30), self._settings.null_string)
        self.add_lookupatt("suburb", datatypes.varchar(30), self._settings.null_string)
        self.add_lookupatt(
            "house_number", datatypes.varchar(10), self._settings.null_string
        )
        self.add_lookupatt("road", datatypes.varchar(50), self._settings.null_string)
        self.add_lookupatt(
            "postcode", datatypes.varchar(30), self._settings.null_string
        )
        # self.add_lookupatt("city_district", datatypes.varchar(30), "UNKNOWN")
        # self.add_lookupatt("district", datatypes.varchar(30), "UNKNOWN")
        # self.add_lookupatt("borough", datatypes.varchar(30), "UNKNOWN")
        # self.add_lookupatt("subdivision", datatypes.varchar(30), "UNKNOWN")
        # self.add_lookupatt("hamlet", datatypes.varchar(30), "UNKNOWN")
        # self.add_lookupatt("croft", datatypes.varchar(30), "UNKNOWN")
        # self.add_lookupatt("isolated_dwelling", datatypes.varchar(30), "UNKNOWN")
        # self.add_lookupatt("neighborhood", datatypes.varchar(30), "UNKNOWN")
        # self.add_lookupatt("allotments", datatypes.varchar(30), "UNKNOWN")
        # self.add_lookupatt("quarter", datatypes.varchar(30), "UNKNOWN")
        # self.add_lookupatt("city_block", datatypes.varchar(30), "UNKNOWN")
        # self.add_lookupatt("residential", datatypes.varchar(30), "UNKNOWN")
        # self.add_lookupatt("farm", datatypes.varchar(30), "UNKNOWN")
        # self.add_lookupatt("farmyard", datatypes.varchar(30), "UNKNOWN")
        # self.add_lookupatt("industrial", datatypes.varchar(30), "UNKNOWN")
        # self.add_lookupatt("commercial", datatypes.varchar(30), "UNKNOWN")
        # self.add_lookupatt("retail", datatypes.varchar(30), "UNKNOWN")

    def _row_expander(self, row: dict[str, Any], namemapping: dict[str, str]):
        if self.__is_all_unknown(row):
            row[self.key] = self._settings.null_row_no
        return row

    def __is_all_unknown(self, row: dict[str, Any]):
        unknowns = {self._settings.null_string, self._settings.null_string[0:3]}
        for value in row.values():
            if value not in unknowns:
                return False
        return True
