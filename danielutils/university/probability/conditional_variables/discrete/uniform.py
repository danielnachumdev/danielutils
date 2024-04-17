from fractions import Fraction

from ...supp import DiscreteSupp
from ...operator import Operator

from .discrete import DiscreteConditionalVariable
from ...protocols import ExpectedValueCalculable, VariableCalculable


class Uniform(DiscreteConditionalVariable, ExpectedValueCalculable, VariableCalculable):
    def evaluate(self, n: int, op: Operator) -> Fraction:
        if n not in self.supp:
            return Fraction(0, 1)

        if op == Operator.EQ:
            return self.p

        assert False  # TODO
        return self.evaluate(n, op.inverse)

    def __init__(self, size) -> None:
        super().__init__(Fraction(1, size), DiscreteSupp(range(1, size + 1)))

    def expected_value(self) -> Fraction:
        return Fraction(Fraction.from_float(self.supp.start + self.supp.stop), 2)

    def variance(self) -> Fraction:
        return Fraction(
            Fraction.from_float((self.supp.stop - self.supp.start - 1) ** 2 - 1),
            12
        )

    __all__ = ['Uniform']
