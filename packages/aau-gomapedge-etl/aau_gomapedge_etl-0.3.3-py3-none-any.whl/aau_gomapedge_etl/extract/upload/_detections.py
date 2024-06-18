from duckdb import DuckDBPyConnection, DuckDBPyRelation


def extract(con: DuckDBPyConnection, detections: DuckDBPyRelation):
    con.execute(
        """
INSERT INTO model(name, version, size)
    SELECT DISTINCT model_id,
                    model_version,
                    model_size
    FROM detections AS raw_data
WHERE NOT EXISTS (
    SELECT 1
    FROM model
    WHERE name = raw_data.model_id
      AND version = model_version
      AND size = model_size
);


INSERT INTO detection(
    trip_id,
    img_seq_id,
    obj_seq_id,
    model_id,
    user,
    timestamp,
    x,
    y,
    width,
    height,
    img_width,
    img_height,
    device_cls,
    device_score,
    img
)
    SELECT trip_id,
           img_seq_id,
           obj_seq_id,
           model.model_id AS model_id,
           user,
           timestamp,
           x,
           y,
           width,
           height,
           img_width,
           img_height,
           device_cls,
           device_score,
           img
    FROM detections AS raw_data
        INNER JOIN model ON raw_data.model_id = model.name 
                        AND raw_data.model_version = model.version
                        AND raw_data.model_size = model.size;
"""
    )
