from pygame import Surface
from src.Data.Fonts import msyh_font
from src.Data.Surface import black_surface
from src.Data.Surface.texture import red_close_surface
from src.InputSystem import InputAction
from src.Libs.Utils.types import vec2
from src.Libs.Window.display import Display
from src.Surface import SurfaceRender
from src.Window import Window


class EmbeddedWindow(Window):
    TITLE = 20
    def __init__(self, width=0, height=0, title="Window", icon=None):
        super().__init__(width, height + self.TITLE, title, icon)
        self.icon = SurfaceRender(self.icon) if self.icon else black_surface

        self.active: bool = False

        self.bg = Surface((self._width, self._height - self.TITLE))
        self.bg_rect = self.bg.get_rect()
        self.bg.fill("Gray")

        self.title_bar = Surface((self._width, self.TITLE))
        self.title_bar_rect = self.title_bar.get_rect()
        self.title_bar.fill("Yellow")

        self.close_btn = Surface((self.TITLE - self.TITLE // 4, self.TITLE - self.TITLE // 4))
        self.close_btn_rect = self.close_btn.get_rect(right = self.width - self.TITLE // 6, centery = self.title_bar_rect.centery)
        self.close_btn.fill("Gray")

        self.max = False

        self.is_dragging = False
        self.drag_offset = 0

    def init(self) -> None:
        self.is_dragging = False
        self.drag_offset = 0

    def handle_event(self, event: InputAction):
        super().handle_event(event)
        if event.IsBtnDown(Display.get_global_rect(self.title_bar_rect, self.box_rect)) and not self.max:
            mouse_pos = event.mousePosition
            self.is_dragging = True
            self.drag_offset = mouse_pos - Display.get_global_size(self.x, self.y)

        elif event.IsMouseUp() or self.max:
            self.is_dragging = False
        elif event.mouseMotion and self.is_dragging and not self.max:
            new_pos = vec2(event.GetMousePosition()) - self.drag_offset
            new_pos.x = max(0, int(min(new_pos.x - self.box.get_width() / 2,
                                       self.parent.surface_display.get_width() - self.title_bar_rect.width)))
            new_pos.y = max(0, int(min(new_pos.y - self.box.get_height() / 2,
                                       self.parent.surface_display.get_height() - self.title_bar_rect.height)))
            new_pos += (self.box.get_width() / 2, self.box.get_height() / 2)
            new_pos = Display.get_return_size(new_pos.x, new_pos.y)
            self._x, self._y = new_pos

        if event.IsBtnDown(Display.get_global_rect(self.close_btn_rect, self.box_rect)):
            self.close()

    def open(self, x, y) -> None:
        self._x, self._y = x, y
        self.active = True

    def close(self) -> None:
        self.active = False

    def _draw_text(self) -> None:
        surf = msyh_font.render(self.TITLE + self.TITLE // 4).render(self.title, "Black")
        rec = surf.get_rect(left = Display.get_global_width(self.TITLE // 4 + self.TITLE * 0.8), centery=self.title_bar_rect.centery)
        self.title_bar.blit(surf, rec)

    def _draw_icon(self) -> None:
        icon_surf = self.icon.render(self.TITLE - self.TITLE // 4, self.TITLE - self.TITLE // 4)
        icon_rect = icon_surf.get_rect(left = Display.get_global_width(self.TITLE // 6), centery=self.title_bar_rect.centery)
        self.title_bar.blit(icon_surf, icon_rect)

    def _draw_close_btn(self):
        self.close_btn = Surface(Display.get_global_size(self.TITLE - self.TITLE // 4, self.TITLE - self.TITLE // 4))
        self.close_btn_rect = self.close_btn.get_rect(right=Display.get_global_width(self.width - self.TITLE // 6), centery=self.title_bar_rect.centery)
        self.close_btn.fill("Gray")

        close_btn = red_close_surface.render(self.TITLE - self.TITLE // 4 - self.TITLE // 10, self.TITLE - self.TITLE // 4 - self.TITLE // 10)
        close_btn_rect = close_btn.get_rect(center=Display.center_object(self.close_btn, self.title_bar).center)
        self.close_btn.blit(close_btn, close_btn_rect)
        self.title_bar.blit(self.close_btn, self.close_btn_rect)

    def _draw(self):
        self.bg = Surface(Display.get_global_size(self._width, self._height - self.TITLE))
        self.bg_rect = self.bg.get_rect(top=Display.get_global_height(self.TITLE))
        self.bg.fill("Gray")

        self.title_bar = Surface(Display.get_global_size(self._width, self.TITLE))
        self.title_bar_rect = self.title_bar.get_rect()
        self.title_bar.fill("Yellow")

        self.box.blit(self.bg, self.bg_rect)
        self._draw_text()
        self._draw_icon()
        self._draw_close_btn()
        self.box.blit(self.title_bar, self.title_bar_rect)

    def render(self) -> None:
        super().render()
        self.box_rect = self.box.get_rect(center=Display.get_global_size(self.w_x, self.w_y))
        self.box.fill("White")
        self._draw()
        self.parent.box.blit(self.box, self.box_rect)