from typing import Callable, Type, Any, Union, Tuple
import functools
from .Functions import isoneof, isoneof_strict
from .Exceptions import OverloadDuplication, OverloadNotFound


def NotFullyImplemented(func: Callable) -> Callable:
    """decorator to mark function as not fully implemented for development purposes

    Args:
        func (Callable): the function to decorate
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        print(
            f"As marked by the developer {func.__module__}.{func.__name__} is not fully implemented and may not work propely")
        return func(*args, **kwargs)
    return wrapper


def memo(func: Callable) -> Callable:
    """decorator to memorize function calls in order to improve preformance by using more memory

    Args:
        func (Callable): function to memorize
    """
    cache: dict[Tuple, Any] = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if (args, *kwargs.items()) not in cache:
            cache[(args, *kwargs.items())] = func(*args, **kwargs)
        return cache[(args, *kwargs.items())]
    return wrapper


def validate(*args) -> Callable:
    """validate decorator

        Is passed types of variables to perform type checking over
        The arguments must be passed in the same order

        for each parameter respectivly you can choose three things:
        1. None - to skip
        2. Type - a type to check 
        3. Tuple/list - (Union[Type, list[Type]], Callable[[Any], bool], str)
            where Type is the type for type checking validation,
            condition is a function to call on the value which return bool.
            str is the message to raise inside the ValueError when condition fails

    Returns:
        Callable: return decorated function
    """
    def wrapper(func: Callable) -> Callable:
        def validate_type(v: Any, T: Type, validation_func: Callable[[Any], bool] = isinstance) -> None:
            if not validation_func(v, T):
                raise TypeError(
                    f"In {func.__module__}.{func.__name__}(...) for argument '{ v.__name__ if hasattr(v, '__name__') else v}' its  type is '{type(v)}' but must be of type '{T}'")

        def validate_condition(v: Any, condition: Callable[[Any], bool], msg: str = None) -> None:
            if not condition(v):
                raise ValueError(
                    msg or f"In {func.__module__}.{func.__name__}(...), argument: '{str(v)}' doesnt comply with constraints given in {condition.__module__}.{condition.__name__}")

        @functools.wraps(func)
        def inner(*innerargs, **innerkwargs) -> Any:
            for i in range(min(len(args), len(innerargs))):
                if args[i] is not None:
                    if isoneof(args[i], [list, Tuple]):
                        class_type, condition = args[i][0], args[i][1]

                        # Type validation
                        if isoneof(class_type, [list, Tuple]):
                            validate_type(innerargs[i], class_type, isoneof)
                        else:
                            validate_type(innerargs[i], class_type, isinstance)

                        # constraints validation
                        if condition is not None:
                            message = args[i][2] if len(args[i]) > 2 else None
                            validate_condition(
                                innerargs[i], condition, message)
                    else:
                        validate_type(innerargs[i], args[i])
            return func(*innerargs, **innerkwargs)
        return inner
    return wrapper


@NotFullyImplemented
@validate(str, Type, bool, Callable, str)
def opt(opt_name: str, opt_type: Type, is_required: bool = True, constraints: Callable[[Any], bool] = None, constraints_description: str = None) -> Callable:
    """the opt decorator is to easily handle function options

    Args:
        name (str): name of option
        type (Type): type of option
        required (bool, optional): if this option is required. Defaults to True.
        constraints (Callable[[Any], bool], optional): a function to check constraints on the option. Defaults to None.
        constraints_description (str, optional): a message to show if constraints check fails. Defaults to None.

    Returns:
        Callable: return decorated function
    """
    def wrapper(func):
        @ functools.wraps(func)
        def inner(*args, **kwargs):
            if is_required and args[0] is None:
                raise ValueError(
                    f"{opt_name} was marked as required and got None")
            if not isinstance(args[0], opt_type):
                raise TypeError(
                    f"{opt_name} has value of wrong type: {args[0]} which is {type(args[0])} instead of {opt_type}")
            return func(*args, **kwargs)
        return inner
    return wrapper


__overload_func_dict: dict[str, dict[Tuple, Callable]] = dict()


def overload(*types) -> Callable:
    """decorator for overloading functions

    Raises:
        OverloadDuplication: if a functions is overloaded twice the same
        OverloadNotFound: if an overloaded function is called with types that has no variant of the function
    """
    # make sure to use uniqe global dictonary
    global __overload_func_dict

    # allow input of both tuples and lists for flexabily
    types = list(types)
    for i, maybe_list_of_types in enumerate(types):
        if isoneof(maybe_list_of_types, [list, Tuple]):
            types[i] = tuple(sorted(list(maybe_list_of_types),
                             key=lambda sub_type: sub_type.__name__))
    types = tuple(types)

    def wrapper(func: Callable) -> Callable:
        name = f"{func.__module__}.{func.__name__}"

        if name not in __overload_func_dict:
            __overload_func_dict[name] = dict()

        if types in __overload_func_dict[name]:
            raise OverloadDuplication(
                f"{name} already has an overload with {types}")

        __overload_func_dict[name][types] = func

        @functools.wraps(func)
        def inner(*args, **kwargs) -> Any:

            for variable_types, curr_func in __overload_func_dict[f"{func.__module__}.{func.__name__}"].items():
                if len(variable_types) != len(args):
                    continue

                for i, variable_type in enumerate(variable_types):
                    if isoneof(variable_type, [list, Tuple]):
                        if not isoneof_strict(args[i], variable_type):
                            break
                    else:
                        if not isinstance(args[i], variable_type):
                            break
                else:
                    return curr_func(*args, **kwargs)

            raise OverloadNotFound(
                f"function {func.__module__}.{func.__name__} is not overloaded with {types}")

        return inner
    return wrapper


@NotFullyImplemented
def abstractmethod(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        raise NotImplementedError(
            f"{func.__module__}.{func.__name__} MUST be overrided in a child class")
    return wrapper


@NotFullyImplemented
def override(func: Callable) -> Callable:
    pass

    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
