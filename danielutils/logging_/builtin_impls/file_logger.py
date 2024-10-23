from pathlib import Path

from danielutils import delete_file, directory_exists, create_directory

from ..logger_strategy_impl_base import LoggerStrategyImplBase


class FIleLogger(LoggerStrategyImplBase):
    def __init__(self, output_path: str, logger_id: str, delete_if_already_exists: bool = True, channel: str = "all"):
        if delete_if_already_exists:
            delete_file(output_path)
        if not directory_exists(parent := str(Path(output_path).parent.absolute().resolve())):
            create_directory(parent)
        self.output_path: str = str(Path(output_path).absolute().resolve())

        def foo(s: str):
            with open(self.output_path, "a+") as f:
                f.write(s)

        super().__init__(foo, logger_id, channel)


__all__ = [
    "FIleLogger"
]
