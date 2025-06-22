import asyncio
import json
from collections import defaultdict
from datetime import datetime
from typing import Callable, Literal, Optional, Coroutine, List, Iterable, Any, Mapping, Tuple



try:
    from tqdm import tqdm
except ImportError:
    from ..mock_ import MockImportObject
    tqdm = MockImportObject("'tqdm' is not installed. Please install 'tqdm' to use AsyncWorkerPool feature.")


class AsyncWorkerPool:
    DEFAULT_ORDER_IF_KEY_EXISTS = (
        "pool", "timestamp", "worker_id", "task_id", "task_name", "num_tasks", "tasks", "level", "message", "exception"
    )

    def __init__(self, pool_name: str, num_workers: int = 5, show_pbar: bool = False) -> None:
        self._num_workers: int = num_workers
        self._pool_name: str = pool_name
        self._show_pbar: bool = show_pbar
        self._pbar: Optional[tqdm] = None
        self._queue: asyncio.Queue[
            Optional[Tuple[Callable, Iterable[Any], Mapping[Any, Any], Optional[str]]]] = asyncio.Queue()
        self._workers: List = []

    async def worker(self, worker_id) -> None:
        """Worker coroutine that continuously fetches and executes tasks from the queue."""
        task_index = 0
        tasks = defaultdict(list)
        while True:
            task = await self._queue.get()
            if task is None:  # Sentinel value to shut down the worker
                break
            func, args, kwargs, name = task
            task_index += 1
            self._info(f"Started", task_id=task_index, task_name=name, worker_id=worker_id)
            try:
                await func(*args, **kwargs)
                tasks["success"].append(name)
                self._info(f"Finished", task_id=task_index, worker_id=worker_id, task_name=name)
            except Exception as e:
                self._error(f"Failed", task_id=task_index, exception=e, worker_id=worker_id,
                            task_name=name)
                tasks["failure"].append(name)

            if self._pbar:
                self._pbar.update(1)
            self._queue.task_done()
        self._info(f"Done", worker_id=worker_id, tasks=tasks, num_tasks=task_index)

    async def start(self) -> None:
        """Starts the worker pool."""
        if self._show_pbar:
            self._pbar = tqdm(total=self._queue.qsize(), desc="#Tasks")
        self._workers = [asyncio.create_task(self.worker(i + 1)) for i in range(self._num_workers)]

    async def submit(
            self,
            func: Callable[..., Coroutine[None, None, None]],
            args: Optional[Iterable[Any]] = None,
            kwargs: Optional[Mapping[Any, Any]] = None,
            name: Optional[str] = None
    ) -> None:
        """Submit a new task to the queue."""
        await self._queue.put((func, args or (), kwargs or {}, name))

    async def join(self) -> None:
        """Stops the worker pool by waiting for all tasks to complete and shutting down workers."""
        await self._queue.join()  # Wait until all tasks are processed
        for _ in range(self._num_workers):
            await self._queue.put(None)  # Send sentinel values to stop workers
        await asyncio.gather(*self._workers)  # Wait for workers to finish

    @classmethod
    def log(
            cls,
            level: Literal["INFO", "WARNING", "ERROR"],
            message: str,
            order: Optional[Iterable[str]] = DEFAULT_ORDER_IF_KEY_EXISTS,
            **kwargs
    ) -> None:
        kwargs["level"] = level
        kwargs["message"] = message
        kwargs["timestamp"] = datetime.now().isoformat()
        ordered_kwargs = kwargs
        if order:
            ordered_kwargs = {key: kwargs[key] for key in order if key in kwargs}
            ordered_kwargs.update(kwargs)
        print(json.dumps(ordered_kwargs, default=str))

    def _info(self, message: str, **kwargs) -> None:
        self.log("INFO", message, pool=self._pool_name, **kwargs)

    def _warn(self, message: str, **kwargs) -> None:
        self.log("WARNING", message, pool=self._pool_name, **kwargs)

    def _error(self, message: str, **kwargs) -> None:
        self.log("ERROR", message, pool=self._pool_name, **kwargs)


__all__ = [
    "AsyncWorkerPool",
]
