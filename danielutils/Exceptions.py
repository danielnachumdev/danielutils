class OverloadException(Exception):
    """Base exception for overload decorator
    """
    pass


class OverloadNotFound(OverloadException):
    """
    Exception to raise if a function is called with certain argument types but this function hasn't been overloaded with those types
    """
    pass


class OverloadDuplication(OverloadException):
    """
    Exception to raise if a function is overloaded twice with same argument types
    """
    pass


class ValidationError(Exception):
    pass


class ValidationTypeError(ValidationError, TypeError):
    pass


class ValidationReturnTypeError(ValidationError, TypeError):
    pass


class ValidationValueError(ValidationError, ValueError):
    pass


class ValidationDuplicationError(ValidationError):
    pass


class TimeoutError(AssertionError):
    pass
