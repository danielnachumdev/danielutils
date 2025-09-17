import logging
from typing import Type, Generic, TypeVar
from ..logging_.utils import get_logger

logger = get_logger(__name__)

T = TypeVar("T", bound=Type)


class Builder(Generic[T]):
    PREFIX: str = "foo"

    def __init__(self, dcls: T):
        logger.info(f"Initializing Builder for class: {dcls.__qualname__}")
        setattr(self, f"{Builder.PREFIX}_dcls", dcls)
        setattr(self, f"{Builder.PREFIX}_kwargs", {})

    def __getattribute__(self, item: str):
        if item.startswith(Builder.PREFIX) or item == "build":
            return super().__getattribute__(item)
        
        cls = super().__getattribute__(f"{Builder.PREFIX}_dcls")
        
        if item not in cls.__dataclass_fields__:
            error_msg = f"'{cls.__qualname__}' object has no attribute '{item}'"
            logger.error(f"AttributeError: {error_msg}")
            raise AttributeError(error_msg)

        def inner(o) -> Builder:
            getattr(self, f"{Builder.PREFIX}_kwargs")[item] = o
            return self

        return inner

    def build(self) -> T:
        dcls = getattr(self, f"{Builder.PREFIX}_dcls")
        kwargs = getattr(self, f"{Builder.PREFIX}_kwargs")
        instance = dcls(**kwargs)
        logger.info(f"Successfully built instance of {dcls.__qualname__}")
        return instance


def builder(dcls: T):
    logger.info(f"Applying @builder decorator to class: {dcls.__qualname__}")
    
    if not hasattr(dcls, "__dataclass_fields__"):
        error_msg = "Can only create builders out of @dataclass classes"
        logger.error(f"RuntimeError: {error_msg}")
        raise RuntimeError(error_msg)
    
    for name in dcls.__dataclass_fields__.keys():
        if name.startswith("build"):
            error_msg = f"@builder reserves attributes that has 'build' prefix. Invalid attribute: '{name}'"
            logger.error(f"AttributeError: {error_msg}")
            raise AttributeError(error_msg)
    
    @classmethod  # type: ignore
    def builder_impl(cls) -> Builder[T]:
        return Builder[T](cls)

    setattr(dcls, "builder", builder_impl)
    logger.info(f"Successfully applied @builder decorator to {dcls.__qualname__}")
    return dcls


__all__ = [
    "builder"
]
