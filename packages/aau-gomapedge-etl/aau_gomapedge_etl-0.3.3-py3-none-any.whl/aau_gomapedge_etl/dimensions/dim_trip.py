from email.policy import default

from simpleetl import datatypes

from aau_gomapedge_etl.model import (
    REAL,
    UUID,
    WKB_GEOGRAPHY_LINESTRING,
    WKB_GEOGRAPHY_POINT,
    Settings,
)

from .base_dim import BaseDimension


class DimTrip(BaseDimension):
    def __init__(self, settings: Settings):
        schema = settings.dim_schema
        table = schema.trip_table
        super().__init__(
            table,
            settings,
            integerkey=True,
        )
        self.add_lookupatt("user_id", UUID)
        self.add_lookupatt("start_time", datatypes.timestamp)
        self.add_lookupatt("end_time", datatypes.timestamp)
        self.add_att("match_duration", REAL)
        self.add_att("raw_duration", REAL)
        self.add_att("match_distance", REAL)
        self.add_att("point_cnt", datatypes.int)
        self.add_att("max_speed", REAL, default_value="nan")
        self.add_att("min_speed", REAL, default_value="nan")
        self.add_att("avg_speed", REAL, default_value="nan")
        self.add_att("max_accuracy", REAL)
        self.add_att("min_accuracy", REAL)
        self.add_att("avg_accuracy", REAL)
        self.add_att("max_altitude", REAL)
        self.add_att("min_altitude", REAL)
        self.add_att("avg_altitude", REAL)
        self.add_att("match_start_point", WKB_GEOGRAPHY_POINT)
        self.add_att("match_end_point", WKB_GEOGRAPHY_POINT)
        self.add_att("raw_start_point", WKB_GEOGRAPHY_POINT)
        self.add_att("raw_end_point", WKB_GEOGRAPHY_POINT)
        self.add_att("raw_trajectory", WKB_GEOGRAPHY_LINESTRING)
        self.add_att("match_trajectory", WKB_GEOGRAPHY_LINESTRING)
