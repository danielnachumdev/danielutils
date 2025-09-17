import logging
from typing import Callable, Any, Optional
from ..logging_.utils import get_logger

logger = get_logger(__name__)


def try_get(supplier: Callable[[], Any]) -> Optional[Any]:
    """try to get a value from a function and return the value or return None on fail

    Args:
        supplier (Callable[[], Any]): supplier function

    Returns:
        Optional[Any]: return value
    """
    try:
        result = supplier()
        logger.debug("try_get succeeded for supplier: %s", supplier.__name__)
        return result
    except Exception as e:
        logger.debug("try_get failed for supplier: %s with %s: %s", supplier.__name__, type(e).__name__, e)
        return None


__all__ = [
    "try_get"
]
