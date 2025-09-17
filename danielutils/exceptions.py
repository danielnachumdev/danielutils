
import logging

from .logging_.utils import get_logger

logger = get_logger(__name__)


class OverloadException(Exception):
    """Base exception for overload decorator
    """


class OverloadNotFound(OverloadException):
    """Exception to raise if a function is called with certain
    argument types but this function hasn't been overloaded with those types
    """


class OverloadDuplication(OverloadException):
    """
    Exception to raise if a function is overloaded twice with same argument types
    """


# class ValidationError(Exception):
#     """_summary_

#     Args:
#         Exception (_type_): _description_

#     Returns:
#         _type_: _description_
#     """


# class ValidationTypeError(ValidationError, TypeError):
#     pass


# class ValidationReturnTypeError(ValidationError, TypeError):
#     pass


# class ValidationValueError(ValidationError, ValueError):
#     pass


# class ValidationDuplicationError(ValidationError):
#     pass


class ValidationException(Exception):
    """generic validation exception for validate decorator
    """


class EmptyAnnotationException(ValidationException):
    """exception for validate decorator to be used if a function needs to 
    be validated but has an empty annotation for one of the arguments
    """


class InvalidDefaultValueException(ValidationException):
    """exception for validate decorator to be used if a function has
    a default value that doesn't conform to the annotated type
    """


class InvalidReturnValueException(ValidationException):
    """exception for validate decorator to be used if a function has
    an annotated return value but the actual return value doesn't conform to it
    """


class PrintCatchOne:
    """a utility class to be used with a "with" block to print 
    any exception that happens inside of it rather than exiting the program
    """

    def __enter__(self):
        return self

    def __exit__(self, cls, instance, traceback):
        if instance:
            logger.error(f"Exception caught in PrintCatchOne: {cls} {instance}")
            from .colors import error  # pylint: disable=cyclic-import
            error(f"{cls} {instance}")
            return isinstance(instance, cls)
        return False
