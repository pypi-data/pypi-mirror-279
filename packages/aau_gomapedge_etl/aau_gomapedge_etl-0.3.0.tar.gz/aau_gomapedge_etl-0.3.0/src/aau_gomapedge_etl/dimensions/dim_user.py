from simpleetl import datatypes

from aau_gomapedge_etl.model import UUID
from aau_gomapedge_etl.model.settings import Settings

from .base_dim import BaseDimension


class DimUser(BaseDimension):
    def __init__(self, settings: Settings):
        table = settings.dim_schema.user_table
        super().__init__(table, settings, integerkey=True)

        self.add_lookupatt("user_id", UUID)
        self.add_att("creation_time", datatypes.timestamp)
        self.add_att("user_agent", datatypes.text)

        varchar_30 = [
            "browser_family",
            "browser_version",
            "os_family",
            "os_version",
            "device_family",
            "device_brand",
            "device_model",
        ]
        for column in varchar_30:
            self.add_att(column, datatypes.varchar(30))
