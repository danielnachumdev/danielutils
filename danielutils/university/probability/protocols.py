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


@runtime_checkable
class Equatable(Protocol):
    def is_equal(self, other) -> bool: ...


__all__ = [
    'Evaluable',
    'VariableCalculable',
    "ExpectedValueCalculable",
    'Equatable',
]
