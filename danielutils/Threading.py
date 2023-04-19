from .Decorators import atomic

# although it's related to threading, atomic decorator implemented at .Decorators
import threading
from typing import Callable
import functools


def threadify(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        threading.Thread(target=func, args=args, kwargs=kwargs).start()
    return wrapper


__all__ = [
    "threadify"
]
