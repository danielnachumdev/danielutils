import logging
from typing import Any
import importlib
from ..logging_.utils import get_logger

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
        logger.info(f"Successfully loaded object '{obj_name}' from module '{module_name}'")
        return obj
    except ImportError as e:
        logger.error(f"Failed to import module '{module_name}': {e}")
        raise
    except AttributeError as e:
        logger.error(f"Object '{obj_name}' not found in module '{module_name}': {e}")
        raise


__all__ = [
    "dynamically_load"
]
