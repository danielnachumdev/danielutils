from abc import ABC, abstractmethod


class ActivationFunction(ABC):
    @abstractmethod
    def __call__(self, x: float) -> float: ...


__all__ = [
    'ActivationFunction'
]
