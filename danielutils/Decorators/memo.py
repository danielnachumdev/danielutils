from typing import Callable, Any, TypeVar
import functools
import platform
from .validate import validate

if platform.python_version() >= "3.9":
    from typing import ParamSpec
    T = TypeVar("T")
    P = ParamSpec("P")
    FuncT = Callable[P, T]
else:
    FuncT = Callable  # type:ignore


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
