import asyncio
import json
import logging
from collections import defaultdict
from typing import Callable, Optional, Coroutine, List, Iterable, Any, Mapping, Tuple

try:
    from tqdm import tqdm
except ImportError:
    from ..mock_ import MockImportObject

    tqdm = MockImportObject("'tqdm' is not installed. Please install 'tqdm' to use AsyncWorkerPool feature.")

logger: logging.Logger = logging.getLogger(__name__)

class AsyncWorkerPool:
    DEFAULT_ORDER_IF_KEY_EXISTS = (
        "pool", "timestamp", "worker_id", "task_id", "task_name", "num_tasks", "tasks", "level", "message", "exception"
    )

    def __init__(self, pool_name: str, num_workers: int = 5, show_pbar: bool = False) -> None:
        logger.info(f"Initializing AsyncWorkerPool '{pool_name}' with {num_workers} workers, show_pbar={show_pbar}")
        self._num_workers: int = num_workers
        self._pool_name: str = pool_name
        self._show_pbar: bool = show_pbar
        self._pbar: Optional[tqdm] = None
        self._queue: asyncio.Queue[
            Optional[Tuple[Callable, Iterable[Any], Mapping[Any, Any], Optional[str]]]] = asyncio.Queue()
        self._workers: List = []
        logger.debug(f"AsyncWorkerPool '{pool_name}' initialized successfully")

    async def worker(self, worker_id) -> None:
        """Worker coroutine that continuously fetches and executes tasks from the queue."""
        logger.debug(f"Worker {worker_id} starting")
        task_index = 0
        tasks = defaultdict(list)
        while True:
            task = await self._queue.get()
            if task is None:  # Sentinel value to shut down the worker
                logger.debug(f"Worker {worker_id} received shutdown signal")
                break
            func, args, kwargs, name = task
            task_index += 1
            logger.info(f"Task {task_index} '{name}' started on worker {worker_id}")
            try:
                await func(*args, **kwargs)
                tasks["success"].append(name)
                logger.info(f"Task {task_index} '{name}' finished on worker {worker_id}")
            except Exception as e:
                logger.error(f"Task {task_index} '{name}' failed on worker {worker_id}: {type(e).__name__}: {e}")
                tasks["failure"].append(name)

            if self._pbar:
                self._pbar.update(1)
            self._queue.task_done()
        logger.info(f"Worker {worker_id} completed {task_index} tasks (success: {len(tasks['success'])}, failure: {len(tasks['failure'])})")

    async def start(self) -> None:
        """Starts the worker pool."""
        logger.info(f"Starting worker pool '{self._pool_name}' with {self._num_workers} workers")
        if self._show_pbar:
            self._pbar = tqdm(total=self._queue.qsize(), desc="#Tasks")
        self._workers = [asyncio.create_task(self.worker(i + 1)) for i in range(self._num_workers)]
        logger.info(f"Worker pool '{self._pool_name}' started successfully")

    async def submit(
            self,
            func: Callable[..., Coroutine[None, None, None]],
            args: Optional[Iterable[Any]] = None,
            kwargs: Optional[Mapping[Any, Any]] = None,
            name: Optional[str] = None
    ) -> None:
        """Submit a new task to the queue."""
        logger.debug(f"Adding new job '{name}' to queue")
        await self._queue.put((func, args or (), kwargs or {}, name))

    async def join(self) -> None:
        """Stops the worker pool by waiting for all tasks to complete and shutting down workers."""
        logger.info(f"Starting join process for worker pool '{self._pool_name}'")
        await self._queue.join()  # Wait until all tasks are processed
        for _ in range(self._num_workers):
            await self._queue.put(None)  # Send sentinel values to stop workers
        await asyncio.gather(*self._workers)  # Wait for workers to finish
        logger.info(f"Join process completed for worker pool '{self._pool_name}'")


__all__ = [
    "AsyncWorkerPool",
]
