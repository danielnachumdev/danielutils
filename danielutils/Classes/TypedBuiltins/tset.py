from __future__ import annotations
from typing import Any, TypeVar, Generator
from .tbase import tbase
from ...Functions import isoftype

T = TypeVar("T")


class tset(set, tbase):
    """like builtin set but only allows specified type
    """

    def __init__(self, T: T):
        tbase.__init__(T)
        set.__init__()

    def add(self, v: Any):
        if isoftype(v, self.T):
            set.add(v)

    def clone(self) -> tset:
        res = tset(self.T)
        for v in self:
            res.add(v)
        return res

    def __iter__(self) -> Generator[T, None, None]:
        yield from set.__iter__()

    def union(self, other: tset) -> tset:
        res = self.clone()
        for v in other:
            res.add(v)
        return res


__all__ = [
    "tset"
]
