import logging
import struct
import uuid
from pathlib import Path
from typing import Any

import psycopg2
from duckdb import DuckDBPyConnection, DuckDBPyRelation
from pyarrow import parquet
from pygrametl.datasources import SQLSource
from simpleetl import FactTable, datatypes

from aau_gomapedge_etl.dimensions import (
    DimAggregator,
    DimClass,
    DimDataLoader,
    DimDate,
    DimGrouper,
    DimPostprocessor,
    DimPreprocessor,
    DimTime,
)
from aau_gomapedge_etl.model import (
    REAL,
    UUID,
    WKT_GEOGRAPHY_POINT,
    DetectionAggMetadata,
)
from aau_gomapedge_etl.model.settings import Settings, Table
from aau_gomapedge_etl.utilities import simpleetl_utils, timestamp_utils

from . import __common

logger = logging.getLogger("FactDetectionAggLoader")


def __create_fact_bridge(settings: Settings) -> FactTable:
    fct_schema = settings.fact_schema
    tbl = fct_schema.detection_bridge_table
    detection_key = settings.fact_schema.detection_table.key
    detection_agg_key = settings.fact_schema.detection_agg_table.key

    fct = FactTable(
        settings.fact_schema.name,
        table=tbl.name,
        key=tbl.key,
        lookupatts=[detection_key, detection_agg_key],
    )
    fct.add_column_mapping(detection_key, datatypes.bigint)
    fct.add_column_mapping(detection_agg_key, datatypes.bigint)

    return fct


def __create_fact_table(settings: Settings) -> FactTable:
    tbl = settings.fact_schema.detection_agg_table

    fct = FactTable(
        settings.fact_schema.name,
        table=tbl.name,
        key=tbl.key,
        lookupatts=[
            "src_id",
            "src_fingerprint",
            "data_loader_no",
            "preprocess_no",
            "grouper_no",
            "agg_no",
            "postprocess_no",
        ],
    )

    fct.add_column_mapping("id", datatypes.int, "src_id")
    fct.add_column_mapping("src_fingerprint", UUID)

    dim_date = DimDate(settings)
    fct.add_dim_mapping(dim_date, "src_date_no", {dim_date.key: "src_date_no"})

    dim_time = DimTime(settings)
    fct.add_dim_mapping(dim_time, "src_time_no", {dim_time.key: "src_time_no"})

    dim_class = DimClass(settings)
    fct.add_dim_mapping(
        dim_class, settings.dim_schema.cls_table.key, {"cls_name": "cls"}
    )

    dim_data_loader = DimDataLoader(settings)
    fct.add_dim_mapping(dim_data_loader, dim_data_loader.key)

    dim_preprocessor = DimPreprocessor(settings)
    fct.add_dim_mapping(dim_preprocessor, dim_preprocessor.key)

    dim_grouper = DimGrouper(settings)
    fct.add_dim_mapping(dim_grouper, dim_grouper.key)

    dim_aggregator = DimAggregator(settings)
    fct.add_dim_mapping(dim_aggregator, dim_aggregator.key)

    dim_postprocessor = DimPostprocessor(settings)
    fct.add_dim_mapping(dim_postprocessor, dim_postprocessor.key)

    fct.add_column_mapping("detections", datatypes.int)
    fct.add_column_mapping("heading", REAL)
    fct.add_column_mapping("score", REAL)
    fct.add_column_mapping("location", WKT_GEOGRAPHY_POINT)

    return fct


def __extract_metadata(data: Path) -> dict[str, Any]:
    metadata: dict[bytes, bytes] = parquet.read_metadata(data).metadata
    timestamp: int = struct.unpack("i", metadata[b"timestamp"])[0]
    return {
        "loader_name": metadata[b"data_loader"].decode(),
        "pre_name": metadata[b"preprocessor"].decode(),
        "grp_name": metadata[b"grouper"].decode(),
        "agg_name": metadata[b"aggregator"].decode(),
        "post_name": metadata[b"postprocessor"].decode(),
        "src_fingerprint": uuid.UUID(bytes=metadata[b"md5"]),
        "src_date_no": timestamp_utils.timestamp_to_datekey(timestamp),
        "src_time_no": timestamp_utils.timestamp_to_timekey(timestamp),
    }


def __load_fact_detection_agg(
    con: DuckDBPyConnection,
    agg_tbl: DuckDBPyRelation,
    metadata: DetectionAggMetadata,
    settings: Settings,
):
    def processfunc(row: dict[str, Any]) -> bool:
        row.update(metadata.__dict__)
        row["location"] = f"POINT({row['lng']} {row['lat']})"
        return True

    con.execute("CREATE TABLE detection_agg AS SELECT * FROM agg_tbl;")
    source = SQLSource(
        con,
        """SELECT * FROM detection_agg;""",
    )
    simpleetl_utils.runETL(
        __create_fact_table(settings), source, settings, prefunc=processfunc
    )


def __load_detection_bridge(
    con: DuckDBPyConnection, metadata: DetectionAggMetadata, settings: Settings
):
    fact_schema = settings.fact_schema
    dim_schema = settings.dim_schema
    detection_agg_tbl = fact_schema.detection_agg_table

    query = f"""
ATTACH '{settings.db.dsn}' AS dw (TYPE POSTGRES);

SELECT UNNEST(ids) AS {settings.fact_schema.detection_table.key},
       {detection_agg_tbl.key}
FROM detection_agg
    INNER JOIN dw.{fact_schema.name}.{detection_agg_tbl.name} 
        ON id = src_id
        AND {detection_agg_tbl.name}.src_fingerprint = $fingerprint
    INNER JOIN dw.{dim_schema.name}.{dim_schema.data_loader_table.name} USING ({dim_schema.data_loader_table.key})
    INNER JOIN dw.{dim_schema.name}.{dim_schema.preprocess_table.name}  USING ({dim_schema.preprocess_table.key})
    INNER JOIN dw.{dim_schema.name}.{dim_schema.grouper_table.name}     USING ({dim_schema.grouper_table.key})
    INNER JOIN dw.{dim_schema.name}.{dim_schema.aggregator_table.name}  USING ({dim_schema.aggregator_table.key})
    INNER JOIN dw.{dim_schema.name}.{dim_schema.postprocess_table.name} USING ({dim_schema.postprocess_table.key})
WHERE loader_name = $data_loader
  AND pre_name = $pre_name
  AND grp_name = $grp_name
  AND agg_name = $agg_name
  AND post_name = $post_name;
"""
    source = SQLSource(
        con,
        query,
        parameters={
            "fingerprint": metadata.src_fingerprint,
            "data_loader": metadata.loader_name,
            "pre_name": metadata.pre_name,
            "grp_name": metadata.grp_name,
            "agg_name": metadata.agg_name,
            "post_name": metadata.post_name,
        },
    )
    simpleetl_utils.runETL(__create_fact_bridge(settings), source, settings)


def __get_fkey_constraint_name(src_tbl: Table, taget_tbl: Table) -> str:
    return f"{src_tbl.name}_{taget_tbl.key}_fkey"


def __drop_fkey(con, schema: str, src_tbl: Table, taget_tbl: Table):
    constraint_name = __get_fkey_constraint_name(src_tbl, taget_tbl)
    with con.cursor() as curs:
        curs.execute(
            f"""
ALTER TABLE IF EXISTS {schema}.{src_tbl.name} 
    DROP CONSTRAINT IF EXISTS {constraint_name};"""
        )


def __add_fkey(con, schema: str, src_tbl: Table, taget_tbl: Table):
    constraint_name = __get_fkey_constraint_name(src_tbl, taget_tbl)
    with con.cursor() as curs:
        curs.execute(
            f"""
ALTER TABLE IF EXISTS {schema}.{src_tbl.name}
    ADD CONSTRAINT {constraint_name} 
    FOREIGN KEY ({taget_tbl.key}) 
    REFERENCES {schema}.{taget_tbl.name} ({taget_tbl.key});
"""
        )


def __drop_bridge_fkey(con, settings: Settings):
    schema = settings.fact_schema
    src_tbl = schema.detection_bridge_table
    __drop_fkey(con, schema.name, src_tbl, settings.fact_schema.detection_table)
    __drop_fkey(con, schema.name, src_tbl, settings.fact_schema.detection_agg_table)
    con.commit()


def __add_bridge_fkey(con, settings: Settings):
    schema = settings.fact_schema
    src_tbl = schema.detection_bridge_table
    __add_fkey(con, schema.name, src_tbl, settings.fact_schema.detection_table)
    __add_fkey(con, schema.name, src_tbl, settings.fact_schema.detection_agg_table)
    con.commit()


def load(
    con: DuckDBPyConnection,
    data: DuckDBPyRelation,
    metadata: DetectionAggMetadata,
    settings: Settings,
):
    __common.configure_db(con)
    __load_fact_detection_agg(con, data, metadata, settings)

    pg_con = psycopg2.connect(settings.db.dsn)
    __drop_bridge_fkey(pg_con, settings)
    __load_detection_bridge(con, metadata, settings)
    __add_bridge_fkey(pg_con, settings)
    pg_con.close()
