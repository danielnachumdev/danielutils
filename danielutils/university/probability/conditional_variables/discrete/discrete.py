from abc import abstractmethod

from ..conditional_variable import ConditionalVariable
from ...supp import DiscreteSupp


class DiscreteConditionalVariable(ConditionalVariable):
    @property
    @abstractmethod
    def supp(self) -> DiscreteSupp:
        pass


__all__ = [
    "DiscreteConditionalVariable"
]
