from ..Typing import Union, Callable, Any
from ..Classes import frange


class Sigma:
    def __init__(self, expression: Callable, zero=0):
        self.expression = expression
        self.zero = zero

    def __call__(self, range: Union[range, frange]) -> Any:
        res = self.zero
        for v in range:
            res += self.expression(v)
        return res


__all__ = [
    "Sigma"
]
