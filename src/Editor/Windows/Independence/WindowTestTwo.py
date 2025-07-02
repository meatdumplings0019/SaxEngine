from pygame import Surface

from src.Color import MColor
from src.InputSystem import InputAction
from src.InputSystem.KeyCode import KeyCode
from src.Window.IndependenceWindow import IndependenceWindow


class WindowTestTwo(IndependenceWindow):
    def __init__(self) -> None:
        super().__init__(720, 720, "test2")

    def handle_event(self, event: InputAction) -> None:
        if event.IsKeyDown(KeyCode.K_1):
            self.manager.switch("test1")

    def render(self):
        font = Surface((400, 400))
        font.fill(MColor("yellow").to())
        rect = font.get_rect(topleft=(0, 0))
        self.surface_display.blit(font, rect)