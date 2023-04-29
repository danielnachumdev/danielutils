from typing import Callable
import time
import functools
from .decorate_conditionally import decorate_conditionally
from .threadify import threadify


def delay_call(seconds: float | int, blocking: bool = True) -> Callable:
    """will delay the call to a function by the given amount of seconds

    Args:
        seconds (float | int): the amount of time to wait
        blocking (bool, optional): whether to block the main thread when waiting or to wait in a different thread. Defaults to True.
    """
    def deco(func):
        @decorate_conditionally(threadify, not blocking)
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            time.sleep(seconds)
            func(*args, **kwargs)
        return wrapper
    return deco


__all__ = [
    "delay_call"
]
