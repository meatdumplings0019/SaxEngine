from src.Window.Embedded import EmbeddedWindow


class EmbeddedTestTwo(EmbeddedWindow):
    def __init__(self):
        super().__init__(640, 240, "Test2")