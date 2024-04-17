from enum import Enum


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

    MUL = "*"
    DIV = "/"
    MODULUS = "%"
    GIVEN = '|'
    AND = '&'
    POW = '**'

    @property
    def inverse(self) -> 'Operator':
        """
        Returns the inverse of the operator.
        Returns:
            Operator (Enum): the inverse of the operator.
        """
        return {
            Operator.EQ: Operator.NE,
            Operator.NE: Operator.EQ,
            Operator.GT: Operator.LE,
            Operator.LE: Operator.GT,
            Operator.GE: Operator.LT,
            Operator.LT: Operator.GE
        }[self]


__all__ = [
    "Operator"
]
