from dataclasses import dataclass
from pathlib import Path
from uuid import UUID

from duckdb import DuckDBPyConnection, DuckDBPyRelation


@dataclass(slots=True)
class Trip:
    id: int
    directory: Path
    __processed_file_name = ".extracted"

    @property
    def name(self) -> str:
        return self.directory.name

    @property
    def trajectory(self) -> Path:
        return self.directory.joinpath("trajectory.csv")

    @property
    def detections(self) -> Path:
        return self.directory.joinpath("detections.csv")

    @property
    def has_detections(self) -> bool:
        return self.detections.is_file()

    @property
    def has_trajectory(self) -> bool:
        return self.trajectory.is_file()

    @property
    def is_processed(self) -> bool:
        return self.directory.joinpath(self.__processed_file_name).is_file()

    def mark_as_processed(self) -> None:
        self.directory.joinpath(self.__processed_file_name).touch()

    def get_trajectory_tbl(
        self,
        con: DuckDBPyConnection,
        user_id: UUID,
        sep: str,
    ) -> DuckDBPyRelation:
        con.load_extension("spatial")
        return con.query(
            f"""
SELECT $trip_id                        AS trip_id,
       sequenceId                      AS img_seq_id,
       $user_id                        AS user,
       epoch_ms(timestamp)             AS timestamp,
       ST_POINT(longitude, latitude)   AS point,
       accuracy,
       altitude,
       altitudeAccuracy                AS altitude_accuracy,
       heading,
       speed
FROM read_csv(
    $path,
    delim = $sep,
    header = true
);
""",
            params={
                "trip_id": self.id,
                "path": self.trajectory.as_posix(),
                "sep": sep,
                "user_id": user_id,
            },
        )

    def get_detection_tbl(
        self,
        con: DuckDBPyConnection,
        user_id: UUID,
        separator: str,
    ) -> DuckDBPyRelation:
        if not self.has_detections:
            return con.query("SELECT 'empty' WHERE 0=1;")

        return con.query(
            """
    SELECT $trip_id                                              AS trip_id,
           sequenceId                                            AS img_seq_id,
           row_number() OVER (PARTITION BY sequenceId, $trip_id) AS obj_seq_id,
           $user                                                 AS user,
           epoch_ms(timestamp)                                   AS timestamp,
           x,
           y,
           width,
           height,
           imgWidth                                              AS img_width,
           imgHeight                                             AS img_height,
           classifier                                            AS device_cls,
           score                                                 AS device_score,
           modelId                                               AS model_id,
           modelVersion                                          AS model_version,
           modelSize                                             AS model_size,
           from_base64(crop)                                     AS img
    FROM read_csv(
        $path,
        delim = $sep,
        header = true
    );
    """,
            params={
                "trip_id": self.id,
                "user": user_id,
                "path": self.detections.as_posix(),
                "sep": separator,
            },
        )


def get_trips_from_filesystem(
    root: Path, include_extracted: bool = False
) -> list[Trip]:
    trips: list[Trip] = []
    trip_id = 1
    for directory in filter(lambda p: p.is_dir(), root.iterdir()):
        trip = Trip(trip_id, directory)
        if not include_extracted and trip.is_processed:
            continue

        if trip.has_trajectory:
            trips.append(trip)
            trip_id += 1

    return trips
