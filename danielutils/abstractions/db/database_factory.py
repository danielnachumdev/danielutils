from abc import ABC, abstractmethod
import logging
from typing import Literal, Dict, Any, Optional, Tuple
from .database import Database
from .implementations import InMemoryDatabase, SQLiteDatabase, PersistentInMemoryDatabase, RedisDatabase
from ...logging_.utils import get_logger
logger = get_logger(__name__)

MAPPING = {
    "sqlite": SQLiteDatabase,
    "memory": InMemoryDatabase,
    "persistent_memory": PersistentInMemoryDatabase,
    "redis": RedisDatabase
}


class DatabaseFactory(ABC):
    """Factory class for creating database instances"""

    _instances: Dict[str, Database] = {}

    @classmethod
    def get_database(
            cls,
            db_type: Literal["sqlite", "memory", "persistent_memory", "redis"] = "persistent_memory",
            db_args: Optional[Tuple[Any, ...]] = None,
            db_kwargs: Optional[Dict[str, Any]] = None
    ) -> Database:
        """
        Get a database instance based on the specified type. Returns existing instance if available.

        Args:
            db_args (Optional[Tuple[Any, ...]]): Positional arguments for database initialization
            db_type (str): Type of database to create (default: "persistent_memory")
                Supported types: "sqlite", "memory", "persistent_memory"
            db_kwargs (Optional[Dict[str, Any]]): Keyword arguments for database initialization
        Returns:
            Database: Database instance
        """
        logger.debug(f"Requesting database instance: type={db_type}, args_count={len(db_args) if db_args else 0}, kwargs_count={len(db_kwargs) if db_kwargs else 0}")
        
        if db_type not in cls._instances:
            logger.info(f"Creating new database instance: {db_type}")
            if db_type not in MAPPING:
                logger.error(f"Unsupported database type requested: {db_type}")
                raise ValueError(f"Unsupported database type: '{db_type}'")

            # Convert None to empty tuple/dict for database initialization
            args = db_args or ()
            kwargs = db_kwargs or {}
            logger.debug(f"Initializing {db_type} database with args={args}, kwargs={kwargs}")
            cls._instances[db_type] = MAPPING[db_type](*args, **kwargs)
            logger.info(f"Database instance created successfully: {db_type}")
        else:
            logger.debug(f"Returning existing database instance: {db_type}")
        
        return cls._instances[db_type]

    @classmethod
    @abstractmethod
    def get_database_from_settings(cls) -> Database:
        """
        Get a database instance using the application settings.
        This is the preferred method for getting a database instance in the application.
        """


__all__ = [
    "DatabaseFactory"
]
