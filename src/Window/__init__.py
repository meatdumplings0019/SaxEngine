from src.Surface.CustomizeSurface import CustomizeSurface


class Window(CustomizeSurface):
    def __init__(self, width=0, height=0, title="Window", icon=None) -> None:
        super().__init__((width, height))
        self.title = title
        self.icon = icon