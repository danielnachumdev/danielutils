from queue import Queue
import logging
from typing import Optional, Any, Type as t_type, Tuple as Tuple, List as List
from threading import Semaphore
from .worker import Worker
from ...reflection import get_python_version
from ...logging_.utils import get_logger

if get_python_version() >= (3, 9):
    from builtins import type as t_type, tuple as Tuple, list as List  # type:ignore
logger = get_logger(__name__)


class WorkerPool:
    """A worker pool class
    """

    def __init__(self, num_workers: int, worker_class: t_type[Worker], w_kwargs: dict, global_variables: dict) -> None:
        logger.info("Initializing WorkerPool with %s workers, worker_class=%s", num_workers, worker_class.__name__)
        self.num_workers = num_workers
        self.global_variables: dict = global_variables
        self.q: Queue[Tuple[Any]] = Queue()
        self.worker_class = worker_class
        self.workers: List[Worker] = []
        self.sem = Semaphore(0)
        self.w_kwargs = w_kwargs
        logger.debug("WorkerPool initialized: num_workers=%s, global_vars_count=%s, worker_kwargs_count=%s", num_workers, len(global_variables), len(w_kwargs))

    def submit(self, job: Any) -> None:
        """submit a job to the pool
        the object can be anything you want as long as you use it 
        correctly in your implemented worker class

        Args:
            job (Any): job object
        """
        logger.debug("Submitting job to pool: job_type=%s", type(job).__name__)
        # we create a tuple to signal that it is indeed a job object and we haven't just got None
        # see Worker._loop
        self.q.put((job,))
        self.sem.release()
        logger.debug("Job submitted successfully, queue_size=%s, semaphore_value=%s", self.q.qsize(), self.sem._value)

    def _acquire(self) -> Optional[Tuple[Any]]:
        """acquire a new job from the pool

        Returns:
            Optional[tuple[Any]]: optional tuple of job object
        """
        logger.debug("Acquiring job from pool")
        self.sem.acquire()
        if self.q.unfinished_tasks > 0:
            job = self.q.get()
            logger.debug("Job acquired successfully, remaining_tasks=%s", self.q.unfinished_tasks)
            return job
        logger.debug("No jobs available in pool")
        return None

    def start(self) -> None:
        """starts running the pool of workers
        """
        logger.info("Starting worker pool with %s workers", self.num_workers)
        for i in range(self.num_workers):
            logger.debug("Creating worker %s/%s", i+1, self.num_workers)
            w = self.worker_class(i, self, **self.w_kwargs)
            w.run()
            self.workers.append(w)
            logger.debug("Worker %s started successfully", i+1)
        logger.info("Worker pool started with %s workers", len(self.workers))

    def _notify(self) -> None:
        """a function that the worker calls after finishing processing a job object (Any)
        this function is called automatically from Worker.work()
        """
        logger.debug("Worker notification received, unfinished_tasks=%s", self.q.unfinished_tasks)
        self.q.task_done()
        if self.q.unfinished_tasks <= 0:
            logger.debug("All tasks completed, releasing all workers")
            self.sem.release(self.num_workers)
        logger.debug("Notification processed, remaining_tasks=%s", self.q.unfinished_tasks)

    def join(self) -> None:
        """
        waits for all the workers to finish and will return afterwards
        Returns:
            None
        """
        logger.info("Joining worker pool with %s workers", len(self.workers))
        for i, w in enumerate(self.workers):
            logger.debug("Joining worker %s/%s", i+1, len(self.workers))
            w.thread.join()
            logger.debug("Worker %s joined successfully", i+1)
        logger.info("All workers joined successfully")


__all__ = [
    "WorkerPool"
]
