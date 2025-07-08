import functools
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Callable, TypeVar, cast, Optional, Set
from .database_exceptions import DBException
from .database_definitions import TableSchema, SelectQuery, UpdateQuery, DeleteQuery

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
            try:
                return await db_method(self, *args, **kwargs)
            except DBException:
                raise
            except Exception as e:
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
        for name, method in cls.__dict__.items():
            if (
                    callable(method) and
                    not name.startswith('_') and
                    not isinstance(method, (classmethod, staticmethod))
                    and name in cls._get_functions_with_auto_converted_exceptions()
            ):
                setattr(cls, name, cls._wrap_db_exceptions(method))

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
        return DBException(f"Database error: {str(e)}")

    async def __aenter__(self) -> 'Database':
        """
        Context manager entry point. Connects to the database.

        Returns:
            Database: The database instance for use in the context
        """
        await self.connect()
        return self

    async def __aexit__(self, exc_type: Optional[type], exc_val: Optional[Exception], exc_tb: Optional[Any]) -> None:
        """
        Context manager exit point. Disconnects from the database.

        Args:
            exc_type: The type of exception that was raised, if any
            exc_val: The exception instance that was raised, if any
            exc_tb: The traceback for the exception, if any
        """
        await self.disconnect()

    @abstractmethod
    async def connect(self) -> None:
        """Establish connection to the database"""

    @abstractmethod
    async def disconnect(self) -> None:
        """Close the database connection"""

    @abstractmethod
    async def get_schemas(self) -> Dict[str, TableSchema]:
        """
        Get the complete database schema

        Returns:
            Dict[str, TableSchema]: Dictionary mapping table names to their schemas
        """

    @abstractmethod
    async def create_table(self, schema: TableSchema) -> None:
        """
        Create a new table in the database

        Args:
            schema (TableSchema): Schema definition for the table
        """

    @abstractmethod
    async def insert(self, table: str, data: Dict[str, Any]) -> Any:
        """
        Insert a record into the specified table

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

        Args:
            query (SelectQuery): Query definition containing table name, conditions, ordering, etc.

        Returns:
            List[Dict[str, Any]]: List of dictionaries containing the selected records
        """

    @abstractmethod
    async def update(self, query: UpdateQuery) -> int:
        """
        Update records in the database

        Args:
            query (UpdateQuery): Query definition containing table name, conditions, and data to update

        Returns:
            int: Number of affected rows
        """

    @abstractmethod
    async def delete(self, query: DeleteQuery) -> int:
        """
        Delete records from the database

        Args:
            query (DeleteQuery): Query definition containing table name and conditions

        Returns:
            int: Number of affected rows
        """


__all__ = [
    "Database"
]
