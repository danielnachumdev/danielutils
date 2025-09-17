import asyncio
import functools
import logging
import os
import unittest
from inspect import iscoroutinefunction
from typing import Callable, Type, Coroutine, Union, Any

from ...random_ import RandomDataGenerator
from ...io_ import create_directory, delete_directory, directory_exists
from ...path import get_current_working_directory, set_current_working_directory
from ...logging_.utils import get_logger

logger = get_logger(__name__)


def dispatch_function(func: Union[Callable, Coroutine], *args, **kwargs) -> Any:
    if asyncio.iscoroutinefunction(func):
        return asyncio.run(func(*args, **kwargs))
    elif asyncio.iscoroutine(func):
        return asyncio.run(func)
    else:
        return func(*args, **kwargs)


def get_available_folder_name(prefix_path: str, random_suffix_length: int = 15) -> str:
    res = f"{prefix_path}_{RandomDataGenerator.name(random_suffix_length)}"
    while directory_exists(res):
        res = f"{prefix_path}_{RandomDataGenerator.name(random_suffix_length)}"
    return res


def improved_setup(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(self):
        self.cwd = get_available_folder_name(f"./{self.__class__.__name__}_test_folder")
        logger.debug("Creating test directory: %s", self.cwd)
        create_directory(self.cwd)
        self.prev_cwd = get_current_working_directory()
        set_current_working_directory(os.path.join(self.prev_cwd, self.cwd))
        logger.debug("Changed working directory to: %s", self.cwd)
        if func is not None:
            func(self)

    @functools.wraps(func)
    async def async_wrapper(self):
        self.cwd = get_available_folder_name(f"./{self.__class__.__name__}_test_folder")
        logger.debug("Creating async test directory: %s", self.cwd)
        create_directory(self.cwd)
        self.prev_cwd = get_current_working_directory()
        set_current_working_directory(os.path.join(self.prev_cwd, self.cwd))
        logger.debug("Changed working directory to: %s", self.cwd)
        if func is not None:
            await func(self)

    return async_wrapper if iscoroutinefunction(func) else wrapper


def improved_teardown(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(self):
        if func is not None:
            func(self)
        logger.debug("Restoring working directory to: %s", self.prev_cwd)
        set_current_working_directory(self.prev_cwd)
        logger.debug("Cleaning up test directory: %s", self.cwd)
        delete_directory(self.cwd)

    @functools.wraps(func)
    async def async_wrapper(self):
        if func is not None:
            await func(self)
        logger.debug("Restoring working directory to: %s", self.prev_cwd)
        set_current_working_directory(self.prev_cwd)
        logger.debug("Cleaning up async test directory: %s", self.cwd)
        delete_directory(self.cwd)

    return async_wrapper if iscoroutinefunction(func) else wrapper


class AutoCWDTestCase(unittest.TestCase):
    @staticmethod
    def _dummy(*args, **kwargs) -> None:
        pass

    @classmethod
    def __init_subclass__(cls: Type, **kwargs) -> None:
        logger.debug("Initializing AutoCWDTestCase subclass: %s", cls.__name__)
        dct = dict(cls.__dict__)
        impl_setUp = dct.get("setUp", cls._dummy)
        impl_tearDown = dct.get("tearDown", cls._dummy)
        setattr(cls, "setUp", improved_setup(impl_setUp))
        setattr(cls, "tearDown", improved_teardown(impl_tearDown))


class AsyncAutoCWDTestCase(unittest.IsolatedAsyncioTestCase):
    @staticmethod
    async def _async_dummy(*args, **kwargs) -> None:
        pass

    @classmethod
    def __init_subclass__(cls: Type, **kwargs) -> None:
        logger.debug("Initializing AsyncAutoCWDTestCase subclass: %s", cls.__name__)
        dct = dict(cls.__dict__)
        async_impl_setUp = dct.get("asyncSetUp", cls._async_dummy)
        async_impl_tearDown = dct.get("asyncTearDown", cls._async_dummy)
        setattr(cls, "asyncSetUp", improved_setup(async_impl_setUp))
        setattr(cls, "asyncTearDown", improved_teardown(async_impl_tearDown))


__all__ = [
    'AutoCWDTestCase',
    "AsyncAutoCWDTestCase"
]
