﻿from pygame import Surface
from src.Editor.Windows.Embedded.EmbeddedTest1 import EmbeddedTestOne
from src.InputSystem import InputAction
from src.InputSystem.KeyCode import KeyCode
from src.Libs.display import Display
from src.Window.IndependenceWindow import IndependenceWindow


class WindowTestOne(IndependenceWindow):
    def __init__(self) -> None:
        super().__init__(1280, 720, "test1")
        self.add("test1", EmbeddedTestOne())
        self.open_children("test1")

    def handle_event(self, event: InputAction) -> None:
        super().handle_event(event)
        if event.IsKeyDown(KeyCode.K_2):
            self.manager.switch("test2")

    def render(self):
        super().render()
        font = Surface(Display.get_global_size(400, 400))
        font.fill("Blue")
        rect = font.get_rect(topleft=(0, 0))
        self.surface_display.blit(font, rect)