from src.Window.EmbeddedWindow import EmbeddedWindow


class EmbeddedTestOne(EmbeddedWindow):
    def __init__(self):
        super().__init__(400, 200, "Test1")
        self.open()
        print(1)