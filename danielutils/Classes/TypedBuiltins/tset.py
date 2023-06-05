from typing import Generic, TypeVar
from .factory import create_typed_class
T = TypeVar("T")
parent: type = create_typed_class("tset", set)


class tset(parent, Generic[T]):  # type:ignore
    def subscribable_init(self, *args, **kwargs):
        print(self.get_params())


__all__ = [
    "tset"
]
