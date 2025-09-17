from typing import Tuple

try:
    from typing import ParamSpec
except ImportError:
    from .reflection import get_python_version

    if get_python_version() >= (3, 9):
        ParamSpec = lambda name: [Any]  # type: ignore
    else:
        from typing import Any

        ParamSpec = lambda name: [Any]  # type: ignore

try:
    from typing import TypeAlias
except ImportError:
    from typing import Any

    TypeAlias = Any  # type: ignore

__all__ = [
    "ParamSpec",
    "TypeAlias"
]
