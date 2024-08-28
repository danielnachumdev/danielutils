def singleton(og_class):
    instance = None
    original_new = getattr(og_class, '__new__')
    original_init = getattr(og_class, '__init__')

    def __new__(cls, *args, **kwargs):
        nonlocal instance
        if instance is None:
            # index 0 is the current class.
            # in the minimal case index 1 has 'object' class
            # otherwise the immediate parent of current class
            cls_index, og_index = 0, list(cls.__mro__).index(og_class)
            blacklist = {*cls.__mro__[:og_index + 1]}
            for candidate in cls.__mro__[og_index + 1:]:
                if candidate not in blacklist:
                    try:
                        instance = candidate.__new__(cls, *args, **kwargs)
                        break
                    except:
                        pass
            else:
                instance = object.__new__(cls)
        return instance

    is_init: bool = False

    def __init__(self, *args, **kwargs) -> None:
        nonlocal is_init
        if not is_init:
            original_init(self, *args, **kwargs)
            is_init = True

    setattr(og_class, "__new__", __new__)
    setattr(og_class, "__init__", __init__)
    setattr(og_class, "instance", lambda: instance)
    return og_class


__all__ = [
    "singleton"
]
