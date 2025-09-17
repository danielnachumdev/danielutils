import logging
from abc import ABC, abstractmethod
from typing import Dict, Optional, Type, Any, Sequence
from ...logging_.utils import get_logger

try:
    from sqlalchemy import inspect, Column
    from sqlalchemy.orm import DeclarativeBase
except ImportError:
    from ...mock_ import MockImportObject

    inspect = MockImportObject("'sqlalchemy' is not installed")  # type:ignore
    Column = MockImportObject("'sqlalchemy' is not installed")  # type:ignore
    DeclarativeBase = type("DeclarativeBase", (object,), {})  # type:ignore

from .database import Database
from .database_definitions import ColumnType, TableSchema, TableColumn as ColumnSchema, TableIndex as IndexSchema
logger = get_logger(__name__)

TYPE_MAPPING = {
    'INTEGER': ColumnType.INTEGER,
    'BIGINT': ColumnType.INTEGER,
    'FLOAT': ColumnType.FLOAT,
    'NUMERIC': ColumnType.FLOAT,
    'DECIMAL': ColumnType.FLOAT,
    'BOOLEAN': ColumnType.BOOLEAN,
    'TEXT': ColumnType.TEXT,
    'VARCHAR': ColumnType.TEXT,
    'CHAR': ColumnType.TEXT,
    'UUID': ColumnType.TEXT,
    'DATETIME': ColumnType.DATETIME,
    'DATE': ColumnType.DATE,
    'TIME': ColumnType.TIME,
    'JSON': ColumnType.JSON,
    'BLOB': ColumnType.BLOB,
}


async def validate_schema(db: Database, table_name: str, expected_schema: TableSchema) -> bool:
    """
    Validate that the existing table schema matches the expected schema.

    Args:
        db: Database instance
        table_name: Name of the table to validate
        expected_schema: Expected table schema

    Returns:
        bool: True if schema matches, False otherwise
    """
    try:
        # Get existing schema
        existing_schemas = await db.get_schemas()
        if table_name not in existing_schemas:
            logger.warning(f"Table '{table_name}' does not exist")
            return False

        existing_schema = existing_schemas[table_name]

        # Compare columns
        if len(existing_schema.columns) != len(expected_schema.columns):
            logger.warning(
                f"Column count mismatch in '{table_name}': "
                f"expected {len(expected_schema.columns)}, "
                f"got {len(existing_schema.columns)}"
            )
            return False

        # Compare each column
        for expected_col, existing_col in zip(sorted(expected_schema.columns, key=lambda c: c.name),
                                              sorted(existing_schema.columns, key=lambda c: c.name)):
            if (
                    expected_col.name != existing_col.name or
                    expected_col.type != existing_col.type or
                    expected_col.primary_key != existing_col.primary_key or
                    expected_col.nullable != existing_col.nullable or
                    expected_col.unique != existing_col.unique or
                    expected_col.foreign_key != existing_col.foreign_key
            ):
                logger.warning(f"Column mismatch in '{table_name}': expected {expected_col}, got {existing_col}")
                return False

        # Compare indexes
        if len(existing_schema.indexes) != len(expected_schema.indexes):
            logger.warning(
                f"Index count mismatch in '{table_name}': "
                f"expected {len(expected_schema.indexes)}, "
                f"got {len(existing_schema.indexes)}"
            )
            return False

        # Compare each index
        for expected_idx, existing_idx in zip(sorted(expected_schema.indexes, key=lambda idx: idx.name),
                                              sorted(existing_schema.indexes, key=lambda idx: idx.name)):
            if (
                    expected_idx.name != existing_idx.name or
                    expected_idx.columns != existing_idx.columns or
                    expected_idx.unique != existing_idx.unique
            ):
                logger.warning(f"Index mismatch in '{table_name}': expected {expected_idx}, got {existing_idx}")
                return False

        return True

    except Exception as e:
        logger.error(f"Error validating schema for '{table_name}': {str(e)}")
        return False


def get_column_type(column: Column) -> ColumnType:
    """Convert SQLAlchemy column type to our ColumnType enum"""
    # Ensure autoincrement for integer primary key named 'id'
    if (
            column.name == 'id'
            and getattr(column, 'primary_key', False)
            and ('INTEGER' in str(column.type).upper() or 'BIGINT' in str(column.type).upper())
    ):
        return ColumnType.AUTOINCREMENT
    # Check for autoincrement attribute
    if getattr(column, 'autoincrement', False) == True:
        return ColumnType.AUTOINCREMENT
    # Then check the column type
    type_name = str(column.type).upper()
    for sql_type, our_type in TYPE_MAPPING.items():
        if sql_type in type_name:
            return our_type
    return ColumnType.TEXT  # Default to TEXT if type not found


def get_foreign_key(column: Column) -> Optional[Dict[str, str]]:
    """Extract foreign key information from a column"""
    for fk in column.foreign_keys:
        return {
            "table": fk.column.table.name,
            "column": fk.column.name
        }
    return None


def get_default_value(column: Column) -> Optional[Any]:
    """Extract default value from a column"""
    if column.default is not None:
        if hasattr(column.default, 'arg'):
            return column.default.arg
        return column.default
    return None


def model_to_schema(model_class: Type[DeclarativeBase]) -> TableSchema:
    """Convert a SQLAlchemy model to our TableSchema"""
    mapper = inspect(model_class)
    table_name = mapper.local_table.name  # type: ignore

    # Convert columns
    columns = []
    for column in mapper.columns:
        # Get unique constraint from column
        is_unique = False
        if column.unique:
            is_unique = True
        elif column.index and column.index.unique:  # type: ignore
            is_unique = True

        col_schema = ColumnSchema(
            name=column.name,
            type=get_column_type(column),
            primary_key=column.primary_key,
            nullable=column.nullable,  # type: ignore
            unique=is_unique,
            foreign_key=get_foreign_key(column),
            default=get_default_value(column)
        )
        columns.append(col_schema)

    # Convert indexes
    indexes = []
    for index in mapper.local_table.indexes:  # type: ignore
        # Skip indexes that are already handled by unique constraints
        if len(index.columns) == 1 and index.columns[0].unique:
            continue

        idx_schema = IndexSchema(
            name=index.name,
            columns=[col.name for col in index.columns],
            unique=index.unique
        )
        indexes.append(idx_schema)

    return TableSchema(
        name=table_name,
        columns=columns,
        indexes=indexes
    )


class DatabaseInitializer(ABC):
    # Map SQLAlchemy types to our ColumnType enum

    @classmethod
    @abstractmethod
    def _get_models(cls) -> Sequence[Type[DeclarativeBase]]:
        """Get all pydantic models from our models"""

    @classmethod
    def _get_table_schemas(cls) -> Dict[str, TableSchema]:
        """Get all table schemas from our models"""
        models = cls._get_models()
        res = {}
        for model in models:
            try:
                res[model.__tablename__] = model_to_schema(model)
            except Exception as e:
                raise Exception(f"Failed parsing '{model.__tablename__}'") from e
        return res

    @classmethod
    async def init_db(cls, db: Database) -> None:
        """
        Initialize the database by creating or validating all required tables.

        Args:
            db: Database instance to initialize
        """
        try:
            await db.connect()

            # Get existing schemas
            existing_schemas = await db.get_schemas()

            # Get table schemas from models
            table_schemas = cls._get_table_schemas()

            # Create or validate each table
            for table_name, expected_schema in table_schemas.items():
                if table_name not in existing_schemas:
                    logger.info(f"Creating table '{table_name}'")
                    await db.create_table(expected_schema)
                else:
                    logger.info(f"Validating table '{table_name}'")
                    if not await validate_schema(db, table_name, expected_schema):
                        raise ValueError(
                            f"Schema validation failed for table '{table_name}'. "
                            "Please check the logs for details."
                        )

            logger.info("Database initialization completed successfully")

        except Exception as e:
            logger.error(f"Error initializing database: {str(e)}")
            raise


__all__ = [
    "DatabaseInitializer"
]
