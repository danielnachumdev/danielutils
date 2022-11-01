from __future__ import annotations
from ..Decorators import overload, validate


class Polynomial:
    def __init__(self, prefixes: list[int], powers: list[int]):

        self.prefixes = sorted(prefixes)
        self.powers = sorted(powers)

    def __len__(self) -> int:
        return len(self.prefixes)

    def __call__(self, value):
        res = 0
        for i in range(len(self)):
            res += self.prefixes[i]*(value**self.powers[i])
        return res

    @overload(None, int)
    def __add__(self, num: int) -> Polynomial:
        if self.powers[-1] == 0:
            prefixes = self.prefixes
            prefixes[-1] += num
            return Polynomial(prefixes, self.powers)
        return Polynomial(self.prefixes+[num], self.powers+[0])
