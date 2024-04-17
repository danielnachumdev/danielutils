from abc import abstractmethod
from fractions import Fraction

from ..conditional_variable import ConditionalVariable
from ...supp import DiscreteSupp


class DiscreteConditionalVariable(ConditionalVariable):
    def __init__(self, p: Fraction, supp: DiscreteSupp):
        self._p = p
        self._supp = supp

    @property
    def supp(self) -> DiscreteSupp:
        return self._supp

    @property
    def p(self) -> Fraction:
        return self._p

    def __repr__(self)->str:
        return f"{self.__class__.__name__}({self.p})"

__all__ = [
    "DiscreteConditionalVariable"
]
