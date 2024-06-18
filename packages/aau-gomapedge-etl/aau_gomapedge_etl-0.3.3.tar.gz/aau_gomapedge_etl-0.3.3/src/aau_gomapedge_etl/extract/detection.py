import duckdb
from duckdb import DuckDBPyConnection, DuckDBPyRelation

from aau_gomapedge_etl.model import Settings


def __configure_db(con: DuckDBPyConnection, settings: Settings):
    con.install_extension("spatial")
    con.load_extension("spatial")
    con.execute(
        f"ATTACH 'dbname={settings.db.name} user={settings.db.username} password={settings.db.password.get_secret_value()} host={settings.db.host} port={settings.db.port}' AS dw (TYPE POSTGRES, READ_ONLY);"
    )


def extract(settings: Settings) -> DuckDBPyRelation:
    with duckdb.connect(":memory:") as con:
        __configure_db(con, settings)

        dim_schema = settings.dim_schema
        fact_schema = settings.fact_schema

        return con.query(
            f"""
SELECT {fact_schema.detection_table.key}    AS id,
       img_seq_id,
       {dim_schema.trip_table.key},
       heading::REAL                        AS heading,
       width,
       height,
       ST_X(ST_GeomFromHEXWKB(match_point)) AS lng,
       ST_Y(ST_GeomFromHEXWKB(match_point)) AS lat,
       etl_score                            AS score,
       cls_name                             AS cls
FROM dw.fact.fact_gps
    INNER JOIN dw.fact.fact_detection USING (trip_no, img_seq_id)
    INNER JOIN dw.dim.dim_cls ON cls_no = etl_cls_no
WHERE etl_score > 0.9
  AND heading IS NOT NULL
ORDER BY {dim_schema.trip_table.key}, img_seq_id, {fact_schema.detection_table.key};
"""
        )
