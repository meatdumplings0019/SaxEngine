import pygame
from pygame import Surface
from src.InputSystem import InputAction
from src.Window import Window


class WindowTestTwo(Window):
    def __init__(self) -> None:
        super().__init__(720, 720, "test2")

    def handle_event(self, event: InputAction) -> None:
        if event.IsKeyDown(pygame.K_1):
            self.manager.switch("test11")

    def render(self):
        font = Surface((400, 400))
        font.fill("Yellow")
        rect = font.get_rect(topleft=(0, 0))
        self.surface_display.blit(font, rect)