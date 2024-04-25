from typing import TypeVar, List as t_list
from copy import deepcopy
from fractions import Fraction
from ...reflection import get_python_version

if get_python_version() >= (3, 9):
    from builtins import list as t_list
    from builtins import dict as t_dict
from ...print_ import mprint

Number = TypeVar("Number", int, float, Fraction, complex)


class Polynomial:
    def __init__(self, coefficients: t_list[Number], powers: t_list[Number]):
        self._coefficients = coefficients
        self._powers = powers

    @property
    def coefficients(self) -> t_list[Fraction]:
        return deepcopy(self._coefficients)

    @property
    def powers(self) -> t_list[Fraction]:
        return deepcopy(self._powers)

    def __len__(self):
        return len(self.coefficients)


__all__ = [
    "Polynomial"
]
