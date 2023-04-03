import json
from .Decorators import validate_explicit


@validate_explicit(dict)
def dict_to_json(d: dict) -> str:
    return json.dumps(d, indent=4)


@validate_explicit(str)
def json_to_dict(j: str) -> dict:
    return json.loads(j)


__all__ = [
    "dict_to_json",
    "json_to_dict"
]
