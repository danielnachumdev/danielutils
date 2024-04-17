from fractions import Fraction
from .expected_value import expected_value as E
from ..conditional_variables import ConditionalVariable


def variance(X: ConditionalVariable) -> Fraction:
    return E(X ** 2) - E(X) ** 2


__all__ = [
    'variance'
]
