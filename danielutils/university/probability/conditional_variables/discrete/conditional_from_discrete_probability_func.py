from typing import Callable
from fractions import Fraction
from .discrete import DiscreteConditionalVariable
from ...supp import DiscreteSupp
from ...operator import Operator


class ConditionalFromDiscreteProbabilityFunc(DiscreteConditionalVariable):
    def evaluate(self, n: int, op: Operator) -> Fraction:
        if op == Operator.EQ:
            return self.f(n)
        if op == Operator.LT:
            res = 0
            for k in range(n):
                res += self.evaluate(k, Operator.EQ)
            return res
        if op == Operator.LE:
            return self.evaluate(n, Operator.LT) + self.evaluate(n, Operator.EQ)

        return 1 - self.evaluate(n, op.inverse)

    def __init__(self, p: Callable[[int], Fraction], supp: DiscreteSupp) -> None:
        super().__init__(None, supp)
        self.f = p

    @property
    def p(self):
        raise AttributeError(f"{self.__class__.__name__} has no attribute 'p'")

    def __repr__(self):
        return self.__class__.__name__

__all__ = [
    'ConditionalFromDiscreteProbabilityFunc',
]
