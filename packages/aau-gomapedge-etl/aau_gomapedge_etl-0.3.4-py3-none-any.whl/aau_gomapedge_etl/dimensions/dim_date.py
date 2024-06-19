import math
from collections import defaultdict
from datetime import datetime
from typing import Any

from pygrametl import getvalue
from simpleetl import LOG, datatypes

from aau_gomapedge_etl.model import Settings

from .base_dim import BaseDimension


class DimDate(BaseDimension):
    def __init__(self, settings: Settings) -> None:
        schema = settings.dim_schema
        table = schema.date_table
        super().__init__(
            table,
            settings,
            integerkey=True,
        )
        self.add_lookupatt(
            table.key,
            datatypes.datekey,
            default_value=self._settings.null_row_no,  # type: ignore Incorrect inferred type hint for default_value
        )

        small_int_atts = [
            "year",
            "month",
            "day",
            "weekday",
            "iso_weeknumber",
            "iso_weekday",
            "iso_year",
            "quarter",
        ]
        for name in small_int_atts:
            self.add_att(name, datatypes.smallint)

        text_atts = ["season_str", "day_str", "month_str"]
        for name in text_atts:
            self.add_att(name, datatypes.text)

        self.add_att("date", datatypes.date)

    def _row_expander(self, row: dict[str, Any], namemapping: dict[str, str]):
        """A method for handling and converting date formats from a string and
        exploding and adding it to a dictionary.

        TODO: Add example
        :param row: The data dictionary, which contains the raw date, but which
                    the output is going to be applied to too.
        :param namemapping: A dictionary describing key mappings of the input
                            dictionary.
        :return: A dictionary, containing values for the dimdate dimension.
        """

        datekey: int = getvalue(row, self.key, namemapping)
        if datekey == self._settings.null_row_no:
            return self.__create_null_row()

        try:
            dt = datetime.strptime(str(datekey), "%Y%m%d")
        except ValueError:
            LOG.warning(f"Unexpected time format! {str(datekey)}")
            return self.__create_null_row()

        outrow = {}
        outrow["day"] = dt.day
        outrow["month"] = dt.month
        outrow["year"] = dt.year
        outrow["quarter"] = math.ceil(dt.month / 3)
        outrow["weekday"] = dt.weekday()
        (outrow["iso_year"], outrow["iso_weeknumber"], outrow["iso_weekday"]) = (
            dt.isocalendar()
        )
        outrow["date_no"] = int(
            "".join(
                [str(dt.year), str(dt.month).rjust(2, "0"), str(dt.day).rjust(2, "0")]
            )
        )
        outrow["date"] = "-".join(
            [str(dt.year), str(dt.month).rjust(2, "0"), str(dt.day).rjust(2, "0")]
        )
        wds = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]

        mrds = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ]
        outrow["month_str"] = mrds[dt.month - 1]
        outrow["day_str"] = wds[dt.weekday()]
        season = 0
        if 3 <= dt.month <= 5:
            season = 1
        elif 6 <= dt.month <= 8:
            season = 2
        elif 9 <= dt.month <= 11:
            season = 3
        seasons = ["Winter", "Spring", "Summer", "Autumn"]
        outrow["season"] = season
        outrow["season_str"] = seasons[season]
        return outrow

    def __create_null_row(self):
        null_row = defaultdict[str, int | None](lambda: None)
        null_row[self.key] = self._settings.null_row_no
        return null_row
