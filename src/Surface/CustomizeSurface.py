from pygame import Surface

from src.Libs.Window.display import Display
from src.Surface import BaseSurface


class CustomizeSurface(BaseSurface):
    def __init__(self, size: tuple[int, int] | Surface, pos: tuple[int, int] = (0,0)) -> None:
        super().__init__()
        if isinstance(size, tuple):
            self.width, self.height = size
            self.box = Surface((self.width, self.height))
        elif isinstance(size, Surface):
            self.width,  self.height = size.get_size()
            self.box = size.copy()
        self.box_rect = self.box.get_rect()

        self.x, self.y = pos

        self.parent = None

    @property
    def surface_display(self):
        return self.parent.surface_display

    @property
    def w_x(self):
        return self.x + getattr(self.parent, 'w_x', 0)

    @property
    def w_y(self):
        return self.y + getattr(self.parent, 'w_y', 0)

    def render(self) -> None:
        self.box = Surface(Display.get_global_size(self.width, self.height))
        self.box_rect = self.box.get_rect(topleft=Display.get_global_size(self.w_x, self.w_y))

    def afterRender(self) -> None:
        self.surface_display.blit(self.box, self.box_rect)