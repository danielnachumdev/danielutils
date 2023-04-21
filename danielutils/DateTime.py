from datetime import datetime


def get_datetime() -> datetime:
    return datetime.now()


__all__ = [
    "get_datetime"
]
