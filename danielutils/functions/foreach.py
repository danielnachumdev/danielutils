import logging
from typing import TypeVar, Iterable
from ..custom_types import Consumer
from .logging_.utils import get_logger

logger = get_logger(__name__)

T = TypeVar('T')


def foreach(iterable: Iterable[T], consumer: Consumer[T]) -> None:
    logger.info(f"Applying consumer to iterable")
    for v in iterable:
        consumer(v)
    logger.info("Foreach operation completed")


__all__ = [
    'foreach'
]
