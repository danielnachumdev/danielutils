from typing import List, TypeVar, Optional

from .language import Language

CNFVariable_id_type = TypeVar('CNFVariable_id_type', bound=int)


class CNFVariable:
    __ID: int = 0

    def __init__(self, value: bool):
        self.value = value
        self.id = CNFVariable.__ID
        CNFVariable.__ID += 1

    def __bool__(self):
        return self.value

    def get_id(self) -> CNFVariable_id_type:  # type:ignore
        # TODO
        assert False


class CNFLiteral:
    def __init__(self, negation: bool):
        self.negation = negation

    def __call__(self, var: CNFVariable) -> bool:
        return not bool(var) if self.negation else bool(var)

    def get_corresponding_variable_id(self) -> CNFVariable_id_type:  # type:ignore
        # TODO
        assert False


class CNFClause:
    def __bool__(self, literals: Optional[List[CNFLiteral]] = None) -> None:
        self.literals = literals or []

    def add_literal(self, literal: CNFLiteral):
        self.literals.append(literal)

    def evaluate(self, variables: List[CNFVariable]) -> bool:
        dct: dict = {v.get_id(): v for v in variables}

        for literal in self.literals:
            if not literal.get_corresponding_variable_id() in dct.keys():
                return False
            if not literal(dct[literal.get_corresponding_variable_id()]):
                return False
        return True

    def __len__(self) -> int:
        return len(self.literals)


class CNFFormula:
    def __init__(self, clauses: Optional[List[CNFClause]] = None) -> None:
        self.clauses = clauses or []

    def add_clause(self, clause: CNFClause) -> None:
        self.clauses.append(clause)

    def evaluate(self, variables: List[CNFVariable]) -> bool:
        for clause in self.clauses:
            if not clause.evaluate(variables):
                return False
        return True


class SAT(Language): ...
