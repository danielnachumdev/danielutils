class MockModule:
    def __init__(self, msg: str):
        self._msg = msg

    def __getattr__(self, item):
        raise ImportError(self._msg)

    def __call__(self, *args, **kwargs):
        raise ImportError(self._msg)

__all__=[
    "MockModule"
]