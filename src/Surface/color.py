from pygame import Surface

from src.Libs.Utils.types import ColorType
from src.Surface import SurfaceRender


class SurfaceColor(SurfaceRender):
    def __init__(self, color: ColorType):
        self._color = color
        surface = Surface((64, 64))
        surface.fill(self._color)
        super().__init__(surface)

    @property
    def color(self) -> ColorType:
        return self._color