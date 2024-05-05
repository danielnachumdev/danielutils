from abc import ABC, abstractmethod


class Transformation:
    @abstractmethod
    @staticmethod
    def transform(img): ...

    def __call__(self, img):
        return self.transform(img)
