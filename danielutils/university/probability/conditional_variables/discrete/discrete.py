from abc import abstractmethod
from fractions import Fraction
from typing import Union

from ..conditional_variable import ConditionalVariable
from ...supp import DiscreteSupp


class DiscreteConditionalVariable(ConditionalVariable):
    def __init__(self, p: Union[float, Fraction], supp: DiscreteSupp):
        self._p: Fraction = p if isinstance(p, Fraction) else Fraction.from_float(p)
        self._supp: DiscreteSupp = supp

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
