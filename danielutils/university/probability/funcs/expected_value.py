from typing import Union, Any, Callable, Dict

from fractions import Fraction
from ..conditional_variable import ConditionalVariable
from .probability_function import probability_function as P
from ..expressions import ProbabilityExpression
from ..operator import Operator
from ..protocols import ExpectedValueCalculable

_mapping: Callable[[Any], Dict[Operator, Callable]] = lambda const: {
    Operator.POW: lambda n: n ** const,
    Operator.MUL: lambda n: n * const,
    Operator.DIV: lambda n: n / const,
    Operator.MODULUS: lambda n: n & const,
}


def expected_value(obj: Union[ConditionalVariable, ProbabilityExpression]) -> Fraction:
    if isinstance(obj, ExpectedValueCalculable):
        return obj.expected_value()
    res = Fraction(0, 1)
    if isinstance(obj, ConditionalVariable):
        X = obj
        for n in X.supp:
            res += n * P(X == n)  # type:ignore
        return res
    if isinstance(obj.rhs, int):
        const = obj.rhs
        op = obj.op
        X = obj.lhs

        def f(n: Union[int, float, Fraction]) -> Union[int, float, Fraction]:
            return _mapping(const)[op](n)

        for n in X.supp:
            res += f(n) * P(X == n)  # type:ignore
        return res
    assert False


__all__ = ['expected_value']
