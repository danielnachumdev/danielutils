from __future__ import annotations
from typing import Any, Iterable
from ..Decorators import validate, overload
from ..Functions import isoftype


class tlist(list):
    """tlist is same as builtin python list but with added type restriction

    Args:
        type (type): the allowed type, can be nested type
        iterable (Iterable, optional): the value to create the tlist from. Defaults to None.
    """

    def _get_error_msg(self, v: Any) -> str:
        """generates the generic error message

        Args:
            v (Any): value to include in the message

        Returns:
            str: the error message
        """
        return f"A value is of the wrong type:\n'{v}' is of type '{type(v)}' but should be of type '{self.T}'"

    @validate
    def __init__(self, T: type, iterable: Iterable = None):
        """_summary_

        Args:
            type (type): the allowed type, can be nested type
        iterable (Iterable, optional): the value to create the tlist from. Defaults to None.

        Raises:
            TypeError: _description_
        """
        self.T = T
        if iterable is not None:
            for v in iterable:
                if not isoftype(v, T):
                    raise TypeError(self._get_error_msg(v))
                super().append(v)

    def __setitem__(self, index: int, value: Any) -> None:
        if not isoftype(value, self.T):
            raise TypeError(self._get_error_msg(value))
        super()[index] = value

    def append(self, value: Any) -> None:
        if not isoftype(value, self.T):
            raise TypeError(self._get_error_msg(value))
        super().append(value)

    @validate
    def extend(self, iterable: Iterable) -> None:
        for v in iterable:
            self.append(v)

    # TODO implement this function
    def __add__(self, other: tlist | list) -> tlist:
        raise NotImplementedError("Should be implemented")


class tdict(dict):
    """like builtin dict but only a specif type is allowed
    """
    @overload(None, type, type)
    def __init__(self, key_t: type, val_t: type):
        self.key_t = key_t
        self.val_t = val_t
        super().__init__()

    @overload(None, type, type, Iterable)
    def __init__(self, keyt: type, val_t: type, iterable: Iterable[tuple]):
        self.key_t = keyt
        self.val_t = val_t
        super().__init__(iterable)

    @overload(None, type, type, dict)
    def __init__(self, key_t: type, val_t: type, ** kwargs):
        """dict(type,type) -> new empty dictionary dict(mapping) -> new dictionary initialized from a mapping object's
    (key, value) pairs
dict(type,type,iterable) -> new dictionary initialized as if via:
    d = {} for k, v in iterable:
        d[k] = v
dict(type,type,**kwargs) -> new dictionary initialized with the name=value pairs
    in the keyword argument list. For example: dict(one=1, two=2)
        """
        self.key_t = key_t
        self.val_t = val_t
        super().__init__(**kwargs)

    def __setitem__(self, key, value) -> None:
        if not isoftype(key, self.key_t):
            raise TypeError(
                f"In class 'tdict' error creating new key-value pair as"
                f" key = '{key}' is not of type '{self.key_t}'")
        if not isoftype(value, self.val_t):
            raise TypeError(
                f"In class 'tdict' error creating new key-value pair"
                f" as value = '{value}' is not of type '{ self.val_t}'")
        super().__setitem__(key, value)

    def __str__(self):
        return f"dict[{self.key_t.__name__}, {self.val_t.__name__}]: {super().__str__()}"


# TODO tset
class tset(set):
    """like builtin set but only allows specified type
    """

    def __init__(self):
        pass


__all__ = [
    "tlist",
    "tdict"
]
