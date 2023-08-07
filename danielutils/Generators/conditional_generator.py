from typing import Generator, Callable, Any


def generate_except(generator: Generator[Any, None, None],
                    binary_consumer: Callable[[int, Any], bool]) -> Generator[Any, None, None]:
    """will yield from generator except from when the predicate will return False

    Args:
        generator (Generator[Any, None, None]): generator
        binary_consumer (Callable[[int, Any], bool]): predicate. (item_index, item)

    Yields:
        Generator[Any, None, None]: filtered generator
    """
    for i, value in enumerate(generator):
        if not binary_consumer(i, value):
            yield value


def generate_when(generator: Generator[Any, None, None],
                  binary_consumer: Callable[[int, Any], bool]) -> Generator[Any, None, None]:
    """will yield from generator except from when the predicate will return True

    Args:
        generator (Generator[Any, None, None]): generator
        binary_consumer (Callable[[int, Any], bool]): predicate. (item_index, item)

    Yields:
        Generator[Any, None, None]: filtered generator
    """
    for i, value in enumerate(generator):
        if binary_consumer(i, value):
            yield value


__all__ = [
    "generate_when",
    "generate_except"
]
