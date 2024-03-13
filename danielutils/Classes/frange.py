from typing import Iterable, Callable, Optional


class frange:
    """this class is the same like builtin range but with float values
    """

    def __init__(self, start: float, stop: Optional[float] = None,
                 step: float = 1, round_method: Callable[[float], float] = lambda f: round(f, 3)):
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

    def __len__(self) -> int:
        return int((self.stop-self.start)//self.step)

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.start}, {self.stop}, {self.step})"


class brange(frange):
    """like frange but with tqdm
    """

    def __iter__(self):
        itr = super().__iter__()
        try:
            from my_tqdm import tqdm  # type:ignore  # pylint: disable=import-error
            return iter(tqdm(itr, desc=f"{self}", total=len(self)))
        except:
            return itr


__all__ = [
    "frange",
    "brange"
]
