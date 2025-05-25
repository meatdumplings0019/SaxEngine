from src.Libs.resolution import get_window_resolution

class Window:
    FULLSCREEN_SIZE = get_window_resolution()
    def __init__(self, width = 0, height = 0, title = "Window") -> None:
        self.manager = None
        self.s_width = width
        self.s_height = height
        self.width = self.s_width
        self.height = self.s_height
        self.title = title

    def return_size(self) -> None:
        self.width = self.s_width
        self.height = self.s_height