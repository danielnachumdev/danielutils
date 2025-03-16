from abc import ABC, abstractmethod


class TimeStrategy(ABC):
    @abstractmethod
    def next(self): ...

    def __call__(self, *args, **kwargs):
        return self.next()

    @abstractmethod
    def reset(self): ...


class ConstantTimeStrategy(TimeStrategy):
    def __init__(self, timeout: float):
        self.timeout = timeout

    def next(self) -> float:
        return self.timeout

    def reset(self) -> None:
        pass  # No state to reset


class LinearTimeStrategy(TimeStrategy):
    def __init__(self, base_timeout: float, step: float):
        self.base_timeout = base_timeout
        self.step = step
        self.current_timeout = base_timeout

    def next(self) -> float:
        timeout = self.current_timeout
        self.current_timeout += self.step
        return timeout

    def reset(self) -> None:
        self.current_timeout = self.base_timeout


class MultiplicativeTimeStrategy(TimeStrategy):
    def __init__(self, base_timeout: float, factor: float):
        self.base_timeout = base_timeout
        self.factor = factor
        self.current_timeout = base_timeout

    def next(self) -> float:
        timeout = self.current_timeout
        self.current_timeout *= self.factor
        return timeout

    def reset(self) -> None:
        self.current_timeout = self.base_timeout


__all__ = [
    "TimeStrategy",
    "ConstantTimeStrategy",
    "LinearTimeStrategy",
    "MultiplicativeTimeStrategy"
]
