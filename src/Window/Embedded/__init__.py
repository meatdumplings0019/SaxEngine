from pygame import Surface

from src.Data.Fonts import msyh_font
from src.Libs.Window.display import Display
from src.Window import Window


class EmbeddedWindow(Window):
    TITLE = 20
    def __init__(self, width=0, height=0, title="Window", icon=None):
        super().__init__(width, height + self.TITLE, title, icon)
        from src.Window.Independence import IndependenceWindow
        self.parent: IndependenceWindow | None = None
        self.active: bool = False

        self.bg = Surface((self.width, self.height))
        self.bg_rect = self.bg.get_rect()
        self.bg.fill("Gray")

        self.title_bar = Surface((self.width, self.TITLE))
        self.title_bar_rect = self.title_bar.get_rect()
        self.title_bar.fill("Yellow")

    def open(self, x, y) -> None:
        self.s_x, self.s_y = x, y
        self.active = True

    def close(self) -> None:
        self.active = False

    def _draw_text(self) -> None:
        surf = msyh_font.render(self.TITLE + self.TITLE // 4).render(self.title, "Black")
        rec = surf.get_rect(topleft=Display.get_global_size(self.TITLE // 4, self.TITLE // 8))
        self.box.blit(surf, rec)

    def _draw(self):
        self.bg = self.box.copy()
        self.bg_rect = self.bg.get_rect()
        self.bg.fill("Gray")

        self.title_bar = Surface(Display.get_global_size(self.s_width, self.TITLE))
        self.title_bar_rect = self.title_bar.get_rect()
        self.title_bar.fill("Yellow")

        self.box.blit(self.bg, self.bg_rect)
        self.box.blit(self.title_bar, self.title_bar_rect)
        self._draw_text()

    def render(self) -> None:
        super().render()
        self.box_rect = self.box.get_rect(center=Display.get_global_size(self.s_x, self.s_y))
        self._draw()
        self.parent.box.blit(self.box, self.box_rect)