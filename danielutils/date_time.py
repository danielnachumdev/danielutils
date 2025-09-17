from datetime import datetime, timezone


def get_datetime() -> datetime:
    """return the current datetime

    Returns:
        datetime: current datetime
    """
    return datetime.now()

def utc_now() -> datetime:
    """return the current datetime in UTC

    Returns:
        datetime: current datetime in UTC
    """
    return datetime.now(timezone.utc)

__all__ = [
    "get_datetime",
    "utc_now"
]
