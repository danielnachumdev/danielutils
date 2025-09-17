import logging
from ..logging_.utils import get_logger
logger = get_logger(__name__)

try:
    from ..reflection import get_python_version  # type:ignore
except ImportError:
    from reflection import get_python_version

python_version = get_python_version()

if python_version >= (3, 10):
    logger.info("Python version >= 3.10, importing Java interface modules")
    from .interfaces import *
    from .java_interface import *
else:
    logger.warning(f"Java interface module requires Python 3.10+, current version: {python_version}")
