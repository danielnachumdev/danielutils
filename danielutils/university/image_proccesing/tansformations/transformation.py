from abc import ABC, abstractmethod
from typing import Any

ImageT=Any
class Transformation:
    @abstractmethod
    @staticmethod
    def transform(img: ImageT) -> ImageT: ...

    def __call__(self, img: ImageT) -> ImageT:
        return self.transform(img)
