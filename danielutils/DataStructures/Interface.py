from typing import Callable, Iterable
import inspect
import re


def flatten_iterables(iterable: Iterable) -> list:
    res = []
    for obj in iterable:
        if isinstance(obj, Iterable) and not isinstance(obj, str):
            res.extend(flatten_iterables(obj))
        else:
            res.append(obj)
    return res


def is_func_implemented(func) -> bool:
    src = inspect.getsource(func).splitlines()
    is_minimal_deceleration = (len(src) == 2 and src[1].strip() == "pass")
    is_default_override = (func.__qualname__.startswith("Interface"))
    return (not is_minimal_deceleration) and (not is_default_override)


def unimplemented_functions(cls) -> list[str]:
    res = []
    for func_name in get_declared_function_names(cls):
        func = cls.__dict__[func_name]
        if not is_func_implemented(func):
            res.append(func_name)
    return res


def implemented_functions(cls):
    res = []
    for func_name in get_declared_function_names(cls):
        func = cls.__dict__[func_name]
        if is_func_implemented(func):
            res.append(func_name)
    return res


def get_declared_function_names(cls) -> list[str]:
    src = inspect.getsource(cls).splitlines()
    for line in src:
        if re.match(r".*def \w+\(.*\).*:", line):
            func_name = re.findall(r".*def (\w+)\(.*", line)[0]
            yield func_name


def create_init_handler(cls_name, missing: list[str] = None):
    def inner(*args, **kwargs):
        if missing:
            raise NotImplementedError(
                f"Can't instantiate '{cls_name}' because it is an interface. It is missing implementations for {missing}")
        else:
            raise NotImplementedError(
                f"'{cls_name}' is an interface, Can't create instances")
    return inner


def create_generic_handler(cls_name, func_name):
    def inner(*args, **kwargs):
        raise NotImplementedError(
            f"Interface {func_name} must be implemented")
    return inner


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


class Interface(type):
    KEY = "__isinterface__"

    def __new__(cls, name, bases, namespace):
        if len(bases) == 0:
            return Interface.__handle_new_interface(cls, name, bases, namespace)
        else:
            return Interface.__handle_new_subclass(cls, name, bases, namespace)

    @staticmethod
    def __handle_new_interface(cls, name, bases, namespace):
        namespace["__init__"] = create_init_handler(name)
        for k, v in namespace.items():
            if isinstance(v, Callable) and not k == "__init__":
                if not is_func_implemented(v):
                    namespace[k] = create_generic_handler(name, k)
        namespace[Interface.KEY] = True
        return super().__new__(cls, name, bases, namespace)

    @staticmethod
    def __handle_new_subclass(cls, name, bases, namespace):
        need_to_be_implemented = set()
        ancestry = set()
        for base in bases:
            clstree = inspect.getclasstree([base], unique=True)
            ancestry.update(flatten_iterables(clstree))
            for item in clstree:
                if isinstance(item, tuple):
                    derived, parent = item
                    if derived is object:
                        continue
                    need_to_be_implemented.update(
                        unimplemented_functions(derived))
                else:
                    if len(item) == 1:
                        item = item[0]
                        derived, parent = item
                        if derived is object:
                            continue
                        if len(parent) == 1:
                            parent = parent[0]
                            if parent is not object:
                                need_to_be_implemented.update(unimplemented_functions(
                                    parent))
                        else:
                            breakpoint()  # TODO is reachable?
                            pass
                        need_to_be_implemented.difference_update(
                            implemented_functions(derived))
                        need_to_be_implemented.update(
                            unimplemented_functions(derived))
                    else:
                        breakpoint()  # TODO is reachable?
                        pass
        if object in ancestry:
            ancestry.remove(object)

        missing = []
        for func_name in need_to_be_implemented:
            if func_name not in namespace or not is_func_implemented(namespace[func_name]):
                for ancestor in ancestry:
                    if func_name in implemented_functions(ancestor):
                        break
                else:
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
                if "__init__" not in namespace:
                    namespace["__init__"] = object.__init__
        return super().__new__(cls, name, bases, namespace)

    @staticmethod
    def is_cls_interface(cls: type):
        if hasattr(cls, Interface.KEY):
            return cls.__dict__[Interface.KEY]
        return False


__all__ = [
    "Interface"
]
