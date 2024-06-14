from typing import Any, Callable, Iterable

from simpleetl import FactTable
from simpleetl import runETL as run_simpleetl

from aau_gomapedge_etl.model import Settings


def runETL(
    fct: FactTable,
    source: Iterable[dict[str, Any]],
    settings: Settings,
    prefunc: Callable[[dict[str, Any]], bool] | None = None,
    processfunc: Callable[[dict[str, Any]], bool] | None = None,
) -> dict[str, Any]:
    db = settings.db
    return run_simpleetl(
        fct,
        source,
        db_host=db.host,
        db_port=db.port,
        db_name=db.name,
        db_user=db.username,
        db_pass=db.password.get_secret_value(),
        prefunc=prefunc,
        processfunc=processfunc,
    )
