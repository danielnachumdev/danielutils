from .evaluable import Evaluable


def ProbabilityFunction(expr: Evaluable) -> float:
    return expr.evaluate()


def ExpectedValue(X: "ConditionalVariable") -> float:
    from danielutils import Ber, Geo
    if isinstance(X, Ber):
        return X.p
    elif isinstance(X, Geo):
        return 0
    if X.supp.is_finite:
        res = 0
        for x in X.supp:
            res += x * ProbabilityFunction(X == x)
        return res
    raise ValueError(f"Can't compute expected value for {X}")


E = ExpectedValue


def Variance(X: "ConditionalVariable") -> float:
    return (E(X)) ** 2 - E(X ** 2)


def Covariance(X: "ConditionalVariable", Y: "ConditionalVariable") -> float:
    # cov := E((X - E(X)) * (Y - E(Y))) <=> E(X * Y) - E(X) - E(Y)
    return E(X * Y) - E(X) - E(Y)


__all__ = [
    "ProbabilityFunction",
    "ExpectedValue",
    "Variance"
]
