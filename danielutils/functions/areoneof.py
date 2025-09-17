import logging
from typing import Sequence, Any, Union
from .isoneof import isoneof
from ..reflection import get_python_version
from ..logging_.utils import get_logger

logger = get_logger(__name__)
if get_python_version() < (3, 9):
    from typing import List as List, Tuple as Tuple
else:
    from builtins import list as List, tuple as Tuple  # type:ignore


def areoneof(values: Sequence[Any], types: Union[List[type], Tuple[type]]) -> bool:
    """performs 'isoneof(values[0],types) and ... and isoneof(values[...],types)'

    Args:
        values (Sequence[Any]): Sequence of values
        types (Sequence[Type]): Sequence of types

    Raises:
        TypeError: if types is not a Sequence
        TypeError: if values is not a Sequence

    Returns:
        bool: the result of the check
    """
    logger.debug(f"Checking if {len(values)} values are one of types: {types}")
    if not isinstance(types, Sequence):
        logger.error("'types' parameter is not a Sequence")
        raise TypeError("'types' must be of type Sequence")
    if not isinstance(values, Sequence):
        logger.error("'values' parameter is not a Sequence")
        raise TypeError("'values' must be of type Sequence")
    
    for i, v in enumerate(values):
        if not isoneof(v, types):
            logger.debug(f"Value at index {i} ({v}) is not one of the specified types")
            return False
    
    logger.debug("All values match one of the specified types")
    return True


__all__ = [
    "areoneof"
]
