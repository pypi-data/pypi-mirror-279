import hashlib
import logging
import struct
import time
import uuid
from enum import Enum
from io import BytesIO
from pathlib import Path
from typing import Any

from duckdb import DuckDBPyConnection, DuckDBPyRelation
from pyarrow import ipc, parquet

from aau_gomapedge_etl.model import DetectionAggMetadata

from . import timestamp_utils


def __compute_md5(arrow_tbl):
    buffer = BytesIO()
    with ipc.new_stream(buffer, arrow_tbl.schema) as writer:
        writer.write_table(arrow_tbl)
    buffer.seek(0)
    return hashlib.md5(buffer.getvalue()).digest()


def write_detection_extract(tbl: DuckDBPyRelation, out: Path) -> None:
    arrow_tbl = tbl.to_arrow_table()

    md5 = __compute_md5(arrow_tbl)
    logging.info(f"Fingerprint: {md5.hex()}")
    metadata = {
        "timestamp": struct.pack("i", int(time.time())),
        "md5": md5,
    }

    arrow_metadata = arrow_tbl.schema.metadata or {}
    metadata = {**arrow_metadata, **metadata}
    arrow_tbl = arrow_tbl.replace_schema_metadata(metadata)
    parquet.write_table(arrow_tbl, out.as_posix())


def write_detection_transform(
    tbl: DuckDBPyRelation,
    out: Path,
    loader: Enum,
    preprocessor: Enum,
    grouper: Enum,
    aggregator: Enum,
    postprocessor: Enum,
    metadata: dict[bytes, bytes] = {},
) -> None:
    arrow_tbl = tbl.to_arrow_table()
    transformer_metadata = {
        "data_loader": loader.value,
        "preprocessor": preprocessor.value,
        "grouper": grouper.value,
        "aggregator": aggregator.value,
        "postprocessor": postprocessor.value,
    }
    arrow_metadata = arrow_tbl.schema.metadata or {}
    new_metadata = {**arrow_metadata, **transformer_metadata, **metadata}
    arrow_tbl = arrow_tbl.replace_schema_metadata(new_metadata)

    parquet.write_table(arrow_tbl, out.as_posix())


def read_detection_transform_metadata(path: Path) -> DetectionAggMetadata:
    metadata: dict[bytes, bytes] = parquet.read_metadata(path).metadata
    timestamp: int = struct.unpack("i", metadata[b"timestamp"])[0]
    return DetectionAggMetadata(
        loader_name=metadata[b"data_loader"].decode(),
        pre_name=metadata[b"preprocessor"].decode(),
        grp_name=metadata[b"grouper"].decode(),
        agg_name=metadata[b"aggregator"].decode(),
        post_name=metadata[b"postprocessor"].decode(),
        src_fingerprint=uuid.UUID(bytes=metadata[b"md5"]),
        src_date_no=timestamp_utils.timestamp_to_datekey(timestamp),
        src_time_no=timestamp_utils.timestamp_to_timekey(timestamp),
    )


def read_detection_transform(con: DuckDBPyConnection, path: Path) -> DuckDBPyRelation:
    return con.query(
        """
SELECT row_number() OVER (ORDER BY cls, ids, heading, score, lng, lat) AS id,
       cls,
       ids,
       len(ids) AS detections,
       heading,
       score,
       lng,
       lat
FROM read_parquet($parquet);
""",
        params={"parquet": path.as_posix()},
    )
