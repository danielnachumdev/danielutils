from .database import Database
from .database_factory import DatabaseFactory


def get_db() -> Database:
    return DatabaseFactory.get_database_from_settings()
 