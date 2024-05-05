from .activation_function import ActivationFunction


class ReLU(ActivationFunction):
    def __call__(self, x: float) -> float:
        return max(x, 0)


__all__ = [
    "ReLU"
]
