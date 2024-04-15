from typing import Any, Generic, TypeVar, Optional, TypeGuard

from .database import Database, K, V

I = TypeVar('I')
O = TypeVar('O')


class CachedDatabase(Database, Generic[I, O]):
    """
    A database that is composed of two types of databases.
    Args:
        primary (Database): is intended to be the "real" database which is usually slower than the `cache`
        cache (Database): is intended to be a cache layer over `primary` which will be faster when reading
        *
        notify_primary (bool): if a single Database instance is as `primary` for multiple CachedDatabase and the current CachedDatabase instance 'set' method is used, it will also update the cache on different CachedDatabase instances. Defaults to False
        notify_cache (bool): same as `notify_primary` but will update other primaries on different CachedDatabase instances
    Returns:
        None
    """

    def _on_notify(self, updater: 'Database', obj: Any) -> None:
        key, value = obj
        if self._cache is not updater:
            if not self._cache == updater:
                self._cache.set(key, value)

        if self._primary is not updater:
            if not self._primary == updater:
                self._primary.set(key, value)

    def __init__(self, primary: Database, cache: Database, *, notify_primary: bool = False, notify_cache: bool = False):
        super().__init__()
        primary._register_subscriber(self)
        cache._register_subscriber(self)
        self._primary = primary
        self._cache = cache
        self._notify_primary = notify_primary
        self._notify_cache = notify_cache

    def get(self, key: I, default: Any = Database.DEFAULT) -> Optional[O]:
        res = self._cache.get(key, default)
        if res is not default:
            return res
        res = self._primary.get(key, default)
        if res is not default:
            self._cache.set(key, res)
        return res

    def set(self, key: I, value: O) -> None:
        self._cache.set(key, value)
        if self._notify_cache:
            self._cache._notify_subscribers((key, value))
        self._primary.set(key, value)
        if self._notify_primary:
            self._primary._notify_subscribers((key, value))

    def delete(self, key: I) -> None:
        self._cache.delete(key)
        self._primary.delete(key)

    def contains(self, key: I) -> bool:
        if self._cache.contains(key):
            return True
        if (res := self.get(key)) is not Database.DEFAULT:
            self._cache.set(key, res)
            return True
        return False


__all__ = [
    "CachedDatabase"
]
