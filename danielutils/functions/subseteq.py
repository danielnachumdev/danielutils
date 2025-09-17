import logging
from ..logging_.utils import get_logger

logger = get_logger(__name__)


def subseteq(l1: list, l2: list) -> bool:
    """return whether l1 is in list l2

    Args:
        l1 (list): first list
        l2 (list): second list

    Returns:
        bool: boolean result
    """
    logger.debug("Checking if %s is subset of %s", l1, l2)
    result = set(l1).issubset(set(l2))
    logger.debug("Subset check result: %s", result)
    return result


__all__ = [
    "subseteq"
]
