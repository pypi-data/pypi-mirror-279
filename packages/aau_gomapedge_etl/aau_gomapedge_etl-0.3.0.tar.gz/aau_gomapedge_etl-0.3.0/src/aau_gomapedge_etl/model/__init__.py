import uuid
from dataclasses import dataclass
from typing import Protocol

from .db_types import (
    BYTEA,
    REAL,
    UUID,
    WKB_GEOGRAPHY_LINESTRING,
    WKB_GEOGRAPHY_POINT,
    WKB_GEOGRAPHY_POINT_NOT_NULL,
    WKT_GEOGRAPHY_POINT,
)
from .osrm import (
    Gaps,
    MatchResponse,
    Profile,
    Route,
    RouteLeg,
    RouteMatch,
    RouteStep,
    Waypoint,
    WaypointMatch,
)
from .settings import Settings


@dataclass
class DetectionAggMetadata:
    loader_name: str
    pre_name: str
    grp_name: str
    agg_name: str
    post_name: str
    src_fingerprint: uuid.UUID
    src_date_no: int
    src_time_no: int


class ReverseGeocoder(Protocol):
    def reverse(self, location: tuple[float, float]) -> str: ...


__all__ = [
    "UUID",
    "BYTEA",
    "WKB_GEOGRAPHY_LINESTRING",
    "WKB_GEOGRAPHY_POINT",
    "WKB_GEOGRAPHY_POINT_NOT_NULL",
    "WKT_GEOGRAPHY_POINT",
    "REAL",
    "Settings",
    "MatchResponse",
    "Profile",
    "Route",
    "RouteLeg",
    "RouteMatch",
    "RouteStep",
    "Waypoint",
    "WaypointMatch",
    "Gaps",
]
