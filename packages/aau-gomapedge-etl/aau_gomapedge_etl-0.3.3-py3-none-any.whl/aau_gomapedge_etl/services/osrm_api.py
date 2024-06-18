from typing import Any, Iterable, Literal
from urllib import parse

from pydantic_core import Url
from requests import Session

from aau_gomapedge_etl.model import Gaps, MatchResponse, Profile


class OSRM:
    __slots__ = ("__session", "__base_url")

    def __init__(self, url: Url) -> None:
        self.__base_url = url
        self.__session = Session()

    @property
    def url(self) -> Url:
        return self.__base_url

    def match(
        self,
        profile: Profile,
        coords: Iterable[tuple[float, float]],
        radiuses: Iterable[float] | None = None,
        timestamps: Iterable[int] | None = None,
        step: bool = False,
        gaps: Gaps | None = None,
        geometries: Literal["polyline", "polyline6", "geojson"] | None = None,
    ) -> MatchResponse:
        url = f"/match/v1/{profile}/{self.__to_coord_str(coords)}"
        query: dict[str, str] = {}
        if radiuses is not None:
            query["radiuses"] = ";".join([f"{r:.2f}" for r in radiuses])
        if timestamps is not None:
            query["timestamps"] = ";".join([str(r) for r in timestamps])
        if step:
            query["steps"] = "true"
        if geometries is not None:
            query["geometries"] = geometries
        if gaps is not None:
            query["gaps"] = gaps

        response = self.__get(url, params=query)
        if response.status_code != 200:
            raise ValueError(f"Response code {response.status_code}: {response.text}")
        return MatchResponse.model_validate_json(response.content)

    def __to_coord_str(self, coords: Iterable[tuple[float, float]]) -> str:
        return ";".join((f"{x:.5f},{y:.5f}" for x, y in coords))

    def __get(self, url: str, params: dict[str, Any] | None = None):
        url = parse.urljoin(self.__base_url.unicode_string(), url)
        return self.__session.get(url, params=params)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__session.close()
