import danielutils
def ProbabilityFunction(expr) -> float:
    return expr.evaluate()


P = ProbabilityFunction


def ExpectedValue(X: "ConditionalVariable") -> float:
    from danielutils import Ber, Geo
    if isinstance(X, Ber):
        return X.p
    elif isinstance(X, Geo):
        return 0
    res = 0
    for x in X.supp:
        res += x * P(X == x)
    return res


E = ExpectedValue
__all__ = [
    "ProbabilityFunction",
    "P",
    "ExpectedValue",
    "E"
]
