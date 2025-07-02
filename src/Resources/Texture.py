import pygame
from src.Resources import Resource


class TextureResource(Resource):
    @staticmethod
    def load_func(path):
        return pygame.image.load(path).convert_alpha()

    def __init__(self, path):
        super().__init__(path, self.load_func)