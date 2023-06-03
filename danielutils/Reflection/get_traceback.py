import traceback


def get_traceback() -> list[str]:
    """returns the traceback of the stack until current frame

    Returns:
        list[str]: list of frames as strings
    """
    return traceback.format_stack()[8:-2]


__all__ = [
    "get_traceback"
]
