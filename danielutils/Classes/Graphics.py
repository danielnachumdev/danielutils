# from __future__ import annotations

# from PIL.ImageDraw import ImageDraw as graphics
# from PIL import ImageFont, Image, ImageDraw
# import PIL


# class Graphics:

#     def __init__(self, bg_color: Tuple(int, int, int, int)) -> None:
#         self.bg_color = bg_color
#         self.g: graphics = None

#     def set_background_color(self, bg_color):
#         self.bg_color = bg_color

#     def draw_line(self):
#         pass

#     def draw_image(self, img: PIL.Image, rotation: float = 0):
#         rotation %= 360

#         self.g.bitmap(((img.width, img.height)),
#                       img, fill=self.bg_color)

#     def draw_text(self, x: int, y: int, center: bool = False):
#         pass

#     @staticmethod
#     def create_graphics_from(img: PIL.Image) -> Graphics:
#         pass

#     def save(self, path: str) -> None:
#         pass
