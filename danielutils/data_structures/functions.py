import logging
from typing import Any, Union
from ..functions import isoftype
from danielutils.logging_.utils import get_logger
from .logging_.utils import get_logger
logger = get_logger(__name__)


def default_weight_function(v: Any) -> Union[int, float]:
    """will return the weight of an object

    Args:
        v (Any): object

    Raises:
        AttributeError: if the object is not a number or doesn't have __weight__ function defined

    Returns:
        Union[int, float]: the object's weight
    """
    logger.debug(f"Computing weight for object: {v}")
    if isoftype(v, Union[int, float]):  # type:ignore
        logger.debug(f"Object is numeric, returning value: {v}")
        return v
    if hasattr(v, "__weight__"):
        logger.debug(f"Object has __weight__ method, calling it")
        result = v.__weight__()
        logger.debug(f"Weight method returned: {result}")
        return result
    logger.error(f"Object {v} has no __weight__ function and is not numeric")
    raise AttributeError(f"{v} has no __weight__ function")


__all__ = [
    "default_weight_function"
]
