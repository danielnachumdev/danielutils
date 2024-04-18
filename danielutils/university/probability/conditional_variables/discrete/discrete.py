from fractions import Fraction
from typing import Union

from ..conditional_variable import ConditionalVariable
from ...supp import DiscreteSupp
from ...operator import Operator


class DiscreteConditionalVariable(ConditionalVariable):
    def is_equal(self, other) -> bool:
        if not isinstance(other, DiscreteConditionalVariable):
            return False
        return self.__class__ == other.__class__ and self.p == other.p

    def __init__(self, p: Union[float, Fraction], supp: DiscreteSupp):
        self._p: Fraction = p if isinstance(p, Fraction) else Fraction.from_float(p)
        self._supp: DiscreteSupp = supp

    def between(self, a, b, op1: Operator, op2: Operator) -> Fraction:
        a, b = min(a, b), max(a, b)
        if not (float(a).is_integer() and float(b).is_integer()):
            # a = a - (a % self.supp.step)
            # b = b - (b % self.supp.step)
            raise NotImplementedError("Only integers are currently implemented")
        return 1 - (self.evaluate(a, op1.inverse) + self.evaluate(b, op2.inverse))

    @property
    def supp(self) -> DiscreteSupp:
        return self._supp

    @property
    def p(self) -> Fraction:
        return self._p

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.p})"


__all__ = [
    "DiscreteConditionalVariable"
]
