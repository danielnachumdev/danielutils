from typing import Callable, Any, Dict, List


def is_default_implementation(func: Callable) -> bool:
    return type(func).__qualname__ == "wrapper_descriptor"


def usable(func: Callable) -> bool:
    return func is not None and not is_default_implementation(func)


def total_ordering(cls: type) -> type:
    funcs: Dict[str, Callable[[Any, Any], Any]] = {
        '__eq__': getattr(cls, '__eq__'),
        '__ne__': getattr(cls, '__ne__'),
        '__gt__': getattr(cls, '__gt__'),
        '__ge__': getattr(cls, '__ge__'),
        '__lt__': getattr(cls, '__lt__'),
        '__le__': getattr(cls, '__le__'),
    }
    g1: List[Callable[[Any, Any], Any]] = [funcs["__eq__"], funcs["__ne__"]]
    u1 = any(map(usable, g1))
    g2: List[Callable[[Any, Any], Any]] = [funcs["__ge__"], funcs["__gt__"]]
    u2 = any(map(usable, g2))
    g3: List[Callable[[Any, Any], Any]] = [funcs["__lt__"], funcs["__le__"]]
    u3 = any(map(usable, g3))
    if sum(map(int, [u1, u2, u3])) < 2:
        raise ValueError("There are not enough functions from different groups implemented")
    mapping = {
        '__eq__': {
            # a==b <=> not a!=b
            ('__ne__',): lambda self, other: not funcs['__eq__'](self, other),
            # a==b <=> a<=b and b<=a
            ('__le__',): lambda self, other: funcs['__le__'](self, other) and funcs['__le__'](other, self),
            # a==b <=> a>=b and b>=a
            # a==b <=> not a<b and not b<a
            # a==b <=> not a>b and not b>a
            # a==b <=> a<=b and not a<b
            ('__le__', '__lt__'): lambda self, other: funcs['__le__'](self, other) and not funcs['__lt__'](self, other),
            # a==b <=> a>=b and not a>b
            ('__ge__', '__ge__'): lambda self, other: funcs['__ge__'](self, other) and not funcs['__gt__'](self, other),
            # a==b <=> a<=b and not a>=b
            ('__le__', '__ge__'): lambda self, other: funcs['__ge__'](self, other) and funcs['__le__'](self, other),
            # not a<b and not b>a
            ('__lt__', '__gt__'): lambda self, other: not funcs['__lt__'](self, other) and not funcs['__gt__'](other,
                                                                                                               self),
        },
        '__ne__': {
            ('__eq__',): lambda self, other: not funcs['__eq__'](self, other),
        },
        '__lt__': {
            ('__ge__',): lambda self, other: not funcs['__ge__'](self, other),
            ('__eq__', '__le__'): lambda self, other: funcs['__le__'](self, other) and not funcs['__eq__'](self, other),
        },
        '__le__': {
            ('__gt__',): lambda self, other: not funcs['__gt__'](self, other),
            ('__eq__', '__lt__'): lambda self, other: funcs['__lt__'](self, other) or funcs['__eq__'](self, other),
        },
        '__gt__': {
            ('__le__',): lambda self, other: not funcs['__le__'](self, other),
            ('__eq__', '__ge__'): lambda self, other: funcs['__ge__'](self, other) and not funcs['__eq__'](self, other),
        },
        '__ge__': {
            ('__lt__',): lambda self, other: not funcs['__lt__'](self, other),
            ('__eq__', '__gt__'): lambda self, other: funcs['__gt__'](self, other) or funcs['__eq__'](self, other),
        },
    }
    for name, f in funcs.items():
        if usable(f):
            continue
        for option, implementation in mapping[name].items():
            if all(map(usable, (funcs[dep] for dep in option))):
                funcs[name] = implementation
                break
    for name, f in funcs.items():
        setattr(cls, name, f)
    return cls


__all__ = [
    "total_ordering"
]
