from simpleetl import datatypes

from aau_gomapedge_etl.model.settings import Settings

from .base_dim import BaseDimension


class DimPreprocessor(BaseDimension):
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.__table = settings.dim_schema.preprocess_table
        super().__init__(self.__table, settings, integerkey=True)

        self.add_lookupatt("pre_name", datatypes.varchar(50))
