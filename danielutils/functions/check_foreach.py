import logging
from typing import Sequence, Any, Callable
from .logging_.utils import get_logger

logger = get_logger(__name__)


def check_foreach(values: Sequence[Any], condition: Callable[[Any], bool]) -> bool:
    """
    Check if a condition is true for all values in a sequence.

    Args:
        values (Sequence[Any]): Values to perform check on
        condition (Callable[[Any], bool]): Condition to check on all values

    Returns:
        bool: returns True iff condition return True for all values individually
    """
    logger.debug(f"Checking condition on {len(values)} values")
    
    if not isinstance(values, Sequence):
        logger.warning("Values parameter is not a Sequence")
        return False
    if not callable(condition):
        logger.warning("Condition parameter is not callable")
        return False
    
    for i, v in enumerate(values):
        if not condition(v):
            logger.debug(f"Condition failed at index {i} with value: {v}")
            return False
    
    logger.debug("All values passed the condition check")
    return True


__all__ = [
    "check_foreach"
]
