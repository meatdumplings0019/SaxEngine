from pygame import Surface

from src.Color import MColor
from src.Editor.Windows.Embedded.EmbeddedTest2 import EmbeddedTestTwo
from src.InputSystem import InputAction
from src.InputSystem.KeyCode import KeyCode
from src.Window.Independence import IndependenceWindow


class WindowTestTwo(IndependenceWindow):
    def __init__(self) -> None:
        super().__init__(720, 720, "test2")
        self.add("test1", EmbeddedTestTwo())
        self.open_children("test1")

    def handle_event(self, event: InputAction) -> None:
        super().handle_event(event)
        if event.IsKeyDown(KeyCode.K_1):
            self.parent.switch("test1")

    def render(self) -> None:
        super().render()
        font = Surface((400, 400))
        font.fill(MColor("yellow").to())
        rect = font.get_rect(topleft=(0, 0))
        self.box.blit(font, rect)