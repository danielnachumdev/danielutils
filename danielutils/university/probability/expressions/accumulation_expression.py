from fractions import Fraction
from typing import Callable, Any
from ..protocols import Evaluable
from ..operator import Operator
from ....data_structures import BinarySyntaxTree as BST


class AccumulationExpression(Evaluable):
    OPERATOR_TYPE = Callable[['AccumulationExpression', Any], 'AccumulationExpression']

    def __init__(self, lhs: 'ProbabilityExpression', op: Operator, rhs: 'ProbabilityExpression'):
        N = BST.Node
        l = N(lhs.op, N(lhs.lhs), N(lhs.rhs))
        r = N(rhs.op, N(rhs.lhs), N(rhs.rhs))
        self._tree = BST(N(op, l, r))

    @staticmethod
    def _create_operator(op, reverse: bool = False) -> Callable[
        ['AccumulationExpression', Any], 'AccumulationExpression']:
        def operator(self, other: Any) -> 'AccumulationExpression':
            op
            assert False
            return self

        return operator

    __gt__: OPERATOR_TYPE = _create_operator(Operator.GT)
    __ge__: OPERATOR_TYPE = _create_operator(Operator.GE)
    __lt__: OPERATOR_TYPE = _create_operator(Operator.LT)
    __le__: OPERATOR_TYPE = _create_operator(Operator.LE)
    __and__: OPERATOR_TYPE = _create_operator(Operator.AND)
    __or__: OPERATOR_TYPE = _create_operator(Operator.GIVEN)

    def evaluate(self) -> Fraction:
        # self._tree.evaluate({
        #     Operator.GT: lambda X, n: X.evaluate(n, Operator.GT),
        #     Operator.GE: lambda X, n: X.evaluate(n, Operator.GE),
        #     Operator.LT: lambda X, n: X.evaluate(n, Operator.LT),
        #     Operator.LE: lambda X, n: X.evaluate(n, Operator.LE),
        #     Operator.EQ: lambda X, n: X.evaluate(n, Operator.EQ),
        #     Operator.NE: lambda X, n: X.evaluate(n, Operator.NE),
        # })
        if self._tree.root.data==Operator.AND:
            pass

    def _insert_right(self, obj) -> None:
        pass

    def _insert_left(self, obj) -> None:
        pass


__all__ = [
    'AccumulationExpression'
]
