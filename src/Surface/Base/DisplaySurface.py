import pygame

from src.Surface.Base import BaseSurface


class DisplaySurface(BaseSurface):
    def __init__(self) -> None:
        self.surface_display = pygame.display.get_surface()

    def update_surface(self) -> None:
        self.surface_display = pygame.display.get_surface()