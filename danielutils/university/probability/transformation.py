from fractions import Fraction
from typing import Union

from .conditional_variable import ConditionalVariable
from .supp import Supp, FrangeSupp, ContinuseSupp
from .operator import Operator


class Transformation:
    def __init__(self, var: Union[ConditionalVariable, 'Transformation'], op: Operator,
                 value: Union[int, float, Fraction]) -> None:
        self.var = var
        self.op = op
        self.value = value

    def supp(self) -> Supp:
        if isinstance(self.var, ConditionalVariable):
            return self.var.supp
        return self.image()

    def image(self) -> Supp:
        # TODO
        if isinstance(self.var, ConditionalVariable):
            if self.var.supp.is_finite:
                for s in self.var.supp:
                    pass

    def _transform_one(self, n: Union[int, float, Fraction]) -> Union[int, float, Fraction]:
        return {
            Operator.ADD: lambda k: k + self.value,
            Operator.SUB: lambda k: k - self.value,
            Operator.MUL: lambda k: k * self.value,
            Operator.POW: lambda k: k ** self.value,
            Operator.DIV: lambda k: k / self.value,
        }[self.op](n)


__all__ = [
    "Transformation"
]
