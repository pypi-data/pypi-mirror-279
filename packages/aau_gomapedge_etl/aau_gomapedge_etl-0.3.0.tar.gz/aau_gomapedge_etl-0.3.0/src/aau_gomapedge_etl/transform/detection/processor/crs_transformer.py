from duckdb import DuckDBPyConnection, DuckDBPyRelation

from .protocol import Processor


class CrsTransformer(Processor):
    def __init__(
        self, con: DuckDBPyConnection, source_crs: str, target_crs: str
    ) -> None:
        super().__init__()
        self.__con = con
        self.__source_crs = source_crs
        self.__target_crs = target_crs

    @property
    def source_crs(self) -> str:
        return self.__source_crs

    @property
    def target_crs(self) -> str:
        return self.__target_crs

    def process(self, tbl: DuckDBPyRelation) -> DuckDBPyRelation:
        columns = list(tbl.columns)
        columns.remove("location")

        return self.__con.query(
            f"""
SELECT {",".join(columns)}, ST_Transform(location, $source_crs, $target_crs) AS location
FROM tbl;
""",
            params={"source_crs": self.__source_crs, "target_crs": self.__target_crs},
        )
