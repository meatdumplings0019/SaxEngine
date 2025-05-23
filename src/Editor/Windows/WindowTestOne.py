import pygame
from pygame import Surface

from src.InputSystem import InputAction
from src.Libs.display import Display
from src.Resources.Font import FontResource
from src.Window import Window


class WindowTestOne(Window):
    def __init__(self) -> None:
        super().__init__(1280, 720, "test1")

    def handle_event(self, event: InputAction) -> None:
        if event.IsKeyDown(pygame.K_2):
            self.manager.switch("test2")

    def render(self):
        font = Surface(Display.get_global_size(400, 400))
        font.fill("Blue")
        rect = font.get_rect(topleft=(0, 0))
        self.surface_display.blit(font, rect)