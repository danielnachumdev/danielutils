import logging
from typing import Iterable, Optional, Generator, Any
import itertools
from ..logging_.utils import get_logger

logger = get_logger(__name__)


def powerset(iterable: Iterable[Any], length: Optional[int] = None) -> Generator[tuple, None, None]:
    """returns the powerset of specified length of an iterable
    """
    logger.debug("Generating powerset for iterable with length: %s", length)
    if length is None:
        if hasattr(iterable, "__len__"):
            length = len(iterable)  # type:ignore
            logger.debug("Auto-detected length: %s", length)
        else:
            logger.error("Cannot determine length of iterable")
            raise ValueError(
                "when using powerset must supply length explicitly or object should support len()")
    
    logger.debug("Generating combinations for lengths 0 to %s", length)
    for i in range(length+1):
        logger.debug("Generating combinations of length %s", i)
        yield from itertools.combinations(iterable, i)
    logger.debug("Powerset generation completed")


__all__ = [
    "powerset"
]
