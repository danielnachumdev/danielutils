import functools
import inspect
from typing import Callable,  get_type_hints
from ..Functions import isoftype
from ..Exceptions import EmptyAnnotationException,\
    InvalidDefaultValueException, ValidationException, InvalidReturnValueException


def validate(strict: Callable | bool = True) -> Callable:
    """A decorator that validates the annotations and types of the arguments and return
    value of a function.

        * 'None' is allowed as default value for everything
        * Because of their wide known use, generally accepted keywords 'self', 'cls', 'args', 'kwargs'
        are not validated.

    Args:
        func (Callable): The function to be decorated.

    Raises:
        TypeError: if the decorated object is nto a Callable
        EmptyAnnotationException: If an argument is not annotated.
        InvalidDefaultValueException: If an argument's default value is not of the annotated type.
        ValidationException: If an argument's value is not of the expected type.
        InvalidReturnValueException: If the return value is not of the expected type.

    Returns:
        Callable: A wrapper function that performs the validation and calls the original function.
    """
    if not isoftype(strict, bool | Callable):
        raise TypeError(
            "the argument for validate must be a Callable or a boolean to mark strict use")

    def deco(func):
        nonlocal strict
        SKIP_SET = {"self", "cls", "args", "kwargs"}
        if not isinstance(func, Callable):
            raise TypeError(
                "The validate decorator must only decorate a function")
        func_name = f"{func.__module__}.{func.__qualname__}"
        # get the signature of the function
        signature = inspect.signature(func)
        for arg_name, arg_param in signature.parameters.items():
            if arg_name not in SKIP_SET:
                arg_type = arg_param.annotation
                # check if an annotation is missing
                if arg_type == inspect.Parameter.empty:
                    raise EmptyAnnotationException(
                        f"In {func_name}, argument '{arg_name}' is not annotated")

            # check if the argument has a default value
            default_value = signature.parameters[arg_name].default
            if default_value != inspect.Parameter.empty:
                # allow everything to be set to None as default
                if default_value is None:
                    continue
                # if it does, check the type of the default value
                if not isoftype(default_value, arg_type):
                    raise InvalidDefaultValueException(
                        f"In {func_name}, argument '{arg_name}'s default value is annotated \
                        as {arg_type} but got '{default_value}' which is {type(default_value)}")

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """wrapper function for the type validating - will run on each call independently
            """
            hints = None
            # check all arguments
            bound = signature.bind(*args, **kwargs)
            for variable_name, variable_value in bound.arguments.items():
                if variable_name in SKIP_SET:
                    continue
                expected_type = func.__annotations__[variable_name]

                if isinstance(expected_type, str):
                    # why does this even happen?
                    if hints is None:
                        hints = get_type_hints(func)
                    expected_type = hints[variable_name]

                if not isoftype(variable_value, expected_type, strict=strict):
                    raise ValidationException(
                        f"In {func_name}, argument '{variable_name}' is annotated as "
                        f"{expected_type} but got '{variable_value}' which is {type(variable_value)}")

            # call the function
            result = func(*args, **kwargs)

            # check the return type
            return_type = type(None) if ("inspect._empty" in str(signature.return_annotation)
                                         or signature.return_annotation is None) else signature.return_annotation
            if isinstance(return_type, str):
                # why does this even happen?
                return_type = get_type_hints(func)["return"]
            if return_type is not type(None) and not isoftype(result, return_type):
                raise InvalidReturnValueException(
                    f"In function {func_name}, the return type is annotated as "
                    f"{return_type} but got '{result}' which is {type(result)}")
            return result
        return wrapper
    if isinstance(strict, Callable):
        func = strict
        strict = True
        return deco(func)
    return deco


# def validate(func: Callable) -> Callable:
    # """A decorator that validates the annotations and types of the arguments and return
    # value of a function.

    #     * 'None' is allowed as default value for everything
    #     * Because of their use in classes, the generally accepted keywords 'self' and 'cls'
    #     are not validated to not break intellisense when using 'Any'

    # Args:
    #     func (Callable): The function to be decorated.

    # Raises:
    #     TypeError: if the decorated object is nto a Callable
    #     EmptyAnnotationException: If an argument is not annotated.
    #     InvalidDefaultValueException: If an argument's default value is not of the annotated type.
    #     ValidationException: If an argument's value is not of the expected type.
    #     InvalidReturnValueException: If the return value is not of the expected type.

    # Returns:
    #     Callable: A wrapper function that performs the validation and calls the original function.
    # """
    # SKIP_SET = {"self", "cls"}
    # if not isinstance(func, Callable):
    #     raise TypeError("The validate decorator must only decorate a function")
    # func_name = f"{func.__module__}.{func.__qualname__}"
    # # get the signature of the function
    # signature = inspect.signature(func)
    # for arg_name, arg_param in signature.parameters.items():
    #     if arg_name not in SKIP_SET:
    #         arg_type = arg_param.annotation
    #         # check if an annotation is missing
    #         if arg_type == inspect.Parameter.empty:
    #             raise EmptyAnnotationException(
    #                 f"In {func_name}, argument '{arg_name}' is not annotated")

    #     # check if the argument has a default value
    #     default_value = signature.parameters[arg_name].default
    #     if default_value != inspect.Parameter.empty:
    #         # allow everything to be set to None as default
    #         if default_value is None:
    #             continue
    #         # if it does, check the type of the default value
    #         if not isoftype(default_value, arg_type):
    #             raise InvalidDefaultValueException(
    #                 f"In {func_name}, argument '{arg_name}'s default value is annotated \
    #                 as {arg_type} but got '{default_value}' which is {type(default_value)}")

    # @functools.wraps(func)
    # def wrapper(*args, **kwargs):
    #     """wrapper function for the type validating - will run on each call independently
    #     """
    #     hints = None
    #     # check all arguments
    #     bound = signature.bind(*args, **kwargs)
    #     for variable_name, variable_value in bound.arguments.items():
    #         if variable_name in SKIP_SET:
    #             continue
    #         expected_type = func.__annotations__[variable_name]

    #         if isinstance(expected_type, str):
    #             # why does this even happen?
    #             if hints is None:
    #                 hints = get_type_hints(func)
    #             expected_type = hints[variable_name]

    #         if not isoftype(variable_value, expected_type):
    #             raise ValidationException(
    #                 f"In {func_name}, argument '{variable_name}' is annotated as \
    #                     {expected_type} but got '{variable_value}' which is {type(variable_value)}")

    #     # call the function
    #     result = func(*args, **kwargs)

    #     # check the return type
    #     return_type = type(None) if ("inspect._empty" in str(signature.return_annotation)
    #                                  or signature.return_annotation is None) else signature.return_annotation
    #     if isinstance(return_type, str):
    #         # why does this even happen?
    #         return_type = get_type_hints(func)["return"]
    #     if return_type is not type(None) and not isoftype(result, return_type):
    #         raise InvalidReturnValueException(
    #             f"In function {func_name}, the return type is annotated as "
    #             f"{return_type} but got '{result}' which is {type(result)}")
    #     return result
    # return wrapper

# @validate
# def NotImplemented(func: Callable) -> Callable:
#     """decorator to mark function as not implemented for development purposes

#     Args:
#         func (Callable): the function to decorate
#     """
#     @ functools.wraps(func)
#     def wrapper(*args, **kwargs) -> Any:
#         raise NotImplementedError(
#             f"As marked by the developer {func.__module__}.{func.__qualname__} is not implemented yet..")
#     return wrapper


__all__ = [
    "validate"
]
