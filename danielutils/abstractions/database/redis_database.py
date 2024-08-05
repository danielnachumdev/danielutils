from typing import Any, Optional, TypeVar

from danielutils import serialize, deserialize

try:
    import redis
except ImportError:
    from ...mock_ import MockImportObject

    redis = MockImportObject("`redis` is not installed")  # type:ignore
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
        return deserialize(self._db.get(serialize(key)))  # type: ignore

    def set(self, key: K, value: V) -> None:
        self._db.set(serialize(key), serialize(value))

    def delete(self, key: K) -> None:
        self._db.delete(serialize(key))

    def contains(self, key: K) -> bool:
        return bool(self._db.exists(serialize(key)))


__all__ = [
    "RedisDatabase"
]
