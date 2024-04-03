from typing import Callable

import danielutils


def ProbabilityFunction(expr) -> float:
    return expr.evaluate()


def ExpectedValue(X: "ConditionalVariable") -> float:
    from danielutils import Ber, Geo
    if isinstance(X, Ber):
        return X.p
    elif isinstance(X, Geo):
        return 0
    res = 0
    for x in X.supp:
        res += x * ProbabilityFunction(X == x)
    return res


E: Callable = ExpectedValue
__all__ = [
    "ProbabilityFunction",
    "ExpectedValue",
]
