import json
import logging
from .decorators import validate
from .logging_.utils import get_logger
logger = get_logger(__name__)


@validate  # type:ignore # type:ignore
def dict_to_json(dct: dict) -> str:
    """converts a python dict to a json object

    Args:
        d (dict): the dict to convert

    Returns:
        str: the json as string
    """
    logger.debug("Converting dict with %d keys to JSON", len(dct))
    result = json.dumps(dct, indent=4)
    logger.debug("JSON conversion completed, result length: %d", len(result))
    return result


@validate  # type:ignore
def json_to_dict(json_str: str) -> dict:
    """converts a json object from a string to a python dict

    Args:
        j (str): the json str to convert

    Returns:
        dict: a python dict from the json
    """
    logger.debug("Converting JSON string (length: %d) to dict", len(json_str))
    result = json.loads(json_str)
    logger.debug("JSON parsing completed, dict has %d keys", len(result))
    return result


__all__ = [
    "dict_to_json",
    "json_to_dict"
]
