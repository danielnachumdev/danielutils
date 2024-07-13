from typing import ContextManager
class OptionalContext(ContextManager):
    def __init__(self, predicate: bool, context: ContextManager):
        self.predicate = predicate
        self.context = context

    def __enter__(self):
        if self.predicate:
            self.context.__enter__()

    def __exit__(self, __exc_type, __exc_value, __traceback):
        if self.predicate:
            self.context.__exit__(__exc_type, __exc_value, __traceback)


__all__=[
    "OptionalContext"
]