from enum import Enum


class Operators(Enum):
    GIVEN = "|"
    EQ = "=="
    LT = ">"
    LE = ">="
    GT = "<"
    GE = "<="
    NE = "!="


__all__ = [
    "Operators"
]
