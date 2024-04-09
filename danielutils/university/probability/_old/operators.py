from enum import Enum


class Operators(Enum):
    GIVEN = "|"
    AND = "&"
    EQ = "=="
    LT = "<"
    LE = "<="
    GT = ">"
    GE = ">="
    NE = "!="
    ADD = "+"
    SUB = "-"
    POW = "**"

    # def __repr__(self):
    #     return f"Operators.{self.name} '{self.value}'"


__all__ = [
    "Operators"
]
