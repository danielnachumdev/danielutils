import logging
from typing import Iterable
from ..logging_.utils import get_logger

logger = get_logger(__name__)


def flatten(iterable: Iterable) -> list:
    """
    Flattens a given iterable into a list.

    This function takes as input an iterable that may contain nested iterables (like lists or tuples),
    and returns a flat list where all elements of the input are expanded.
    Non-iterable elements in the input iterable are appended as they are.

    Args:
        iterable (Iterable): The iterable to flatten. Can contain nested iterables.

    Returns:
        list: A flat list containing all elements of the input iterable.
    """
    result = []
    for i in iterable:
        if isinstance(i, Iterable):
            result.extend(flatten(i))
        else:
            result.append(i)
    
    return result

__all__=[
    "flatten"
]