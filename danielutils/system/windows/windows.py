# from functools import partial
# from screeninfo import get_monitors
# import pyautogui
# from PIL import ImageGrab, Image
# ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)


# def screenshot(xy: tuple[int, int] = (0, 0), wh: tuple[int, int] = None) -> Image:
#     """creates a screenshot of the screen in an arbitrary location and size

#     Args:
#         xy (tuple[int, int], optional): the top left location of the screenshot. Defaults to (0, 0).
#         wh (tuple[int, int], optional): the size of the screenshot in pixels. Defaults to None. if None will
#         create a screen shot of all monitors
#     Returns:
#         Image: _description_
#     """
#     if wh is None:
#         wh = (0, 0)
#         for monitor_index in range(get_monitor_count()):
#             size = get_monitor_size(monitor_index)
#             wh = (wh[0]+size[0], wh[1]+size[1])
#     return pyautogui.screenshot(None, (xy[0], xy[1], wh[0], wh[1]))


# def screenshot_monitor(index: int) -> Image:
#     """creates a screenshot of the monitor

#     Args:
#         index (int): the monitor's index

#     Returns:
#         Image: the screenshot
#     """
#     return screenshot(get_monitor_location(index), get_monitor_size(index))


# def get_monitor_size(index: int) -> tuple[int, int]:
#     """returns the size of the monitor

#     Args:
#         index (int): the monitor's index

#     Returns:
#         tuple[int, int]: the size
#     """
#     monitor = get_monitors()[index]
#     return monitor.width, monitor.height


# def get_monitor_location(index: int) -> tuple[int, int]:
#     """returns the coordinates of the location of the monitor

#     Args:
#         index (int): the monitor's index

#     Returns:
#         tuple[int, int]: the coordinates
#     """
#     monitor = get_monitors()[index]
#     return monitor.x, monitor.y


# def get_monitor_count() -> int:
#     """return the number of displays connected to this computer

#     Returns:
#         int: amount of displays
#     """
#     return len(get_monitors())


# __all__ = [
#     "screenshot",
#     "get_monitor_size",
#     "get_monitor_count",
#     "screenshot_monitor"
# ]
