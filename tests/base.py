"""
Common base test classes for all tests.
"""
import asyncio
import unittest
import logging
from typing import Any, Union, TypeVar, Awaitable, Coroutine

# WARNING: Do NOT use setup_stdou_logging_handler here!
# We want to catch logs from danielutils initialization, so we need to set up
# logging manually before importing any danielutils modules.

# Set up basic logging to stdout to catch all logs including danielutils initialization
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
    stream=None  # This will use stderr by default, but we want stdout
)

# Override the root logger to use stdout instead of stderr
root_logger = logging.getLogger()
for handler in root_logger.handlers[:]:
    root_logger.removeHandler(handler)

# Add stdout handler
stdout_handler = logging.StreamHandler()
stdout_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')
stdout_handler.setFormatter(formatter)
root_logger.addHandler(stdout_handler)

from danielutils.logging_.utils import get_logger

T = TypeVar('T')


class BaseTest(unittest.TestCase):
    """Base test class with common functionality for all tests."""

    def setUp(self) -> None:
        """Set up test fixtures before each test method."""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        test_class_name = self.__class__.__name__
        test_method_name = getattr(self, '_testMethodName', 'unknown_test')
        logger_name = f"{test_class_name}.{test_method_name}"
        self.logger = get_logger(logger_name)

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
