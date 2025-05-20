import pygame
from src.InputSystem import InputAction
from src.InputSystem.KeyCode import KeyCode
from src.Libs.resolution import get_window_resolution

class Window:
    FULLSCREEN_SIZE = get_window_resolution()
    def __init__(self, width = 0, height = 0, title = "Window", full_key: int=KeyCode.K_F11) -> None:
        self.manager = None
        self._width = width
        self._height = height
        self.width = self._width
        self.height = self._height
        self.title = title
        self.window_state = 0

        self.is_fullscreen = False
        self.full_key = full_key

        self.surface_display = pygame.display.get_surface()

    def update_surface(self):
        self.surface_display = pygame.display.get_surface()

    def return_size(self):
        self.width = self._width
        self.height = self._height

    def handle_event(self, event: InputAction): ...
    def update(self):...
    def render(self): ...
    def enter(self): ...
    def exit(self): ...