from src.InputSystem.KeyCode import KeyCode
from src.Window import Window


class IndependenceWindow(Window):
    def __init__(self, width = 0, height = 0, title = "Window", full_key: KeyCode = KeyCode.K_F11) -> None:
        super().__init__(width, height, title)
        self.window_state = 0

        self.is_fullscreen = False
        self.full_key = full_key