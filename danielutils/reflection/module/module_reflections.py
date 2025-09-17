import logging
from typing import Any
import importlib
from ...logging_.utils import get_logger

logger = get_logger(__name__)


def dynamically_load(module_name: str, obj_name: str) -> Any:
    """dynamically loads the module and returns the object from this file

    Args:
        module_name (str): name of python module, (typically a file name without extension)
        obj_name (str): the name of the wanted object

    Returns:
        Any: the object
    """
    try:
        module = importlib.import_module(module_name)
        obj = getattr(module, obj_name)
        logger.info("Successfully loaded object '%s' from module '%s'", obj_name, module_name)
        return obj
    except ImportError as e:
        logger.error("Failed to import module '%s': %s", module_name, e)
        raise
    except AttributeError as e:
        logger.error("Object '%s' not found in module '%s': %s", obj_name, module_name, e)
        raise


__all__ = [
    "dynamically_load"
]
