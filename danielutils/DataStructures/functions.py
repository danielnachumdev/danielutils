from ..Functions import isoftype


def weight(v) -> int | float:
    if isoftype(v, int | float):
        return v
    if hasattr(v, "__weight__"):
        return v.__weight__()
    raise AttributeError(f"{v} has no __weight__ function")


__all__ = [
    "weight"
]
