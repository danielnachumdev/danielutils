import logging
from typing import Dict, Any, List, Optional

try:
    from sqlalchemy import create_engine, MetaData, Table, Column, inspect, text, select, update, delete, Engine
    from sqlalchemy.orm import sessionmaker, Session
    from sqlalchemy.sql import or_
    from sqlalchemy.types import Integer, String, DateTime, Boolean, Float, JSON, LargeBinary
except ImportError:
    from ....mock_ import MockImportObject

    create_engine = MockImportObject("'sqlalchemy' is not installed")  # type:ignore
    MetaData = MockImportObject("'sqlalchemy' is not installed")  # type:ignore
    Table = MockImportObject("'sqlalchemy' is not installed")  # type:ignore
    Column = MockImportObject("'sqlalchemy' is not installed")  # type:ignore
    inspect = MockImportObject("'sqlalchemy' is not installed")  # type:ignore
    text = MockImportObject("'sqlalchemy' is not installed")  # type:ignore
    select = MockImportObject("'sqlalchemy' is not installed")  # type:ignore
    update = MockImportObject("'sqlalchemy' is not installed")  # type:ignore
    delete = MockImportObject("'sqlalchemy' is not installed")  # type:ignore
    Engine = MockImportObject("'sqlalchemy' is not installed")  # type:ignore
    sessionmaker = MockImportObject("'sqlalchemy' is not installed")  # type:ignore
    Session = MockImportObject("'sqlalchemy' is not installed")  # type:ignore
    or_ = MockImportObject("'sqlalchemy' is not installed")  # type:ignore
    Integer = MockImportObject("'sqlalchemy' is not installed")  # type:ignore
    String = MockImportObject("'sqlalchemy' is not installed")  # type:ignore
    DateTime = MockImportObject("'sqlalchemy' is not installed")  # type:ignore
    Boolean = MockImportObject("'sqlalchemy' is not installed")  # type:ignore
    Float = MockImportObject("'sqlalchemy' is not installed")  # type:ignore
    JSON = MockImportObject("'sqlalchemy' is not installed")  # type:ignore
    LargeBinary = MockImportObject("'sqlalchemy' is not installed")  # type:ignore

import os
from ..database import Database
from ..database_definitions import (
    TableColumn, TableSchema, TableIndex, TableForeignKey,
    SelectQuery, UpdateQuery, DeleteQuery, Operator, OrderDirection,
    ColumnType
)
from ..database_exceptions import DBException, DBValidationError, DBQueryError, DBConnectionError


class SQLiteDatabase(Database):
    """SQLite implementation of the Database abstract class using SQLAlchemy"""

    @classmethod
    def _default_class_exception_conversion(cls, e: Exception) -> Exception:
        """
        Convert SQLite/SQLAlchemy specific exceptions to standard database exceptions.
        """
        if 'sqlalchemy' in str(type(e).__module__):
            if 'OperationalError' in str(type(e)):
                return DBConnectionError(f"Database connection error: {str(e)}", e)
            elif 'IntegrityError' in str(type(e)):
                return DBValidationError(f"Data validation error: {str(e)}", e)
            elif 'ProgrammingError' in str(type(e)):
                return DBQueryError(f"Query error: {str(e)}", e)
        return DBException(f"Database error: {str(e)}", e)

    def __init__(
            self,
            url: Optional[str] = None,
            db_name: Optional[str] = None,
            **engine_kwargs
    ):
        """
        Initialize SQLite database connection
        Args:
            url (str, optional): SQLAlchemy database URL. If not provided, will use db_name or environment/config.
            db_name (str, optional): Database file name. Used only if url is not provided.
            **engine_kwargs: Additional keyword arguments for SQLAlchemy create_engine.
        """
        self.engine: Optional[Engine] = None
        self.SessionLocal = None
        self.metadata = MetaData()
        # Determine the connection URL
        if url:
            self.url = url
        elif db_name:
            self.url = f"sqlite:///{db_name}"
        else:
            # Try environment variable, then fallback
            self.url = os.environ.get(
                "SQLALCHEMY_DATABASE_URI", "sqlite:///:memory:")
        self.engine_kwargs = engine_kwargs
        self.connect()

    async def connect(self) -> None:
        """Establish connection to SQLite database"""
        try:
            self.engine = create_engine(
                self.url, pool_pre_ping=True, **self.engine_kwargs)
            self.SessionLocal = sessionmaker(
                autocommit=False, autoflush=False, bind=self.engine)
            self.metadata.reflect(bind=self.engine)
            logging.info(f"Connected to SQLite database at '{self.url}'")
        except Exception as e:
            logging.error(
                f"Error connecting to SQLite database at '{self.url}': {e}")
            raise

    async def disconnect(self) -> None:
        """Close the SQLite database connection"""
        if self.engine:
            self.engine.dispose()
            logging.info("Disconnected from SQLite database")

    def _get_column_type(self, sqlalchemy_type: Any) -> ColumnType:
        """Convert SQLAlchemy type to ColumnType enum"""
        type_str = str(sqlalchemy_type).upper()

        # Map SQLAlchemy types to ColumnType
        type_map = {
            'INTEGER': ColumnType.INTEGER,
            'BIGINT': ColumnType.BIGINT,
            'SMALLINT': ColumnType.SMALLINT,
            'FLOAT': ColumnType.FLOAT,
            'DOUBLE': ColumnType.DOUBLE,
            'DECIMAL': ColumnType.DECIMAL,
            'BOOLEAN': ColumnType.BOOLEAN,
            'TEXT': ColumnType.TEXT,
            'VARCHAR': ColumnType.VARCHAR,
            'CHAR': ColumnType.CHAR,
            'DATE': ColumnType.DATE,
            'TIME': ColumnType.TIME,
            'DATETIME': ColumnType.DATETIME,
            'TIMESTAMP': ColumnType.TIMESTAMP,
            'BLOB': ColumnType.BLOB,
            'JSON': ColumnType.JSON,
            'UUID': ColumnType.UUID
        }

        # Handle special cases
        if 'AUTOINCREMENT' in type_str:
            return ColumnType.AUTOINCREMENT
        if 'VARCHAR' in type_str:
            return ColumnType.VARCHAR
        if 'CHAR' in type_str:
            return ColumnType.CHAR

        # Try to find a match in the type map
        for sql_type, column_type in type_map.items():
            if sql_type in type_str:
                return column_type

        raise ValueError(f"Unsupported SQLAlchemy type: {type_str}")

    async def get_schemas(self) -> Dict[str, TableSchema]:
        """
        Get the complete database schema

        Returns:
            Dict[str, TableSchema]: Dictionary mapping table names to their schemas
        """
        if not self.engine:
            raise RuntimeError("Database not connected")

        inspector = inspect(self.engine)
        schemas = {}

        for table_name in inspector.get_table_names():
            # Get all indexes first to check for unique constraints
            indexes = inspector.get_indexes(table_name)
            unique_columns = set()
            for idx in indexes:
                if idx['unique'] and len(idx['column_names']) == 1:
                    unique_columns.add(idx['column_names'][0])

            columns = []
            for col in self.metadata.tables[table_name].columns:
                # Convert SQLAlchemy type to ColumnType
                try:
                    column_type = self._get_column_type(col.type)
                except ValueError as e:
                    logging.warning(
                        f"Could not map type for column {col['name']} in table {table_name}: {e}")
                    continue

                # Handle default values
                default = col.default
                if default is not None and hasattr(default, 'arg'):
                    default = default.arg

                # Check if column is unique (either by constraint or index)
                is_unique = getattr(col, "unique", False) or col.name in unique_columns

                column = TableColumn(
                    name=col.name,
                    type=column_type,
                    nullable=col.nullable,
                    primary_key=col.primary_key,
                    unique=is_unique,
                    default=default
                )
                columns.append(column)

            # Get indexes (excluding single-column unique indexes as they're handled above)
            table_indexes = []
            for idx in indexes:
                if not (idx['unique'] and len(idx['column_names']) == 1):
                    table_indexes.append(TableIndex(
                        name=idx['name'],
                        columns=idx['column_names'],
                        unique=idx['unique']
                    ))

            # Get foreign keys
            foreign_keys = []
            for fk in inspector.get_foreign_keys(table_name):
                foreign_keys.append(TableForeignKey(
                    name=fk.get(
                        'name', f"fk_{table_name}_{fk['constrained_columns'][0]}"),
                    columns=fk['constrained_columns'],
                    reference_table=fk['referred_table'],
                    reference_columns=fk['referred_columns']
                ))

            schemas[table_name] = TableSchema(
                name=table_name,
                columns=columns,
                indexes=table_indexes,
                foreign_keys=foreign_keys
            )

        return schemas

    def _get_sqlalchemy_type(self, column_type: ColumnType) -> Any:
        """Convert ColumnType to SQLAlchemy type"""
        type_map = {
            ColumnType.INTEGER: Integer,
            ColumnType.AUTOINCREMENT: Integer,
            ColumnType.SMALLINT: Integer,
            ColumnType.MEDIUMINT: Integer,
            ColumnType.TINYINT: Integer,
            ColumnType.BIGINT: Integer,
            ColumnType.FLOAT: Float,
            ColumnType.DOUBLE: Float,
            ColumnType.DECIMAL: Float,
            ColumnType.BOOLEAN: Boolean,
            ColumnType.TEXT: String,
            ColumnType.VARCHAR: String,
            ColumnType.CHAR: String,
            ColumnType.DATE: DateTime,
            ColumnType.TIME: DateTime,
            ColumnType.DATETIME: DateTime,
            ColumnType.TIMESTAMP: DateTime,
            ColumnType.BLOB: LargeBinary,
            ColumnType.JSON: JSON,
            ColumnType.UUID: String
        }
        return type_map.get(column_type)

    async def create_table(self, schema: TableSchema) -> None:
        """
        Create a new table in the SQLite database

        Args:
            schema (TableSchema): Schema definition for the table
        """
        try:
            columns = []
            for column in schema.columns:
                # Convert ColumnType to SQLAlchemy type
                sql_type = self._get_sqlalchemy_type(column.type)
                if sql_type is None:
                    raise ValueError(f"Unsupported column type: {column.type}")

                # Create column with all properties
                col = Column(
                    column.name,
                    sql_type,
                    nullable=column.nullable,
                    primary_key=column.primary_key,
                    unique=column.unique,
                    default=column.default
                )
                columns.append(col)

            # Create table with all columns
            table = Table(schema.name, self.metadata, *columns)
            table.create(self.engine)
            logging.info(f"Created table: '{schema.name}'")
        except Exception as e:
            logging.error(f"Error creating table '{schema.name}': {e}")
            raise

    def _get_session(self) -> Session:
        """Get a new database session"""
        return self.SessionLocal()

    async def insert(self, table: str, data: Dict[str, Any]) -> int:
        """
        Insert a record into the specified table

        Args:
            table (str): Name of the table
            data (Dict[str, Any]): Dictionary containing column names and values

        Returns:
            int: ID of the inserted record
        """
        try:
            with self._get_session() as session:
                table_obj = self.metadata.tables[table]
                stmt = table_obj.insert().values(**data)
                result = session.execute(stmt)
                session.commit()
                return result.inserted_primary_key[0]
        except Exception as e:
            logging.error(f"Error inserting into '{table}': {e}")
            raise

    async def get(self, query: SelectQuery) -> List[Dict[str, Any]]:
        """
        Get records from the database

        Args:
            query (SelectQuery): Query definition containing table name, conditions, ordering, etc.

        Returns:
            List[Dict[str, Any]]: List of dictionaries containing the selected records
        """
        try:
            with self._get_session() as session:
                table_obj = self.metadata.tables[query.table]

                # Start with base select
                if query.columns:
                    stmt = select(*[table_obj.c[col] for col in query.columns])
                else:
                    stmt = select(table_obj)

                # Apply joins
                if query.joins:
                    for join in query.joins:
                        join_table = self.metadata.tables[join.table]
                        join_conditions = []
                        for condition in join.conditions:
                            left_col = table_obj.c[condition.column]
                            right_col = join_table.c[condition.value]
                            join_conditions.append(left_col == right_col)
                        stmt = stmt.join(join_table, *join_conditions)

                # Apply where clause
                if query.where:
                    where_conditions = []
                    for condition in query.where.conditions:
                        col = table_obj.c[condition.column]
                        if condition.operator == Operator.EQ:
                            where_conditions.append(col == condition.value)
                        elif condition.operator == Operator.NEQ:
                            where_conditions.append(col != condition.value)
                        elif condition.operator == Operator.GT:
                            where_conditions.append(col > condition.value)
                        elif condition.operator == Operator.GTE:
                            where_conditions.append(col >= condition.value)
                        elif condition.operator == Operator.LT:
                            where_conditions.append(col < condition.value)
                        elif condition.operator == Operator.LTE:
                            where_conditions.append(col <= condition.value)
                        elif condition.operator == Operator.LIKE:
                            where_conditions.append(col.like(condition.value))
                        elif condition.operator == Operator.ILIKE:
                            where_conditions.append(col.ilike(condition.value))
                        elif condition.operator == Operator.IN:
                            where_conditions.append(col.in_(condition.values))
                        elif condition.operator == Operator.NOT_IN:
                            where_conditions.append(~col.in_(condition.values))
                        elif condition.operator == Operator.IS_NULL:
                            where_conditions.append(col.is_(None))
                        elif condition.operator == Operator.IS_NOT_NULL:
                            where_conditions.append(col.is_not(None))

                    if query.where.operator == "AND":
                        stmt = stmt.where(*where_conditions)
                    else:  # OR
                        stmt = stmt.where(or_(*where_conditions))

                # Apply order by
                if query.order_by:
                    for order in query.order_by:
                        col = table_obj.c[order.column]
                        if order.direction == OrderDirection.DESC:
                            col = col.desc()
                        stmt = stmt.order_by(col)

                # Apply group by
                if query.group_by:
                    stmt = stmt.group_by(*[table_obj.c[col]
                                           for col in query.group_by])

                # Apply having
                if query.having:
                    having_conditions = []
                    for condition in query.having.conditions:
                        col = table_obj.c[condition.column]
                        if condition.operator == Operator.EQ:
                            having_conditions.append(col == condition.value)
                        # ... (similar to where conditions)
                    if query.having.operator == "AND":
                        stmt = stmt.having(*having_conditions)
                    else:  # OR
                        stmt = stmt.having(or_(*having_conditions))

                # Apply limit and offset
                if query.limit is not None:
                    stmt = stmt.limit(query.limit)
                if query.offset is not None:
                    stmt = stmt.offset(query.offset)

                result = session.execute(stmt)
                # Convert result rows to dictionaries
                return [dict(zip(result.keys(), row)) for row in result]
        except Exception as e:
            logging.error(f"Error selecting from '{query.table}': {e}")
            raise

    async def update(self, query: UpdateQuery) -> int:
        """
        Update records in the database

        Args:
            query (UpdateQuery): Query definition containing table name, conditions, and data to update

        Returns:
            int: Number of affected rows
        """
        try:
            with self._get_session() as session:
                table_obj = self.metadata.tables[query.table]
                stmt = update(table_obj).values(**query.data)

                if query.where:
                    where_conditions = []
                    for condition in query.where.conditions:
                        col = table_obj.c[condition.column]
                        if condition.operator == Operator.EQ:
                            where_conditions.append(col == condition.value)
                        # ... (similar to get method where conditions)
                    if query.where.operator == "AND":
                        stmt = stmt.where(*where_conditions)
                    else:  # OR
                        stmt = stmt.where(or_(*where_conditions))

                result = session.execute(stmt)
                session.commit()
                return result.rowcount
        except Exception as e:
            logging.error(f"Error updating '{query.table}': {e}")
            raise

    async def delete(self, query: DeleteQuery) -> int:
        """
        Delete records from the database

        Args:
            query (DeleteQuery): Query definition containing table name and conditions

        Returns:
            int: Number of affected rows
        """
        try:
            with self._get_session() as session:
                table_obj = self.metadata.tables[query.table]
                stmt = delete(table_obj)

                if query.where:
                    where_conditions = []
                    for condition in query.where.conditions:
                        col = table_obj.c[condition.column]
                        if condition.operator == Operator.EQ:
                            where_conditions.append(col == condition.value)
                        # ... (similar to get method where conditions)
                    if query.where.operator == "AND":
                        stmt = stmt.where(*where_conditions)
                    else:  # OR
                        stmt = stmt.where(or_(*where_conditions))

                result = session.execute(stmt)
                session.commit()
                return result.rowcount
        except Exception as e:
            logging.error(f"Error deleting from '{query.table}': {e}")
            raise


__all__ = [
    "SQLiteDatabase"
]
