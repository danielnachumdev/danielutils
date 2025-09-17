import functools
import logging
from typing import Callable, Any, TypeVar, Dict, Generator, List, Set, Optional
from copy import deepcopy
from .validate import validate
from ..versioned_imports import ParamSpec
from ..logging_.utils import get_logger

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
    logger.debug("Creating memo decorator for function %s", func.__name__)
    cache: Dict[tuple, Any] = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        cache_key = (args, *kwargs.items())
        if cache_key not in cache:
            logger.debug("Cache miss for %s, computing result", func.__name__)
            cache[cache_key] = func(*args, **kwargs)
            logger.debug("Result cached for %s", func.__name__)
        else:
            logger.debug("Cache hit for %s, returning cached result", func.__name__)
        return deepcopy(cache[cache_key])

    logger.debug("Memo decorator applied to %s", func.__name__)
    return wrapper


def memo_generator(func: Callable[P, Generator]) -> Callable[P, Generator]:
    logger.debug("Creating memo_generator decorator for function %s", func.__name__)
    cache: Dict[tuple, Any] = {}

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Generator:
        args = tuple(args)
        cache_key = (args, *kwargs.items())
        if cache_key not in cache:
            logger.debug("Cache miss for generator %s, computing and caching result", func.__name__)
            lst = []
            for v in func(*args, **kwargs):
                lst.append(v)
                yield v
            cache[cache_key] = lst
            logger.debug("Generator result cached for %s", func.__name__)
        else:
            logger.debug("Cache hit for generator %s, yielding from cache", func.__name__)
            yield from cache[cache_key]

    logger.debug("Memo_generator decorator applied to %s", func.__name__)
    return wrapper


__all__ = [
    "memo",
    "memo_generator"
]
