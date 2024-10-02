from typing import Type, List, Optional, Iterator
from .progress_bar import ProgressBar
from ..print_ import bprint


class ProgressBarPool:
    def __init__(
            self,
            pbar_class: Type[ProgressBar],
            num_of_bars: int = 1,
            global_options: Optional[dict] = None,
            individual_options: Optional[List[Optional[dict]]] = None
    ) -> None:
        self.bars: List[ProgressBar] = []
        if global_options is None:
            global_options = {}
        if individual_options is None:
            individual_options = [{} for _ in range(num_of_bars)]
        if len(individual_options) != num_of_bars:
            raise ValueError(
                "must supply the same number of options as there are bars")
        for i in range(num_of_bars):
            if individual_options[i] is None:
                individual_options[i] = {}
        max_desc_length: int = max([len(individual_options[i].get("desc", f"pbar {i}")) for i in range(num_of_bars)])
        for i in range(num_of_bars):
            final_options: dict = global_options.copy()
            final_options.update(individual_options[i])  # type:ignore
            if "desc" not in final_options:
                final_options["desc"] = f"pbar {i}"
            final_options["desc"] = final_options["desc"].ljust(max_desc_length, " ")
            t = pbar_class(
                position=i,
                pool=self,
                **final_options
            )
            self.bars.append(t)
        self.writes: List[str] = []

    def __getitem__(self, index: int) -> ProgressBar:
        return self.bars[index]

    def write(self, msg: str, end: str = "\n") -> None:
        prev_rows = bprint.rows.copy()
        for w in self.writes:
            prev_rows.remove(w)
        self.writes.append(msg + end)
        rows = self.writes.copy() + prev_rows
        for _ in bprint.rows:
            bprint.move_up()
            bprint.clear_line()
        bprint.rows.clear()

        for row in rows:
            bprint(row, end="")
        pass

    def __iter__(self) -> Iterator[ProgressBar]:
        return iter(self.bars)


__all__ = [
    "ProgressBarPool",
]
