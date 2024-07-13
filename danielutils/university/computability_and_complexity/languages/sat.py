from typing import List

from .language import Language


class CNFVariable:
    __ID: int = 0

    def __init__(self, value: bool):
        self.value = value
        self.id = CNFVariable.__ID
        CNFVariable.__ID += 1

    def __bool__(self):
        return self.value


class CNFLiteral:
    def __init__(self, negation: bool):
        self.negation = negation

    def __call__(self, var: CNFVariable) -> bool:
        return not bool(var) if self.negation else bool(var)


class CNFClause:
    def __bool__(self, literals: List[CNFLiteral]) -> None:
        self.literals = literals

    def add_literal(self, literal: CNFLiteral):
        self.literals.append(literal)

    def evaluate(self, variables: List[CNFVariable]) -> bool:
        for literal in self.literals:
            pass


class CNFFormula: ...


class SAT(Language): ...
