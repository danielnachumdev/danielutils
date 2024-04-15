class MockImportObject:
    """
    A class to create a mock object that will raise an import error when you try to interact with it in some way
    """

    def __init__(self, msg: str):
        self._msg = msg

    def __getattr__(self, item):
        raise ImportError(self._msg)

    def __call__(self, *args, **kwargs):
        raise ImportError(self._msg)


__all__ = [
    "MockImportObject"
]
