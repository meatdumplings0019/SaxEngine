import pygame
from pygame import Rect

from src.Libs.Utils.types import vec2


class Display:
    default_size = 1280, 720
    @staticmethod
    def get_global_width(width, surface=None, size: tuple = default_size) -> int:
        if not surface:
            surface = pygame.display.get_surface()
        s_width, s_height = surface.get_size()
        return int(s_width / size[0] * width)

    @staticmethod
    def get_global_height(height, surface=None, size: tuple = default_size) -> int:
        if not surface:
            surface = pygame.display.get_surface()
        s_width, s_height = surface.get_size()
        return int(s_height / size[1] * height)

    @staticmethod
    def get_global_size(width, height, surface=None, size: tuple = default_size) -> vec2:
        return vec2(Display.get_global_width(width, surface, size), Display.get_global_height(height, surface, size))

    @staticmethod
    def get_return_width(width, surface=None, size: tuple = default_size) -> int:
        if not surface:
            surface = pygame.display.get_surface()
        s_width, s_height = surface.get_size()
        return int(size[0] / s_width * width)

    @staticmethod
    def get_return_height(height, surface=None, size: tuple = default_size) -> int:
        if not surface:
            surface = pygame.display.get_surface()
        s_width, s_height = surface.get_size()
        return int(size[1] / s_height * height)

    @staticmethod
    def get_return_size(width, height, surface=None, size: tuple = default_size) -> vec2:
        return vec2(Display.get_return_width(width, surface, size), Display.get_return_height(height, surface, size))

    @staticmethod
    def center_object(parent_surface, child_surface) -> Rect:
        parent_rect = parent_surface.get_rect()
        child_rect = child_surface.get_rect()
        child_rect.center = parent_rect.center
        return child_rect

    @staticmethod
    def get_global_rect(child_rect: Rect, parent_rect: Rect) -> Rect:
        child_pos = vec2(parent_rect.topleft) + vec2(child_rect.topleft)
        return Rect(child_pos.x, child_pos.y, child_rect.width, child_rect.height)