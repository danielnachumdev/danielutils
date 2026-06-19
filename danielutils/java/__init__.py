import logging
from ..logging_.utils import get_logger
logger = get_logger(__name__)

from .java_interface import *

try:
    from ..reflection import get_python_version  # type:ignore
except ImportError:
    from reflection import get_python_version

python_version = get_python_version()

if python_version >= (3, 10):
    logger.info("Python version >= 3.10, importing Java interface modules")
    from .interfaces import *
else:
    logger.debug("Skipping optional Java interface modules on Python %s", python_version)
