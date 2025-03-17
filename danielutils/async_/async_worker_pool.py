import asyncio
import json
from typing import Callable, Literal, Optional, Coroutine



class AsyncWorkerPool:
    def __init__(self, num_workers: int) -> None:
        self.num_workers = num_workers
        self.queue = asyncio.Queue()
        self.workers = []

    async def worker(self, worker_id) -> None:
        """Worker coroutine that continuously fetches and executes tasks from the queue."""
        task_count = 0
        while True:
            task = await self.queue.get()
            if task is None:  # Sentinel value to shut down the worker
                break
            task_count += 1
            func, args, kwargs = task
            self.info(f"Worker {worker_id} started with task {task_count}")

            try:
                await func(*args, **kwargs)
            except Exception as e:
                self.error(f"Worker {worker_id} failed task {task_count}", exception = e)

            self.info(f"Worker {worker_id} finished with task {task_count}")
            self.queue.task_done()
        self.info(f"Worker {worker_id} done.")

    async def start(self) -> None:
        """Starts the worker pool."""
        self.workers = [asyncio.create_task(self.worker(i + 1)) for i in range(self.num_workers)]

    async def submit(self, func: Callable[..., Coroutine[None, None, None]], *args, **kwargs) -> None:
        """Submit a new task to the queue."""
        await self.queue.put((func, args, kwargs))

    async def join(self) -> None:
        """Stops the worker pool by waiting for all tasks to complete and shutting down workers."""
        await self.queue.join()  # Wait until all tasks are processed
        for _ in range(self.num_workers):
            await self.queue.put(None)  # Send sentinel values to stop workers
        await asyncio.gather(*self.workers)  # Wait for workers to finish

    def log(self, level: Literal["INFO", "WARNING", "ERROR"], message: str, **kwargs) -> None:
        kwargs["level"] = level
        kwargs["message"] = message
        print(json.dumps(kwargs, default=str))

    def info(self, message: str, **kwargs) -> None:
        self.log("INFO", message, **kwargs)

    def warn(self, message: str, **kwargs) -> None:
        self.log("WARNING", message, **kwargs)

    def error(self, message: str, **kwargs) -> None:
        self.log("ERROR", message, **kwargs)


__all__ = [
    "AsyncWorkerPool",
]
