import pygame
from src.Resources import Resource


class TextureResource(Resource):
    @staticmethod
    def load_func(path) -> pygame.Surface:
        return pygame.image.load(path)

    def __init__(self, path) -> None:
        super().__init__(path, self.load_func)