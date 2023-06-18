from typing import Generator, Callable, Any


def generate_except(generator: Generator[Any, None, None], binary_consumer: Callable[[int, Any], bool]) -> Generator[Any, None, None]:
    for i, value in enumerate(generator):
        if not binary_consumer(i, value):
            yield value


def generate_when(generator: Generator[Any, None, None], binary_consumer: Callable[[int, Any], bool]) -> Generator[Any, None, None]:
    for i, value in enumerate(generator):
        if binary_consumer(i, value):
            yield value


__all__ = [
    "generate_when",
    "generate_except"
]
