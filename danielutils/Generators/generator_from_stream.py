from typing import IO, Generator, Any, Iterable, Union
from ..Decorators import validate


@validate
def generator_from_stream(stream: Union[IO, Iterable[Any]]) -> Generator[Any, None, None]:
    """will yield values from a given stream

    Args:
        stream (IO): the stream

    Yields:
        Generator[Any, None, None]: the resulting generator
    """
    for v in stream:
        yield v


__all__ = [
    "generator_from_stream"
]
