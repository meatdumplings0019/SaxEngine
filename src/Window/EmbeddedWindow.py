import pygame
from pygame import Surface
from src.InputSystem import InputAction
from src.Libs.display import Display
from src.Libs.draw import draw_antialiased_x, draw_rect
from src.Libs.types import vec2
from src.Resources.Font import FontResource
from src.Window import Window

class EmbeddedWindow(Window):
    TITLE = 20
    def __init__(self, width: int = 0, height: int = 0, title: str = "Window") -> None:
        super().__init__(width, height, title)
        from src.Window.IndependenceWindow import IndependenceWindow
        self.parent: IndependenceWindow | None = None
        self.active: bool = False
        self.pos = self.width, self.height
        self.window_box = Surface((width, height + self.TITLE))
        self.window_rect = self.window_box.get_rect()

        self.bg = Surface((self.width, self.height))
        self.bg_rect = self.bg.get_rect(topleft = (0, self.TITLE))
        self.bg.fill("Gray")

        self.title_bar = Surface((self.width, self.TITLE))
        self.title_bar_rect = self.title_bar.get_rect(topleft = (0, 0))
        self.title_bar.fill("Yellow")

        self.close_btn = Surface((self.TITLE - self.TITLE // 4, self.TITLE - self.TITLE // 4))
        self.close_btn_rect = self.close_btn.get_rect(topright = (self.width - self.TITLE // 8, self.TITLE // 8))
        self.close_btn.fill("Gray")

        self.max_btn = Surface((self.TITLE - self.TITLE // 4, self.TITLE - self.TITLE // 4))
        self.max_btn_rect = self.max_btn.get_rect(topright=(self.width - self.TITLE // 8 - self.TITLE - self.TITLE // 4 , self.TITLE // 8))
        self.max_btn.fill("Gray")

        self.res = FontResource("./Assets/Fonts/JeTBrainsMono.ttf")

        self.max = False

        self.is_dragging = False
        self.drag_offset = 0

        self.s_width = self.width
        self.s_height = self.height

    def init(self) -> None:
        self.is_dragging = False
        self.drag_offset = 0

    def open(self, pos: vec2, glo: bool = False) -> None:
        self.pos = pos if glo else Display.get_global_size(pos.x, pos.y)
        self.active = True

    def close(self) -> None:
        self.active = False

    def enter(self) -> None:
        self.init()

    def exit(self) -> None:
        ...

    def update(self) -> None: ...

    def handle_event(self, event: InputAction) -> None:
        if event.IsBtnDown(Display.get_global_rect(self.title_bar_rect, self.window_rect)) and not self.max:
            mouse_pos = event.GetMousePosition()
            self.is_dragging = True
            self.drag_offset = mouse_pos - Display.get_global_size(self.pos[0], self.pos[1])
        elif event.IsMouseUp() or self.max:
            self.is_dragging = False

        elif event.IsMouseMotion() and self.is_dragging and not self.max:
            new_pos = pygame.Vector2(event.GetMousePosition()) - self.drag_offset
            new_pos.x = max(0, int(min(new_pos.x - self.window_box.get_width() / 2, self.parent.surface_display.get_width() - self.title_bar_rect.width)))
            new_pos.y = max(0, int(min(new_pos.y - self.window_box.get_height() / 2 , self.parent.surface_display.get_height()  - self.title_bar_rect.height)))
            new_pos += (self.window_box.get_width() / 2, self.window_box.get_height() / 2)
            new_pos = Display.get_return_size(new_pos.x, new_pos.y)
            self.pos = new_pos

        if event.IsBtnDown(Display.get_global_rect(self.close_btn_rect, self.window_rect)):
            self.close()

        if event.IsBtnDown(Display.get_global_rect(self.max_btn_rect, self.window_rect)):
            self.max = not self.max
            self.max_window()

    def draw_close_btn(self) -> None:
        rect_size = Display.get_global_size(self.TITLE - self.TITLE / 4, self.TITLE - self.TITLE / 4)
        self.close_btn = Surface(rect_size)
        self.close_btn_rect = self.close_btn.get_rect()
        self.close_btn_rect.centery = self.title_bar_rect.centery
        self.close_btn_rect.right = self.title_bar_rect.width - Display.get_global_width(self.TITLE // 8)
        self.close_btn.fill("Gray")

        pygame.draw.rect(self.close_btn, "Black", (0, 0, *rect_size), int(Display.get_global_width(2)))
        srf = draw_antialiased_x(Display.get_global_size(10, 10))
        rec = Display.center_object(self.close_btn, srf)
        self.close_btn.blit(srf, rec)
        self.window_box.blit(self.close_btn, self.close_btn_rect)

    def draw_max_btn(self) -> None:
        rect_size = Display.get_global_size(self.TITLE - self.TITLE / 4, self.TITLE - self.TITLE / 4)
        self.max_btn = Surface(rect_size)
        self.max_btn_rect = self.close_btn.get_rect()
        self.max_btn_rect.centery = self.title_bar_rect.centery
        self.max_btn_rect.right = self.title_bar_rect.width - Display.get_global_width(self.TITLE // 8 + (self.TITLE - self.TITLE // 4) + self.TITLE // 8)
        self.max_btn.fill("Gray")

        pygame.draw.rect(self.max_btn, "Black", (0, 0, *rect_size), int(Display.get_global_width(2)))
        srf = draw_rect(Display.get_global_size(10, 10))
        rec = Display.center_object(self.close_btn, srf)
        self.max_btn.blit(srf, rec)
        self.window_box.blit(self.max_btn, self.max_btn_rect)

    def draw_text(self) -> None:
        surf = self.res.render(self.TITLE - self.TITLE//4).render(self.title, "Black")
        rec = surf.get_rect(topleft=(0,0))
        self.window_box.blit(surf, rec)

    def draw(self) -> None:
        self.window_box = Surface(Display.get_global_size(self.width, self.height + self.TITLE))
        pos = self.parent.surface_display.get_rect().center if self.max else Display.get_global_size(self.pos[0], self.pos[1])
        self.window_rect = self.window_box.get_rect(center=pos)

        self.bg = Surface(Display.get_global_size(self.width, self.height))
        self.bg_rect = self.bg.get_rect(topleft = Display.get_global_size(0, self.TITLE))
        self.bg.fill("Gray")

        self.title_bar = Surface(Display.get_global_size(self.width, self.TITLE))
        self.title_bar_rect = self.title_bar.get_rect(topleft = (0, 0))
        self.title_bar.fill("Yellow")

        self.window_box.blit(self.bg, self.bg_rect)
        self.window_box.blit(self.title_bar, self.title_bar_rect)
        self.draw_text()
        self.draw_close_btn()
        self.draw_max_btn()

    def max_window(self):
        if self.max:
            self.width = self.parent.s_width
            self.height = self.parent.s_height - self.TITLE
        else:
            self.width = self.s_width
            self.height = self.s_height

    def render(self) -> None:
        self.draw()
        self.parent.surface_display.blit(self.window_box, self.window_rect)