from typing import Optional


class DBException(Exception):
    """Base class for all database exceptions"""

    def __init__(self, message: str, status_code: Optional[int] = None) -> None:
        super().__init__(message)
        self.status_code = status_code


class DBConnectionError(DBException):
    """Raised when there is an error connecting to the database"""


class DBQueryError(DBException):
    """Raised when there is an error executing a query"""


class DBSchemaError(DBException):
    """Raised when there is an error with database schema operations"""


class DBValidationError(DBException):
    """Raised when there is a validation error"""


__all__ = [
    "DBException",
    "DBConnectionError",
    "DBQueryError",
    "DBSchemaError",
    "DBValidationError"
]
