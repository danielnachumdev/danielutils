import asyncio
from asyncio import Task
from typing import List, Coroutine, Any, Tuple, Optional, Set, AsyncIterator, Iterator, TypeVar


async def return_first(coros: List[Coroutine], timeout: Optional[int] = None) -> List[Tuple[int, Any]]:
    tasks: List[Task] = [asyncio.create_task(coro) for coro in coros]
    result: Tuple[Set[Task], Set[Task]] = await asyncio.wait(tasks, timeout=timeout,
                                                             return_when=asyncio.FIRST_COMPLETED)
    done: Set[Task] = result[0]
    # pending: Set[Task] = result[1]

    res = []
    for task in done:
        res.append((tasks.index(task), task.result()))

    return res


async def return_all(coros: List[Coroutine], timeout: Optional[int] = None) -> List[Any]:
    tasks: List[Task] = [asyncio.create_task(coro) for coro in coros]
    result: Tuple[Set[Task], Set[Task]] = await asyncio.wait(tasks, timeout=timeout,
                                                             return_when=asyncio.ALL_COMPLETED)
    done: Set[Task] = result[0]

    return [task.result() for task in done]


async def cast_aiter(itr: Iterator) -> AsyncIterator:
    for x in itr:
        yield x


T = TypeVar("T")


async def async_enumerate(iterable: AsyncIterator[T], start: int = 0) -> AsyncIterator[Tuple[int, T]]:
    index = start
    async for item in iterable:
        yield index, item
        index += 1


__all__ = [
    "return_first",
    "return_all",
    'cast_aiter'
]
