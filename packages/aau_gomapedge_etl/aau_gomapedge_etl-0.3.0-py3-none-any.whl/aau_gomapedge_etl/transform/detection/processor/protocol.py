from typing import Protocol

from duckdb import DuckDBPyRelation


class Processor(Protocol):
    def process(self, data: DuckDBPyRelation) -> DuckDBPyRelation: ...
