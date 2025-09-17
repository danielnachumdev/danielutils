import functools
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Callable, TypeVar, cast, Optional, Set
from .database_exceptions import DBException
from .database_definitions import TableSchema, SelectQuery, UpdateQuery, DeleteQuery
from ...logging_.utils import get_logger
logger = get_logger(__name__)

# Type variable for the decorator
F = TypeVar('F', bound=Callable[..., Any])


class Database(ABC):
    """Abstract base class for database operations"""

    @classmethod
    def _wrap_db_exceptions(cls, db_method: F) -> F:
        """
        Private decorator to wrap database implementation methods and convert implementation-specific
        exceptions to our standard database exceptions.
        """

        @functools.wraps(db_method)
        async def wrapper(self: 'Database', *args: Any, **kwargs: Any) -> Any:
            method_name = db_method.__name__
            logger.debug(f"Executing database method: {method_name}")
            try:
                result = await db_method(self, *args, **kwargs)
                logger.debug(f"Database method '{method_name}' completed successfully")
                return result
            except DBException as e:
                logger.error(f"Database method '{method_name}' failed with DBException: {e}")
                raise
            except Exception as e:
                logger.error(f"Database method '{method_name}' failed with {type(e).__name__}: {e}")
                raise cls._default_class_exception_conversion(e)

        return cast(F, wrapper)

    @classmethod
    def _get_functions_with_auto_converted_exceptions(cls) -> Set[str]:
        return {
            "connect",
            "disconnect",
            "get_schemas",
            "create_table",
            "insert",
            "get",
            "update",
            "delete"
        }

    @classmethod
    def __init_subclass__(cls) -> None:
        """Initialize subclass by wrapping all public methods with exception handling"""
        logger.debug(f"Initializing Database subclass: {cls.__name__}")
        wrapped_methods = []
        for name, method in cls.__dict__.items():
            if (
                    callable(method) and
                    not name.startswith('_') and
                    not isinstance(method, (classmethod, staticmethod))
                    and name in cls._get_functions_with_auto_converted_exceptions()
            ):
                setattr(cls, name, cls._wrap_db_exceptions(method))
                wrapped_methods.append(name)
        logger.debug(f"Database subclass '{cls.__name__}' initialized with {len(wrapped_methods)} wrapped methods: {wrapped_methods}")

    @classmethod
    def _default_class_exception_conversion(cls, e: Exception) -> Exception:
        """
        Handle implementation-specific exceptions. Override this method in implementations
        to provide custom exception handling.

        Args:
            e (Exception): The original exception

        Returns:
            Exception: The converted exception
        """
        logger.warning(f"Converting exception {type(e).__name__} to DBException: {e}")
        return DBException(f"Database error: {str(e)}")

    async def __aenter__(self) -> 'Database':
        """
        Context manager entry point. Connects to the database.

        Returns:
            Database: The database instance for use in the context
        """
        logger.debug(f"Entering database context for {self.__class__.__name__}")
        await self.connect()
        logger.debug(f"Database context entered successfully for {self.__class__.__name__}")
        return self

    async def __aexit__(self, exc_type: Optional[type], exc_val: Optional[Exception], exc_tb: Optional[Any]) -> None:
        """
        Context manager exit point. Disconnects from the database.

        Args:
            exc_type: The type of exception that was raised, if any
            exc_val: The exception instance that was raised, if any
            exc_tb: The traceback for the exception, if any
        """
        logger.debug(f"Exiting database context for {self.__class__.__name__}")
        if exc_type is not None:
            logger.warning(f"Database context exited with exception: {exc_type.__name__}: {exc_val}")
        await self.disconnect()
        logger.debug(f"Database context exited successfully for {self.__class__.__name__}")

    @abstractmethod
    async def connect(self) -> None:
        """Establish connection to the database
        Note: Implementations should log connection attempts and results
        """

    @abstractmethod
    async def disconnect(self) -> None:
        """Close the database connection
        Note: Implementations should log disconnection attempts and results
        """

    @abstractmethod
    def is_connected(self) -> bool:
        """Check if the database connection is open
        Note: Implementations should log connection status checks
        """

    @abstractmethod
    async def get_schemas(self) -> Dict[str, TableSchema]:
        """
        Get the complete database schema
        Note: Implementations should log schema retrieval operations

        Returns:
            Dict[str, TableSchema]: Dictionary mapping table names to their schemas
        """

    @abstractmethod
    async def create_table(self, schema: TableSchema) -> None:
        """
        Create a new table in the database
        Note: Implementations should log table creation operations

        Args:
            schema (TableSchema): Schema definition for the table
        """

    @abstractmethod
    async def insert(self, table: str, data: Dict[str, Any]) -> Any:
        """
        Insert a record into the specified table
        Note: Implementations should log insert operations with table name and data size

        Args:
            table (str): Name of the table to insert into
            data (Dict[str, Any]): Dictionary containing column names and values

        Returns:
            Any: ID of the inserted record
        """

    @abstractmethod
    async def get(self, query: SelectQuery) -> List[Dict[str, Any]]:
        """
        Get records from the database
        Note: Implementations should log query operations with table name and result count

        Args:
            query (SelectQuery): Query definition containing table name, conditions, ordering, etc.

        Returns:
            List[Dict[str, Any]]: List of dictionaries containing the selected records
        """

    @abstractmethod
    async def update(self, query: UpdateQuery) -> int:
        """
        Update records in the database
        Note: Implementations should log update operations with table name and affected row count

        Args:
            query (UpdateQuery): Query definition containing table name, conditions, and data to update

        Returns:
            int: Number of affected rows
        """

    @abstractmethod
    async def delete(self, query: DeleteQuery) -> int:
        """
        Delete records from the database
        Note: Implementations should log delete operations with table name and affected row count

        Args:
            query (DeleteQuery): Query definition containing table name and conditions

        Returns:
            int: Number of affected rows
        """


__all__ = [
    "Database"
]
