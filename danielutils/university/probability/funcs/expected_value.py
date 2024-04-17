from ..conditional_variables import ConditionalVariable
from fractions import Fraction
from .probability_function import probability_function as P


def expected_value(X: ConditionalVariable) -> Fraction:
    res = Fraction(0, 1)
    for n in X.supp:
        res += n * P(X == n)
    return res


__all__ = ['expected_value']
