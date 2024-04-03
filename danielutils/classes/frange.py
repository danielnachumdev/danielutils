from typing import Iterable, Callable, Optional, Iterator


class frange(Iterable[float]):
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

    def __eq__(self, other):
        if not isinstance(other, frange):
            raise NotImplementedError
        return self.start == other.start and self.stop == other.stop and self.step == other.step

    def __iter__(self) -> Iterable:
        if self.stop < self.start:
            return
        if self.start > self.stop:
            return
        if abs(self.stop - self.start) < abs(self.step):
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
        return int((self.stop - self.start) // self.step)

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.start}, {self.stop}, {self.step})"

    @property
    def _is_whole_step(self) -> bool:
        return self.step - int(self.step) == 0

    def __contains__(self, item):
        if item < self.start:
            return False
        if item >= self.stop:
            return False

        if self._is_whole_step:
            if not item - int(item) == 0:
                return False

        return item / self.step - item // self.step == 0

    def normalize(self) -> 'frange':
        return frange(self.start / self.step, self.stop / self.step, 1)

    def intersect(self, other: 'frange') -> 'frange':
        a, b = self.normalize(), other.normalize()
        start1, stop1 = a.start, a.stop
        start2, stop2 = b.start, b.stop
        remainder1, remainder2 = start1 - int(start1), start2 - int(start2)
        if remainder1 == remainder2:
            if stop1 == float("inf") or stop2 == float("inf"):
                return frange(max(start1, start2), float("inf"))
            return frange(max(start1, start2), min(stop1, stop2))
        raise NotImplementedError("this part is not implemented yet")
        if remainder1 != 0 and remainder2 / remainder1 - remainder2 // remainder1 == 0:
            pass

        pass


class frange_iterator(Iterator[float]):
    def __init__(self, obj: frange):
        self.r = obj

    def __next__(self):
        if self.r.stop < self.r.start:
            return
        if self.r.start > self.r.stop:
            return
        if abs(self.r.stop - self.r.start) < abs(self.r.step):
            return
        if self.r.stop > 0 and self.r.step < 0:
            return
        if self.r.stop < 0 and self.r.step > 0:
            return

        cur = self.r.start
        while cur < self.r.stop:
            yield self.r.method(cur)
            cur += self.r.step

    def __iter__(self):
        return self


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
