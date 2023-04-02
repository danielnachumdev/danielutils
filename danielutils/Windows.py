from screeninfo import get_monitors
import pyautogui
from PIL import ImageGrab, Image
import PIL
from functools import partial
ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)


def screenshot(xy: tuple[int, int] = (0, 0), wh: tuple[int, int] = None) -> Image:
    if wh is None:
        wh = (0, 0)
        for monitor_index in range(get_monitor_count()):
            size = get_monitor_size(monitor_index)
            wh = (wh[0]+size[0], wh[1]+size[1])
    return pyautogui.screenshot(None, (xy[0], xy[1], wh[0], wh[1]))


def screenshot_monitor(index: int) -> Image:
    return screenshot(get_monitor_location(index), get_monitor_size(index))


def get_monitor_size(index: int) -> tuple[int, int]:
    monitor = get_monitors()[index]
    return monitor.width, monitor.height


def get_monitor_location(index) -> tuple[int, int]:
    monitor = get_monitors()[index]
    return monitor.x, monitor.y


def get_monitor_count() -> int:
    """return the number of displays connected to this computer

    Returns:
        int: amount of displays
    """
    return len(get_monitors())


__all__ = [
    "screenshot",
    "get_monitor_size",
    "get_monitor_count",
    "screenshot_monitor"
]
