from io import BytesIO
from typing import Any

from duckdb import DuckDBPyConnection, DuckDBPyRelation
from duckdb.typing import BLOB, DuckDBPyType
from PIL import Image
from yolonnx.services import Classifier

CLASSIFIER_RESULT_STRUCT = DuckDBPyType({"cls": str, "score": float})  # type: ignore


def classify_db_function_factory(classifier: Classifier):
    def classify(data: bytes) -> dict[str, Any]:
        img = Image.open(BytesIO(data))
        cls_results = classifier.run(img)

        if len(cls_results) == 0:
            return {"cls": None, "score": None}
        else:
            cls_result = cls_results[0]
            return {"cls": cls_result.name, "score": cls_result.score}

    return classify


def create_db_function(con: DuckDBPyConnection, classifier: Classifier):
    con.create_function(
        "classify",
        classify_db_function_factory(classifier),
        [BLOB],
        CLASSIFIER_RESULT_STRUCT,
    )


def extract(con: DuckDBPyConnection, detections: DuckDBPyRelation):
    con.sql(
        """
INSERT INTO classification (
    trip_id,
    img_seq_id,
    obj_seq_id,
    cls,
    score
)
    SELECT trip_id,
           img_seq_id,
           obj_seq_id,
           UNNEST(CASE WHEN img IS NULL THEN {'cls': NULL, 'score': NULL} ELSE classify(img) END)
    FROM detections;
"""
    )
