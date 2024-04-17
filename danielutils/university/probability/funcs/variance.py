from fractions import Fraction
from .expected_value import expected_value as E
from ..conditional_variables import ConditionalVariable
from ..protocols import VariableCalculable


def variance(obj: ConditionalVariable) -> Fraction:
    if isinstance(obj, VariableCalculable):
        return obj.variance()
    X = obj
    return E(X ** 2) - E(X) ** 2


__all__ = [
    'variance'
]
