from pathlib import Path

from duckdb import DuckDBPyConnection
from pygrametl.datasources import SQLSource
from simpleetl import FactTable, datatypes

from aau_gomapedge_etl.dimensions import DimAddress, DimDate, DimTime, DimTrip, DimUser
from aau_gomapedge_etl.model import WKB_GEOGRAPHY_POINT_NOT_NULL, Settings
from aau_gomapedge_etl.utilities import simpleetl_utils

from . import __common


def __create_fact_table(settings: Settings) -> FactTable:
    schema = settings.fact_schema
    table = schema.gps_table

    fct = FactTable(
        schema=schema.name,
        table=table.name,
        key=table.key,
        migrate_updates=False,
        track_last_updated=False,
        lookupatts=["user_no", "trip_no", "date_no", "time_no", "img_seq_id"],
    )
    fct.add_column_mapping("img_seq_id", datatypes.int)

    dim_date = DimDate(settings)
    fct.add_dim_mapping(dim_date, "date_no", {dim_date.key: "date_no"})
    dim_time = DimTime(settings)
    fct.add_dim_mapping(dim_time, "time_no", {dim_time.key: "time_no"})
    dim_user = DimUser(settings)
    fct.add_dim_mapping(dim_user, dim_user.key)
    dim_trip = DimTrip(settings)
    fct.add_dim_mapping(dim_trip, dim_trip.key)
    dim_address = DimAddress(settings)
    fct.add_dim_mapping(dim_address, dim_address.key)

    fct.add_column_mapping("trip_split_id", datatypes.smallint)
    fct.add_column_mapping("gps_accuracy", datatypes.numeric18_10)
    fct.add_column_mapping("alt", datatypes.numeric18_10)
    fct.add_column_mapping("alt_accuracy", datatypes.numeric18_10)
    fct.add_column_mapping("heading", datatypes.numeric18_10)
    fct.add_column_mapping("speed", datatypes.numeric18_10)
    fct.add_column_mapping("raw_point", WKB_GEOGRAPHY_POINT_NOT_NULL)
    fct.add_column_mapping("match_point", WKB_GEOGRAPHY_POINT_NOT_NULL)

    fct.add_index(["raw_point"])
    fct.add_index(["match_point"])

    return fct


def load(con: DuckDBPyConnection, settings: Settings):
    __common.configure_db(con)
    query_dir = Path(__file__).parents[1].joinpath("__sql")
    transform_query = query_dir.joinpath("transform.sql")
    gps_fact_load_query = query_dir.joinpath("load_fact_gps.sql")

    source = SQLSource(
        con,
        gps_fact_load_query.read_text(),
        initsql=transform_query.read_text(),
    )
    simpleetl_utils.runETL(__create_fact_table(settings), source, settings)
