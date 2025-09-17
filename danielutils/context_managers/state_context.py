import logging
from contextlib import contextmanager
from ..custom_types import Procedure
from ..logging_.utils import get_logger

logger = get_logger(__name__)


@contextmanager
def StateContext(set_state: Procedure, restore_state: Procedure):
    logger.debug("Entering StateContext")
    try:
        logger.info("Setting state")
        set_state()
        logger.debug("State set successfully, yielding control")
        yield
    finally:
        logger.info("Restoring state")
        restore_state()
        logger.debug("State restored successfully")


__all__ = [
    'StateContext'
]
