from pygame import Surface
from pygame.transform import scale

from src.Libs.Window.display import Display


class SurfaceRender:
    def __init__(self, surface: Surface):
        self._surface = surface

    def render(self, w: int, h: int) -> Surface:
        return scale(self._surface, Display.get_global_size(w, h))