import pygame
from src.InputSystem import InputAction
from src.InputSystem.KeyCode import KeyCode
from src.Libs.resolution import get_window_resolution
from src.Manager.SceneManager import SceneManager
from src.Scene.EmptyScene import EmptyScene


class Window:
    FULLSCREEN_SIZE = get_window_resolution()
    def __init__(self, width = 0, height = 0, title = "Window", full_key: int=KeyCode.K_F11) -> None:
        self.manager = None
        self._width = width
        self._height = height
        self.width = self._width
        self.height = self._height
        self.title = title
        self.window_state = 0

        self.is_fullscreen = False
        self.full_key = full_key

        self.scene_manager = SceneManager()
        self.scene_manager.add("empty", EmptyScene())
        self.scene_init()
        if self.scene_manager.has("empty"):
            self.scene_manager.switch("empty")

        self.surface_display = pygame.display.get_surface()

    def scene_init(self):
        self.scene_manager.remove("empty")

    def update_surface(self):
        self.surface_display = pygame.display.get_surface()

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