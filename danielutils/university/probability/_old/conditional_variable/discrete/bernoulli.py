from university.probability._old.operators import Operators
from ..conditional_variable import ConditionalVariable
from university.probability._old.supp import DiscreteSetSupp


class Bernoulli(ConditionalVariable):
    def __hash__(self):
        return hash((self.__class__.__qualname__, self.p))

    def _supp(self):
        return DiscreteSetSupp({0, 1})

    def __init__(self, p: float) -> None:
        self.p = p

    def _evaluate(self, op, val):
        if op == Operators.EQ:
            if val == 1:
                return self.p
            return 1 - self.p
        elif op == Operators.NE:
            return 1 - self.evaluate(Operators.EQ, val)
        raise NotImplementedError("this part needs to be implemented")


Ber = Bernoulli

__all__ = [
    "Bernoulli",
    "Ber"
]
