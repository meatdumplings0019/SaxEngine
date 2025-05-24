import pygame
from src.InputSystem import InputAction
from src.InputSystem.KeyCode import KeyCode
from src.Libs.message import Message
from src.Manager.SceneManager import SceneManager
from src.Window import Window
from src.Window.EmbeddedWindow import EmbeddedWindow


class IndependenceWindow(Window):
    def __init__(self, width = 0, height = 0, title = "Window", full_key: KeyCode = KeyCode.K_F11):
        super().__init__(width, height, title)
        self.window_state = 0

        self.is_fullscreen = False
        self.full_key = full_key

        self.surface_display = pygame.display.get_surface()

        self.embedded_windows: dict[str, EmbeddedWindow] = {}

        self.scene_manager = SceneManager()
        self.scene_init()
        self.scene_manager.init()

    def scene_init(self):
        ...

    def update_surface(self):
        self.surface_display = pygame.display.get_surface()
        self.scene_manager.update_surface()

    def add(self, _id, _val: EmbeddedWindow) -> Message[bool]:
        if not _id in self.embedded_windows:
            try:
                _val.parent = self
                self.embedded_windows[_id] = _val
                # for i, w in self.embedded_windows.keys():
                    # if not w.parent is self:
                    #     self.embedded_windows.pop(i)

                return Message(True)
            except Exception as e:
                return Message(False, e)

        return Message(False, f"{_id} in")

    def handle_event(self, event: InputAction):
        self.scene_manager.handle_event(event)

    def update(self):
        self.scene_manager.update()

    def render(self):
        self.scene_manager.render()
        for i, w in self.embedded_windows.items():
            if w.active:
                w.render()

    def enter(self):
        self.scene_manager.enter()
        for i, w in self.embedded_windows.items():
            w.enter()

    def exit(self):
        self.scene_manager.exit()
        for i, w in self.embedded_windows.items():
            w.exit()