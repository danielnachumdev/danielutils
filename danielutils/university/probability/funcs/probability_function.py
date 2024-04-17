from ..protocols import Evaluable
from fractions import Fraction


def probability_function(*evaluables: Evaluable[Fraction]) -> Fraction:
    res = Fraction(1, 1)
    for evaluable in evaluables:
        res *= evaluable.evaluate()
    return res


__all__ = [
    'probability_function',
]
