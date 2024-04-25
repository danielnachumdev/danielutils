from typing import Any, Callable, Optional
from fractions import Fraction
from ..protocols import Evaluable
from ..operator import Operator


def _create_operator(op: Operator, reverse: bool = False) -> Callable[['ConditionalVariable', Any], Evaluable]:
    def operator(self: 'ProbabilityExpression', other: Any) -> Evaluable:
        lhs, rhs = self, other
        if reverse:
            lhs, rhs = rhs, lhs
        from .accumulation_expression import AccumulationExpression

        if op in Operator.order_operators():
            if isinstance(rhs, (int, float, Fraction)):
                if op in Operator.inequalities():
                    rhs = ProbabilityExpression(lhs.lhs, op, rhs)
                    return AccumulationExpression(lhs, Operator.AND, rhs)
                elif op == Operator.EQ:
                    return AccumulationExpression(lhs, op, ProbabilityExpression(rhs))
            elif isinstance(rhs, (ProbabilityExpression, AccumulationExpression)):
                if isinstance(other, ProbabilityExpression):
                    # TODO P((0<X)<(Y<5))
                    # I think that this is the solution
                    return AccumulationExpression(self, op, other)
            raise NotImplementedError("Illegal state")
        if op in {Operator.AND, Operator.GIVEN}:
            if not isinstance(other, ProbabilityExpression):
                raise NotImplementedError("Illegal state")
            return AccumulationExpression(lhs, op, rhs)
        raise NotImplementedError("Illegal state 2")

    return operator
class ProbabilityExpression(Evaluable):
    OPERATOR_TYPE = Callable[['ProbabilityExpression', Any], 'AccumulationExpression']


    def __init__(self, lhs: Evaluable, op: Optional[Operator] = None, rhs: Optional[Any] = None):
        self._lhs = lhs
        self._op = op
        self._rhs = rhs

    __eq__: OPERATOR_TYPE = _create_operator(Operator.EQ)
    __gt__: OPERATOR_TYPE = _create_operator(Operator.GT)
    __ge__: OPERATOR_TYPE = _create_operator(Operator.GE)
    __lt__: OPERATOR_TYPE = _create_operator(Operator.LT)
    __le__: OPERATOR_TYPE = _create_operator(Operator.LE)
    __or__: OPERATOR_TYPE = _create_operator(Operator.GIVEN)
    __ror__: OPERATOR_TYPE = _create_operator(Operator.GIVEN, reverse=True)
    __and__: OPERATOR_TYPE = _create_operator(Operator.AND)
    __rand__: OPERATOR_TYPE = _create_operator(Operator.AND, reverse=True)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.lhs} {self.op.value} {self.rhs})"

    def __hash__(self) -> int:
        return hash((self.__class__, self.lhs, self.op, self.rhs))

    @property
    def lhs(self):
        return self._lhs

    @property
    def op(self):
        return self._op

    @property
    def rhs(self):
        return self._rhs

    @property
    def is_partial(self) -> bool:
        return self.op is not None and self.rhs is not None

    def evaluate(self) -> Fraction:
        return self.lhs.evaluate(self.rhs, self.op)

    def is_equal(self, other) -> bool:
        if not isinstance(other, ProbabilityExpression):
            raise TypeError(
                f"Cant compare equality between {self.__class__.__qualname__} and non ConditionalExpression")
        from ..conditional_variable import ConditionalVariable
        if isinstance(self.lhs, ConditionalVariable) and not isinstance(other.lhs, ConditionalVariable):
            return False
        if not isinstance(self.lhs, ConditionalVariable) and isinstance(other.lhs, ConditionalVariable):
            return False
        # We need this complicated thing instead of doing self.lhs == other.lhs (and same for rhs) because we
        # cant use __eq__

        # TODO make better
        if isinstance(self.lhs, ConditionalVariable):
            if not (self.lhs.__class__ == other.lhs.__class__):
                return False
        else:
            if not (self.lhs == other.lhs):
                return False

        if isinstance(self.rhs, ConditionalVariable):
            if not (self.rhs.__class__ == other.rhs.__class__):
                return False
        else:
            if not (self.rhs == other.rhs):
                return False

        return self.op == other.op


__all__ = [
    'ProbabilityExpression',
]
