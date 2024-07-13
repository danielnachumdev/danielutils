import functools
from typing import Callable, Any, TypeVar, Dict, Generator, List, Set, Optional
from copy import deepcopy
from .validate import validate
from ..versioned_imports import ParamSpec

T = TypeVar("T")
P = ParamSpec("P")
FuncT = Callable[P, T]  # type:ignore


@validate  # type:ignore
def memo(func: FuncT) -> FuncT:
    """decorator to memorize function calls in order to improve performance by using more memory

    Args:
        func (Callable): function to memorize
    """
    cache: Dict[tuple, Any] = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if (args, *kwargs.items()) not in cache:
            cache[(args, *kwargs.items())] = func(*args, **kwargs)
        return deepcopy(cache[(args, *kwargs.items())])

    return wrapper


def memo_generator(func: Callable[[...], Generator]) -> Callable[[...], Generator]:
    cache: Dict[tuple, Any] = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Generator:
        args = tuple(args)
        if (args, *kwargs.items()) not in cache:
            lst = []
            for v in func(*args, **kwargs):
                lst.append(v)
                yield v
            cache[(args, *kwargs.items())] = lst
        else:
            yield from cache[(args, *kwargs.items())]

    return wrapper


__all__ = [
    "memo",
    "memo_generator"
]
