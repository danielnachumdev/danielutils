from typing import Callable, Iterable
import inspect
import re
import traceback


class InterfaceHelper:
    ORIGINAL_INIT = "__originalinit__"

    def flatten_iterables(iterable: Iterable) -> list:
        res = []
        for obj in iterable:
            if isinstance(obj, Iterable) and not isinstance(obj, str):
                res.extend(InterfaceHelper.flatten_iterables(obj))
            else:
                res.append(obj)
        return res

    def is_func_implemented(func) -> bool:
        if hasattr(func, Interface.FUNCKEY):
            return not func.__dict__[Interface.FUNCKEY]

        src = inspect.getsource(func)
        if re.match(Interface.IMPLICIT_ABSTRACT, src):
            return False

        is_default_override = (
            func.__qualname__.startswith(InterfaceHelper.__name__))
        return not is_default_override

    def unimplemented_functions(cls) -> list[str]:
        res = []
        for func_name in InterfaceHelper.get_declared_function_names(cls):
            func = cls.__dict__[func_name]
            if not InterfaceHelper.is_func_implemented(func):
                res.append(func_name)
        return res

    def implemented_functions(cls) -> list[str]:
        res = []
        for func_name in InterfaceHelper.get_declared_function_names(cls):
            func = cls.__dict__[func_name]
            if InterfaceHelper.is_func_implemented(func):
                res.append(func_name)
        return res

    def get_declared_function_names(cls) -> list[str]:
        src = inspect.getsource(cls).splitlines()
        for line in src:
            if re.match(r".*def \w+\(.*\).*:", line):
                func_name = re.findall(r".*def (\w+)\(.*", line)[0]
                yield func_name
    __mro_dict = dict()

    def create_init_handler(cls_name, missing: list[str] = None):

        def __interfaceinit__(*args, **kwargs):
            instance = args[0]
            if instance not in InterfaceHelper.__mro_dict:
                InterfaceHelper.__mro_dict[instance] = 1
            else:
                InterfaceHelper.__mro_dict[instance] += 1

            caller_frame = traceback.format_stack()[-2]
            is_super_call = bool(re.match(
                r"\s+File \".*\", line \d+, in __init__\n\s+super\(\)\.__init__\(.*\)\n", caller_frame))
            if is_super_call:
                mro = instance.__class__.mro()
                for cls in mro[InterfaceHelper.__mro_dict[instance]:]:
                    if hasattr(cls, InterfaceHelper.ORIGINAL_INIT):
                        result = getattr(cls, InterfaceHelper.ORIGINAL_INIT)(
                            *args, **kwargs)
                        if instance in InterfaceHelper.__mro_dict:
                            del InterfaceHelper.__mro_dict[instance]
                        return result
                raise NotImplementedError(
                    f"Can't use super().__init__(...) in {cls_name}.__init__(...) if the __init__ function is not defined a parent interface")

            del InterfaceHelper.__mro_dict[instance]
            if missing:
                raise NotImplementedError(
                    f"Can't instantiate '{cls_name}' because it is an interface. It is missing implementations for {missing}")
            raise NotImplementedError(
                f"'{cls_name}' is an interface, Can't create instances")
        return __interfaceinit__

    def create_generic_handler(cls_name, func_name):
        def __interfacehandler__(*args, **kwargs):
            raise NotImplementedError(
                f"Interface {func_name} must be implemented")
        return __interfacehandler__


class Interface(type):
    IMPLICIT_ABSTRACT = r"\s*def \w+\(.*?\)(?:\s*->\s*\w+)?:\n(?:\s*\"{3}.*\"{3}\n)?\s*\.{3}\n"
    KEY = "__isinterface__"
    FUNCKEY = "__isabstractmethod__"

    @staticmethod
    def abstractmethod(func):
        setattr(func, Interface.FUNCKEY, True)
        return func

    def __new__(cls, name, bases, namespace):
        if len(bases) == 0:
            return Interface.__handle_new_interface(cls, name, bases, namespace)
        else:
            return Interface.__handle_new_subclass(cls, name, bases, namespace)

    @staticmethod
    def __handle_new_interface(cls, name, bases, namespace):
        if "__init__" in namespace:
            namespace[InterfaceHelper.ORIGINAL_INIT] = namespace["__init__"]
        namespace["__init__"] = InterfaceHelper.create_init_handler(name)
        for k, v in namespace.items():
            if isinstance(v, Callable) and not k == "__init__":
                if not InterfaceHelper.is_func_implemented(v):
                    namespace[k] = InterfaceHelper.create_generic_handler(
                        name, k)
        namespace[Interface.KEY] = True
        return super().__new__(cls, name, bases, namespace)

    @staticmethod
    def __handle_new_subclass(cls, name, bases, namespace):
        need_to_be_implemented = set()
        ancestry = set()
        for base in bases:
            clstree = inspect.getclasstree([base], unique=True)
            ancestry.update(InterfaceHelper.flatten_iterables(clstree))
            for item in clstree:
                if isinstance(item, tuple):
                    derived, parent = item
                elif len(item) == 1:
                    item = item[0]
                    derived, parent = item
                else:
                    # multiple inheritance case - need to be implemented
                    breakpoint()
                    continue

                if derived is object:
                    continue

                if isinstance(parent, tuple):
                    if len(parent) != 1:
                        breakpoint()
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
        del item, clstree, derived, parent, base

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
            if "__init__" in need_to_be_implemented:
                namespace["__init__"] = InterfaceHelper.create_init_handler(
                    name, missing)
        else:
            namespace[Interface.KEY] = False
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
