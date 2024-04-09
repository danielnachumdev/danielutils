from abc import abstractmethod
from typing import Union
from ..operator import Operator
from ..evaluable import Evaluable
from ..complex_expression import ComplexExpression


class ConditionalVariable(Evaluable):
    @abstractmethod
    def evaluate(self, op: Operator, n: float) -> float: ...

    @staticmethod
    def _create_handler(op: Operator):
        def handler(self: "ConditionalVariable", other: Union[Evaluable, float]) -> ComplexExpression:
            pass

        return handler

    __eq__ = _create_handler(Operator.EQ)
    __ne__ = _create_handler(Operator.NE)
    __gt__ = _create_handler(Operator.GT)
    __ge__ = _create_handler(Operator.GE)
    __lt__ = _create_handler(Operator.LT)
    __le__ = _create_handler(Operator.LE)


__all__ = [
    "ConditionalVariable"
]
