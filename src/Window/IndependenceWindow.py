import pygame
from src.InputSystem import InputAction
from src.InputSystem.KeyCode import KeyCode
from src.Libs.message import Message
from src.Manager.SceneManager import SceneManager
from src.Window import Window
from src.Window.EmbeddedWindow import EmbeddedWindow


class IndependenceWindow(Window):
    def __init__(self, width = 0, height = 0, title = "Window", full_key: KeyCode = KeyCode.K_F11) -> None:
        super().__init__(width, height, title)
        self.window_state = 0

        self.is_fullscreen = False
        self.full_key = full_key

        self.surface_display = pygame.display.get_surface()

        self.embedded_windows: dict[str, EmbeddedWindow] = {}

        self.scene_manager = SceneManager()
        self.scene_init()
        self.scene_manager.init()

    def scene_init(self) -> None: ...

    def update_surface(self) -> None:
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

    def handle_event(self, event: InputAction) -> None:
        self.scene_manager.handle_event(event)
        for i, w in self.embedded_windows.items():
            w.handle_event(event)

    def update(self) -> None:
        self.scene_manager.update()
        for i, w in self.embedded_windows.items():
            w.update()

    def afterRender(self) -> None: ...

    def render(self) -> None:
        self.scene_manager.render()

    def beforeRender(self) -> None:
        for i, w in self.embedded_windows.items():
            if w.active:
                w.render()

    def enter(self) -> None:
        self.scene_manager.enter()
        for i, w in self.embedded_windows.items():
            w.enter()

    def exit(self) -> None:
        self.scene_manager.exit()
        for i, w in self.embedded_windows.items():
            w.exit()

    def open_children(self, _id: str, pos = None, glo: bool = False) -> Message[bool]:
        if not pos:
            pos = self.width / 2, self.height / 2
            glo = True

        try:
            obj = self.embedded_windows[_id]
            obj.open(pos, glo)
            return Message(True)
        except Exception as e:
            return Message(False, e)