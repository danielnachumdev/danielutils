import functools
import unittest
from typing import Optional, Callable
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

    def _cleanup_wrapper(self, method: Callable, exception) -> Callable:
        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            try:
                return method(*args, **kwargs)
            except exception:
                self.tearDown()
                self.doCleanups()
                raise

        return wrapper


__all__ = [

]
