
import types
from typing import Generic, TypeVar, Any, Union, Iterable, get_args, SupportsIndex
from ...Decorators import OverloadMeta
from ...Functions import isoftype
from ...Reflection import get_caller_name
T = TypeVar("T", bound=Any)


def types_subseteq(a: type | Iterable[type], b: type | Iterable[type]) -> bool:
    def to_set(x) -> set[int]:
        if type(x) in {types.UnionType}:
            return set(id(xi) for xi in get_args(x))

        return set([id(x)])

    return to_set(a).issubset(to_set(b))


class tlist(Generic[T]):
    """like 'list' but with runtime type safety

    """
    @classmethod
    def __class_getitem__(cls, item: type):
        def __class_getitem_wrapper__(*args, **kwargs):
            return cls(item, *args, **kwargs)
        return __class_getitem_wrapper__

    def __init__(self, item, *args, **kwargs) -> None:
        if not get_caller_name(0) == "__class_getitem_wrapper__":
            raise ValueError(
                f"Can't instantiate {self.__class__.__name__} without a supplied type")
        self.params = item
        self.lst: list[T] = []
        self._additional_init(self, *args, **kwargs)

    @OverloadMeta.overload
    def _additional_init(self, lst: Union[list, "tlist"]):
        self.extend(lst)

    @_additional_init.overload
    def init_empty(self):
        """inits an empty tlist
        """

    @_additional_init.overload
    def init_from_set_and_dict(self, obj: set | dict):
        """inits the tlist from a set or a dict object
        Args:
            obj (set | dict): the set or dict instance
        """
        self.extend(list(obj))

    def extend(self, other: Iterable) -> "tlist":
        """extends a tlist from a list or a tlist

        Args:
            other (list | tlist): the list to extend from

        Returns:
            tlist: Self
        """
        if isinstance(other, tlist):
            if types_subseteq(other.params, self.params):
                self.lst.extend(other.lst)
                return self
        for value in other:
            self.append(value)
        return self

    def append(self, value: T) -> "tlist":
        """appends a value to the list

        Args:
            value (T): the value to append

        Raises:
            ValueError: if a value is not of the correct type

        Returns:
            tlist: self
        """
        if not isoftype(value, self.params):
            raise TypeError(
                f"In tlist.append: values must be of type {self.params}, but '{value}' is of type {type(value)}")
        self.lst.append(value)
        return self

    def __iter__(self):
        return iter(self.lst)

    def __str__(self) -> str:
        return "tlist "+str(self.lst)

    def __repr__(self) -> str:
        return "tlist "+repr(self.lst)

    def __getitem__(self, index: SupportsIndex) -> T:
        return self.lst[index]

    def __setitem__(self, index: SupportsIndex, value: T):
        if not isoftype(value, self.params):
            raise TypeError(
                "Can't add value to tlist because it is of the wrong type")
        self.lst[index] = value

    def __len__(self) -> int:
        return len(self.lst)

    # def insert(self, index: int, item: Any) -> None:
    #     """Inserts an item at a specific position in the list."""
    #     ...

    # def remove(self, item: Any) -> None:
    #     """Removes the first occurrence of an item from the list."""
    #     ...

    # def pop(self, index: Optional[int] = -1) -> Any:
    #     """Removes and returns the item at the specified index.
    #     If no index is provided, it removes and returns the last item in the list.
    #     """
    #     ...

    # def index(self, item: Any, start: int = 0, end: Optional[int] = None) -> int:
    #     """Returns the index of the first occurrence of an item in the list within the given range."""
    #     ...

    # def count(self, item: Any) -> int:
    #     """Returns the number of occurrences of an item in the list."""
    #     ...

    # def sort(self, key: Optional[callable] = None, reverse: bool = False) -> None:
    #     """Sorts the list in ascending order.
    #     The optional `key` argument allows custom sorting based on a specific criterion,
    #     and the `reverse` argument determines whether to sort in descending order.
    #     """
    #     ...

    # def reverse(self) -> None:
    #     """Reverses the order of the items in the list."""
    #     ...

    # def copy(self) -> list:
    #     """Returns a shallow copy of the list."""
    #     ...

    # def clear(self) -> None:
    #     """Removes all items from the list."""
    #     ...

    # def length(self) -> int:
    #     """Returns the number of items in the list."""
    #     ...

    # @classmethod
    # def create_list(cls, iterable: Iterable[Any]) -> 'MyList':
    #     """Creates a new MyList object initialized with the elements from the given iterable."""
    #     ...


__all__ = [
    "tlist"
]
