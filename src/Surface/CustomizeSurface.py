from pygame import Surface

from src.Libs.Window.display import Display
from src.Surface.DisplaySurface import DisplaySurface


class CustomizeSurface(DisplaySurface):
    def __init__(self, size: tuple[int, int] | Surface, pos: tuple[int, int] = (0,0)) -> None:
        super().__init__()
        if isinstance(size, tuple):
            self.s_width, self.s_height = size
            self.box = Surface((self.s_width, self.s_height))
        elif isinstance(size, Surface):
            self.s_width,  self.s_height = size.get_size()
            self.box = size.copy()

        self.box_rect = self.box.get_rect()

        self.width = self.s_width
        self.height = self.s_height

        self.s_x, self.s_y = pos

    def return_size(self) -> None:
        self.width = self.s_width
        self.height = self.s_height

    def render(self) -> None:
        self.box = Surface(Display.get_global_size(self.width, self.height))
        self.box_rect = self.box.get_rect(topleft=Display.get_global_size(self.s_x, self.s_y))

    def afterRender(self) -> None:
        self.surface_display.blit(self.box, self.box_rect)