from datetime import datetime


def get_datetime() -> datetime:
    """return the current datetime

    Returns:
        datetime: current datetime
    """
    return datetime.now()


__all__ = [
    "get_datetime"
]
