def singleton(og_class):
    instance = None

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
                    instance = candidate.__new__(cls, *args, **kwargs)
                    break
        return instance

    setattr(og_class, "__new__", __new__)
    return og_class

__all__=[
    "singleton"
]