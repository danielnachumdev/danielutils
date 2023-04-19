from typing import Callable, Iterable
import inspect
import re


def flatten_iterables(iterable: Iterable) -> list:
    """Convert iterables (lists, tuples, sets...) to list (excluding string and dictionary)

    Args:
        iterables (Iterable): Iterables to flatten

    Returns:
        list: return a flattened list
    """
    lis = []
    for i in iterable:
        if isinstance(i, Iterable) and not isinstance(i, str):
            lis.extend(flatten_iterables(i))
        else:
            lis.append(i)
    return lis


def handle_tuple(tup):
    pass


class Interface(type):
    KEY = "__isinterface__"

    def __new__(cls, name, bases, namespace):
        if len(bases) == 0:
            return Interface.handle_new_interface(cls, name, bases, namespace)
        else:
            return Interface.handle_new_subclass(cls, name, bases, namespace)

    @staticmethod
    def create_init_handler(cls_name, missing: list[str] = None):
        def inner(*args, **kwargs):
            if missing:
                raise NotImplementedError(
                    f"Can't instantiate '{cls_name}' because it is an interface. It is missing implementations for {missing}")
            else:
                raise NotImplementedError(
                    f"'{cls_name}' is an interface, Can't create instances")
        return inner

    @staticmethod
    def create_generic_handler(cls_name, func_name):
        def inner(*args, **kwargs):
            raise NotImplementedError(
                f"Interface {func_name} must be implemented")
        return inner

    @staticmethod
    def is_func_implemented(func) -> bool:
        src = inspect.getsource(func).splitlines()
        return not (len(src) == 2 and src[1].strip() == "pass") and not (func.__qualname__.startswith("Interface"))

    @staticmethod
    def handle_new_interface(cls, name, bases, namespace):
        namespace["__init__"] = Interface.create_init_handler(name)
        for k, v in namespace.items():
            if isinstance(v, Callable) and not k == "__init__":
                if not Interface.is_func_implemented(v):
                    namespace[k] = Interface.create_generic_handler(name, k)
        namespace[Interface.KEY] = True
        return super().__new__(cls, name, bases, namespace)

    @staticmethod
    def get_decalred_function_names(cls) -> list[str]:
        src = inspect.getsource(cls).splitlines()
        function_names = []
        for line in src:
            if re.match(r".*def \w+\(.*\).*:", line):
                func_name = re.findall(r".*def (\w+)\(.*", line)[0]
                function_names.append(func_name)
        return function_names

    @staticmethod
    def unimplemented_functions(cls) -> list[str]:
        res = []
        for func_name in Interface.get_decalred_function_names(cls):
            func = cls.__dict__[func_name]
            if not Interface.is_func_implemented(func):
                res.append(func_name)
        return res

    @staticmethod
    def implemented_functions(cls):
        res = []
        for func_name in Interface.get_decalred_function_names(cls):
            func = cls.__dict__[func_name]
            if Interface.is_func_implemented(func):
                res.append(func_name)
        return res

    @staticmethod
    def handle_new_subclass(cls, name, bases, namespace):
        need_to_be_implemented = set()
        for base in bases:
            clstree = inspect.getclasstree([base], unique=True)
            for item in clstree:
                if isinstance(item, tuple):
                    derived, parent = item
                    if derived is object:
                        continue
                    need_to_be_implemented.update(
                        Interface.unimplemented_functions(derived))
                else:
                    if len(item) == 1:
                        item = item[0]
                        derived, parent = item
                        if derived is object:
                            continue
                        if len(parent) == 1:
                            parent = parent[0]
                            if parent is not object:
                                need_to_be_implemented.update(Interface.unimplemented_functions(
                                    parent))
                        else:
                            breakpoint()
                            pass
                        need_to_be_implemented.difference_update(
                            Interface.implemented_functions(derived))
                        need_to_be_implemented.update(
                            Interface.unimplemented_functions(derived))
                    else:
                        breakpoint()
                        pass

        missing = []
        for func_name in need_to_be_implemented:
            if func_name not in namespace or not Interface.is_func_implemented(namespace[func_name]):
                namespace[Interface.KEY] = True
                missing.append(func_name)

        if "__init__" in need_to_be_implemented:
            if Interface.KEY in namespace:
                namespace["__init__"] = Interface.create_init_handler(
                    name)
        else:
            if missing:
                namespace["__init__"] = Interface.create_init_handler(
                    name, missing)
            else:
                pass
        return super().__new__(cls, name, bases, namespace)

    @staticmethod
    def check_parent(parent):
        clstree = inspect.getclasstree([parent])
        parents = []
        for obj in clstree:
            if isinstance(obj, tuple):
                if obj[0] is not object:
                    parents.append(obj[0])
            elif isinstance(obj, list):
                for tup in obj:
                    if tup[0] is not object:
                        parents.append(tup[0])
        for parent in parents:
            if Interface.is_cls_interface(parent):
                pass

    @staticmethod
    def is_cls_interface(cls: type):
        if hasattr(cls, Interface.KEY):
            return cls.__dict__[Interface.KEY]
        return False


__all__ = [
    "Interface"
]
