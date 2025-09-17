from threading import Thread
from abc import ABC, abstractmethod
from typing import Optional, Any, Tuple as Tuple
import logging
import danielutils  # this is explicitly this way to prevent circular import
from ...reflection import get_python_version
from ...logging_.utils import get_logger

if get_python_version() >= (3, 9):
    from builtins import tuple as Tuple  # type:ignore

logger = get_logger(__name__)


class Worker(ABC):
    """A Worker Interface
    """

    def __init__(self, id: int,
                 pool: "danielutils.abstractions.multiprogramming.worker_pool.WorkerPool") -> None:  # pylint: disable=redefined-builtin #noqa
        logger.debug("Initializing Worker with id=%s", id)
        self.id = id
        self.pool = pool
        self.thread: Thread = Thread(target=self._loop)
        logger.debug("Worker %s initialized successfully", id)

    @abstractmethod
    def _work(self, obj: Any) -> None:
        """execution of a single job
        """

    def _loop(self) -> None:
        """main loop of the worker
        """
        logger.debug("Worker %s main loop started", self.id)
        while True:
            try:
                obj = self.acquire()
                if obj is not None:
                    logger.debug("Worker %s acquired job: %s", self.id, type(obj[0]).__name__)
                    self.work(obj[0])
                else:
                    logger.debug("Worker %s received None job, exiting loop", self.id)
                    break
            except Exception as e:  # pylint: disable=broad-exception-caught
                logger.error("Worker %s thread encountered an error: %s: %s", self.id, type(e).__name__, e)
                break
        logger.debug("Worker %s main loop ended", self.id)

    def run(self) -> None:
        """will start self._run() as a new thread with the argument given in __init__
        """
        logger.debug("Starting worker %s thread", self.id)
        self.thread.start()
        logger.debug("Worker %s thread started successfully", self.id)

    def is_alive(self) -> bool:
        """returns whether the worker is alive or not
        """
        is_alive = self.thread.is_alive()
        logger.debug("Worker %s is_alive: %s", self.id, is_alive)
        return is_alive

    def work(self, obj: Any) -> None:
        """performed the actual work that needs to happen
        execution of a single job
        """
        logger.debug("Worker %s starting work on job: %s", self.id, type(obj).__name__)
        try:
            self._work(obj)
            logger.debug("Worker %s completed work on job: %s", self.id, type(obj).__name__)
        except Exception as e:
            logger.error("Worker %s failed to process job %s: %s: %s", self.id, type(obj).__name__, type(e).__name__, e)
            raise
        finally:
            self._notify()

    def _notify(self) -> None:
        """utility method to be called on the end of each iteration of work 
        to signal actions if needed
        will call 'notification_function'
        """
        logger.debug("Worker %s notifying pool of job completion", self.id)
        # TODO
        self.pool._notify_subscribers()  # type:ignore  # pylint: disable=protected-access

    def acquire(self) -> Optional[Tuple[Any]]:
        """acquire a new job object to work on from the pool
        will return a tuple of only one object (the job) or None if there are no more jobs
        Returns:
            Optional[tuple[Any]]: tuple of job object or None
        """
        logger.debug("Worker %s attempting to acquire job from pool", self.id)
        job = self.pool._acquire()  # pylint: disable=protected-access
        if job is not None:
            logger.debug("Worker %s acquired job: %s", self.id, type(job[0]).__name__)
        else:
            logger.debug("Worker %s no jobs available in pool", self.id)
        return job


__all__ = [
    "Worker"
]
