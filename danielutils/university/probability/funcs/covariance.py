from fractions import Fraction
from .expected_value import expected_value as E
from ..conditional_variable import ConditionalVariable

def covariance(X: ConditionalVariable, Y: ConditionalVariable) -> Fraction:
    # alternative = E((X - E(X)) * (Y - E(Y)))
    return E(X * Y) - E(X) * E(Y)


__all__ = [
    "covariance",
]
