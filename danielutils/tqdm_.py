from typing import Optional, List as t_list
from .reflection import get_python_version

if get_python_version() >= (3, 9):
    from builtins import list as t_list  # type:ignore
try:
    from tqdm import tqdm
except ImportError:
    from .mock_ import MockImportObject

    tqdm = MockImportObject("`tqdm` is not installed")  # type:ignore


class ProgressBarPool:
    """
    My attempt at creating a progress bar pool using tqdm
    """

    def __init__(self, num_of_bars: int = 1, *, global_options: Optional[dict] = None,
                 individual_options: Optional[t_list[Optional[dict]]] = None) -> None:
        self.bars: t_list[tqdm] = []
        if global_options is None:
            global_options = {}
        if individual_options is None:
            individual_options = [{} for _ in range(num_of_bars)]
        if len(individual_options) != num_of_bars:
            raise ValueError("")
        for i in range(num_of_bars):
            if individual_options[i] is None:
                individual_options[i] = {}
        for i in range(num_of_bars):
            final_options: dict = global_options.copy()
            final_options.update(individual_options[i])  # type:ignore
            if "desc" not in final_options:
                final_options["desc"] = f"pbar {i}"
            t = tqdm(
                position=i,
                **final_options
            )
            self.bars.append(t)

    def write(self, *args, sep=" ", end="\n") -> None:
        """
        prints texts to the console **while** using tqdm progress bars
        """
        self.bars[0].write(sep.join((str(a) for a in args)), end=end)


__all__ = [
    "ProgressBarPool"
]
