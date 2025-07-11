from src.Surface.Base.CustomizeSurface import CustomizeSurface


class Window(CustomizeSurface):
    def __init__(self, width=0, height=0, title="Window", icon=None, base_size=None) -> None:
        super().__init__(base_size, (width, height))
        self.title = title
        self.icon = icon

        self.w_width = self.s_width
        self.w_height = self.s_height

    def return_size(self) -> None:
        self.w_width = self.s_width
        self.w_height = self.s_height