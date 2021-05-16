from datetime import datetime, timezone

import time


def get_utc_timestamp() -> float:
    return time.time()


def get_utc_datetime() -> datetime:
    return datetime.fromtimestamp(get_utc_timestamp(), tz=timezone.utc)
