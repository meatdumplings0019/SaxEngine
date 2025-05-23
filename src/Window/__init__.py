import pygame
from src.InputSystem import InputAction
from src.Libs.resolution import get_window_resolution
from src.Manager.SceneManager import SceneManager


class Window:
    FULLSCREEN_SIZE = get_window_resolution()
    def __init__(self, width = 0, height = 0, title = "Window") -> None:
        self.manager = None
        self._width = width
        self._height = height
        self.width = self._width
        self.height = self._height
        self.title = title

        self.scene_manager = SceneManager()
        self.scene_init()
        self.scene_manager.init()

    def scene_init(self): ...

    def return_size(self):
        self.width = self._width
        self.height = self._height

    def handle_event(self, event: InputAction):
        self.scene_manager.handle_event(event)

    def update(self):
        self.scene_manager.update()

    def render(self):
        self.scene_manager.render()

    def enter(self):
        self.scene_manager.enter()

    def exit(self):
        self.scene_manager.exit()