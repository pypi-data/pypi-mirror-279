from duckdb import DuckDBPyConnection
from duckdb.typing import VARCHAR, DuckDBPyType

from aau_gomapedge_etl.utilities import user_utils

USER_AGENT_STRUCT = DuckDBPyType(
    {
        "browser_family": str,
        "browser_version": str,
        "os_family": str,
        "os_version": str,
        "device_family": str,
        "device_brand": str,
        "device_model": str,
    }  # type: ignore
)


def configure_db(con: DuckDBPyConnection):
    con.install_extension("spatial")
    con.load_extension("spatial")
    con.create_function(
        "parse_user_agent", user_utils.parse_user_agent, [VARCHAR], USER_AGENT_STRUCT
    )
