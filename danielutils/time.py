import logging
import time
from datetime import datetime
from typing import Callable, TypeVar
from .versioned_imports import ParamSpec
from .logging_.utils import get_logger

logger = get_logger(__name__)

T = TypeVar("T")
P = ParamSpec("P")


def measure(func: Callable[P, T]) -> Callable[P, float]:
    """A function to measure the execution time of a function.

    Args:
        func (function): The function to be measured.

    Returns:
        float: The time taken in seconds to execute the given function.
    """

    def wrapper(*args, **kwargs) -> float:
        logger.debug("Measuring execution time of function: %s", func.__name__)
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        execution_time = end - start
        logger.debug("Function %s executed in %.4f seconds", func.__name__, execution_time)
        return execution_time

    return wrapper


def epoch_to_datetime(epoch: float) -> datetime:
    """Converts a POSIX timestamp to datetime

    Args:
        epoch (int): time from epoch

    Returns:
        datetime: resulting conversion
    """
    return datetime.fromtimestamp(epoch)


def datetime_to_epoch(dt: datetime) -> float:
    """Converts a datetime to a POSIX timestamp

    Args:
        dt (datetime): datetime object

    Returns:
        int: resulting conversion
    """
    return dt.timestamp()


__all__ = [
    "measure",
    'epoch_to_datetime',
    'datetime_to_epoch'
]
