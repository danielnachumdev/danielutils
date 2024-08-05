from fractions import Fraction
from typing import Union

from ..conditional_variable import ConditionalVariable
from ...supp import FrangeSupp
from ...operator import Operator


class DiscreteConditionalVariable(ConditionalVariable):

    def __init__(self, p: Union[float, Fraction], supp: FrangeSupp):
        self._p: Fraction = p if isinstance(p, Fraction) else Fraction.from_float(p)
        self._supp: FrangeSupp = supp

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.p})"

    @property
    def supp(self) -> FrangeSupp:
        return self._supp

    @property
    def p(self) -> Fraction:
        return self._p

    def between(self, a, b, op1: Operator, op2: Operator) -> Fraction:   # type:ignore
        a, b = min(a, b), max(a, b)
        if not (float(a).is_integer() and float(b).is_integer()):
            # a = a - (a % self.supp.step)
            # b = b - (b % self.supp.step)
            raise NotImplementedError("Only integers are currently implemented")
        return 1 - (self.evaluate(a, op1.inverse) + self.evaluate(b, op2.inverse))

    def is_equal(self, other) -> bool:
        if not isinstance(other, DiscreteConditionalVariable):
            return False
        return self.__class__ == other.__class__ and self.p == other.p


__all__ = [
    "DiscreteConditionalVariable"
]
