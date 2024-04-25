from enum import Enum
from typing import Set as t_set
from ...reflection import get_python_version

if get_python_version() >= (3, 9):
    from builtins import set as t_set


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
    def strong_inequalities() -> t_set['Operator']:
        return {Operator.GT, Operator.LT}

    @staticmethod
    def weak_inequalities() -> t_set['Operator']:
        return {Operator.GE, Operator.LE}

    @staticmethod
    def inequalities() -> t_set['Operator']:
        return Operator.strong_inequalities().union(Operator.weak_inequalities())

    @staticmethod
    def equalities() -> t_set['Operator']:
        return {Operator.EQ, Operator.NE}

    @staticmethod
    def greater_than_inequalities() -> t_set['Operator']:
        return {Operator.GE, Operator.GT}

    @staticmethod
    def less_than_inequalities() -> t_set['Operator']:
        return {Operator.LE, Operator.LT}

    @staticmethod
    def order_operators() -> t_set['Operator']:
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
