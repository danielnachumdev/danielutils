from typing import Generic, TypeVar, Any, Union, Iterable, SupportsIndex
# from ...metaclasses.OverloadMeta import OverloadMeta
from ...functions import isoftype, types_subseteq
# from ...reflection import get_caller_name
from ...decorators import overload
from .factory import create_typed_class
T = TypeVar("T", bound=Any)


# class ptlist(t_list[T], Generic[T]):
#     """like 'list' but with runtime type safety
#     """

#     @classmethod
#     def __class_getitem__(cls, item: type):
#         return cls(item)

#     def __instancecheck__(self, instance: Any) -> bool:
#         if isinstance(instance, ptlist):
#             return types_subseteq(instance._params, self._params)
#         return isoftype(instance, t_list[self._params])  # type: ignore

#     def __init__(self, item) -> None:
#         if not get_caller_name(0) == "__class_getitem__":
#             raise ValueError(
#                 f"Can't instantiate {self.__class__.__name__} without a supplied type")
#         list.__init__(self)
#         self._params = item

#     def __call__(self, *args, **kwargs):
#         # to work with the overloading
#         type(self)._additional_init(self, *args, **kwargs)
#         return self

#     @OverloadMeta.overload
#     def _additional_init(self, lst: Union[list, "ptlist"]):
#         self.extend(lst)

#     @_additional_init.overload
#     def _init_empty(self) -> None:
#         """inits an empty tlist
#         """

#     @_additional_init.overload
#     def _init_from_set_and_dict(self, obj: Union[set, dict]):
#         """inits the tlist from a set or a dict object
#         Args:
#             obj (set | dict): the set or dict instance
#         """
#         self.extend(list(obj))

#     def extend(self, other: Iterable) -> None:
#         """extends a tlist from a list or a tlist

#         Args:
#             other (list | tlist): the list to extend from

#         Returns:
#             tlist: Self
#         """
#         if isinstance(other, ptlist):
#             if types_subseteq(other._params, self._params):
#                 list.extend(self, other)
#                 return
#         for value in other:
#             self.append(value)

#     def append(self, value: T) -> None:
#         """appends a value to the list

#         Args:
#             value (T): the value to append

#         Raises:
#             ValueError: if a value is not of the correct type

#         Returns:
#             tlist: self
#         """
#         if not isoftype(value, self._params):
#             raise TypeError(
#                 f"In tlist.append: values must be of type {self._params}, but '{value}' is of type {type(value)}")
#         list.append(self, value)

#     def __str__(self) -> str:
#         return "tlist "+list.__str__(self)

#     def __repr__(self) -> str:
#         return "tlist "+list.__repr__(self)

#     def __setitem__(self, index: SupportsIndex, value: T):  # type:ignore
#         if not isoftype(value, self._params):
#             raise TypeError(
#                 "Can't add value to tlist because it is of the wrong type")
#         list.__setitem__(self, index, value)

#     def __eq__(self, other: Any) -> bool:
#         if not isoftype(other, Union[ptlist, list]):
#             return list.__eq__(self, other)
#         if isinstance(other, ptlist):
#             if self._params != other._params:
#                 return False
#         if len(self) != len(other):
#             return False
#         for a, b in zip(iter(self), iter(other)):
#             if a != b:
#                 return False
#         return True

#     def __add__(self, other: Any) -> "ptlist":
#         if not isoftype(other, Union[ptlist, list]):
#             raise NotImplementedError()

#         # no need to check because the error handling
#         # will be done inside extend so the error will
#         # propagate up
#         res = ptlist[self._params](self)  # type:ignore
#         res.extend(other)
#         return res

#     def __mul__(self, other: Any) -> "ptlist":
#         if not isinstance(other, int):
#             raise NotImplementedError()

#         res = ptlist[self._params](self)  # type:ignore
#         for _ in range(other-1):
#             res.extend(self)
#         return res


parent: type = create_typed_class("tlist", list)


class tlist(parent, Generic[T]):
    """like 'list' but with runtime type safety
    """

    def subscribable_init(self, *args, **kwargs):
        """the "real" __init__ function
        """
        type(self)._additional_init(self, *args, **kwargs)

    @overload
    def _additional_init(self, lst: Union[list, "tlist"]):
        self.extend(lst)

    @_additional_init.overload
    def _init_empty(self) -> None:
        """inits an empty tlist
        """

    @_additional_init.overload
    def _init_from_set_and_dict(self, obj: Union[set, dict]):
        """inits the tlist from a set or a dict object
        Args:
            obj (set | dict): the set or dict instance
        """
        self.extend(list(obj))

    def extend(self, other: Iterable) -> None:
        """extends a tlist from a list or a tlist

        Args:
            other (list | tlist): the list to extend from

        Returns:
            tlist: Self
        """
        if isinstance(other, tlist):
            if types_subseteq(other.get_params(), self.get_params()):
                list.extend(self, other)
                return
        for value in other:
            self.append(value)

    def append(self, value: T) -> None:
        """appends a value to the list

        Args:
            value (T): the value to append

        Raises:
            ValueError: if a value is not of the correct type

        Returns:
            tlist: self
        """
        if not isoftype(value, self.get_params()[0]):
            raise TypeError(
                f"In tlist.append: values must be of type {self.get_params()[0]},"
                " but '{value}' is of type {type(value)}")
        list.append(self, value)

    def __add__(self, other: Any) -> "tlist":
        if not isoftype(other, Union[list, tlist]):
            raise NotImplementedError()

        # no need to check because the error handling
        # will be done inside extend so the error will
        # propagate up
        res = tlist[self._params](self)  # type:ignore
        res.extend(other)
        return res

    def __mul__(self, other: Any) -> "tlist":
        if not isinstance(other, int):
            raise NotImplementedError()

        res = tlist[self.get_params()[0]](self)  # type:ignore
        for _ in range(other-1):
            res.extend(self)
        return res

    def __setitem__(self, index: SupportsIndex, value: T):  # type:ignore
        if not isoftype(value, self._params):
            raise TypeError(
                "Can't add value to tlist because it is of the wrong type")
        list.__setitem__(self, index, value)


__all__ = [
    "tlist"
]
