from typing import TypeVar
from copy import deepcopy
from fractions import Fraction

from ...print_ import mprint
Number = TypeVar("Number", int, float, Fraction, complex)


class Polynomial:
    def __init__(self, coefficients: list[Number], powers: list[Number]):
        self._coefficients = coefficients
        self._powers = powers

    @property
    def coefficients(self) -> list[Fraction]:
        return deepcopy(self._coefficients)

    @property
    def powers(self) -> list[Fraction]:
        return deepcopy(self._powers)

    def __len__(self):
        return len(self.coefficients)

__all__=[
    "Polynomial"
]