class DefaultDict(dict):
    """
    My implementation to `collections.defaultdict`
    """

    def __init__(self, cls):
        self._cls = cls

    def __getitem__(self, key):
        return super().get(key, self._cls())


__all__ = [
    "DefaultDict"
]
