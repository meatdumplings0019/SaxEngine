from pygame import Surface
from src.Data.Fonts import msyh_font
from src.Data.Surface import black_surface
from src.Libs.Window.display import Display
from src.Surface import SurfaceRender
from src.Window import Window


class EmbeddedWindow(Window):
    TITLE = 20
    def __init__(self, width=0, height=0, title="Window", icon=None):
        super().__init__(width, height + self.TITLE, title, icon)
        self.icon = SurfaceRender(self.icon) if self.icon else black_surface

        self.active: bool = False

        self.bg = Surface((self._width, self._height))
        self.bg_rect = self.bg.get_rect()
        self.bg.fill("Gray")

        self.title_bar = Surface((self._width, self.TITLE))
        self.title_bar_rect = self.title_bar.get_rect()
        self.title_bar.fill("Yellow")

    def open(self, x, y) -> None:
        self._x, self._y = x, y
        self.active = True

    def close(self) -> None:
        self.active = False

    def _draw_text(self) -> None:
        surf = msyh_font.render(self.TITLE + self.TITLE // 4).render(self.title, "Black")
        rec = surf.get_rect(left = self.TITLE // 4 + self.TITLE * 0.8, centery=self.title_bar_rect.centery)
        self.title_bar.blit(surf, rec)

    def _draw_icon(self) -> None:
        icon_surf = self.icon.render(self.TITLE - self.TITLE // 4, self.TITLE - self.TITLE // 4)
        icon_rect = icon_surf.get_rect(left = self.TITLE // 6, centery=self.title_bar_rect.centery)
        self.title_bar.blit(icon_surf, icon_rect)

    def _draw(self):
        self.bg = self.box.copy()
        self.bg_rect = self.bg.get_rect()
        self.bg.fill("Gray")

        self.title_bar = Surface(Display.get_global_size(self._width, self.TITLE))
        self.title_bar_rect = self.title_bar.get_rect()
        self.title_bar.fill("Yellow")

        self.box.blit(self.bg, self.bg_rect)
        self._draw_text()
        self._draw_icon()
        self.box.blit(self.title_bar, self.title_bar_rect)

    def render(self) -> None:
        super().render()
        self.box_rect = self.box.get_rect(center=Display.get_global_size(self.w_x, self.w_y))
        self._draw()
        self.parent.box.blit(self.box, self.box_rect)