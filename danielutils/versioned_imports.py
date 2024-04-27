from .reflection import get_python_version

version = get_python_version()
if version < (3, 9):
    from typing import Tuple as t_tuple, List as t_list, Dict as t_dict, Set as t_set
else:
    # pylint: disable=ungrouped-imports
    from builtins import tuple as t_tuple, list as t_list, dict as t_dict, set as t_set  # type:ignore

if version < (3, 10):
    from typing_extensions import ParamSpec, Concatenate
else:
    from typing import ParamSpec, Concatenate  # type:ignore
__all__ = [
    "ParamSpec",
    "Concatenate",
    "t_set",
    "t_dict",
    "t_list",
    "t_tuple",
]
