from .listener import Listener


class Sender:
    def __init__(self):
        self._listeners: set[Listener] = set()

    def subscribe(self, listener: Listener) -> None:
        self._listeners.add(listener)

    def notify_one(self):
        (l := self._listeners.pop()).notify()
        self.subscribe(l)

    def notify_all(self):
        for l in self._listeners:
            l.notify()


__all__ = [
    "Sender"
]
