from typing import Callable, Any
from ..Colors import warning


def deprecate_with(replacement_func) -> Callable[[Callable], Callable]:
    """will replace a deprecated function with the replacement func and will print a warning"""
    def deco(func):
        warning(f"{func.__module__}.{func.__qualname__} is deprecated, using {replacement_func.__module__}.{replacement_func.__qualname__} instead")

        def wrapper(*args, **kwargs):
            return replacement_func(*args, **kwargs)
        return wrapper
    return deco


__all__ = [
    "deprecate_with"
]
