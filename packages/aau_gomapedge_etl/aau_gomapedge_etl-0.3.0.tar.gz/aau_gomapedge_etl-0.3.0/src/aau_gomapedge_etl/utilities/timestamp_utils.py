from datetime import datetime


def timestamp_to_datekey(timestamp: int) -> int:
    extraction_datetime = datetime.fromtimestamp(timestamp)
    return int(extraction_datetime.strftime("%Y%m%d"))


def timestamp_to_timekey(timestamp: int) -> int:
    extraction_datetime = datetime.fromtimestamp(timestamp)
    return int(extraction_datetime.strftime("%H%M%S"))
