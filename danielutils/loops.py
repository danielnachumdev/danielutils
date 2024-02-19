from typing import Iterable, Generator


def flatten(iterable: Iterable) -> list:
    """
    Flattens a given iterable into a list.

    This function takes as input an iterable that may contain nested iterables (like lists or tuples),
    and returns a flat list where all elements of the input are expanded.
    Non-iterable elements in the input iterable are appended as they are.

    Args:
        iterable (Iterable): The iterable to flatten. Can contain nested iterables.

    Returns:
        list: A flat list containing all elements of the input iterable.
    """
    result = []
    for i in iterable:
        if isinstance(i, Iterable):
            result.extend(flatten(i))
        else:
            result.append(i)
    return result


def _combine2(iter1: Iterable, iter2: Iterable) -> Generator:
    for v1 in iter1:
        for v2 in iter2:
            yield v1, v2


def multiloop(*iterables: Iterable, pre_load: bool = False) -> Generator:
    """
    Generates all combinations of values from multiple iterables.

    This function takes as input any number of iterables and generates all possible combinations of their values.
    It also has an option to pre-load the iterables into memory before generating combinations.

    Args:
        *iterables (list[Iterable]): The iterables to generate combinations from.
        pre_load (bool, optional): If True, pre-loads the iterables into memory. Defaults to False.

    Yields:
        Generator: A generator that yields tuples, each containing one combination of values from the iterables.
    """
    if len(iterables) == 1:
        yield from iterables[0]
        return

    arr: list[Iterable] = list(iterables)
    if pre_load:
        arr = [list(itr) for itr in iterables]

    cur = _combine2(*arr[:2])
    for itr in arr[2:]:
        cur = _combine2(cur, itr)
    for v in cur:
        yield tuple(flatten(v))


__all__ = [
    "flatten",
    "multiloop"
]
