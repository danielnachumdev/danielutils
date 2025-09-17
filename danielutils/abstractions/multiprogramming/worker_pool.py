from queue import Queue
import logging
from typing import Optional, Any, Type as t_type, Tuple as Tuple, List as List
from threading import Semaphore
from .worker import Worker
from ...reflection import get_python_version
from ..logging_.utils import get_logger

if get_python_version() >= (3, 9):
    from builtins import type as t_type, tuple as Tuple, list as List  # type:ignore
from danielutils.logging_.utils import get_logger
logger = get_logger(__name__)


class WorkerPool:
    """A worker pool class
    """

    def __init__(self, num_workers: int, worker_class: t_type[Worker], w_kwargs: dict, global_variables: dict) -> None:
        logger.info(f"Initializing WorkerPool with {num_workers} workers, worker_class={worker_class.__name__}")
        self.num_workers = num_workers
        self.global_variables: dict = global_variables
        self.q: Queue[Tuple[Any]] = Queue()
        self.worker_class = worker_class
        self.workers: List[Worker] = []
        self.sem = Semaphore(0)
        self.w_kwargs = w_kwargs
        logger.debug(f"WorkerPool initialized: num_workers={num_workers}, global_vars_count={len(global_variables)}, worker_kwargs_count={len(w_kwargs)}")

    def submit(self, job: Any) -> None:
        """submit a job to the pool
        the object can be anything you want as long as you use it 
        correctly in your implemented worker class

        Args:
            job (Any): job object
        """
        logger.debug(f"Submitting job to pool: job_type={type(job).__name__}")
        # we create a tuple to signal that it is indeed a job object and we haven't just got None
        # see Worker._loop
        self.q.put((job,))
        self.sem.release()
        logger.debug(f"Job submitted successfully, queue_size={self.q.qsize()}, semaphore_value={self.sem._value}")

    def _acquire(self) -> Optional[Tuple[Any]]:
        """acquire a new job from the pool

        Returns:
            Optional[tuple[Any]]: optional tuple of job object
        """
        logger.debug("Acquiring job from pool")
        self.sem.acquire()
        if self.q.unfinished_tasks > 0:
            job = self.q.get()
            logger.debug(f"Job acquired successfully, remaining_tasks={self.q.unfinished_tasks}")
            return job
        logger.debug("No jobs available in pool")
        return None

    def start(self) -> None:
        """starts running the pool of workers
        """
        logger.info(f"Starting worker pool with {self.num_workers} workers")
        for i in range(self.num_workers):
            logger.debug(f"Creating worker {i+1}/{self.num_workers}")
            w = self.worker_class(i, self, **self.w_kwargs)
            w.run()
            self.workers.append(w)
            logger.debug(f"Worker {i+1} started successfully")
        logger.info(f"Worker pool started with {len(self.workers)} workers")

    def _notify(self) -> None:
        """a function that the worker calls after finishing processing a job object (Any)
        this function is called automatically from Worker.work()
        """
        logger.debug(f"Worker notification received, unfinished_tasks={self.q.unfinished_tasks}")
        self.q.task_done()
        if self.q.unfinished_tasks <= 0:
            logger.debug("All tasks completed, releasing all workers")
            self.sem.release(self.num_workers)
        logger.debug(f"Notification processed, remaining_tasks={self.q.unfinished_tasks}")

    def join(self) -> None:
        """
        waits for all the workers to finish and will return afterwards
        Returns:
            None
        """
        logger.info(f"Joining worker pool with {len(self.workers)} workers")
        for i, w in enumerate(self.workers):
            logger.debug(f"Joining worker {i+1}/{len(self.workers)}")
            w.thread.join()
            logger.debug(f"Worker {i+1} joined successfully")
        logger.info("All workers joined successfully")


__all__ = [
    "WorkerPool"
]
