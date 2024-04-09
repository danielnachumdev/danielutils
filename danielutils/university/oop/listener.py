from abc import ABC, abstractmethod


class Listener(ABC):
    @abstractmethod
    def notify(self): ...


__all__=[
    "Listener"
]