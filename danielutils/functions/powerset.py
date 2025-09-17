import logging
from typing import Iterable, Optional, Generator, Any
import itertools
from ..logging_.utils import get_logger

logger = get_logger(__name__)


def powerset(iterable: Iterable[Any], length: Optional[int] = None) -> Generator[tuple, None, None]:
    """returns the powerset of specified length of an iterable
    """
    logger.debug(f"Generating powerset for iterable with length: {length}")
    if length is None:
        if hasattr(iterable, "__len__"):
            length = len(iterable)  # type:ignore
            logger.debug(f"Auto-detected length: {length}")
        else:
            logger.error("Cannot determine length of iterable")
            raise ValueError(
                "when using powerset must supply length explicitly or object should support len()")
    
    logger.debug(f"Generating combinations for lengths 0 to {length}")
    for i in range(length+1):
        logger.debug(f"Generating combinations of length {i}")
        yield from itertools.combinations(iterable, i)
    logger.debug("Powerset generation completed")


__all__ = [
    "powerset"
]
