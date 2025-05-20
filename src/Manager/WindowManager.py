import pygame

from src.InputSystem import InputAction
from src.Lib.message import Message
from src.Manager import Manager
from src.Window import Window
from src.Window.DefaultWindow import DefaultWindow

class WindowManager(Manager):
    def __init__(self) -> None:
        super().__init__()
        self.current_window = DefaultWindow()
        self.errmsg = None
        self.windows = {}

    def add(self, name: str, value: Window) -> Message[bool]:
        try:
            var = self.windows[name]
            return Message(False, f'{name} in!')
        except KeyError:
            try:
                value.manager = self
                self.windows[name] = value
                return Message(True)
            except Exception as e:
                return Message(False, e)

    def switch(self, key) -> Message[bool]:
        try:
            self.current_window = self.windows[key]
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