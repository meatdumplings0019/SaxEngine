import pygame
from typing import Any

from src.Libs.Window.display import Display
from src.Resources import Resource
from src.Resources.Font.Assets import FontAssets


class FontResource(Resource):
    @staticmethod
    def __load_func(path, size) -> pygame.font.Font:
        return pygame.font.Font(path, size)

    def __init__(self, path) -> None:
        self.font_size = 0
        super().__init__(path, self.__load_func)

    def get_value(self) -> Any:
        return self.func(self.path, self.font_size)

    def render(self, size: int) -> FontAssets:
        self.font_size = Display.get_global_height(size)
        return FontAssets(self.get_value())