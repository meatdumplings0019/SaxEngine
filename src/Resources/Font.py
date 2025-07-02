import pygame
from typing import Any
from pygame import font as pyfont, Surface
from src.Libs.display import Display
from src.Libs.types import color_type
from src.Resources import Resource

class FontAssets:
    def __init__(self, font: pyfont.Font) -> None:
        self.font = font

    def render(self, text: str, color: color_type = "white", bg: color_type | None = None) -> Surface:
        pygame.init()
        return self.font.render(text, True, color, bg)

class FontResource(Resource):
    @staticmethod
    def __load_func(path, size):
        return pyfont.Font(path, size)

    def __init__(self, path) -> None:
        self.font_size = 0
        super().__init__(path, self.__load_func)

    def get_value(self) -> Any:
        return self.func(self.path, self.font_size)

    def render(self, size: int) -> FontAssets:
        self.font_size = Display.get_global_height(size)
        return FontAssets(self.get_value())