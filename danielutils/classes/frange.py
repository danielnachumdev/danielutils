from abc import abstractmethod
from typing import Iterable, Callable, Optional, Iterator, Sequence, overload


class frange(Sequence[float]):
    """this class is the same like builtin range but with float values
    """

    @overload
    @abstractmethod
    def __getitem__(self, index: int) -> float:
        ...

    @overload
    @abstractmethod
    def __getitem__(self, index: slice) -> 'frange':
        ...

    def __getitem__(self, index):
        if isinstance(index, slice):
            index = slice(
                index.start if index.start is not None else 0,
                index.stop if index.stop is not None else len(self),
                index.step if index.step is not None else 1,
            )
            step = self.step * index.step
            start = self.start + step * index.start
            stop = self.start + step * index.stop
            return frange(start, stop, step)
        if index < 0:
            raise ValueError(f"At {self.__class__.__qualname__}.__getitem__ 'index' must be a positive integer")
        return self.start + self.step * index

    @staticmethod
    def from_range(r: range) -> 'frange':
        return frange(r.start, r.stop, r.step)

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

    def __iter__(self) -> Iterator[float]:
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
        if self.stop == float("inf"):
            return float("inf")
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

    # def _normalize_with(self, other: 'frange') -> 'frange':
    #     return frange(self.start / (self.step * other.step), self.stop / (self.step * other.step), 1)
    @staticmethod
    def _find_min_step(s1: float, s2: float) -> float:
        M = max(s1, s2)
        m = min(s1, s2)
        if float.is_integer(M / m):
            return M
        k1, k2 = 1, 1
        while s1 * k1 != s2 * k2:
            if s1 * k1 > s2 * k2:
                k2 += 1
            else:
                k1 += 1

        return s1 * k1

    def intersect(self, other: 'frange') -> 'frange':
        if not isinstance(other, frange):
            raise ValueError("frange.intercept only accepts frange objects")
        a, b = self.normalize(), other.normalize()
        start1, stop1 = a.start, a.stop
        start2, stop2 = b.start, b.stop
        remainder1, remainder2 = start1 - int(start1), start2 - int(start2)
        start = max(self.start, other.start)
        stop = min(self.stop, other.stop)
        if remainder1 == remainder2:
            min_step = self._find_min_step(self.step, other.step)
            if stop1 == float("inf") or stop2 == float("inf"):
                return frange(start, float("inf"), min_step)
            return frange(start, stop, min_step)
        # find k; start1 + remainder1*k == start2 +remainder2*k
        k = (start1 - start2) / (remainder2 - remainder1)
        if k <= 0:
            return frange(0)
        if stop1 == float("inf") or stop2 == float("inf"):
            raise NotImplementedError("this part is not implemented yet. one has inf")
        raise NotImplementedError("this part is not implemented yet")


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
