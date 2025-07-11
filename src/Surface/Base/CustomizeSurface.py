from pygame import Surface, Rect

from src.Libs.Window.display import Display
from src.Surface.Base import BaseSurface


class CustomizeSurface(BaseSurface):
    def __init__(self, base_size: tuple[int, int], size: tuple[int, int] | Surface, pos: tuple[int, int] = (0,0)) -> None:
        super().__init__()
        if isinstance(size, tuple):
            self._width, self._height = size
            self.box = Surface((self._width, self._height))
        elif isinstance(size, Surface):
            self._width,  self._height = size.get_size()
            self.box = size.copy()
        self.box_rect = self.box.get_rect()

        self._x, self._y = pos

        if base_size:
            self.s_width, self.s_height = base_size
        else:
            self.s_width = self.width
            self.s_height = self.height

        self.parent = None

    @property
    def surface_display(self):
        return self.parent.surface_display

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def w_x(self):
        return self._x + getattr(self.parent, 'w_x', 0)

    @property
    def w_y(self):
        return self._y + getattr(self.parent, 'w_y', 0)

    def render(self) -> None:
        self.box = Surface(Display.get_global_size(self.width, self.height, size=(self.s_width, self.s_height)))
        self.box_rect = self.box.get_rect(topleft=Display.get_global_size(self.x, self.y, size=(self.s_width, self.s_height)))

    def get_center_box(self) -> Rect:
        return Display.get_global_rect(self.parent.get_center_box(), self.box_rect)

    def afterRender(self) -> None:
        surface = getattr(self.parent, "box", self.surface_display)
        surface.blit(self.box, self.box_rect)