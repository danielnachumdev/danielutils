from typing import Union

from fractions import Fraction
from ..conditional_variable import ConditionalVariable
from .probability_function import probability_function as P
from ..expressions import ProbabilityExpression
from ..operator import Operator
from ..protocols import ExpectedValueCalculable


def expected_value(obj: Union[ConditionalVariable, ProbabilityExpression]) -> Fraction:
    if isinstance(obj, ExpectedValueCalculable):
        return obj.expected_value()
    res = Fraction(0, 1)
    if isinstance(obj, ConditionalVariable):
        X = obj
        for n in X.supp:
            res += n * P(X == n)
        return res
    if isinstance(obj.rhs, int):
        const = obj.rhs
        op = obj.op
        X = obj.lhs

        def f(n):
            return {
                Operator.POW: lambda n: n ** const,
                Operator.MUL: lambda n: n * const,
                Operator.DIV: lambda n: n / const,
                Operator.MODULUS: lambda n: n & const,
            }[op](n)

        for n in X.supp:
            res += f(n) * P(X == n)
        return res
    assert False


__all__ = ['expected_value']
