import pygame

class Display:
    default_size = 1280, 720
    @staticmethod
    def get_global_width(width) -> int:
        s_width, s_height = pygame.display.get_window_size()
        return int(s_width / Display.default_size[0] * width)

    @staticmethod
    def get_global_height(height) -> int:
        s_width, s_height= pygame.display.get_window_size()
        return int(s_height / Display.default_size[1] * height)

    @staticmethod
    def get_global_size(width, height) -> tuple[int, int]:
        return Display.get_global_width(width), Display.get_global_height(height)