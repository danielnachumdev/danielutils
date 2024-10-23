from typing import Type, Generic, TypeVar

T = TypeVar("T", bound=Type)


class Builder(Generic[T]):
    PREFIX: str = "foo"

    def __init__(self, dcls: T):
        setattr(self, f"{Builder.PREFIX}_dcls", dcls)
        setattr(self, f"{Builder.PREFIX}_kwargs", {})

    def __getattribute__(self, item: str):
        if item.startswith(Builder.PREFIX) or item == "build":
            return super().__getattribute__(item)
        cls = super().__getattribute__(f"{Builder.PREFIX}_dcls")
        if item not in cls.__dataclass_fields__:
            raise AttributeError(f"'{cls.__qualname__}' object has no attribute '{item}'")

        def inner(o) -> Builder:
            getattr(self, f"{Builder.PREFIX}_kwargs")[item] = o
            return self

        return inner

    def build(self) -> T:
        dcls = getattr(self, f"{Builder.PREFIX}_dcls")
        kwargs = getattr(self, f"{Builder.PREFIX}_kwargs")
        return dcls(**kwargs)


def builder(dcls: T):
    if not hasattr(dcls, "__dataclass_fields__"):
        raise RuntimeError("Can only create builders out of @dataclass classes")
    for name in dcls.__dataclass_fields__.keys():
        if name.startswith("build"):
            raise AttributeError(f"@builder reserves attributes that has 'build' prefix. Invalid attribute: '{name}'")

    @classmethod  # type: ignore
    def builder_impl(cls) -> Builder[T]:
        return Builder[T](cls)

    setattr(dcls, "builder", builder_impl)
    return dcls


__all__ = [
    "builder"
]
