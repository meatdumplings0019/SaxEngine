import pygame
from src.InputSystem import InputAction
from src.Surface import BaseSurface


class Scene(BaseSurface):
    def __init__(self) -> None:
        self.manager = None

        self.surface_display = pygame.display.get_surface()

    def update_surface(self) -> None:
        self.surface_display = pygame.display.get_surface()

    def handle_event(self, event: InputAction) -> None: ...
    def update(self) -> None:...
    def render(self) -> None: ...
    def enter(self) -> None: ...
    def exit(self) -> None: ...