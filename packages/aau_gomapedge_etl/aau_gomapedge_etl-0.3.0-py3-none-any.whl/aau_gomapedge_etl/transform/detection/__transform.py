import logging
from typing import Sequence

from duckdb import DuckDBPyRelation

from .aggregator import Aggregator
from .dataloader import Dataloader
from .grouper import Grouper
from .processor import Processor

logger = logging.getLogger(__name__)


def __validate_table_data_types(tbl: DuckDBPyRelation) -> None:
    for col, dtype in zip(tbl.columns, tbl.dtypes):
        match col:
            case "id":
                assert dtype == "BIGINT", "id column must be of type BIGINT"
            case "ids":
                assert dtype == "BIGINT[]", "ids column must be of type BIGINT[]"
            case "trip_no":
                assert dtype == "INTEGER", "trip_no column must be of type INTEGER"
            case "img_seq_id":
                assert dtype == "INTEGER", "img_seq_id column must be of type INTEGER"
            case "cls":
                assert dtype == "VARCHAR", "cls column must be of type VARCHAR"
            case "heading":
                assert dtype == "FLOAT", "heading column must be of type FLOAT"
            case "width":
                assert dtype == "INTEGER", "width column must be of type INTEGER"
            case "height":
                assert dtype == "INTEGER", "height column must be of type INTEGER"
            case "score":
                assert dtype == "FLOAT", "score column must be of type FLOAT"
            case "location":
                assert dtype == "GEOMETRY", "location column must be of type GEOMETRY"


def __validate_input_table(tbl: DuckDBPyRelation):
    cols = {
        "cls",
        "trip_no",
        "img_seq_id",
        "cls",
        "width",
        "height",
        "heading",
        "score",
        "location",
    }

    intersection = cols.intersection(tbl.columns)
    if len(intersection) != len(cols):
        raise ValueError(f"Output table must contain the following columns: {cols}")
    __validate_table_data_types(tbl)


def __validate_output_tbl(tbl: DuckDBPyRelation) -> None:
    cols = {"cls", "ids", "heading", "score", "location"}

    intersection = cols.intersection(tbl.columns)
    if len(intersection) != len(cols):
        raise ValueError(f"Output table must contain the following columns: {cols}")
    __validate_table_data_types(tbl)


def transform(
    data_loader: Dataloader,
    grouper: Grouper,
    aggregator: Aggregator,
    preprocessors: Sequence[Processor],
    postprocessors: Sequence[Processor],
) -> DuckDBPyRelation:

    logger.info("Loading data")
    tbl = data_loader.load()
    logger.info("Validating data")
    __validate_input_table(tbl)

    for preprocessor in preprocessors:
        logger.info(f"Preprocessing data using: %s", type(preprocessor).__name__)
        tbl = preprocessor.process(tbl)

    logger.info("Grouping data")
    tbl = grouper.group(tbl)

    logger.info("Aggregating data using: %s", type(aggregator).__name__)
    tbl = aggregator.aggregate(tbl)

    for postprocessor in postprocessors:
        logger.info(f"Postprocessing data using: %s", type(postprocessor).__name__)
        tbl = postprocessor.process(tbl)

    logger.info("Validating output data")
    __validate_output_tbl(tbl)

    tbl = tbl.select(
        """cls, ids, heading, score, ST_X(location) AS lat, ST_Y(location) AS lng"""
    )
    return tbl
