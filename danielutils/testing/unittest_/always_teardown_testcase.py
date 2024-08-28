import functools
import unittest
from _collections_abc import Coroutine
from typing import Optional, Callable, Type
from unittest import TestResult


class AlwaysTeardownTestCase(unittest.TestCase):
    """
    SafeTestCase makes sure that tearDown / cleanup methods are always run when
    They should be.
    """

    def run(self, result=None) -> Optional[TestResult]:
        test_method = getattr(self, self._testMethodName)
        wrapped_test = self._cleanup_wrapper(test_method, KeyboardInterrupt)
        setattr(self, self._testMethodName, wrapped_test)

        self.setUp = self._cleanup_wrapper(self.setUp, BaseException)

        return super().run(result)

    def _cleanup_wrapper(self, method: Callable, exception: Type[BaseException]) -> Callable:
        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            try:
                return method(*args, **kwargs)
            except exception:
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
        test_method = getattr(self, self._testMethodName)
        wrapped_test = self._cleanup_wrapper(test_method, KeyboardInterrupt)
        setattr(self, self._testMethodName, wrapped_test)

        self.asyncSetUp = self._cleanup_wrapper(self.asyncSetUp, BaseException)

        return super().run(result)

    def _cleanup_wrapper(self, method: Coroutine, exception: Type[BaseException]) -> Callable:
        @functools.wraps(method)
        async def wrapper(*args, **kwargs):
            try:
                return await method(*args, **kwargs)
            except exception:
                self.tearDown()
                self.doCleanups()
                raise

        return wrapper


__all__ = [
    "AlwaysTeardownTestCase",
    "AsyncAlwaysTeardownTestCase",
]
