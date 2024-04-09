import builtins


class ChangeAndContext:
    def __init__(self, new_func) -> None:
        self.old_func = builtins.bool.__call__
        self.new_func = new_func

    def __enter__(self):
        setattr(builtins.bool, "__init__", self.new_func)
        # builtins.bool.__call__ = self.new_func
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        setattr(builtins.bool, "__init__", self.old_func)
        # builtins.bool.__call__ = self.old_func


__all__ = [
    "ChangeAndContext"
]
