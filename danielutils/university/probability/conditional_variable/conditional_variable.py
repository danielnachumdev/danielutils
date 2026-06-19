from abc import ABC, abstractmethod
from fractions import Fraction
from typing import Callable, Any
from ..expressions import ProbabilityExpression, AccumulationExpression
from ..operator import Operator
from ..supp import Supp
from ..protocols import Evaluable

def _create_operator(op: Operator, reverse: bool = False) -> Callable[['ConditionalVariable', Any], Evaluable]:
    def operator(self, other) -> Evaluable:
        lhs, rhs = self, other
        if reverse:
            lhs, rhs = rhs, lhs

        if reverse and op == Operator.ADD and other == 0:
            return self

        if isinstance(other, ConditionalVariable) and op == Operator.ADD:
            combined = _combine_iid_bernoulli_sums(lhs, other)
            if combined is not None:
                return combined

        if isinstance(other, (int, float, Fraction)):
            return ProbabilityExpression(lhs, op, rhs)

        if isinstance(rhs, ProbabilityExpression):
            l = ProbabilityExpression(lhs, op, rhs.lhs)
            r = ProbabilityExpression(rhs.rhs, None, None)
            o = other.op
            return AccumulationExpression(l, o, r)

        raise NotImplementedError("Not Implemented")

    return operator


def _combine_iid_bernoulli_sums(lhs: 'ConditionalVariable', rhs: 'ConditionalVariable'):
    from .discrete.bernoulli import Bernoulli
    from .discrete.binomial import Binomial
    from .discrete.bernoulli_sum import BernoulliSum

    def count_and_p(variable: ConditionalVariable):
        if isinstance(variable, Bernoulli):
            return 1, variable.p
        if isinstance(variable, BernoulliSum):
            return variable.n, variable.p
        if isinstance(variable, Binomial):
            return variable.n, variable.p
        return None, None

    left_n, left_p = count_and_p(lhs)
    right_n, right_p = count_and_p(rhs)
    if left_n is None or right_n is None or left_p != right_p:
        return None
    return BernoulliSum(left_p, left_n + right_n)

class ConditionalVariable(ABC):
    OPERATOR_TYPE = Callable[['ConditionalVariable', Any], Evaluable]


    __eq__: OPERATOR_TYPE = _create_operator(Operator.EQ)  # type:ignore
    __ne__: OPERATOR_TYPE = _create_operator(Operator.NE)  # type:ignore
    __gt__: OPERATOR_TYPE = _create_operator(Operator.GT)
    __ge__: OPERATOR_TYPE = _create_operator(Operator.GE)
    __lt__: OPERATOR_TYPE = _create_operator(Operator.LT)
    __le__: OPERATOR_TYPE = _create_operator(Operator.LE)

    __or__: OPERATOR_TYPE = _create_operator(Operator.GIVEN)
    __ror__: OPERATOR_TYPE = _create_operator(Operator.GIVEN, reverse=True)
    __and__: OPERATOR_TYPE = _create_operator(Operator.AND)
    __rand__: OPERATOR_TYPE = _create_operator(Operator.AND, reverse=True)

    __mul__: OPERATOR_TYPE = _create_operator(Operator.MUL)
    __truediv__: OPERATOR_TYPE = _create_operator(Operator.DIV)
    __mod__: OPERATOR_TYPE = _create_operator(Operator.MODULUS)
    __pow__: OPERATOR_TYPE = _create_operator(Operator.POW)
    __add__: OPERATOR_TYPE = _create_operator(Operator.ADD)
    __radd__: OPERATOR_TYPE = _create_operator(Operator.ADD, reverse=True)
    __sub__: OPERATOR_TYPE = _create_operator(Operator.SUB)
    __rsub__: OPERATOR_TYPE = _create_operator(Operator.SUB, reverse=True)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"

    def is_identical(self, other) -> bool:
        if not isinstance(other, ConditionalVariable):
            return False
        return self is other

    def is_independent(self, other) -> bool:
        if not isinstance(other, ConditionalVariable):
            return False
        if self is other:
            return False
        if not self.supp.is_finite and not other.supp.is_finite:
            raise ValueError("Can't check if two variables are independent if their supp is not finite")

        if self.supp != other.supp:
            return False
        from ..funcs import probability_function as P
        for k in self.supp:
            if not (P((self == k) & (other == k)) == P(self == k) * P(other == k)):
                return False
        return True

    def is_dependent(self, other) -> bool:
        return not self.is_independent(other)

    def is_correlated(self, other) -> bool:
        if not isinstance(other, ConditionalVariable):
            return False
        from ..funcs import covariance as cov
        return cov(self, other) == 0

    def is_uncorrelated(self, other) -> bool:
        return not self.is_correlated(other)

    @abstractmethod
    def evaluate(self, other: Any, operator: Operator) -> Fraction:
        ...

    @abstractmethod
    def between(self, a, b, *args) -> Fraction:
        ...

    @property
    @abstractmethod
    def supp(self) -> Supp:
        ...

    @abstractmethod
    def is_equal(self, other) -> bool:
        ...


__all__ = [
    "ConditionalVariable"
]
