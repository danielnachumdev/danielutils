import functools
import os
import unittest
from typing import Callable, Type

from danielutils import create_directory, get_current_working_directory, set_current_working_directory, delete_directory


def improved_setup(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(self):
        self.cwd = f"./{self.__class__.__name__}_test_folder"
        create_directory(self.cwd)
        self.prev_cwd = get_current_working_directory()
        set_current_working_directory(os.path.join(self.prev_cwd, self.cwd))
        if func is not None:
            func(self)

    return wrapper


def improved_teardown(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(self):
        if func is not None:
            func(self)
        set_current_working_directory(self.prev_cwd)
        delete_directory(self.cwd)

    return wrapper


class AutoCWDTestCase(unittest.TestCase):
    @staticmethod
    def _dummy(*args, **kwargs) -> None:
        pass

    @classmethod
    def __init_subclass__(cls: Type, **kwargs) -> None:
        dct = dict(cls.__dict__)
        impl_setUp = dct.get("setUp", cls._dummy)
        impl_tearDown = dct.get("tearDown", cls._dummy)
        setattr(cls, "setUp", improved_setup(impl_setUp))
        setattr(cls, "tearDown", improved_teardown(impl_tearDown))


__all__ = [
    'AutoCWDTestCase'
]
