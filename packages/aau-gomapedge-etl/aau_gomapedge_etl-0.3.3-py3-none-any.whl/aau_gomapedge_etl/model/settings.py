from pathlib import Path

from pydantic import BaseModel, HttpUrl, SecretStr, computed_field
from pydantic_core import Url
from pydantic_settings import BaseSettings, SettingsConfigDict


class NominatimApi(BaseModel):
    user_agent: str = "GoMapEdgeETL"
    domain: str = "nominatim.rgbmonster.aau.dk"
    scheme: str = "http"


class DbSettings(BaseModel):
    host: str
    port: int
    name: str
    username: str
    password: SecretStr

    @computed_field
    @property
    def dsn(self) -> str:
        return f"dbname={self.name} user={self.username} password={self.password.get_secret_value()} host={self.host} port={self.port}"


class Table(BaseModel):
    name: str
    key: str


class DimensionSchema(BaseModel):
    name: str = "dim"
    user_table: Table = Table(name="dim_user", key="user_no")
    date_table: Table = Table(name="dim_date", key="date_no")
    time_table: Table = Table(name="dim_time", key="time_no")
    trip_table: Table = Table(name="dim_trip", key="trip_no")
    cls_table: Table = Table(name="dim_cls", key="cls_no")
    cls_model_table: Table = Table(name="dim_model", key="model_no")
    obj_img_table: Table = Table(name="dim_obj_img", key="obj_img_no")
    address_table: Table = Table(name="dim_address", key="address_no")
    aggregator_table: Table = Table(name="dim_aggregator", key="agg_no")
    data_loader_table: Table = Table(name="dim_data_loader", key="data_loader_no")
    preprocess_table: Table = Table(name="dim_preprocess", key="preprocess_no")
    grouper_table: Table = Table(name="dim_grouper", key="grouper_no")
    postprocess_table: Table = Table(name="dim_postprocess", key="postprocess_no")
    source_table: Table = Table(name="dim_source", key="source_no")


class FactSchema(BaseModel):
    name: str = "fact"
    gps_table: Table = Table(name="fact_gps", key="gps_no")
    detection_table: Table = Table(name="fact_detection", key="detection_no")
    detection_agg_table: Table = Table(
        name="fact_detection_agg", key="detection_agg_no"
    )
    detection_bridge_table: Table = Table(
        name="detection_bridge", key="detection_bridge_no"
    )


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="GOMAP_EDGE_")

    db: DbSettings = DbSettings(
        host="",
        port=5432,
        name="postgres",
        username="postgres",
        password=SecretStr("pa$$w0rd"),
    )
    dim_schema: DimensionSchema = DimensionSchema()
    fact_schema: FactSchema = FactSchema()
    cache_size: int = 100000
    null_row_no: int = -1
    null_string: str = "UNKNOWN"
    nominatim_api: NominatimApi = NominatimApi()
    osrm_api_url: HttpUrl = Url("https://project-osrm.org/")

    @staticmethod
    def create(path: Path) -> "Settings":
        if path.is_file():
            return Settings.model_validate_json(path.read_text())
        else:
            return Settings()
