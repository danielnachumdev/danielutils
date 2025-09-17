import logging
from typing import Any, Union
from ..functions import isoftype
from ..logging_.utils import get_logger
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
    logger.debug("Computing weight for object: %s", v)
    if isoftype(v, Union[int, float]):  # type:ignore
        logger.debug("Object is numeric, returning value: %s", v)
        return v
    if hasattr(v, "__weight__"):
        logger.debug("Object has __weight__ method, calling it")
        result = v.__weight__()
        logger.debug("Weight method returned: %s", result)
        return result
    logger.error("Object %s has no __weight__ function and is not numeric", v)
    raise AttributeError(f"{v} has no __weight__ function")


__all__ = [
    "default_weight_function"
]
