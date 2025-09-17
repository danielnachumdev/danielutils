"""Comparer class"""
import logging
from typing import Callable,  Union, Generic, TypeVar
from ..logging_.utils import get_logger
from .functions import default_weight_function
logger = get_logger(__name__)

U = TypeVar("U")
V = TypeVar("V")


class Comparer(Generic[U, V]):
    """a Comparer class to be used when comparing two objects
    """

    def __init__(self, func: Callable[[U, V], Union[int, float]]):
        self.func = func
        logger.debug("Comparer initialized with function: %s", func.__name__)

    def compare(self, v1: U, v2: V) -> Union[int, float]:
        """compares two objects

            Args:
                v1 (Any): first object
                v2 (Any): second object

            Returns:
                int: a number specifying the order of the objects
            """
        logger.debug("Comparing objects: %s vs %s", v1, v2)
        result = self.func(v1, v2)
        logger.debug("Comparison result: %s", result)
        return result

    def __call__(self, v1: U, v2: V) -> Union[int, float]:
        return self.compare(v1, v2)


CompareGreater: Comparer[U, V] = Comparer(lambda a, b: default_weight_function(a) -
                                                       default_weight_function(b))
CompareSmaller: Comparer[U, V] = Comparer(lambda a, b: default_weight_function(b) -
                                                       default_weight_function(a))
__all__ = [
    "Comparer",
    "CompareGreater",
    "CompareSmaller"
]
