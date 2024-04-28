from .reflection import get_python_version

version = get_python_version()
if version < (3, 10):
    from typing_extensions import ParamSpec, Concatenate, TypeAlias
else:
    from typing import ParamSpec, Concatenate, TypeAlias  # type:ignore
__all__ = [
    "ParamSpec",
    "Concatenate",
    "TypeAlias",
]
