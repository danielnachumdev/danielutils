from dataclasses import dataclass
from typing import Optional


@dataclass
class ArgumentInfo:
    name: Optional[str]
    type: Optional[str]
    value: Optional[str]


__all__ = [
    "ArgumentInfo",
]
