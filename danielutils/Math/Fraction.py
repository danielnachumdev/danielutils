from __future__ import annotations
from .Functions import sign
from .Constants import PRIMES_1000
from ..Decorators import validate, overload


class Fraction__:
    pass


class Fraction(Fraction__):
    def __init__(self, nominator, denominator):
        self.sign = sign(denominator)*sign(nominator)
        self.nominator = abs(nominator)
        self.denominator = abs(denominator)
        for prime in PRIMES_1000:
            if self.nominator < prime or self.denominator < prime:
                break
            while self.nominator % prime == self.denominator % prime == 0:
                self.nominator /= prime
                self.denominator /= prime
        self.denominator = int(self.denominator)
        self.nominator = int(self.nominator)

    @overload(None, int)
    def __add__(self, v) -> Fraction:
        return self+Fraction(v, 1)

    @overload(None, float)
    def __add__(self, v) -> Fraction:
        pass

    @overload(None, Fraction__)
    def __add__(self, v: Fraction) -> Fraction:
        a, b = self.nominator, self.denominator
        c, d = v.nominator, v.denominator
        return Fraction(a*d+b*c, b*d)

    def __mul__(self, v) -> Fraction:
        pass

    def __str__(self) -> str:
        if self.nominator == 0:
            return 0
        return f"{self.nominator}/{self.denominator}"

    def __repr__(self) -> str:
        return str(self)


__all__ = [
    "Fraction"
]
