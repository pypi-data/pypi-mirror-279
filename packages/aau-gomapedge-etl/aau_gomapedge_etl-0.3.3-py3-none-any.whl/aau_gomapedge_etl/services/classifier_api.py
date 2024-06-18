import requests
from pydantic import BaseModel


class ClassifierResult(BaseModel):
    label: str
    score: float


class ClassifierAPI:
    def __init__(self, host: str) -> None:
        self.__host = host

    def classify_traffic_sign_single(self, img: bytes) -> ClassifierResult | None:
        response = requests.post(
            self.__host + "/single/traffic-sign",
            files={"img_file": img},
        )
        json = response.text
        if json == "null":
            return None
        cls_result = ClassifierResult.model_validate_json(json)
        cls_result.label = cls_result.label.replace("_", ":").replace("-", ".")
        return cls_result
