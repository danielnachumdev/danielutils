# from abc import abstractmethod
# from typing import TypeVar, Generic
#
# from ..java_interface import JavaInterface
#
# T = TypeVar('T')
#
#
# class Comparable(JavaInterface, Generic[T]):
#     @abstractmethod
#     def __lt__(self, other: T) -> bool: ...
#
#     @abstractmethod
#     def __gt__(self, other: T) -> bool: ...
#
#     @abstractmethod
#     def __eq__(self, other: T) -> bool: ...
#
#     @abstractmethod
#     def __le__(self, other: T) -> bool: ...
#
#     @abstractmethod
#     def __ge__(self, other: T) -> bool: ...
#
#     @abstractmethod
#     def __ne__(self, other: T) -> bool: ...
#
#
# __all__ = [
#     "Comparable",
# ]
