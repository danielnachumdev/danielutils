from __future__ import annotations
from typing import Iterable, Any
from .tbase import tbase
from ...Decorators import validate
from ...Functions import isoftype


class tlist(list, tbase):
    """tlist is same as builtin python list but with added type restriction

    Args:
        type (type): the allowed type, can be nested type
        iterable (Iterable, optional): the value to create the tlist from. Defaults to None.
    """

    @validate
    def __init__(self, T: type, *args, **kwargs):
        tbase.__init__(self, T)
        list.__init__(self, *args, **kwargs)

    def __setitem__(self, index: int, value: Any) -> None:
        if not isoftype(value, self.T):
            raise TypeError(self._get_error_msg(value))
        list.__setitem__(self, index, value)

    def copy(self) -> tlist:
        res = tlist(self.T)
        res._extend(list.copy(self))
        return res

    def append(self, value: Any) -> None:
        if not isoftype(value, self.T):
            raise TypeError(self._get_error_msg(value))
        self._append(value)

    def extend(self, iterable: Iterable) -> None:
        for v in iterable:
            self.append(v)

    def __add__(self, other: tlist | list) -> tlist:
        if isinstance(other, tlist):
            if self.T == other.T:
                self._extend(other)
        else:
            for v in other:
                self.append(v)

    def _append(self, value):
        list.append(self, value)

    def _extend(self, iterable):
        list.extend(self, iterable)


__all__ = [
    "tlist"
]
