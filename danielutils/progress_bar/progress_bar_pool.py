from typing import Type, List, Optional
from .progress_bar import ProgressBar


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
        for i in range(num_of_bars):
            final_options: dict = global_options.copy()
            final_options.update(individual_options[i])  # type:ignore
            if "desc" not in final_options:
                final_options["desc"] = f"pbar {i}"
            t = pbar_class(
                position=i,
                **final_options
            )
            self.bars.append(t)

    def __getitem__(self, index: int) -> ProgressBar:
        return self.bars[index]

    def write(self, *args, sep=" ", end="\n") -> None:
        self.bars[0].write(sep.join((str(a) for a in args)), end=end)


__all__ = [
    "ProgressBarPool",
]
