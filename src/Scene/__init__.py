from src.Surface import BaseSurface


class Scene(BaseSurface):
    def __init__(self) -> None:
        super().__init__()
        self.manager = None