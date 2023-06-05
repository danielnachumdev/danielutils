
from typing import Generic, TypeVar
from .factory import create_typed_class
T = TypeVar("T")
parent_ttuple: type = create_typed_class("ttuple", tuple)


class ttuple(parent_ttuple, Generic[T]):
    ...


__all__ = [
    "ttuple"
]
