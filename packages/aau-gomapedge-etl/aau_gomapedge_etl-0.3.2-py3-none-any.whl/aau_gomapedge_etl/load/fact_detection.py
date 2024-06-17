from pathlib import Path

from duckdb import DuckDBPyConnection
from pygrametl.datasources import SQLSource
from simpleetl import FactTable, datatypes

from aau_gomapedge_etl.dimensions import (
    DimClass,
    DimDate,
    DimModel,
    DimObjImg,
    DimTime,
    DimTrip,
    DimUser,
)
from aau_gomapedge_etl.model import REAL, Settings
from aau_gomapedge_etl.utilities import simpleetl_utils

from . import __common


def __create_fact_table(settings: Settings) -> FactTable:
    schema = settings.fact_schema
    table = schema.detection_table
    dim_class = DimClass(settings)
    device_cls_no = f"device_{dim_class.key}"
    fct = FactTable(
        schema=schema.name,
        table=table.name,
        key=table.key,
        migrate_updates=False,
        track_last_updated=False,
        lookupatts=[
            "user_no",
            "trip_no",
            "img_seq_id",
            "x",
            "y",
            "width",
            "height",
            device_cls_no,
        ],
    )
    fct.add_column_mapping("img_seq_id", datatypes.int)

    dim_date = DimDate(settings)
    fct.add_dim_mapping(dim_date, "date_no", {dim_date.key: "date_no"})

    dim_time = DimTime(settings)
    fct.add_dim_mapping(dim_time, "time_no", {dim_time.key: "time_no"})

    dim_user = DimUser(settings)
    fct.add_dim_mapping(dim_user, dim_user.key)

    dim_trip = DimTrip(settings)
    fct.add_dim_mapping(
        dim_trip,
        dim_trip.key,
        {dim_date.key: "start_date_no", dim_time.key: "start_time_no"},
    )

    dim_model = DimModel(settings)
    fct.add_dim_mapping(
        dim_model,
        dim_model.key,
        {"id": "model_id", "version": "model_version", "size": "model_size"},
    )
    fct.add_dim_mapping(dim_class, device_cls_no, {"cls_name": "device_cls"})
    fct.add_dim_mapping(dim_class, "etl_cls_no", {"cls_name": "etl_cls"})

    dim_obj_img = DimObjImg(settings)
    fct.add_dim_mapping(
        dim_obj_img, dim_obj_img.key, {"img": "crop", "hash": "crop_hash"}
    )

    int_columns = ["x", "y", "width", "height", "img_height", "img_width"]
    for col in int_columns:
        fct.add_column_mapping(col, datatypes.int)
    fct.add_column_mapping("device_score", REAL)
    fct.add_column_mapping("etl_score", REAL)

    return fct


def load(con: DuckDBPyConnection, settings: Settings):
    __common.configure_db(con)

    query_dir = Path(__file__).parents[1].joinpath("__sql")
    transform_query = query_dir.joinpath("transform.sql")
    detection_fact_load_query = query_dir.joinpath("load_fact_detection.sql")

    source = SQLSource(
        con,
        detection_fact_load_query.read_text(),
        initsql=transform_query.read_text(),
    )
    simpleetl_utils.runETL(__create_fact_table(settings), source, settings)
