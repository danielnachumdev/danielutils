import logging
from typing import Iterable, Generator, List
from .flatten import flatten
from ..logging_.utils import get_logger

logger = get_logger(__name__)


def _combine2(iter1: Iterable, iter2: Iterable) -> Generator:
    for v1 in iter1:
        for v2 in iter2:
            yield v1, v2


def multiloop(*iterables: Iterable, pre_load: bool = False) -> Generator:
    """
    Generates all combinations of values from multiple iterables.

    This function takes as input any number of iterables and generates all possible combinations of their values.
    It also has an option to pre-load the iterables into memory before generating combinations.

    Args:
        *iterables (list[Iterable]): The iterables to generate combinations from.
        pre_load (bool, optional): If True, pre-loads the iterables into memory. Defaults to False.

    Yields:
        Generator: A generator that yields tuples, each containing one combination of values from the iterables.
    """
    logger.info("Starting multiloop with %s iterables, pre_load=%s", len(iterables), pre_load)
    
    if len(iterables) == 1:
        yield from iterables[0]
        return

    arr: List[Iterable] = list(iterables)
    if pre_load:
        logger.info("Pre-loading iterables into memory")
        arr = [list(itr) for itr in iterables]

    cur = _combine2(*arr[:2])
    for itr in arr[2:]:
        cur = _combine2(cur, itr)
    
    for v in cur:
        flattened = tuple(flatten(v))
        yield flattened


__all__ = [
    "multiloop"
]
