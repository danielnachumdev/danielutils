import logging
from typing import ContextManager
from ..logging_.utils import get_logger

logger = get_logger(__name__)


class MultiContext(ContextManager):
    def __init__(self, *contexts: ContextManager):
        logger.debug(f"Initializing MultiContext with {len(contexts)} contexts")
        self.contexts = contexts

    def __enter__(self):
        logger.info(f"Entering MultiContext with {len(self.contexts)} contexts")
        for i, context in enumerate(self.contexts):
            logger.debug(f"Entering context {i+1}/{len(self.contexts)}: {type(context).__name__}")
            context.__enter__()
        logger.debug("All contexts entered successfully")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.debug(f"Exiting MultiContext with {len(self.contexts)} contexts, exc_type={exc_type}")
        for i, context in enumerate(self.contexts):
            logger.debug(f"Exiting context {i+1}/{len(self.contexts)}: {type(context).__name__}")
            context.__exit__(exc_type, exc_val, exc_tb)
        logger.info("All contexts exited")

    def __getitem__(self, index):
        return self.contexts[index]


__all__ = [
    "MultiContext",
]
