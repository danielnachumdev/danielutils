import logging
from typing import IO, Generator, Any, Iterable, Union
from ..decorators import validate
from ..logging_.utils import get_logger

logger = get_logger(__name__)


@validate  # type:ignore
def generator_from_stream(stream: Union[IO, Iterable[Any]]) -> Generator[Any, None, None]:
    """will yield values from a given stream

    Args:
        stream (IO): the stream

    Yields:
        Generator[Any, None, None]: the resulting generator
    """
    logger.info("Starting generator_from_stream with stream type: %s", type(stream).__name__)
    items_yielded = 0
    
    for v in stream:
        items_yielded += 1
        yield v
    
    logger.info("generator_from_stream completed, yielded %s items", items_yielded)


__all__ = [
    "generator_from_stream"
]
