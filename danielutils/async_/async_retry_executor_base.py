import asyncio
import functools
import json
from datetime import datetime
from typing import Literal, Optional, Any, Mapping, Iterable, Callable, Coroutine

from ..custom_types import Supplier
from ..decorators import normalize_decorator
from .time_strategy import LinearTimeStrategy, ConstantTimeStrategy
from ..versioned_imports import ParamSpec

P = ParamSpec("P")


class AsyncRetryExecutorBase:
    def __init__(
            self,
            timeout_strategy: Supplier[float] = LinearTimeStrategy(30, 5),
            delay_strategy: Supplier[float] = ConstantTimeStrategy(0)
    ) -> None:
        self.timeout_strategy = timeout_strategy
        self.delay_strategy = delay_strategy

    def is_transient(self, e: Exception) -> bool:
        """
        This function will return true if the exception that was raised at a specific attempt should be ignored and we should try again with respet to the amount of retries left
        Args:
            e: exception caught

        Returns:
            boolean
        """
        return False

    async def execute(
            self,
            func: Callable[P, Coroutine],
            *,
            args: Optional[Iterable] = None,
            kwargs: Optional[Mapping] = None,
            max_tries: int = 5
    ) -> Optional[Any]:
        args = list(args) if args else []
        kwargs = dict(kwargs) if kwargs else {}
        for i in range(1, max_tries + 1):
            timeout = self.timeout_strategy()
            delay = self.delay_strategy()
            try:
                return await asyncio.wait_for(func(*args, **kwargs), timeout=timeout)
            except Exception as e:
                if self.is_transient(e):
                    self.warn(f"Failed attempt {i}/{max_tries}", function=func, args=args, kwargs=kwargs, exception=e,
                              timestamp=datetime.now().isoformat())
                    if i < max_tries - 1 and delay > 0:
                        await asyncio.sleep(delay)
                else:
                    raise e
        self.error("Failed all attempts", function=func, args=args, kwargs=kwargs, timestamp=datetime.now().isoformat())
        raise RuntimeError(f"Failed all attempts")

    def log(self, level: Literal["INFO", "WARNING", "ERROR"], message: str, **kwargs) -> None:
        kwargs["level"] = level
        kwargs["message"] = message
        print(json.dumps(kwargs, default=str))

    def info(self, message: str, **kwargs) -> None:
        self.log("INFO", message, **kwargs)

    def warn(self, message: str, **kwargs) -> None:
        self.log("WARNING", message, **kwargs)

    def error(self, message: str, **kwargs) -> None:
        self.log("ERROR", message, **kwargs)


@normalize_decorator
def with_async_retry(func, *retry_executor_args, max_tries: int = 5, **retry_executor_kwargs):
    retry_executor = AsyncRetryExecutorBase(*retry_executor_args, **retry_executor_kwargs)

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await retry_executor.execute(func, args=args, kwargs=kwargs, max_tries=max_tries)

    return wrapper


__all__ = [
    "AsyncRetryExecutorBase",
    "with_async_retry"
]
