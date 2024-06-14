from uuid import UUID as UUID_cls

from simpleetl import Datatype, datatypefuncs


def is_float(x) -> float | None:
    try:
        return float(x)
    except Exception:
        return None


def is_bytes(x) -> bytes | None:
    if isinstance(x, bytes):
        return x
    return None


def is_wkb(x) -> str | None:
    if isinstance(x, bytes):
        return x.hex()
    return None


def is_uuid(x) -> str | None:
    if isinstance(x, UUID_cls):
        return x.hex
    return None


WKT_GEOGRAPHY_POINT = Datatype("GEOGRAPHY(Point, 4326)", datatypefuncs.is_text)
WKB_GEOGRAPHY_POINT_NOT_NULL = Datatype(
    "GEOGRAPHY(Point, 4326)", is_wkb, allow_null=False
)
WKB_GEOGRAPHY_POINT = Datatype("GEOGRAPHY(Point, 4326)", is_wkb, allow_null=True)
WKB_GEOGRAPHY_LINESTRING = Datatype("GEOGRAPHY(LineString, 4326)", is_wkb)
REAL_NOT_NULL = Datatype("REAL", is_float, allow_null=False)
REAL = Datatype("REAL", is_float, allow_null=True)
BYTEA = Datatype("bytea", is_bytes)
UUID = Datatype("uuid", is_uuid)
