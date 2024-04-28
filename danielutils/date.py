import json
from .decorators import validate


@validate  # type:ignore # type:ignore
def dict_to_json(dct: dict) -> str:
    """converts a python dict to a json object

    Args:
        d (dict): the dict to convert

    Returns:
        str: the json as string
    """
    return json.dumps(dct, indent=4)


@validate  # type:ignore
def json_to_dict(json_str: str) -> dict:
    """converts a json object from a string to a python dict

    Args:
        j (str): the json str to convert

    Returns:
        dict: a python dict from the json
    """
    return json.loads(json_str)


__all__ = [
    "dict_to_json",
    "json_to_dict"
]
