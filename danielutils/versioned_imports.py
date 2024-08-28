try:
    from typing import ParamSpec
except ImportError:
    from .reflection import get_python_version

    if get_python_version() >= (3, 9):
        ParamSpec = lambda name: [...]
    else:
        from typing import Any

        ParamSpec = lambda name: [Any]

try:
    from typing import TypeAlias
except ImportError:
    from typing import Any

    TypeAlias = Any

__all__ = [
    "ParamSpec",
    "TypeAlias"
]
