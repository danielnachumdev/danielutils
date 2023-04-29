from typing import Callable
import functools
from .timeout import timeout


def limit_runtime(seconds: float | int) -> Callable:
    def deco(func):
        @timeout(seconds, silent=True)
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            while (True):
                func(*args, **kwargs)
        return wrapper
    return deco


__all__ = [
    "limit_runtime"
]
