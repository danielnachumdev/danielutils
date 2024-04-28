from enum import Enum
from typing import Set as Set
from ...reflection import get_python_version

if get_python_version() >= (3, 9):
    from builtins import set as Set


class Operator(Enum):
    """
    Operator Enum to define the types of operators.
    """
    EQ = "=="
    NE = "!="
    GT = ">"
    GE = ">="
    LT = "<"
    LE = "<="

    @staticmethod
    def strong_inequalities() -> Set['Operator']:
        return {Operator.GT, Operator.LT}

    @staticmethod
    def weak_inequalities() -> Set['Operator']:
        return {Operator.GE, Operator.LE}

    @staticmethod
    def inequalities() -> Set['Operator']:
        return Operator.strong_inequalities().union(Operator.weak_inequalities())

    @staticmethod
    def equalities() -> Set['Operator']:
        return {Operator.EQ, Operator.NE}

    @staticmethod
    def greater_than_inequalities() -> Set['Operator']:
        return {Operator.GE, Operator.GT}

    @staticmethod
    def less_than_inequalities() -> Set['Operator']:
        return {Operator.LE, Operator.LT}

    @staticmethod
    def order_operators() -> Set['Operator']:
        return Operator.inequalities().union(Operator.equalities())

    MUL = "*"
    DIV = "/"
    MODULUS = "%"
    GIVEN = '|'
    AND = '&'
    POW = '**'
    ADD = "+"
    SUB = "-"

    @property
    def inverse(self) -> 'Operator':
        """
        Returns the inverse of the operator.
        Returns:
            Operator (Enum): the inverse of the operator.
        """
        dct = {
            Operator.EQ: Operator.NE,
            Operator.NE: Operator.EQ,
            Operator.GT: Operator.LE,
            Operator.LE: Operator.GT,
            Operator.GE: Operator.LT,
            Operator.LT: Operator.GE
        }
        if self not in dct:
            raise ValueError(f"Operator.{self.name} does not support 'inverse'.")
        return dct[self]


__all__ = [
    "Operator"
]
