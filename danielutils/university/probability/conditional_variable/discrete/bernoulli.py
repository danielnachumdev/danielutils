from ..conditional_variable import ConditionalVariable
from ...supp import DiscreteSetSupp

class Bernoulli(ConditionalVariable):
    def __hash__(self):
        return hash((self.__class__.__qualname__, self.p))

    def _supp(self):
        return DiscreteSetSupp({0, 1})

    def __init__(self, p: float) -> None:
        self.p = p

    def _evaluate(self, val):
        if val == 1:
            return self.p
        return 1 - self.p


Ber = Bernoulli

__all__ = [
    "Bernoulli",
    "Ber"
]
