import pygame
from src.InputSystem import InputAction
from src.Libs.message import Message
from src.Manager import Manager
from src.Window import Window
from src.Window.DefaultWindow import DefaultWindow
from src.Window.EmptyWindow import EmptyWindow
from src.Window.IndependenceWindow import IndependenceWindow
from src.Window.WindowType import WindowType


class WindowManager(Manager):
    def __init__(self) -> None:
        super().__init__()
        self.current_window = DefaultWindow()
        self.windows = {}

    def add(self, name: str, value: Window) -> Message[bool]:
        if not name in self.windows.keys():
            try:
                if isinstance(value, IndependenceWindow):
                    return self.__add_independence_window(name, value)
                return Message(True)
            except Exception as e:
                return Message(False, e)

        return Message(False, f'{name} in!')

    def __add(self, _id, _type, value) -> Message[bool]:
        try:
            value.manager = self
            self.windows[_id] = {
                'type': _type,
                'value': value
            }
            return Message(True)
        except Exception as e:
            return Message(False, e)

    def __add_independence_window(self, _id, window: Window) -> Message[bool]:
        return self.__add(_id, WindowType.independence_window, window)

    def remove(self, name: str) -> Message[bool]:
        try:
            self.windows.pop(name)
            return Message(True)
        except Exception as e:
            return Message(False, e)

    def has(self, name: str) -> bool:
        return name in self.windows

    def get(self, name: str, _type: WindowType = WindowType.independence_window) -> Message[Window]:
        try:
            value = self.windows[name]
            if value.get('type') != _type:
                return Message(DefaultWindow())
            return Message(value.get('value'))
        except Exception as e:
            return Message(DefaultWindow(), e)

    def init(self):
        if not self.windows:
            self.add("empty", EmptyWindow())

        if isinstance(self.current_window, DefaultWindow):
            self.switch(list(self.windows.keys())[0])

    def switch(self, key) -> Message[bool]:
        try:
            self.current_window, _ = self.get(key, WindowType.independence_window)
            self.current_window.update_surface()
            self.set_window_size()
            return Message(True)
        except KeyError as e:
            self.current_window = DefaultWindow()
            self.current_window.update_surface()
            self.set_window_size()
            return Message(False, e)

    def enter(self) -> None:
        self.current_window.enter()

    def update(self) -> None:
        self.current_window.update()

    def render(self) -> None:
        self.current_window.render()

    def handle_event(self, event: InputAction) -> None:
        self.current_window.handle_event(event)
        if event.IsKeyDown(self.current_window.full_key):
            self.fullscreen()

    def exit(self) -> None:
        self.current_window.exit()

    def set_window_size(self):
        pygame.display.set_mode((self.current_window.width, self.current_window.height), self.current_window.window_state)
        pygame.display.set_caption(self.current_window.title)

        self.current_window.update_surface()

    def fullscreen(self):
        if self.current_window.is_fullscreen:
            self.current_window.return_size()
            self.current_window.window_state = 0
        else:
            self.current_window.width, self.current_window.height = Window.FULLSCREEN_SIZE
            self.current_window.window_state = pygame.NOFRAME

        self.current_window.is_fullscreen = not self.current_window.is_fullscreen

        self.set_window_size()