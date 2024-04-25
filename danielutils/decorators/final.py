def final(cls: type) -> type:
    """
    A class Decorator to mark a class as final and add expected behavior
    Args:
        cls: the class to mark

    Returns:
        marked class
    """
    def __init__subclass__(*args, **kwargs):
        raise TypeError(f"'{cls.__qualname__}' is final. Can't create subclasses")

    setattr(cls, "__init_subclass__", __init__subclass__)
    return cls


class Final:
    """
    A parent class to make direct child a Final class. will add expected behaviour.
    """
    def __new__(cls, *args, **kwargs):
        if cls is Final:
            raise TypeError("Can't instantiate 'Final'")
        return super().__new__(cls, *args, **kwargs)

    @classmethod
    def __init_subclass__(cls, **kwargs):
        def __init__subclass__(*args, **kwargs):
            raise TypeError(f"'{cls.__qualname__}' is final. Can't create subclasses")

        setattr(cls, "__init_subclass__", __init__subclass__)


__all__ = [
    "final",
    "Final"
]
