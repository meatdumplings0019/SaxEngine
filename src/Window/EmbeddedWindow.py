import pygame
from pygame import Surface

from src.Libs.display import Display
from src.Resources.Font import FontResource
from src.Window import Window

class EmbeddedWindow(Window):
    TITLE = 20
    def __init__(self, width: int = 0,
             height: int = 0,
             title: str = "Window"):
        super().__init__(width, height, title)
        from src.Window.IndependenceWindow import IndependenceWindow
        self.parent: IndependenceWindow | None = None
        self.active: bool = False
        self.pos = self.width / 2, self.height / 2
        self.window_box = Surface((width, height + self.TITLE))
        self.window_rect = self.window_box.get_rect()

        self.bg = Surface((self.width, self.height))
        self.bg_rect = self.bg.get_rect(topleft = (0, self.TITLE))
        self.bg.fill("Gray")

        self.title_bar = Surface((self.width, self.TITLE))
        self.title_bar_rect = self.title_bar.get_rect(topleft = (0, 0))
        self.title_bar.fill("Yellow")

        self.res = FontResource("./Assets/Fonts/JeTBrainsMono.ttf")

    def init(self):
        self.pos = (1280 / 2, 720 / 2)

    def open(self):
        self.active = True

    def close(self):
        self.active = False

    def enter(self):
        self.init()

    def exit(self):
        ...

    def draw_text(self):
        surf = self.res.render(self.TITLE - self.TITLE//4).render(self.title, "Black")
        rec = surf.get_rect(topleft=(0,0))
        self.window_box.blit(surf, rec)

    def draw(self):
        self.window_box = Surface(Display.get_global_size(self.width, self.height + self.TITLE))
        self.window_rect = self.window_box.get_rect(center=Display.get_global_size(self.pos[0], self.pos[1]))

        self.bg = Surface(Display.get_global_size(self.width, self.height))
        self.bg_rect = self.bg.get_rect(topleft = Display.get_global_size(0, self.TITLE))
        self.bg.fill("Gray")

        self.title_bar = Surface(Display.get_global_size(self.width, self.TITLE))
        self.title_bar_rect = self.title_bar.get_rect(topleft = (0, 0))
        self.title_bar.fill("Yellow")

        self.window_box.blit(self.bg, self.bg_rect)
        self.window_box.blit(self.title_bar, self.title_bar_rect)
        self.draw_text()

    def render(self):
        self.draw()
        self.parent.surface_display.blit(self.window_box, self.window_rect)