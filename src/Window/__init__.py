from src.Surface import BaseSurface


class Window(BaseSurface):
    def __init__(self, width=0, height=0, title="Window", icon=None) -> None:
        super().__init__()
        self.manager = None
        self.s_width = width
        self.s_height = height
        self.width = self.s_width
        self.height = self.s_height
        self.title = title
        self.icon = icon

    def return_size(self) -> None:
        self.width = self.s_width
        self.height = self.s_height