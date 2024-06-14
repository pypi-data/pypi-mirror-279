from simpleetl import datatypes

from aau_gomapedge_etl.model.settings import Settings, Table

from .base_dim import BaseDimension


class DimModel(BaseDimension):
    def __init__(self, settings: Settings) -> None:
        table = settings.dim_schema.cls_model_table
        super().__init__(table, settings, integerkey=True)
        varchar_cols = ["id", "version", "size"]
        for col in varchar_cols:
            self.add_lookupatt(col, datatypes.varchar(30))
