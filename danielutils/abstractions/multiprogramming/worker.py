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
        logger.debug(f"Initializing Worker with id={id}")
        self.id = id
        self.pool = pool
        self.thread: Thread = Thread(target=self._loop)
        logger.debug(f"Worker {id} initialized successfully")

    @abstractmethod
    def _work(self, obj: Any) -> None:
        """execution of a single job
        """

    def _loop(self) -> None:
        """main loop of the worker
        """
        logger.debug(f"Worker {self.id} main loop started")
        while True:
            try:
                obj = self.acquire()
                if obj is not None:
                    logger.debug(f"Worker {self.id} acquired job: {type(obj[0]).__name__}")
                    self.work(obj[0])
                else:
                    logger.debug(f"Worker {self.id} received None job, exiting loop")
                    break
            except Exception as e:  # pylint: disable=broad-exception-caught
                logger.error(f"Worker {self.id} thread encountered an error: {type(e).__name__}: {e}")
                break
        logger.debug(f"Worker {self.id} main loop ended")

    def run(self) -> None:
        """will start self._run() as a new thread with the argument given in __init__
        """
        logger.debug(f"Starting worker {self.id} thread")
        self.thread.start()
        logger.debug(f"Worker {self.id} thread started successfully")

    def is_alive(self) -> bool:
        """returns whether the worker is alive or not
        """
        is_alive = self.thread.is_alive()
        logger.debug(f"Worker {self.id} is_alive: {is_alive}")
        return is_alive

    def work(self, obj: Any) -> None:
        """performed the actual work that needs to happen
        execution of a single job
        """
        logger.debug(f"Worker {self.id} starting work on job: {type(obj).__name__}")
        try:
            self._work(obj)
            logger.debug(f"Worker {self.id} completed work on job: {type(obj).__name__}")
        except Exception as e:
            logger.error(f"Worker {self.id} failed to process job {type(obj).__name__}: {type(e).__name__}: {e}")
            raise
        finally:
            self._notify()

    def _notify(self) -> None:
        """utility method to be called on the end of each iteration of work 
        to signal actions if needed
        will call 'notification_function'
        """
        logger.debug(f"Worker {self.id} notifying pool of job completion")
        # TODO
        self.pool._notify_subscribers()  # type:ignore  # pylint: disable=protected-access

    def acquire(self) -> Optional[Tuple[Any]]:
        """acquire a new job object to work on from the pool
        will return a tuple of only one object (the job) or None if there are no more jobs
        Returns:
            Optional[tuple[Any]]: tuple of job object or None
        """
        logger.debug(f"Worker {self.id} attempting to acquire job from pool")
        job = self.pool._acquire()  # pylint: disable=protected-access
        if job is not None:
            logger.debug(f"Worker {self.id} acquired job: {type(job[0]).__name__}")
        else:
            logger.debug(f"Worker {self.id} no jobs available in pool")
        return job


__all__ = [
    "Worker"
]
