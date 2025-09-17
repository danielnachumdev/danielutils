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

from ..logging_.utils import get_logger

class AsyncWorkerPool:
    DEFAULT_ORDER_IF_KEY_EXISTS = (
        "pool", "timestamp", "worker_id", "task_id", "task_name", "num_tasks", "tasks", "level", "message", "exception"
    )
    
    # Default logger instance
    _logger = get_logger(__name__)
    
    @staticmethod
    def log(level: int, message: str, *args, **kwargs) -> None:
        """
        Static logging method that delegates to the default logger.
        End users can override this method to customize logging behavior.
        
        Args:
            level: Log level (DEBUG=10, INFO=20, WARNING=30, ERROR=40, CRITICAL=50)
            message: Log message
            *args: Additional arguments for message formatting
            **kwargs: Additional keyword arguments for logging
        """
        AsyncWorkerPool._logger.log(level, message, *args, **kwargs)

    def __init__(self, pool_name: str, num_workers: int = 5, show_pbar: bool = False) -> None:
        self.log(logging.INFO, "Initializing AsyncWorkerPool '%s' with %d workers, show_pbar=%s", pool_name, num_workers, show_pbar)
        self._num_workers: int = num_workers
        self._pool_name: str = pool_name
        self._show_pbar: bool = show_pbar
        self._pbar: Optional[tqdm] = None
        self._queue: asyncio.Queue[
            Optional[Tuple[Callable, Iterable[Any], Mapping[Any, Any], Optional[str]]]] = asyncio.Queue()
        self._workers: List = []
        self.log(logging.DEBUG, "AsyncWorkerPool '%s' initialized successfully", pool_name)

    async def worker(self, worker_id) -> None:
        """Worker coroutine that continuously fetches and executes tasks from the queue."""
        self.log(logging.DEBUG, "Worker %d starting", worker_id)
        task_index = 0
        tasks = defaultdict(list)
        while True:
            task = await self._queue.get()
            if task is None:  # Sentinel value to shut down the worker
                self.log(logging.DEBUG, "Worker %d received shutdown signal", worker_id)
                break
            func, args, kwargs, name = task
            task_index += 1
            self.log(logging.INFO, "Task %d '%s' started on worker %d", task_index, name, worker_id)
            try:
                await func(*args, **kwargs)
                tasks["success"].append(name)
                self.log(logging.INFO, "Task %d '%s' finished on worker %d", task_index, name, worker_id)
            except Exception as e:
                self.log(logging.ERROR, "Task %d '%s' failed on worker %d: %s: %s", task_index, name, worker_id, type(e).__name__, e)
                tasks["failure"].append(name)

            if self._pbar:
                self._pbar.update(1)
            self._queue.task_done()
        self.log(logging.INFO, "Worker %d completed %d tasks (success: %d, failure: %d)", worker_id, task_index, len(tasks['success']), len(tasks['failure']))

    async def start(self) -> None:
        """Starts the worker pool."""
        self.log(logging.INFO, "Starting worker pool '%s' with %d workers", self._pool_name, self._num_workers)
        if self._show_pbar:
            self._pbar = tqdm(total=self._queue.qsize(), desc="#Tasks")
        self._workers = [asyncio.create_task(self.worker(i + 1)) for i in range(self._num_workers)]
        self.log(logging.INFO, "Worker pool '%s' started successfully", self._pool_name)

    async def submit(
            self,
            func: Callable[..., Coroutine[None, None, None]],
            args: Optional[Iterable[Any]] = None,
            kwargs: Optional[Mapping[Any, Any]] = None,
            name: Optional[str] = None
    ) -> None:
        """Submit a new task to the queue."""
        self.log(logging.DEBUG, "Adding new job '%s' to queue", name)
        await self._queue.put((func, args or (), kwargs or {}, name))

    async def join(self) -> None:
        """Stops the worker pool by waiting for all tasks to complete and shutting down workers."""
        self.log(logging.INFO, "Starting join process for worker pool '%s'", self._pool_name)
        await self._queue.join()  # Wait until all tasks are processed
        for _ in range(self._num_workers):
            await self._queue.put(None)  # Send sentinel values to stop workers
        await asyncio.gather(*self._workers)  # Wait for workers to finish
        self.log(logging.INFO, "Join process completed for worker pool '%s'", self._pool_name)


__all__ = [
    "AsyncWorkerPool",
]
