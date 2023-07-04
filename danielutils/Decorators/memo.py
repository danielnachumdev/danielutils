from typing import Callable, Any, TypeVar, ParamSpec
import functools
from .validate import validate

T = TypeVar("T")
P = ParamSpec("P")
FuncT = Callable[P, T]


@validate
def memo(func: FuncT) -> FuncT:
    """decorator to memorize function calls in order to improve performance by using more memory

    Args:
        func (Callable): function to memorize
    """
    cache: dict[tuple, Any] = {}

    @ functools.wraps(func)
    def wrapper(*args, **kwargs):
        if (args, *kwargs.items()) not in cache:
            cache[(args, *kwargs.items())] = func(*args, **kwargs)
        return cache[(args, *kwargs.items())]
    return wrapper


__all__ = [
    "memo"
]
