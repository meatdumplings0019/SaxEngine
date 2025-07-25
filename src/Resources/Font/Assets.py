﻿import pygame
from pygame import Surface

from src.Libs.Utils.types import ColorType


class FontAssets:
    def __init__(self, font: pygame.font.Font) -> None:
        self.font = font

    def render(self, text: str, color: ColorType = "white", bg: ColorType = None) -> Surface:
        pygame.init()
        return self.font.render(text, True, color, bg)