from typing import ContextManager


class MultiContext(ContextManager):
    def __init__(self, *contexts: ContextManager):
        self.contexts = contexts

    def __enter__(self):
        for context in self.contexts:
            context.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for context in self.contexts:
            context.__exit__(exc_type, exc_val, exc_tb)

    def __getitem__(self, index):
        return self.contexts[index]


__all__ = [
    "MultiContext",
]
