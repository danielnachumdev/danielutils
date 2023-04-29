import functools
from typing import Callable
import threading
from .validate import validate


@validate
def atomic(func: Callable) -> Callable:
    """will make function thread safe by making it
    accessible for only one thread at one time

    Args:
        func (Callable): function to make thread safe

    Returns:
        Callable: the thread safe function
    """
    lock = threading.Lock()

    @ functools.wraps(func)
    def wrapper(*args, **kwargs):
        with lock:
            return func(*args, **kwargs)
    return wrapper


__all__ = [
    "atomic"
]
