from typing import TypeVar, List as List
from copy import deepcopy
from fractions import Fraction
from ...reflection import get_python_version

if get_python_version() >= (3, 9):
    from builtins import list as List
    from builtins import dict as Dict
from ...print_ import mprint

Number = TypeVar("Number", int, float, Fraction, complex)


class Polynomial:
    def __init__(self, coefficients: List[Number], powers: List[Number]):
        self._coefficients = coefficients
        self._powers = powers

    @property
    def coefficients(self) -> List[Fraction]:
        return deepcopy(self._coefficients)

    @property
    def powers(self) -> List[Fraction]:
        return deepcopy(self._powers)

    def __len__(self):
        return len(self.coefficients)


__all__ = [
    "Polynomial"
]
