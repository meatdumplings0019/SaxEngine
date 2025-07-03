import pygame
from pygame import Surface

from src.Color import MColor


class FontAssets:
    def __init__(self, font: pygame.font.Font) -> None:
        self.font = font

    def render(self, text: str, color: MColor = "white", bg: MColor | None = None) -> Surface:
        pygame.init()
        return self.font.render(text, True, color.to(), bg)