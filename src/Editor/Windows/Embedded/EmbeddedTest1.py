from src.Window.EmbeddedWindow import EmbeddedWindow


class EmbeddedTestOne(EmbeddedWindow):
    def __init__(self):
        super().__init__(720, 480, "Test1")