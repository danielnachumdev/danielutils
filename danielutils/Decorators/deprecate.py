from typing import Callable
from ..Colors import warning, ColoredText


def deprecate_with(replacement_func) -> Callable[[Callable], Callable]:
    """will replace a deprecated function with the replacement func and will print a warning"""
    def deco(func):
        warning(f"{func.__module__}.{func.__qualname__} is deprecated, using {replacement_func.__module__}.{replacement_func.__qualname__} instead")

        def wrapper(*args, **kwargs):
            return replacement_func(*args, **kwargs)
        return wrapper
    return deco


def deprecate(deprecation_message: str):
    """A decorator to print a deprecation message when using a deprecated function

    Args:
        deprecation_message (str): deprecation message
    """
    def deco(func: Callable):
        def wrapper(*args, **kwargs):
            print(ColoredText.orange("Deprecation Warning") +
                  ":", deprecation_message)
            return func(*args, **kwargs)
        return wrapper
    return deco


__all__ = [
    "deprecate_with",
    "deprecate"
]
