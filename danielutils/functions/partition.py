from typing import List, Generator, Tuple, Union


def partitions(n: int, k: int) -> Generator[List[int], None, None]:
    from ..decorators import memo_generator

    @memo_generator
    def helper(n: int, target_sum: int, current_sum: int, topLevel: int, arr: Union[List[int], Tuple[int]]) -> \
            Generator[List[int], None, None]:
        arr = list(arr)
        if n == 1:
            if current_sum <= target_sum:
                if topLevel == 1 or (target_sum - current_sum >= arr[-2]):
                    arr[-1] = target_sum - current_sum
                    yield tuple(arr)
            return

        start = 0
        if n != topLevel:
            start = arr[-1 * n - 1]

        for i in range(start, target_sum + 1):
            arr[-1 * n] = i
            yield from helper(n - 1, target_sum, current_sum + i, topLevel, tuple(arr))

    arr: List[int] = [0] * k
    yield from helper(k, n, 0, k, tuple(arr))


def num_partitions(n: int, k: int) -> int:
    return len(list(partitions(n, k)))


__all__ = [
    "partitions",
    "num_partitions"
]
