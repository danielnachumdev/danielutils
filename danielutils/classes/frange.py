import math_
import decimal
from typing import Callable, Optional, Iterator, Sequence, overload, Union


class frange(Sequence[float]):
    """This class is the same like the builtin range but with float values
    """

    @staticmethod
    def from_range(r: range) -> 'frange':
        """will "downcast" `range` to `frange` correctly"""
        return frange(r.start, r.stop, r.step)

    @staticmethod
    def _is_int(n: Union[int, float]) -> bool:
        if isinstance(n, int):
            return True

        return n.is_integer()

    @staticmethod
    def _lcm_float(a: float, b: float) -> float:
        prec = min(5, max(decimal.getcontext().prec, 10))
        a = round(a, prec)
        b = round(b, prec)
        return math_.lcm(int(a * 10 ** prec), int(b * 10 ** prec)) / 10 ** prec

    @staticmethod
    def _find_min_step(s1: float, s2: float) -> float:
        """
        returns the minimum LCM for two step values
        Args:
            s1 (float): first step value:
            s2 (float): second step value:

        Returns:
            float: minimum LCM
        """
        M = max(s1, s2)
        m = min(s1, s2)
        if float.is_integer(M / m):
            return M
        return frange._lcm_float(s1, s2)

    def __init__(self, start: float, stop: Optional[float] = None,
                 step: float = 1, round_method: Callable[[float], float] = lambda f: round(f, 3)):
        if stop is None:
            stop = start
            start = 0
        self.start = start
        self.stop = stop
        self.step = step
        self.method = round_method

    @overload
    def __getitem__(self, index: int) -> float:
        ...

    @overload
    def __getitem__(self, index: slice) -> 'frange':
        ...

    def __getitem__(self, index: Union[float, slice]) -> Union[float, 'frange']:
        if isinstance(index, slice):
            index = slice(
                index.start if index.start is not None else 0,
                index.stop if index.stop is not None else len(self),
                index.step if index.step is not None else 1,
            )
            if index.step > 0:
                step = self.step * index.step
                start = self.start + step * index.start
                stop = self.start + step * index.stop
                return frange(start, stop, step)
            s = slice(index.start, index.stop, abs(index.step))
            return reversed(self[s])
        if index < 0:
            raise ValueError(f"At {self.__class__.__qualname__}.__getitem__ 'index' must be a positive integer")
        return self.start + self.step * index

    def __reversed__(self) -> 'frange':
        return frange(self.stop - 1, self.start - 1, -self.step)

    def __eq__(self, other):
        if not isinstance(other, frange):
            raise NotImplementedError
        return self.start == other.start and self.stop == other.stop and self.step == other.step

    def __iter__(self) -> Iterator[float]:
        if self.stop < self.start and self.step > 0:
            return
        if self.start > self.stop and self.step > 0:
            return
        if abs(self.stop - self.start) < abs(self.step):
            return
        if self.stop > 0 and self.step < 0:
            return
        if self.stop < 0 and self.step > 0:
            return

        cur = self.start
        while (cur < self.stop and self.step > 0) or (cur > self.stop and self.step < 0):
            yield self.method(cur)
            cur += self.step

    def __len__(self) -> int:
        if self.stop in {float("inf"), -float("inf")}:
            return float("inf")
        return int(abs(self.stop - self.start) // abs(self.step))

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.start}, {self.stop}, {self.step})"

    def __contains__(self, item):
        if item < self.start:
            return False
        if item >= self.stop:
            return False

        if frange._is_int(self.step):
            if not frange._is_int(item):
                return False

        return item / self.step - item // self.step == 0

    @property
    def is_finite(self) -> bool:
        """
        Returns `True` if the range is finite
        inverse if `is_infinite`
        Returns:
            bool
        """
        return len(self) != float("inf")

    @property
    def is_infinite(self) -> bool:
        """
        Returns `True` if the range is infinite
        inverse if `is_finite`
        Returns:
            bool
        """
        return not self.is_finite

    def normalize(self) -> 'frange':
        """
        will normalize the `frange` object
        Returns:
            frange
        """
        return frange(self.start / self.step, self.stop / self.step, 1)

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
            from tqdm_ import tqdm  # type:ignore  # pylint: disable=import-error
            return iter(tqdm(itr, desc=f"{self}", total=len(self)))
        except:
            return itr


__all__ = [
    "frange",
    "brange"
]
