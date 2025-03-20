import asyncio
import json
from datetime import datetime
from typing import Callable, Literal, Optional, Coroutine, List, Iterable, Any, Mapping


class AsyncWorkerPool:
    DEFAULT_ORDER_IF_KEY_EXISTS = (
        "pool", "timestamp", "worker_id", "task_id", "task_name", "num_tasks", "tasks", "level", "message", "exception"
    )

    def __init__(self, pool_name: str, num_workers: int = 5) -> None:
        self.num_workers = num_workers
        self.pool_name = pool_name
        self.queue = asyncio.Queue()
        self.workers = []

    async def worker(self, worker_id) -> None:
        """Worker coroutine that continuously fetches and executes tasks from the queue."""
        task_index = 0
        tasks = {}
        while True:
            task = await self.queue.get()
            if task is None:  # Sentinel value to shut down the worker
                break
            func, args, kwargs, name = task
            task_index += 1
            self.info(f"Started", task_name=name, task_id=task_index, worker_id=worker_id)
            try:
                await func(*args, **kwargs)
                tasks["success"] = name
            except Exception as e:
                self.error(f"Failed", exception=e, worker_id=worker_id, task_name=name,
                           task_id=task_index)
                tasks["error"] = name

            self.info(f"Finished", worker_id=worker_id, task_name=name, task_id=task_index, )
            self.queue.task_done()
        self.info(f"Done", worker_id=worker_id, tasks=tasks, num_tasks=task_index)

    async def start(self) -> None:
        """Starts the worker pool."""
        self.workers = [asyncio.create_task(self.worker(i + 1)) for i in range(self.num_workers)]

    async def submit(
            self,
            func: Callable[..., Coroutine[None, None, None]],
            args: Optional[Iterable[Any]] = None,
            kwargs: Optional[Mapping[Any, Any]] = None,
            name: Optional[str] = None
    ) -> None:
        """Submit a new task to the queue."""
        await self.queue.put((func, args or (), kwargs or {}, name))

    async def join(self) -> None:
        """Stops the worker pool by waiting for all tasks to complete and shutting down workers."""
        await self.queue.join()  # Wait until all tasks are processed
        for _ in range(self.num_workers):
            await self.queue.put(None)  # Send sentinel values to stop workers
        await asyncio.gather(*self.workers)  # Wait for workers to finish

    @classmethod
    def log(
            self,
            level: Literal["INFO", "WARNING", "ERROR"],
            message: str,
            order: Optional[List[str]] = DEFAULT_ORDER_IF_KEY_EXISTS,
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

    def info(self, message: str, **kwargs) -> None:
        self.log("INFO", message, pool=self.pool_name, **kwargs)

    def warn(self, message: str, **kwargs) -> None:
        self.log("WARNING", message, pool=self.pool_name, **kwargs)

    def error(self, message: str, **kwargs) -> None:
        self.log("ERROR", message, pool=self.pool_name, **kwargs)


__all__ = [
    "AsyncWorkerPool",
]
