from src.Libs.resolution import get_window_resolution

class Window:
    FULLSCREEN_SIZE = get_window_resolution()
    def __init__(self, width = 0, height = 0, title = "Window") -> None:
        self.manager = None
        self._width = width
        self._height = height
        self.width = self._width
        self.height = self._height
        self.title = title

    def return_size(self) -> None:
        self.width = self._width
        self.height = self._height