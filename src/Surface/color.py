from pygame import Surface

from src.Libs.Utils.types import ColorType


class SurfaceColor:
    def __init__(self, color: ColorType):
        self._color = color

    @property
    def color(self) -> ColorType:
        return self._color

    def render(self, w: int, h: int) -> Surface:
        surface = Surface((w, h))
        surface.fill(self._color)
        return surface