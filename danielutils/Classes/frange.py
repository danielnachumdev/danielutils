from typing import Iterable, Callable


class frange:
    def __init__(self, start: float, stop: float = None, step: float = 1, round_method: Callable[[float], float] = lambda f: round(f, 3)):
        if stop is None:
            stop = start
            start = 0
        self.start = start
        self.stop = stop
        self.step = step
        self.method = round_method

    def __iter__(self) -> Iterable:
        if self.stop < self.start:
            return
        if self.start > self.stop:
            return
        if abs(self.stop-self.start) < abs(self.step):
            return
        if self.stop > 0 and self.step < 0:
            return
        if self.stop < 0 and self.step > 0:
            return
        cur = self.start
        while cur < self.stop:
            yield self.method(cur)
            cur += self.step


__all__ = [
    "frange"
]