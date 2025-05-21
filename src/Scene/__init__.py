import pygame
from src.InputSystem import InputAction

class Scene:
    def __init__(self) -> None:
        self.manager = None

        self.surface_display = pygame.display.get_surface()

    def update_surface(self):
        self.surface_display = pygame.display.get_surface()

    def handle_event(self, event: InputAction): ...
    def update(self):...
    def render(self): ...
    def enter(self): ...
    def exit(self): ...