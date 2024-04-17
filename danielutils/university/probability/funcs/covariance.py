from fractions import Fraction
from .expected_value import expected_value as E
from ..conditional_variables import ConditionalVariable


def covariance(X: ConditionalVariable, Y: ConditionalVariable) -> Fraction:
    return E(X * Y) - E(X) * E(Y)


__all__ = [
    "covariance",
]
