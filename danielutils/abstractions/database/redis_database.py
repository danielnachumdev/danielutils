from typing import Any, Optional, TypeVar

try:
    import redis
except ImportError:
    from ...mock_ import MockImportObject

    redis = MockImportObject("`redis` is not installed")
from .database import Database

K = TypeVar('K')
V = TypeVar('V')


class RedisDatabase(Database[K, V]):
    """
    An implementation of the `Database` interface using Redis.
    """

    def __init__(self) -> None:
        super().__init__()
        self._db = redis.StrictRedis(host='localhost', port=6379, db=0)

    def _on_notify(self, updater: 'Database', obj: Any) -> None:
        pass

    def get(self, key: K, default: Any = Database.DEFAULT) -> Optional[V]:
        if key not in self:
            return default
        return self._db.get(key)

    def set(self, key: K, value: V) -> None:
        self._db.set(key, value)

    def delete(self, key: K) -> None:
        self._db.delete(key)

    def contains(self, key: K) -> bool:
        return self._db.exists(key)


__all__ = [
    "RedisDatabase"
]
