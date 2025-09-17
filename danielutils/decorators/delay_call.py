import logging
from typing import Callable, TypeVar, Union
import time
import functools
from .decorate_conditionally import decorate_conditionally
from .threadify import threadify
from ..versioned_imports import ParamSpec
from ..logging_.utils import get_logger

logger = get_logger(__name__)

T = TypeVar("T")
P = ParamSpec("P")
FuncT = Callable[P, T]  # type:ignore


def delay_call(seconds: Union[float, int], blocking: bool = True) -> Callable[[FuncT], FuncT]:
    """will delay the call to a function by the given amount of seconds

    Args:
        seconds (float | int): the amount of time to wait
        blocking (bool, optional): whether to block the main thread
        when waiting or to wait in a different thread. Defaults to True.
    """
    logger.debug("Creating delay_call decorator with %ss delay, blocking=%s", seconds, blocking)

    def deco(func: FuncT) -> FuncT:
        logger.debug("Applying delay_call decorator to function %s", func.__name__)
        @decorate_conditionally(threadify, not blocking)
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger.debug("Delaying call to %s by %s seconds", func.__name__, seconds)
            time.sleep(seconds)
            logger.debug("Delay completed, calling %s", func.__name__)
            result = func(*args, **kwargs)
            logger.debug("Delayed function %s completed", func.__name__)
            return result

        logger.debug("Delay_call decorator applied to %s", func.__name__)
        return wrapper

    return deco


__all__ = [
    "delay_call"
]
