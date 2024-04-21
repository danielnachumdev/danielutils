def subseteq(l1: list, l2: list) -> bool:
    """return whether l1 is in list l2

    Args:
        l1 (list): first list
        l2 (list): second list

    Returns:
        bool: boolean result
    """
    return set(l1).issubset(set(l2))


__all__ = [
    "subseteq"
]
