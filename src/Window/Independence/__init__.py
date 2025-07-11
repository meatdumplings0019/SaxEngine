from pygame import Surface

from src.InputSystem import InputAction
from src.InputSystem.KeyCode import KeyCode
from src.Libs.Utils import Message
from src.Libs.Window.display import Display
from src.Window import Window
from src.Window.Embedded import EmbeddedWindow


class IndependenceWindow(Window):
    TITLE = 25
    def __init__(self, width = 0, height = 0, title = "Window", icon=None, full_key: KeyCode = KeyCode.K_F11) -> None:
        super().__init__(width, height - self.TITLE, title, icon, (width, height))
        self._y = self.TITLE

        self.window_state = 0

        self.is_fullscreen = False
        self.full_key = full_key

        self.embedded_windows: dict[str, EmbeddedWindow] = {}

        self.topbar = Surface((self.width, self.TITLE))
        self.topbar_rect = self.topbar.get_rect()
        self.topbar.fill("Blue")

    def add(self, _id, _val: EmbeddedWindow) -> Message[bool]:
        if not _id in self.embedded_windows:
            try:
                _val.parent = self
                self.embedded_windows[_id] = _val
                for i, w in self.embedded_windows.keys():
                    if not w.parent is self:
                        self.embedded_windows.pop(i)

                return Message(True)
            except Exception as e:
                return Message(False, e)

        return Message(False, f"{_id} in")

    def handle_event(self, event: InputAction) -> None:
        super().handle_event(event)
        for i, w in self.embedded_windows.items():
            w.handle_event(event)

    def update(self) -> None:
        super().update()
        for i, w in self.embedded_windows.items():
            w.update()

    def beforeRender(self) -> None:
        for i, w in self.embedded_windows.items():
            if w.active:
                w.afterRender()
                w.render()
                w.beforeRender()
        super().beforeRender()

    def enter(self) -> None:
        super().enter()
        for i, w in self.embedded_windows.items():
            w.enter()

    def exit(self) -> None:
        super().exit()
        for i, w in self.embedded_windows.items():
            w.exit()

    def open_children(self, _id: str, x=None, y=None) -> Message[bool]:
        if not x:
            x = self.width / 2
        if not y:
            y = self.height / 2

        try:
            obj = self.embedded_windows[_id]
            obj.open(x, y)
            return Message(True)
        except Exception as e:
            return Message(False, e)

    def render(self) -> None:
        super().render()
        self.topbar = Surface((self.w_width, Display.get_global_height(self.TITLE, size=(self.s_width, self.s_height))))
        self.topbar_rect = self.topbar.get_rect()
        self.topbar.fill("Green")
        self.surface_display.blit(self.topbar, self.topbar_rect)