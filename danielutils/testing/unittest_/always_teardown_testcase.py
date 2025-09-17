import functools
import logging
import unittest
from _collections_abc import Coroutine
from typing import Optional, Callable, Type
from unittest import TestResult
from ...logging_.utils import get_logger

logger = get_logger(__name__)


class AlwaysTeardownTestCase(unittest.TestCase):
    """
    SafeTestCase makes sure that tearDown / cleanup methods are always run when
    They should be.
    """

    def run(self, result=None) -> Optional[TestResult]:
        logger.debug(f"Setting up AlwaysTeardownTestCase for test: {self._testMethodName}")
        test_method = getattr(self, self._testMethodName)
        wrapped_test = self._cleanup_wrapper(test_method, KeyboardInterrupt)
        setattr(self, self._testMethodName, wrapped_test)

        self.setUp = self._cleanup_wrapper(self.setUp, BaseException)  # type: ignore

        return super().run(result)

    def _cleanup_wrapper(self, method: Callable, exception: Type[BaseException]) -> Callable:
        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            try:
                return method(*args, **kwargs)
            except exception:
                logger.debug(f"Exception {exception.__name__} caught in test, running cleanup for: {method.__name__}")
                self.tearDown()
                self.doCleanups()
                raise

        return wrapper


class AsyncAlwaysTeardownTestCase(unittest.IsolatedAsyncioTestCase):
    """
    SafeTestCase makes sure that tearDown / cleanup methods are always run when
    They should be.
    """

    def run(self, result=None) -> Optional[TestResult]:
        logger.debug(f"Setting up AsyncAlwaysTeardownTestCase for test: {self._testMethodName}")
        test_method = getattr(self, self._testMethodName)
        wrapped_test = self._cleanup_wrapper(test_method, KeyboardInterrupt)
        setattr(self, self._testMethodName, wrapped_test)

        self.asyncSetUp = self._cleanup_wrapper(self.asyncSetUp, BaseException)  # type: ignore

        return super().run(result)

    def _cleanup_wrapper(self, method: Coroutine, exception: Type[BaseException]) -> Callable:
        @functools.wraps(method)  # type: ignore
        async def wrapper(*args, **kwargs):
            try:
                return await method(*args, **kwargs)  # type: ignore
            except exception:
                logger.debug(f"Exception {exception.__name__} caught in async test, running cleanup for: {method.__name__}")
                self.tearDown()
                self.doCleanups()
                raise

        return wrapper


__all__ = [
    "AlwaysTeardownTestCase",
    "AsyncAlwaysTeardownTestCase",
]
