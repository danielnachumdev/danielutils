from contextlib import contextmanager
from ..custom_types import Procedure


@contextmanager
def StateContext(set_state: Procedure, restore_state: Procedure):
    try:
        set_state()
        yield
    finally:
        restore_state()


__all__ = [
    'StateContext'
]
