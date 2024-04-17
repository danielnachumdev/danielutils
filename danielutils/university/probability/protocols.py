from fractions import Fraction
from typing import runtime_checkable, Protocol, TypeVar

T = TypeVar('T')


@runtime_checkable
class Evaluable(Protocol[T]):
    def evaluate(self, *args, **kwargs) -> T: ...


@runtime_checkable
class ExpectedValueCalculable(Protocol):
    def expected_value(self) -> Fraction: ...


@runtime_checkable
class VariableCalculable(Protocol):
    def variance(self) -> Fraction: ...


__all__ = [
    'Evaluable',
    'VariableCalculable',
    "ExpectedValueCalculable"
]
