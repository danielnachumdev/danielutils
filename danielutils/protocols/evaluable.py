import logging
from abc import abstractmethod
from typing import Protocol, TypeVar, runtime_checkable
from .logging_.utils import get_logger

logger = get_logger(__name__)

T = TypeVar('T', covariant=True)


@runtime_checkable
class Evaluable(Protocol[T]):
    @abstractmethod
    def evaluate(self) -> T:
        """
        Evaluate the object and return a value of type T.
        
        Note: This is a protocol method. Implementations should add logging
        to track evaluation operations.
        """
        ...


__all__ = [
    "Evaluable"
]
