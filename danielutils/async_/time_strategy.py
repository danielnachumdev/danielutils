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
        logger.debug(f"Initializing ConstantTimeStrategy with timeout={timeout}")
        self.timeout = timeout

    def next(self) -> float:
        logger.debug(f"ConstantTimeStrategy returning timeout={self.timeout}")
        return self.timeout

    def reset(self) -> None:
        logger.debug("ConstantTimeStrategy reset called (no-op)")
        pass  # No state to reset


class LinearTimeStrategy(TimeStrategy):
    def __init__(self, base_timeout: float, step: float):
        logger.debug(f"Initializing LinearTimeStrategy with base_timeout={base_timeout}, step={step}")
        self.base_timeout = base_timeout
        self.step = step
        self.current_timeout = base_timeout

    def next(self) -> float:
        timeout = self.current_timeout
        self.current_timeout += self.step
        logger.debug(f"LinearTimeStrategy returning timeout={timeout}, next will be {self.current_timeout}")
        return timeout

    def reset(self) -> None:
        logger.debug(f"LinearTimeStrategy resetting to base_timeout={self.base_timeout}")
        self.current_timeout = self.base_timeout


class MultiplicativeTimeStrategy(TimeStrategy):
    def __init__(self, base_timeout: float, factor: float):
        logger.debug(f"Initializing MultiplicativeTimeStrategy with base_timeout={base_timeout}, factor={factor}")
        self.base_timeout = base_timeout
        self.factor = factor
        self.current_timeout = base_timeout

    def next(self) -> float:
        timeout = self.current_timeout
        self.current_timeout *= self.factor
        logger.debug(f"MultiplicativeTimeStrategy returning timeout={timeout}, next will be {self.current_timeout}")
        return timeout

    def reset(self) -> None:
        logger.debug(f"MultiplicativeTimeStrategy resetting to base_timeout={self.base_timeout}")
        self.current_timeout = self.base_timeout


__all__ = [
    "TimeStrategy",
    "ConstantTimeStrategy",
    "LinearTimeStrategy",
    "MultiplicativeTimeStrategy"
]
