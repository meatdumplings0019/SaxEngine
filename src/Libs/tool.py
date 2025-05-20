import pygame

from src.Libs.types import color_type


def draw_text(text, font: str, size: int = 30, color: color_type = 'white', x: int = 0, y: int = 0) -> None:
    pygame.init()
    surface_display = pygame.display.get_surface()
    font_surface = pygame.font.Font(font, size)
    surface = font_surface.render(str(text), True, color)
    rect = surface.get_rect(topleft=(x, y))
    surface_display.blit(surface, rect)