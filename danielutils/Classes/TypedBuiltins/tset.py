from typing import Generic, TypeVar, Iterable
from .factory import create_typed_class
from ...Functions import isoftype
T = TypeVar("T")
parent: type = create_typed_class("tset", set)


class tset(parent, Generic[T]):  # type:ignore
    """like 'set' but with runtime type safety
    """

    def subscribable_init(self, *args, **kwargs):  # pylint: disable=unused-argument
        """the "real" __init__ function
        """
        print(self.get_params())

    def add(self, value: T) -> None:
        """adds an item to the set

        Args:
            value (T): item

        Raises:
            TypeError: if item is if the wrong type
        """
        if not isoftype(value, self.get_params()):
            raise TypeError(
                f"Can't add. Expected {self.get_params()} but got '{value}' which is {type(value)}")
        set.add(self, value)

    def update(self, *s: Iterable[T]) -> None:
        """updates the set with another iterable
        """
        for value in s:
            if isinstance(value, Iterable):
                for subv in value:
                    self.update(subv)  # type:ignore
            else:
                self.add(value)  # type:ignore

    def union(self, *s: Iterable[T]) -> "tset[T]":
        """creates a union of two sets

        Returns:
            tset[T]: the resulting set
        """
        type_set = set(self.get_params())
        for value in s:
            if isinstance(value, Iterable):
                for subv in value:
                    type_set.add(type(subv))
            else:
                type_set.add(type(value))
        final_type = next(iter(type_set))
        for t in type_set:
            final_type = final_type | t
        res = tset[final_type]()  # type:ignore
        # we can skip the type checking because they will be okay
        set.update(res, self)
        for value in s:
            set.update(res, value)
        return res


__all__ = [
    "tset"
]
