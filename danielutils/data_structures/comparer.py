"""Comparer class"""
from typing import Callable, Any, Union, Generic, TypeVar
from .functions import default_weight_function

U = TypeVar("U")
V = TypeVar("V")


class Comparer(Generic[U, V]):
    """a Comparer class to be used when comparing two objects
    """

    def __init__(self, func: Callable[[U, V], Union[int, float]]):
        self.func = func

    def compare(self, v1: U, v2: V) -> Union[int, float]:
        """compares two objects

            Args:
                v1 (Any): first object
                v2 (Any): second object

            Returns:
                int: a number specifying the order of the objects
            """
        return self.func(v1, v2)

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
