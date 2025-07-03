from typing import Any

import pygame

from src.Libs.display import Display
from src.Resources import Resource
from src.Resources.Font import FontAssets


class SysFontResource(Resource):
    @staticmethod
    def __load_func(font, size):
        return pygame.font.SysFont(font, size)

    def __init__(self, font) -> None:
        self.font_size = 0
        super().__init__(font, self.__load_func)

    def get_value(self) -> Any:
        return self.func(self.path, self.font_size)

    def render(self, size: int) -> FontAssets:
        self.font_size = Display.get_global_height(size)
        return FontAssets(self.get_value())