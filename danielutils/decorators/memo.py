import functools
from typing import Callable, Any, TypeVar, Dict as t_dict
from copy import deepcopy
from .validate import validate
from ..versioned_imports import ParamSpec, t_dict

T = TypeVar("T")
P = ParamSpec("P")
FuncT = Callable[P, T]  # type:ignore


@validate
def memo(func: FuncT) -> FuncT:
    """decorator to memorize function calls in order to improve performance by using more memory

    Args:
        func (Callable): function to memorize
    """
    cache: t_dict[tuple, Any] = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if (args, *kwargs.items()) not in cache:
            cache[(args, *kwargs.items())] = func(*args, **kwargs)
        return deepcopy(cache[(args, *kwargs.items())])

    return wrapper


__all__ = [
    "memo"
]
