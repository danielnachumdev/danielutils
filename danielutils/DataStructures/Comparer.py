from .functions import weight
from typing import TypeVar, Callable, Any
T = TypeVar("T")


class Comparer():
    class __Comparer:
        def __init__(self, func):
            self.func = func

        def compare(self, v1, v2):
            return self.func(v1, v2)

        def __call__(self, v1: T, v2: T) -> int:
            return self.compare(v1, v2)

    GREATER = __Comparer(lambda a, b: weight(a)-weight(b))
    SMALLER = __Comparer(lambda a, b: weight(b)-weight(a))

    def __init__(self, func: Callable[[T, T], int]):
        self.__comp = Comparer.__Comparer(func)

    def compare(self, v1, v2):
        return self.__comp(v1, v2)

    def __call__(self, v1: T, v2: T) -> int:
        return self.compare(v1, v2)


__all__ = [
    "Comparer"
]
