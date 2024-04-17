from ..protocols import Evaluable
from fractions import Fraction


def probability_function(evaluable: Evaluable[Fraction]) -> Fraction:
    return evaluable.evaluate()


__all__ = [
    'probability_function',
]
