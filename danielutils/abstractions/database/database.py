from abc import ABC, abstractmethod
from typing import Any, TypeVar, Generic, Optional

K = TypeVar('K')
V = TypeVar('V')


class Database(ABC, Generic[K, V]):
    """
    Abstract base class for database objects.
    """
    DEFAULT = None

    def __init__(self) -> None:
        self._subscribers: set[Database] = set()

    def _register_subscriber(self, subscriber: 'Database') -> None:
        self._subscribers.add(subscriber)

    def _notify_subscribers(self, obj: Any) -> None:
        for subscriber in self._subscribers:
            subscriber._notify(self, obj)  # pylint: disable=protected-access

    def _notify(self, updater: 'Database', obj: Any) -> None:
        """
        Notify all subscribers of an object.
        Args:
            updater: the object calling this method.
            obj: the event to notify.

        Returns:
            None
        """
        self._on_notify(updater, obj)

    @abstractmethod
    def _on_notify(self, updater: 'Database', obj: Any) -> None:
        ...

    @abstractmethod
    def get(self, key: K, default: Any = DEFAULT) -> Optional[V]:
        """
        Get a value from the database by key.
        Args:
            key (K): The key to get the value from.:
            default (Any): The default value to return if the key is not found. Defaults to Database.DEFAULT.

        Returns:
            Optional[V]
        """

    @abstractmethod
    def set(self, key: K, value: V) -> None:
        """
        Set a value in the database.
        Args:
            key (K): The key to set.
            value (V): The value to set.

        Returns:
            None
        """

    @abstractmethod
    def delete(self, key: K) -> None:
        """
        Delete an item from the database.
        Args:
            key (K): The key to delete.:

        Returns:
            None
        """

    @abstractmethod
    def contains(self, key: K) -> bool:
        """
        Check if a key is contained in this database.
        Args:
            key (K): Key to be checked.:

        Returns:
            bool
        """

    def __getitem__(self, key: K) -> V:
        res = self.get(key)
        if res is Database.DEFAULT:
            raise KeyError(key)
        return res

    def __setitem__(self, key: K, value: V) -> None:
        self.set(key, value)

    def __delitem__(self, key: K) -> None:
        self.delete(key)

    def __contains__(self, key: K) -> bool:
        return self.contains(key)


__all__ = [
    "Database",
]
