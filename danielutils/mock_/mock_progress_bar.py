from typing import Optional, Iterable, Sized

import time

from ..progress_bar import ProgressBar
from ..print_ import bprint


class MockProgressBar(ProgressBar):

    def __init__(
            self,
            iterable: Iterable,
            position: int,
            *,
            total: Optional[float] = None,
            desc: str = "",
            leave: bool = True,
            num_bars: int = 1,
            ncols: int = 50,
            **kwargs
    ):
        self.iterable: Iterable = iterable
        if isinstance(self.iterable, Sized):
            total_ = len(self.iterable)
        if total is not None:
            total_ = total
        ProgressBar.__init__(self, total_, position)
        self.num_bars: int = num_bars
        self.leave: bool = leave
        self.desc: str = desc
        self.initial_value: float = 0
        self.current_value: float = 0
        self.ncols: int = ncols
        self.unit: str = "it"
        self.pbar_format = "{l_bar} |{bar}| {n_fmt:.2f}/{total_fmt:.2f}{unit}" \
                           " [{elapsed:.2f}<{remaining}, {rate_fmt:.2f}{unit}{postfix}]"
        self.__dict__.update(kwargs)
        self.initial_start_time = time.time()
        self.prev_update: float = self.initial_start_time
        self.delta: float = 0
        self.prev_value: float = self.initial_value
        self.bprint_row_index = bprint.current_row

    def __iter__(self):
        self.bprint_row_index = bprint.current_row
        for v in self.iterable:
            self.update(1)
            yield v
            bprint.move_up()
            bprint.clear_line()
        if self.position > 0:
            self.reset()
        else:
            self.draw()

    def draw(self) -> None:
        percent = self.current_value / self.total
        num_to_fill = int(percent * self.ncols)
        progress_str = num_to_fill * "#" + (self.ncols - num_to_fill) * " "
        to_print = self.pbar_format.format(
            l_bar=self.desc,
            bar=progress_str,
            n_fmt=self.current_value,
            total_fmt=self.total,
            elapsed=self.prev_update - self.initial_start_time,
            remaining="?",
            rate_fmt=(self.current_value - self.prev_value) /
                     self.delta if self.delta != 0 else 0,
            postfix="/s",
            unit=self.unit
        )
        bprint(to_print)

    def update(self, amount: float = 1):
        self.prev_value = self.current_value
        self.current_value = min(
            self.current_value + amount, self.total)  # type:ignore
        current_time = time.time()
        self.delta = current_time - self.prev_update
        self.prev_update = current_time
        self.draw()

    def _write(self, *args: str, sep: str = " ", end: str = "\n") -> None:
        bprint.move_up()
        bprint.clear_line()
        if not end.endswith("\n"):
            end += "\n"
        bprint(sep.join(map(str, args)), end=end)
        self.draw()

    def reset(self) -> None:
        self.current_value = self.initial_value
        self.initial_start_time = time.time()
        self.delta = 0
        self.prev_value = self.initial_value
        for _ in range(self.num_writes):
            bprint.move_up()
            bprint.clear_line()
        self.num_writes = 0


__all__ = [
    'MockProgressBar'
]
