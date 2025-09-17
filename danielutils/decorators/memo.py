import functools
import logging
from typing import Callable, Any, TypeVar, Dict, Generator, List, Set, Optional
from copy import deepcopy
from .validate import validate
from ..versioned_imports import ParamSpec
from .logging_.utils import get_logger

logger = get_logger(__name__)

T = TypeVar("T")
P = ParamSpec("P")
FuncT = Callable[P, T]  # type:ignore


@validate  # type:ignore
def memo(func: FuncT) -> FuncT:
    """decorator to memorize function calls in order to improve performance by using more memory

    Args:
        func (Callable): function to memorize
    """
    logger.debug(f"Creating memo decorator for function {func.__name__}")
    cache: Dict[tuple, Any] = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        cache_key = (args, *kwargs.items())
        if cache_key not in cache:
            logger.debug(f"Cache miss for {func.__name__}, computing result")
            cache[cache_key] = func(*args, **kwargs)
            logger.debug(f"Result cached for {func.__name__}")
        else:
            logger.debug(f"Cache hit for {func.__name__}, returning cached result")
        return deepcopy(cache[cache_key])

    logger.debug(f"Memo decorator applied to {func.__name__}")
    return wrapper


def memo_generator(func: Callable[P, Generator]) -> Callable[P, Generator]:
    logger.debug(f"Creating memo_generator decorator for function {func.__name__}")
    cache: Dict[tuple, Any] = {}

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Generator:
        args = tuple(args)
        cache_key = (args, *kwargs.items())
        if cache_key not in cache:
            logger.debug(f"Cache miss for generator {func.__name__}, computing and caching result")
            lst = []
            for v in func(*args, **kwargs):
                lst.append(v)
                yield v
            cache[cache_key] = lst
            logger.debug(f"Generator result cached for {func.__name__}")
        else:
            logger.debug(f"Cache hit for generator {func.__name__}, yielding from cache")
            yield from cache[cache_key]

    logger.debug(f"Memo_generator decorator applied to {func.__name__}")
    return wrapper


__all__ = [
    "memo",
    "memo_generator"
]
