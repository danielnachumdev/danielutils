import random
from typing import Any, Optional
from time import sleep
from ..database import Database
from ..database.database import K, V


class InMemoryDatabase(Database):
    """
    A wrapper over `dict` to conform to the `Database` interface.
    """

    def _on_notify(self, updater: 'Database', obj: Any) -> None:
        assert False

    def __init__(self) -> None:
        super().__init__()
        self._db: dict = {}

    def get(self, key: K, default: Any = Database.DEFAULT) -> Optional[V]:
        return self._db.get(key, default)

    def set(self, key: K, value: V) -> None:
        self._db[key] = value

    def delete(self, key: K) -> None:
        self._db.pop(key)

    def contains(self, key: K) -> bool:
        return key in self._db


class MockDatabase(InMemoryDatabase):
    """
    A mock database implementation that allows to add a random simulated delay for calls
    """

    def __init__(self, min_delay: float = 0, max_delay: float = 0) -> None:
        super().__init__()
        if not (0 <= min_delay <= max_delay):  # pylint: disable=superfluous-parens
            raise ValueError("min_delay must be smaller than max_delay and they must be non-negative")
        self._min_delay = min_delay
        self._max_delay = max_delay

    def _sleep(self) -> None:
        if self._min_delay == self._max_delay == 0:
            return
        sleep(random.uniform(self._min_delay, self._max_delay))

    def get(self, key: K, default: Any = Database.DEFAULT) -> Optional[V]:
        self._sleep()
        return super().get(key, default)

    def set(self, key: K, value: V) -> None:
        self._sleep()
        super().set(key, value)

    def delete(self, key: K) -> None:
        self._sleep()
        super().delete(key)

    def contains(self, key: K) -> bool:
        self._sleep()
        return super().contains(key)


__all__ = [
    "InMemoryDatabase",
    'MockDatabase',
]
