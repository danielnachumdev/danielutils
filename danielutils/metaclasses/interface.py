import inspect
import logging
import re
import traceback
import functools
from typing import Callable, Iterable, Any, Generator, Optional, Union, \
    List as List, Set as Set, Type as t_type, Dict as Dict
from ..logging_.utils import get_logger
from ..reflection import get_python_version
if get_python_version() >= (3, 9):
    from builtins import list as List, set as Set, type as t_type, dict as Dict  # type:ignore
# from ..decorators.decorate_conditionally import decorate_conditionally

logger = get_logger(__name__)


class InterfaceHelper:
    """a helper class for Interface metaclass
    """
    ORIGINAL_INIT = "__original_init__"

    @staticmethod
    def flatten_iterables(iterable: Iterable) -> list:
        """will flatten and iterable recursively

        Args:
            iterable (Iterable): iterable to flatten

        Returns:
            list: the flattened result
        """
        res = []
        for obj in iterable:
            if isinstance(obj, Iterable) and not isinstance(obj, str):
                res.extend(InterfaceHelper.flatten_iterables(obj))
            else:
                res.append(obj)
        return res

    @staticmethod
    def is_func_implemented(func: Callable) -> bool:
        """will check if a function is implemented

        Args:
            func (Callable): the function to check

        Returns:
            bool: will return true iff the function is not implemented according to Interface.IMPLICIT_ABSTRACT
                or not decorated with Interface.abstractmethod 
                or not an overridden instance of a default implementation of an Interface's function
        """
        if hasattr(func, Interface.FUNC_KEY):
            return not func.__dict__[Interface.FUNC_KEY]

        src = inspect.getsource(func)
        if re.match(Interface.IMPLICIT_ABSTRACT, src):
            return False

        is_default_override = (
            func.__qualname__.startswith(InterfaceHelper.__name__))
        return not is_default_override

    @staticmethod
    def unimplemented_functions(cls) -> Generator[str, None, None]:
        """will yield all function that are unimplemented in a class according to InterfaceHelper.is_func_implemented

        Yields:
            Generator[str, None, None]: yields str which are function names
        """
        for func_name in InterfaceHelper.get_declared_function_names(cls):
            func = cls.__dict__[func_name]
            if not InterfaceHelper.is_func_implemented(func):
                yield func_name

    @staticmethod
    def implemented_functions(cls) -> Generator[str, None, None]:
        """will yield all function that are implemented in a class according to InterfaceHelper.is_func_implemented

        Yields:
            Generator[str, None, None]: yields str which are function names
        """
        for func_name in InterfaceHelper.get_declared_function_names(cls):
            func = cls.__dict__[func_name]
            if InterfaceHelper.is_func_implemented(func):
                yield func_name

    @staticmethod
    def get_declared_function_names(cls) -> Generator[str, None, None]:
        """will yield the names of all the functions declared inside a class

        Yields:
            Generator[str, None, None]: yields str values which are names of declared functions
        """
        # In python 3.8 this function always return the first occurrence so some tests fail
        src = inspect.getsource(cls).splitlines()
        for line in src:
            if re.match(r".*def \w+\(.*\).*:", line):
                func_name = re.findall(r".*def (\w+)\(.*", line)[0]
                yield func_name

    @staticmethod
    def create_init_handler(cls_name, missing: Optional[Union[List[str],
                            Set[str]]] = None, original: Optional[Callable] = None):
        """this function will create the default interface __init__ function with the wanted behavior"""
        # @decorate_conditionally(functools.wraps, original
        # is not None, [original])  # TODO implement this decorator
        def __interface_init__(*args, **kwargs):
            instance = args[0]
            caller_frame = traceback.format_stack()[-2]
            is_super_call = bool(re.match(
                fr"\s+File \".*\", line \d+, in __init__\n\s+(?:super\(\)|{cls_name})\.__init__\(.*\)\n", caller_frame))
            
            if is_super_call:
                mro = instance.__class__.mro()
                i = 0
                for i, cls in enumerate(mro):
                    if cls.__name__ == cls_name:
                        break
                mro = mro[i:]
                for cls in mro:
                    if hasattr(cls, InterfaceHelper.ORIGINAL_INIT):
                        result = getattr(cls, InterfaceHelper.ORIGINAL_INIT)(
                            *args, **kwargs)
                        return result
                logger.error("No original init found in MRO for %s", cls_name)
                raise NotImplementedError(
                    f"Can't use super().__init__(...) in {cls_name}.__init__(...) "
                    "if the __init__ function is not defined a parent interface")

            if missing:
                logger.warning("Interface %s missing implementations: %s", cls_name, missing)
                raise NotImplementedError(f"Can't instantiate '{cls_name}' because it is an interface."
                                          f" It is missing implementations for {missing}")
            logger.warning("Attempting to instantiate interface %s", cls_name)
            raise NotImplementedError(
                f"'{cls_name}' is an interface, Can't create instances")
        return __interface_init__

    @staticmethod
    def create_generic_handler(cls: str, original: Callable):
        """this function will create the generic function handler

        Args:
            func_name (_type_): the name of the interface
        """
        @functools.wraps(original)
        def __interface_handler__(*args, **kwargs):
            logger.warning("Generic handler called for unimplemented method in interface %s", cls)
            raise NotImplementedError(
                f"Interface {cls} must be implemented")
        return __interface_handler__


class Interface(type):
    """This is a metaclass that will enable better_builtins that inherit it directly (or indirectly)
        to behave like interfaces in OOP languages like java
    """
    IMPLICIT_ABSTRACT = r"\s*def \w+\(.*?\)(?:\s*->\s*\w+)?:\n(?:\s*\"{3}.*\"{3}\n)?\s*\.{3}\n"
    KEY = "__is_interface__"
    FUNC_KEY = "__is_abstractmethod__"

    @staticmethod
    def abstractmethod(func):
        """will explicitly mark a method as an abstract method"""
        setattr(func, Interface.FUNC_KEY, True)
        return func

    def __new__(mcs: t_type['Interface'], name: str, bases: tuple, namespace: dict):
        if len(bases) == 0:
            return mcs._handle_new_interface(mcs, name, bases, namespace)
        return mcs._handle_new_subclass(mcs, name, bases, namespace)

    @staticmethod
    def _handle_new_interface(mcs, name: str, bases: tuple, namespace: Dict[str, Any]) -> type:
        logger.info("Handling new interface creation: %s", name)
        namespace[InterfaceHelper.ORIGINAL_INIT] = None
        if "__init__" in namespace:
            namespace[InterfaceHelper.ORIGINAL_INIT] = namespace["__init__"]
        namespace["__init__"] = InterfaceHelper.create_init_handler(
            name, original=namespace[InterfaceHelper.ORIGINAL_INIT])
        
        abstract_methods = 0
        for k, v in namespace.items():
            if callable(v) and not k == "__init__":
                if not InterfaceHelper.is_func_implemented(v):
                    namespace[k] = InterfaceHelper.create_generic_handler(k, v)
                    abstract_methods += 1
        logger.info("Created interface %s with %s abstract methods", name, abstract_methods)
        namespace[Interface.KEY] = True
        return type.__new__(mcs, name, bases, namespace)

    @staticmethod
    def _handle_new_subclass(mcs: t_type['Interface'], name: str, bases: tuple, namespace: Dict[str, Any]) -> type:
        need_to_be_implemented: set = set()
        ancestry = set()
        for base in bases:
            cls_tree = inspect.getclasstree([base], unique=True)
            ancestry.update(InterfaceHelper.flatten_iterables(cls_tree))
            for item in cls_tree:
                if isinstance(item, tuple):
                    derived, parent = item
                elif len(item) == 1:
                    item = item[0]
                    derived, parent = item
                else:
                    # multiple inheritance case - need to be implemented
                    continue

                if derived is object:
                    continue

                if isinstance(parent, tuple):
                    if len(parent) != 1:
                        pass
                    parent = parent[0]

                if parent is not object:
                    need_to_be_implemented.update(
                        InterfaceHelper.unimplemented_functions(parent))

                need_to_be_implemented.difference_update(
                    InterfaceHelper.implemented_functions(derived))
                need_to_be_implemented.update(
                    InterfaceHelper.unimplemented_functions(derived))

        # cleanup
        del cls_tree, derived, parent

        if object in ancestry:
            ancestry.remove(object)

        missing: set = set()
        for func_name in need_to_be_implemented:
            has_been_declared = func_name in namespace
            if not has_been_declared:
                missing.add(func_name)
                continue

            is_implemented = InterfaceHelper.is_func_implemented(
                namespace[func_name])
            if is_implemented:
                continue

            for ancestor in ancestry:
                if func_name in InterfaceHelper.implemented_functions(ancestor):
                    break
            else:
                missing.add(func_name)

        # cleanup
        del ancestry

        if "__init__" in namespace:
            namespace[InterfaceHelper.ORIGINAL_INIT] = namespace["__init__"]
        else:
            if InterfaceHelper.ORIGINAL_INIT in namespace:
                del namespace[InterfaceHelper.ORIGINAL_INIT]

        if missing:
            namespace[Interface.KEY] = True
            # if "__init__" in need_to_be_implemented:
            namespace["__init__"] = InterfaceHelper.create_init_handler(
                name, missing)
        else:
            namespace[Interface.KEY] = False
            if "__init__" not in namespace:
                namespace["__init__"] = object.__init__

        return type.__new__(mcs, name, bases, namespace)

    @staticmethod
    def is_cls_interface(cls_to_check: type) -> bool:
        """will check if a class is an interface

        Args:
            cls_to_check (type): the class to check

        Returns:
            bool: will return true iff a class is an interface
        """
        if hasattr(cls_to_check, Interface.KEY):
            return cls_to_check.__dict__[Interface.KEY]
        return False


__all__ = [
    "Interface"
]
