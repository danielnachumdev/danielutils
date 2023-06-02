def subseteq(l1: list, l2: list) -> bool:
    return set(l1).issubset(set(l2))


__all__ = [
    "subseteq"
]
