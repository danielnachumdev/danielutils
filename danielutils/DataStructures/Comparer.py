"""Comparer class"""
from typing import Callable, Any
from .functions import default_weight_function


class Comparer():
    """a Comparer class to be used when comparing two objects
    """
    class _Comparer:
        """inner implementation
        """

        def __init__(self, func: Callable[[Any, Any], int]):
            self.func = func

        def compare(self, v1: Any, v2: Any) -> int:
            """compares two objects

            Args:
                v1 (Any): first object
                v2 (Any): second object

            Returns:
                int: a number specifying the order of the objects
            """
            return self.func(v1, v2)

        def __call__(self, v1: Any, v2: Any) -> int:
            return self.compare(v1, v2)

    GREATER = _Comparer(lambda a, b: default_weight_function(
        a)-default_weight_function(b))
    SMALLER = _Comparer(lambda a, b: default_weight_function(
        b)-default_weight_function(a))

    def __init__(self, func: Callable[[Any, Any], int]):
        self.__comp = Comparer._Comparer(func)

    def compare(self, v1: Any, v2: Any) -> int:
        """compares two objects

            Args:
                v1 (Any): first object
                v2 (Any): second object

            Returns:
                int: a number specifying the order of the objects
            """
        return self.__comp(v1, v2)

    def __call__(self, v1: Any, v2: Any) -> int:
        return self.compare(v1, v2)


__all__ = [
    "Comparer"
]
