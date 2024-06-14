from typing import Protocol

from duckdb import DuckDBPyRelation


class Aggregator(Protocol):
    def aggregate(self, tbl: DuckDBPyRelation) -> DuckDBPyRelation: ...
