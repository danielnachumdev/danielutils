from typing import Callable, Iterable, Any, Generator
import inspect
import re
import traceback
import functools
from ..Decorators import decorate_conditionally


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
        src = inspect.getsource(cls).splitlines()
        for line in src:
            if re.match(r".*def \w+\(.*\).*:", line):
                func_name = re.findall(r".*def (\w+)\(.*", line)[0]
                yield func_name

    @staticmethod
    def create_init_handler(cls_name, missing: list[str] = None, original: Callable = None):
        """this function will create the default interface __init__ function with the wanted behavior"""
        # @decorate_conditionally(functools.wraps, original is not None, [original])  # TODO implement this decorator
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
                raise NotImplementedError(
                    f"Can't use super().__init__(...) in {cls_name}.__init__(...) "
                    "if the __init__ function is not defined a parent interface")

            if missing:
                raise NotImplementedError(f"Can't instantiate '{cls_name}' because it is an interface."
                                          f" It is missing implementations for {missing}")
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
            raise NotImplementedError(
                f"Interface {cls} must be implemented")
        return __interface_handler__


class Interface(type):
    """This is a metaclass that will enable classes that inherit it directly (or indirectly)
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

    def __new__(mcs, name: str, bases: tuple, namespace: dict):
        if len(bases) == 0:
            return mcs._handle_new_interface(mcs, name, bases, namespace)
        return mcs._handle_new_subclass(mcs, name, bases, namespace)

    def _handle_new_interface(cls, name: str, bases: tuple, namespace: dict[str, Any]):
        namespace[InterfaceHelper.ORIGINAL_INIT] = None
        if "__init__" in namespace:
            namespace[InterfaceHelper.ORIGINAL_INIT] = namespace["__init__"]
        namespace["__init__"] = InterfaceHelper.create_init_handler(
            name, original=namespace[InterfaceHelper.ORIGINAL_INIT])
        for k, v in namespace.items():
            if isinstance(v, Callable) and not k == "__init__":
                if not InterfaceHelper.is_func_implemented(v):
                    namespace[k] = InterfaceHelper.create_generic_handler(k, v)
        namespace[Interface.KEY] = True
        return super().__new__(cls, name, bases, namespace)

    def _handle_new_subclass(cls, name: str, bases: tuple, namespace: dict[str, Any]):
        need_to_be_implemented = set()
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

        return super().__new__(cls, name, bases, namespace)

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
