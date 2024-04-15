from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

EventType = TypeVar('EventType')


class Publisher(Generic[EventType]):
    def __init__(self):
        self._subscribers: set[Subscriber[EventType]] = set()

    def register(self, subscriber: 'Subscriber') -> None:
        self._subscribers.add(subscriber)

    def unregister(self, subscriber: 'Subscriber') -> None:
        self._subscribers.remove(subscriber)

    def notify(self, event: EventType) -> None:
        for subscriber in self._subscribers:
            subscriber.update(self, event)


class Subscriber(Generic[EventType], ABC):

    @abstractmethod
    def update(self, updater: 'Publisher', event: EventType) -> None: ...


__all__ = [
    "Publisher",
    "Subscriber",
]
