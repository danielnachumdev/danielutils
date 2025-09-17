import logging
from typing import Generator, Callable, Any
from .logging_.utils import get_logger

logger = get_logger(__name__)


def generate_except(generator: Generator[Any, None, None],
                    binary_consumer: Callable[[int, Any], bool]) -> Generator[Any, None, None]:
    """will yield from generator except from when the predicate will return False

    Args:
        generator (Generator[Any, None, None]): generator
        binary_consumer (Callable[[int, Any], bool]): predicate. (item_index, item)

    Yields:
        Generator[Any, None, None]: filtered generator
    """
    logger.info("Starting generate_except filtering")
    items_processed = 0
    items_yielded = 0
    
    for i, value in enumerate(generator):
        items_processed += 1
        if not binary_consumer(i, value):
            items_yielded += 1
            yield value
    
    logger.info(f"generate_except completed: processed {items_processed} items, yielded {items_yielded} items")


def generate_when(generator: Generator[Any, None, None],
                  binary_consumer: Callable[[int, Any], bool]) -> Generator[Any, None, None]:
    """will yield from generator except from when the predicate will return True

    Args:
        generator (Generator[Any, None, None]): generator
        binary_consumer (Callable[[int, Any], bool]): predicate. (item_index, item)

    Yields:
        Generator[Any, None, None]: filtered generator
    """
    logger.info("Starting generate_when filtering")
    items_processed = 0
    items_yielded = 0
    
    for i, value in enumerate(generator):
        items_processed += 1
        if binary_consumer(i, value):
            items_yielded += 1
            yield value
    
    logger.info(f"generate_when completed: processed {items_processed} items, yielded {items_yielded} items")


__all__ = [
    "generate_when",
    "generate_except"
]
