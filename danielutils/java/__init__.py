try:
    from reflection import get_python_version
except ImportError:
    from ..reflection import get_python_version  # type:ignore

if get_python_version() >= (3, 10):
    from .interfaces import *
    from .java_interface import *
