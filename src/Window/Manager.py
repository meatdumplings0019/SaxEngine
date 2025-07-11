import pygame
from pygame import Rect

from src.InputSystem import InputAction
from src.Libs.Utils import Message
from src.Libs.Window.resolution import Resolution_
from src.Manager import Manager
from src.Surface.Base.DisplaySurface import DisplaySurface
from src.Window import Window
from src.Window.Independence import IndependenceWindow
from src.Window.Independence.DefaultWindow import DefaultWindow
from src.Window.Independence.EmptyWindow import EmptyWindow


class WindowManager(Manager, DisplaySurface):
    def __init__(self) -> None:
        super().__init__()
        super(Manager, self).__init__()
        self.current_window = DefaultWindow()
        self.windows: dict[str, IndependenceWindow] = {}

    def add(self, name: str, value: Window) -> Message[bool]:
        if not name in self.windows.keys():
            try:
                return self.__add(name, value)
            except Exception as e:
                return Message(False, e)

        return Message(False, f'{name} in!')

    def __add(self, _id, _val) -> Message[bool]:
        if isinstance(_val, IndependenceWindow):
            _val.parent = self
            self.windows[_id] = _val
            return Message(True)

        return Message(False)

    def remove(self, name: str) -> Message[bool]:
        try:
            self.windows.pop(name)
            return Message(True)
        except Exception as e:
            return Message(False, e)

    def has(self, name: str) -> bool:
        return name in self.windows

    def get(self, name: str) -> Message[Window]:
        try:
            return Message(self.windows[name])
        except Exception as e:
            return Message(DefaultWindow(), e)

    def init(self) -> None:
        if not self.windows:
            self.add("empty", EmptyWindow())

        if isinstance(self.current_window, DefaultWindow):
            self.switch(list(self.windows.keys())[0])

    def switch(self, key) -> Message[bool]:
        try:
            self.current_window.exit()
            self.current_window, _ = self.get(key)
            self.set_window_size()
            self.current_window.enter()
            return Message(True)
        except KeyError as e:
            self.current_window.exit()
            self.current_window = DefaultWindow()
            self.set_window_size()
            self.current_window.enter()
            return Message(False, e)

    def enter(self) -> None:
        self.current_window.enter()

    def update(self) -> None:
        self.current_window.update()

    def render(self) -> None:
        self.current_window.afterRender()
        self.current_window.render()
        self.current_window.beforeRender()

    def handle_event(self, event: InputAction) -> None:
        self.current_window.handle_event(event)
        if event.IsKeyDown(self.current_window.full_key):
            self.fullscreen()

    def exit(self) -> None:
        self.current_window.exit()

    def get_center_box(self) -> Rect:
        return self.surface_display.get_rect()

    def set_window_size(self) -> None:
        pygame.display.set_mode((self.current_window.w_width, self.current_window.w_height), self.current_window.window_state)
        pygame.display.set_caption(self.current_window.title)

        self.update_surface()

    def fullscreen(self) -> None:
        if self.current_window.is_fullscreen:
            self.current_window.return_size()
            self.current_window.window_state = 0
        else:
            self.current_window.w_width, self.current_window.w_height = Resolution_.windowResolution
            self.current_window.window_state = pygame.NOFRAME

        self.current_window.is_fullscreen = not self.current_window.is_fullscreen

        self.set_window_size()