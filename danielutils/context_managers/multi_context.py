import logging
from typing import ContextManager
from ..logging_.utils import get_logger

logger = get_logger(__name__)


class MultiContext(ContextManager):
    def __init__(self, *contexts: ContextManager):
        logger.debug("Initializing MultiContext with %s contexts", len(contexts))
        self.contexts = contexts

    def __enter__(self):
        logger.info("Entering MultiContext with %s contexts", len(self.contexts))
        for i, context in enumerate(self.contexts):
            logger.debug("Entering context %s/%s: %s", i+1, len(self.contexts), type(context).__name__)
            context.__enter__()
        logger.debug("All contexts entered successfully")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.debug("Exiting MultiContext with %s contexts, exc_type=%s", len(self.contexts), exc_type)
        for i, context in enumerate(self.contexts):
            logger.debug("Exiting context %s/%s: %s", i+1, len(self.contexts), type(context).__name__)
            context.__exit__(exc_type, exc_val, exc_tb)
        logger.info("All contexts exited")

    def __getitem__(self, index):
        return self.contexts[index]


__all__ = [
    "MultiContext",
]
