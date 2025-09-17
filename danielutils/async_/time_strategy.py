from abc import ABC, abstractmethod
import logging
from ..logging_.utils import get_logger
logger = get_logger(__name__)


class TimeStrategy(ABC):
    @abstractmethod
    def next(self): ...

    def __call__(self, *args, **kwargs):
        return self.next()

    @abstractmethod
    def reset(self): ...


class ConstantTimeStrategy(TimeStrategy):
    def __init__(self, timeout: float):
        logger.debug("Initializing ConstantTimeStrategy with timeout=%s", timeout)
        self.timeout = timeout

    def next(self) -> float:
        logger.debug("ConstantTimeStrategy returning timeout=%s", self.timeout)
        return self.timeout

    def reset(self) -> None:
        logger.debug("ConstantTimeStrategy reset called (no-op)")
        pass  # No state to reset


class LinearTimeStrategy(TimeStrategy):
    def __init__(self, base_timeout: float, step: float):
        logger.debug("Initializing LinearTimeStrategy with base_timeout=%s, step=%s", base_timeout, step)
        self.base_timeout = base_timeout
        self.step = step
        self.current_timeout = base_timeout

    def next(self) -> float:
        timeout = self.current_timeout
        self.current_timeout += self.step
        logger.debug("LinearTimeStrategy returning timeout=%s, next will be %s", timeout, self.current_timeout)
        return timeout

    def reset(self) -> None:
        logger.debug("LinearTimeStrategy resetting to base_timeout=%s", self.base_timeout)
        self.current_timeout = self.base_timeout


class MultiplicativeTimeStrategy(TimeStrategy):
    def __init__(self, base_timeout: float, factor: float):
        logger.debug("Initializing MultiplicativeTimeStrategy with base_timeout=%s, factor=%s", base_timeout, factor)
        self.base_timeout = base_timeout
        self.factor = factor
        self.current_timeout = base_timeout

    def next(self) -> float:
        timeout = self.current_timeout
        self.current_timeout *= self.factor
        logger.debug("MultiplicativeTimeStrategy returning timeout=%s, next will be %s", timeout, self.current_timeout)
        return timeout

    def reset(self) -> None:
        logger.debug("MultiplicativeTimeStrategy resetting to base_timeout=%s", self.base_timeout)
        self.current_timeout = self.base_timeout


__all__ = [
    "TimeStrategy",
    "ConstantTimeStrategy",
    "LinearTimeStrategy",
    "MultiplicativeTimeStrategy"
]
