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
    def __init__(self, T: type, iterable: Iterable = None):
        """_summary_

        Args:
            type (type): the allowed type, can be nested type
        iterable (Iterable, optional): the value to create the tlist from. Defaults to None.

        Raises:
            TypeError: _description_
        """
        tbase.__init__(T)
        if iterable is not None:
            for v in iterable:
                if not isoftype(v, T):
                    raise TypeError(self._get_error_msg(v))
                list.append(v)

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


__all__ = [
    "tlist"
]
