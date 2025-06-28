import json
from typing import Dict, Any, List, Optional, Literal, Union
from enum import Enum
from datetime import datetime, date, time
from uuid import UUID

try:
    from pydantic import BaseModel, Field, ConfigDict
except ImportError:
    BaseModel = type("BaseModel", (object,), {})
    Field = lambda **kwargs: kwargs
    ConfigDict = lambda **kwargs: kwargs


class ColumnType(str, Enum):
    """SQL column types"""
    INTEGER = "INTEGER"
    AUTOINCREMENT = "AUTOINCREMENT"
    SMALLINT = "SMALLINT"
    MEDIUMINT = "MEDIUMINT"
    TINYINT = "TINYINT"
    BIGINT = "BIGINT"
    FLOAT = "FLOAT"
    DOUBLE = "DOUBLE"
    DECIMAL = "DECIMAL"
    BOOLEAN = "BOOLEAN"
    TEXT = "TEXT"
    VARCHAR = "VARCHAR"
    CHAR = "CHAR"
    DATE = "DATE"
    TIME = "TIME"
    DATETIME = "DATETIME"
    TIMESTAMP = "TIMESTAMP"
    BLOB = "BLOB"
    JSON = "JSON"
    UUID = "UUID"


class BaseDBModel(BaseModel):
    """Base model with JSON serialization support"""
    model_config = ConfigDict(
        json_encoders={
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat(),
            time: lambda v: v.isoformat(),
            UUID: lambda v: str(v),
            Enum: lambda v: v.value
        },
        arbitrary_types_allowed=True
    )

    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return self.model_dump()

    def to_json(self) -> str:
        """Convert model to JSON string"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> 'BaseDBModel':
        """Create model instance from JSON string"""
        data = json.loads(json_str)
        return cls.model_validate(data)


class TableColumn(BaseDBModel):
    """Represents a database column definition"""
    name: str
    type: ColumnType
    nullable: bool = True
    primary_key: bool = False
    unique: bool = False
    default: Any = None
    foreign_key: Optional[Dict[str, str]] = None


class TableIndex(BaseDBModel):
    """Represents a database index definition"""
    name: str
    columns: List[str]
    unique: bool = False


class TableForeignKey(BaseDBModel):
    """Represents a foreign key constraint"""
    name: str
    columns: List[str]
    reference_table: str
    reference_columns: List[str]
    on_delete: Optional[str] = None
    on_update: Optional[str] = None


class TableSchema(BaseDBModel):
    """Represents a complete table schema"""
    name: str
    columns: List[TableColumn]
    indexes: List[TableIndex] = Field(default_factory=list)
    foreign_keys: List[TableForeignKey] = Field(default_factory=list)


class Operator(str, Enum):
    """SQL comparison operators"""
    EQ = "="
    NEQ = "!="
    GT = ">"
    GTE = ">="
    LT = "<"
    LTE = "<="
    LIKE = "LIKE"  # Not supported in InMemoryDatabase
    ILIKE = "ILIKE"  # Not supported in InMemoryDatabase
    CONTAINS = "CONTAINS"  # Case-insensitive contains
    CONTAINS_CS = "CONTAINS_CS"  # Case-sensitive contains
    IN = "IN"
    NOT_IN = "NOT IN"
    IS_NULL = "IS NULL"
    IS_NOT_NULL = "IS NOT NULL"
    AND = "AND"
    OR = "OR"


class JoinType(str, Enum):
    """SQL join types"""
    INNER = "INNER JOIN"
    LEFT = "LEFT JOIN"
    RIGHT = "RIGHT JOIN"
    FULL = "FULL JOIN"


class OrderDirection(str, Enum):
    """SQL order directions"""
    ASC = "ASC"
    DESC = "DESC"


class Condition(BaseDBModel):
    """A single SQL condition"""
    column: str
    operator: Operator
    value: Optional[Any] = None
    values: Optional[List[Any]] = None  # For IN/NOT IN operators


class Join(BaseDBModel):
    """SQL join definition"""
    type: JoinType
    table: str
    conditions: List[Condition]


class OrderBy(BaseDBModel):
    """SQL ORDER BY clause"""
    column: str
    direction: OrderDirection = OrderDirection.ASC


class WhereClause(BaseDBModel):
    """SQL WHERE clause with conditions"""
    conditions: List[Condition]
    operator: Literal["AND", "OR"] = "AND"


class SelectQuery(BaseDBModel):
    """Complete SELECT query definition"""
    table: str
    columns: Optional[List[str]] = None
    where: Optional[WhereClause] = None
    joins: Optional[List[Join]] = None
    order_by: Optional[List[OrderBy]] = None
    group_by: Optional[List[str]] = None
    having: Optional[WhereClause] = None
    limit: Optional[int] = None
    offset: Optional[int] = None


class UpdateQuery(BaseDBModel):
    """Complete UPDATE query definition"""
    table: str
    data: Dict[str, Any]
    where: Optional[WhereClause] = None


class DeleteQuery(BaseDBModel):
    """Complete DELETE query definition"""
    table: str
    where: Optional[WhereClause] = None


# Helper functions for JSON serialization
def serialize_to_json(obj: Union[BaseDBModel, List[BaseDBModel], Dict[str, Any]]) -> str:
    """Serialize any supported object to JSON string"""
    if isinstance(obj, BaseDBModel):
        return obj.to_json()
    elif isinstance(obj, list):
        return json.dumps([item.to_dict() if isinstance(item, BaseDBModel) else item for item in obj])
    elif isinstance(obj, dict):
        return json.dumps({k: v.to_dict() if isinstance(v, BaseDBModel) else v for k, v in obj.items()})
    return json.dumps(obj)


def deserialize_from_json(json_str: str, model_class: type[BaseDBModel]) -> Union[BaseDBModel, List[BaseDBModel]]:
    """Deserialize JSON string to model instance(s)"""
    data = json.loads(json_str)
    if isinstance(data, list):
        return [model_class.model_validate(item) for item in data]
    return model_class.model_validate(data)


__all__ = [
    "ColumnType",
    "TableColumn",
    "TableIndex",
    "TableForeignKey",
    "TableSchema",
    "Operator",
    "JoinType",
    "OrderDirection",
    "Condition",
    "Join",
    "OrderBy",
    "WhereClause",
    "SelectQuery",
    "UpdateQuery",
    "DeleteQuery",
    "serialize_to_json",
    "deserialize_from_json"
]
