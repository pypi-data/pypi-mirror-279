import time
from collections import defaultdict
from typing import Any

from pygrametl import getvalue
from simpleetl import LOG, datatypes

from aau_gomapedge_etl.model import Settings

from .base_dim import BaseDimension


class DimTime(BaseDimension):
    def __init__(self, settings: Settings) -> None:
        schema = settings.dim_schema
        table = schema.time_table
        super().__init__(
            table,
            settings,
            integerkey=True,
        )
        self.add_lookupatt(
            table.key,
            datatypes.timekey,
            self._settings.null_row_no,  # type: ignore Incorrect inferred type hint for default_value
        )

        smallintatts = [
            "hour",
            "minute",
            "second",
            "quarter",
            "five_minute",
            "min_from_midnight",
        ]
        for name in smallintatts:
            self.add_att(name, datatypes.smallint)

        textatts = ["quarter_str", "five_minute_str"]
        for name in textatts:
            self.add_att(name, datatypes.text)

        self.add_att("time", datatypes.time)

    def _row_expander(self, row: dict[str, Any], namemapping: dict[str, str]):
        """Convert time formats before applying to dimensions.

        TODO: Add example
        :param row: The data dictionary, which contains the raw date, but which
                    the output is going to be applied to too.
        :param namemapping: A dictionary describing key mappings of the input
                            dictionary.
        :return: A dictionary, containing values for the dimtime dimension.
        """
        timekey = getvalue(row, "time_no", namemapping)

        if timekey == self._settings.null_row_no:
            return self.__create_null_row()

        thistime = str(timekey).zfill(4)
        try:
            (_, _, _, hour, minute, second, _, _, _) = time.strptime(thistime, "%H%M%S")
        except ValueError:
            LOG.warning(f"Unexpected time format! {str(timekey)} - {str(thistime)}")
            return self.__create_null_row()

        outrow = {}
        outrow["time_no"] = row["time_no"]
        outrow["hour"] = hour
        outrow["minute"] = minute
        outrow["second"] = second
        outrow["time"] = ":".join(
            [str(hour), str(minute).rjust(2, "0"), str(second).zfill(2)]
        )
        outrow["quarter"] = hour * 4 + int(minute / 15)
        outrow["five_minute"] = hour * 12 + int(minute / 5)
        outrow["quarter_str"] = ":".join(
            [str(hour).rjust(2, "0"), str(int(minute / 15) * 15).rjust(2, "0")]
        )
        outrow["five_minute_str"] = ":".join(
            [str(hour).rjust(2, "0"), str(int(minute / 5) * 5).rjust(2, "0")]
        )
        outrow["min_from_midnight"] = hour * 60 + minute

        return outrow

    def __create_null_row(self):
        null_row = defaultdict[str, int | None](lambda: None)
        null_row[self.key] = self._settings.null_row_no
        return null_row
