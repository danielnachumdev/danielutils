"""
Common base test classes for all tests.
"""
import asyncio
import unittest
import logging
from typing import Any, Union, TypeVar, Awaitable, Coroutine

T = TypeVar('T')


class BaseTest(unittest.TestCase):
    """Base test class with common functionality for all tests."""

    def _setup_test_logger(self) -> None:
        """Set up a unique logger for this test method."""
        test_class_name = self.__class__.__name__
        test_method_name = getattr(self, '_testMethodName', 'unknown_test')
        logger_name = f"{test_class_name}.{test_method_name}"

        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.INFO)

        # Add a handler if none exists
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            # Include filename and line number for better debugging
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def setUp(self) -> None:
        """Set up test fixtures before each test method."""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        # Set up unique logger for this test method
        self._setup_test_logger()

    def tearDown(self) -> None:
        """Clean up after each test method."""
        # Cancel all pending tasks
        pending = asyncio.all_tasks(self.loop)
        for task in pending:
            task.cancel()

        # Run the loop to process cancellations
        if pending:
            self.loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))

        # Close the loop
        self.loop.close()

    def run_async(self, coro: Union[Coroutine[Any, Any, T], Awaitable[T]]) -> T:
        """Run an async coroutine in the test loop and return the result with proper typing."""
        return self.loop.run_until_complete(coro)


__all__ = [
    "BaseTest"
]
