from .evaluable import Evaluable


def ProbabilityFunction(expr: Evaluable) -> float:
    return expr.evaluate()


def ExpectedValue(expr: Evaluable) -> float:
    pass


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
