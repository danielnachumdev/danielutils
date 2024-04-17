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

    @staticmethod
    def strong_inequalities() -> set['Operator']:
        return {Operator.GT, Operator.LT}

    @staticmethod
    def weak_inequalities() -> set['Operator']:
        return {Operator.GE, Operator.LE}

    @staticmethod
    def inequalities() -> set['Operator']:
        return Operator.strong_inequalities().union(Operator.weak_inequalities())

    @staticmethod
    def equalities() -> set['Operator']:
        return {Operator.EQ, Operator.NE}

    @staticmethod
    def greater_than_inequalities() -> set['Operator']:
        return {Operator.GE, Operator.GT}

    @staticmethod
    def less_than_inequalities() -> set['Operator']:
        return {Operator.LE, Operator.LT}

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
