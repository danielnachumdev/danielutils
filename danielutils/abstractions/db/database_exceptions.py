class DBException(Exception):
    """Base class for all database exceptions"""


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
