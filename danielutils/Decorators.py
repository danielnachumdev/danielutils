from typing import Callable, Type, Any, Union, Tuple
import functools
from .Functions import areoneof, isoneof, isoneof_strict
# from .Exceptions import OverloadDuplication, OverloadNotFound, ValidationTypeError, ValidationValueError


def NotImplemented(func: Callable) -> Callable:
    """decorator to mark function as not implemented for development purposes

    Args:
        func (Callable): the function to decorate
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        raise NotImplementedError(
            f"As marked by the developer {func.__module__}.{func.__name__} is not implemented yet..")
    return wrapper


def PartallyImplemented(func: Callable) -> Callable:
    """decorator to mark function as not fully implemented for development purposes

    Args:
        func (Callable): the function to decorate
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        print(
            f"As marked by the developer, {func.__module__}.{func.__name__} may not be fully implemented and may not work propely")
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


__validation_set = set()


def validate(*args) -> Callable:
    """validate decorator

        Is passed types of variables to perform type checking over\n
        The arguments must be passed in the same order\n

    for each parameter respectivly you can choose one of four options:\n
        1. None - to skip\n
        2. Type - a type to check \n
        3. Sequence of Type to check if the type is contained in the sequence\n
        4. Sequence that contains three arguments:\n
            4.1 a Type or Sequence[Type]\n
            4.2 a function to call on argument\n
            4.3 a str to display in a ValueError iff the condition from 4.2 fails\n
    """
    from .Exceptions import ValidationDuplicationError, ValidationTypeError, ValidationValueError

    def wrapper(func: Callable) -> Callable:
        global __validation_set
        func_id = f"{func.__module__}.{func.__name__}"
        if func_id not in __validation_set:
            __validation_set.add(func_id)
        else:
            raise ValidationDuplicationError(
                "validate decorator is being used on two functions in the same module with the same name\nmaybe use @overload instead")

        def validate_type(v: Any, T: Type, validation_func: Callable[[Any], bool] = isinstance) -> None:
            if not validation_func(v, T):
                raise ValidationTypeError(
                    f"In {func.__module__}.{func.__name__}(...)\nThe argument is: '{ v.__name__ if hasattr(v, '__name__') else v}'\nIt has the type of '{type(v)}'\nIt should be from type(s): '{T}'")

        def validate_condition(v: Any, constraint: Callable[[Any], bool], msg: str = None) -> None:
            if not constraint(v):
                raise ValidationValueError(
                    msg or f"In {func.__module__}.{func.__name__}(...)\nThe argument '{str(v)}' has failed provided constraint\nConstraint in {constraint.__module__}.{constraint.__name__}")

        @functools.wraps(func)
        def inner(*innerargs, **innerkwargs) -> Any:
            for i in range(min(len(args), len(innerargs))):
                if args[i] is not None:
                    if isoneof(args[i], [list, Tuple]):
                        # multiple type only:
                        if areoneof(args[i], [Type]):
                            validate_type(innerargs[i], args[i], isoneof)

                        else:  # maybe with condition:
                            class_type, constraint = args[i][0], args[i][1]

                            # Type validation
                            if isoneof(class_type, [list, Tuple]):
                                validate_type(
                                    innerargs[i], class_type, isoneof)
                            else:
                                validate_type(
                                    innerargs[i], class_type, isinstance)

                            # constraints validation
                            if constraint is not None:
                                message = args[i][2] if len(
                                    args[i]) > 2 else None
                                validate_condition(
                                    innerargs[i], constraint, message)
                    else:
                        validate_type(innerargs[i], args[i])
            return func(*innerargs, **innerkwargs)
        return inner
    return wrapper


__overload_dict: dict[str, dict[Tuple, Callable]] = dict()


def overload(*types) -> Callable:
    """decorator for overloading functions\n
    Usage\n-------\n
    @overload(str,str)\n
    def print_name_and_color(name,color):
        ...\n\n
    @overload(str,[int,float]))\n
    def print_name_and_age(name,age):
        ...\n\n

    also, use 'None' to skip\n\n\n
    \nRaises:
        OverloadDuplication: if a functions is overloaded twice (or more) with same argument types
        OverloadNotFound: if an overloaded function is called with types that has no variant of the function

    \nNotice:
        The function's __doc__ will hold the value of the last variant only
    """
    from .Exceptions import OverloadDuplication, OverloadNotFound
    # make sure to use uniqe global dictonary
    global __overload_dict

    # allow input of both tuples and lists for flexabily
    types = list(types)
    for i, maybe_list_of_types in enumerate(types):
        if isoneof(maybe_list_of_types, [list, Tuple]):
            types[i] = tuple(sorted(list(maybe_list_of_types),
                             key=lambda sub_type: sub_type.__name__))
    types = tuple(types)

    def wrapper(func: Callable) -> Callable:

        # assing current overload to overload dictionary
        name = f"{func.__module__}.{func.__name__}"

        if name not in __overload_dict:
            __overload_dict[name] = dict()

        if types in __overload_dict[name]:
            # raise if current overload already exists for current function
            raise OverloadDuplication(
                f"{name} has duplicate overloading for type(s): {types}")

        __overload_dict[name][types] = func

        @functools.wraps(func)
        def inner(*args, **kwargs) -> Any:

            # select corret overload
            for variable_types, curr_func in __overload_dict[f"{func.__module__}.{func.__name__}"].items():
                if len(variable_types) != len(args):
                    continue

                for i, variable_type in enumerate(variable_types):
                    if variable_type is not None:
                        if isoneof(variable_type, [list, Tuple]):
                            if not isoneof_strict(args[i], variable_type):
                                break
                        else:
                            if not isinstance(args[i], variable_type):
                                break
                else:
                    return curr_func(*args, **kwargs)

            # or raise exception if no overload exists for current arguments
            raise OverloadNotFound(
                f"function {func.__module__}.{func.__name__} is not overloaded with {[type(v) for v in args]}")

        return inner
    return wrapper


def abstractmethod(func: Callable) -> Callable:
    """A decorator to mark a function to be 'pure vitual' / 'abstract'

    Args:
        func (Callable): the function to mark

    Raises:
        NotImplementedError: the error that will rise when the marked function will be called if not overriden in a derived class
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        raise NotImplementedError(
            f"{func.__module__}.{func.__name__} MUST be overrided in a child class")
    return wrapper


purevirtual = abstractmethod

__virtualization_tables = dict()


@NotImplemented
def virtual(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


@NotImplemented
def override(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


@validate([[str, Callable], None, None])
def deprecate(obj: Union[str, Callable] = None) -> Callable:
    """decorator to mark function as depracated

    Args:
        obj (Union[str, None, Callable], optional): Defaults to None.

        Can operate in two configurations:\n
        1. obj is the function that you want to depracate\n
        \t@deprecate\n
        \tdef foo(...):\n
        \t\t...\n\n
        2. obj is an advise message\n
        \t@deprecate("instead use ...")\n
        \tdef foo(...):
        \t\t...
    """
    # if callable(obj):
    if isinstance(obj, Callable):
        @functools.wraps(obj)
        def inner(*args, **kwargs) -> Any:
            print(
                f"As marked by the developer, {obj.__module__}.{obj.__name__} is deprecated")
            return obj(*args, **kwargs)
        return inner

    @validate(Callable)
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def inner(*args, **kwargs) -> Any:
            print(
                f"As marked by the developer, {func.__module__}.{func.__name__} is deprecated")
            if obj:
                print(obj)
            return func(*args, **kwargs)
        return inner
    return wrapper


# @PartallyImplemented
# @validate(str, Type, bool, Callable, str)
# def opt(opt_name: str, opt_type: Type, is_required: bool = True, constraints: Callable[[Any], bool] = None, constraints_description: str = None) -> Callable:
#     """the opt decorator is to easily handle function options

#     Args:
#         name (str): name of option
#         type (Type): type of option
#         required (bool, optional): if this option is required. Defaults to True.
#         constraints (Callable[[Any], bool], optional): a function to check constraints on the option. Defaults to None.
#         constraints_description (str, optional): a message to show if constraints check fails. Defaults to None.

#     Returns:
#         Callable: return decorated function
#     """
#     def wrapper(func):
#         @ functools.wraps(func)
#         def inner(*args, **kwargs):
#             if is_required and args[0] is None:
#                 raise ValueError(
#                     f"{opt_name} was marked as required and got None")
#             if not isinstance(args[0], opt_type):
#                 raise TypeError(
#                     f"{opt_name} has value of wrong type: {args[0]} which is {type(args[0])} instead of {opt_type}")
#             return func(*args, **kwargs)
#         return inner
#     return wrapper
