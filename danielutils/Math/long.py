from __future__ import annotations
from ..Typing import Tuple
from ..Decorators import validate, overload
from .Functions import sign


class long__:
    pass


class long(long__):
    @overload(None, str, str)
    def __init__(self, prefix: str, fraction: str):
        self.prefix = prefix
        self.fraction = fraction
        self.sign = sign(int(prefix[:3]))

    @overload(None, str)
    def __init__(self, number_as_text: str):
        if "." in number_as_text:
            self.prefix, self.fraction = number_as_text.split(".")
        else:
            self.prefix, self.fraction = number_as_text, '0'
        self.sign = sign(int(self.prefix[:3]))

    @overload(None)
    def __init__(self):
        self.prefix = "0"
        self.fraction = "0"
        self.sign = 1

    def __str__(self) -> str:
        if self.sign == 1:
            if self.fraction == '0':
                return self.prefix
            return f"{self.prefix}.{self.fraction}"
        else:
            if self.fraction == '0':
                return f"-{self.prefix}"
            return f"-{self.prefix}.{self.fraction}"

    def __repr__(self) -> str:
        return str(self)

    @overload(None, int)
    def __add__(self, v: int) -> long:
        return self + long(f"{v}.0")

    @overload(None, float)
    def __add__(self, v: float) -> long:
        return self + long(f"{v}")

    @overload(None, long__)
    def __add__(self, v: long) -> long:
        def long_addition(s1: str, s2: str) -> str:
            l1 = len(s1)
            l2 = len(s2)
            start_index = min(l1, l2)-1
            if l1 <= l2:
                append_to_res = s2[:l2-1-start_index]
            else:
                append_to_res = s1[start_index+1:]
            res = ""
            carry = 0
            for i in range(0, start_index+1, ):
                dig1 = int(s1[-(i+1)])
                dig2 = int(s2[-(i+1)])
                sum = dig1+dig2+carry
                carry = sum // 10
                sum = sum % 10
                res += str(sum)
            if len(append_to_res) > 0:
                append_to_res = str(int(append_to_res)+carry)
            res += append_to_res
            res = res[::-1]
            return res
        fraction = long_addition(self.fraction, v.fraction)
        prefix = long_addition(self.prefix, v.prefix)
        return long(prefix, fraction)

    @overload(None, int)
    def __mul__(self, v: int) -> long:
        return self * long(f"{v}.0")

    @overload(None, float)
    def __mul__(self, v: float) -> long:
        return self * long(f"{v}")

    @overload(None, long__)
    def __mul__(self, v: long) -> long:
        def long_multiplication(s1: str, s2: str) -> long:
            l1 = len(s1)
            l2 = len(s2)
            start_index = min(l1, l2)-1
            res = long()
            for i in range(start_index, -1, -1):
                for j in range(start_index, -1, -1):
                    dig1 = int(s1[i])
                    dig2 = int(s2[j])
                    total = str(dig1*dig2)
                    total = total.ljust(len(total)+l1-i+l2-j-2, '0')
                    res += long(total)
            return res
        fraction = long_multiplication(self.fraction, v.fraction)
        prefix = long_multiplication(self.prefix, v.prefix)
        return long(prefix.prefix, fraction.prefix)


__all__ = [
    "long"
]
