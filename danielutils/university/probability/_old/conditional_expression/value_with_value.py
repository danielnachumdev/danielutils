from .conditional_expression import ConditionalExpression


class ValueWithValue(ConditionalExpression):
    def _evaluate(self, op) -> float:
        return int(self._lhs == self._rhs)


__all__ = [
    "ValueWithValue"
]
