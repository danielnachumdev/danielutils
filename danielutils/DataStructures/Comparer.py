"""Comparer class"""
from typing import Callable, Any
from .functions import default_weight_function


class Comparer():
    """a Comparer class to be used when comparing two objects
    """

    def __init__(self, func: Callable[[Any, Any], int | float]):
        self.func = func

    def compare(self, v1: Any, v2: Any) -> int | float:
        """compares two objects

            Args:
                v1 (Any): first object
                v2 (Any): second object

            Returns:
                int: a number specifying the order of the objects
            """
        return self.func(v1, v2)

    def __call__(self, v1: Any, v2: Any) -> int | float:
        return self.compare(v1, v2)


CompareGreater = Comparer(lambda a, b: default_weight_function(a) -
                          default_weight_function(b))
CompareSmaller = Comparer(lambda a, b: default_weight_function(b) -
                          default_weight_function(a))
__all__ = [
    "Comparer",
    "CompareGreater",
    "CompareSmaller"
]
