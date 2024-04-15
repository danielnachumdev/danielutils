from typing import Any

from .evaluable import Evaluable


class BasicExpression(Evaluable):
    def evaluate(self, *args, **kwargs) -> Any:
        pass
