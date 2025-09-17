import asyncio
import functools
import logging
from datetime import datetime
from typing import Literal, Optional, Any, Mapping, Iterable, Callable, Coroutine

from ..custom_types import Supplier
from ..decorators import normalize_decorator
from .time_strategy import LinearTimeStrategy, ConstantTimeStrategy
from ..versioned_imports import ParamSpec
from .logging_.utils import get_logger

P = ParamSpec("P")
from danielutils.logging_.utils import get_logger
logger = get_logger(__name__)


class AsyncRetryExecutor:
    def __init__(
            self,
            timeout_strategy: Supplier[float] = LinearTimeStrategy(30, 5),
            delay_strategy: Supplier[float] = ConstantTimeStrategy(0)
    ) -> None:
        logger.info(f"Initializing AsyncRetryExecutor with timeout_strategy={type(timeout_strategy).__name__}, delay_strategy={type(delay_strategy).__name__}")
        self.timeout_strategy = timeout_strategy
        self.delay_strategy = delay_strategy
        logger.debug(f"AsyncRetryExecutor initialized successfully")

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
        logger.info(f"Starting async retry execution for {func.__name__} with max_tries={max_tries}")
        
        for i in range(1, max_tries + 1):
            timeout = self.timeout_strategy()
            delay = self.delay_strategy()
            logger.debug(f"Attempt {i}/{max_tries} with timeout={timeout}s, delay={delay}s")
            try:
                result = await asyncio.wait_for(func(*args, **kwargs), timeout=timeout)
                logger.info(f"Async retry execution succeeded on attempt {i}")
                return result
            except Exception as e:
                if self.is_transient(e):
                    logger.warning(f"Failed attempt {i}/{max_tries} with transient exception: {type(e).__name__}: {e}")
                    if i < max_tries - 1 and delay > 0:
                        logger.debug(f"Waiting {delay}s before next attempt")
                        await asyncio.sleep(delay)
                else:
                    logger.error(f"Non-transient exception on attempt {i}: {type(e).__name__}: {e}")
                    raise e
        logger.error(f"Failed all {max_tries} attempts for {func.__name__}")
        raise RuntimeError(f"Failed all attempts")


@normalize_decorator
def with_async_retry(func, *retry_executor_args, max_tries: int = 5, **retry_executor_kwargs):
    retry_executor = AsyncRetryExecutor(*retry_executor_args, **retry_executor_kwargs)

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await retry_executor.execute(func, args=args, kwargs=kwargs, max_tries=max_tries)

    return wrapper


__all__ = [
    "AsyncRetryExecutor",
    "with_async_retry"
]
