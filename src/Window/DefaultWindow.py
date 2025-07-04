from src.Window.IndependenceWindow import IndependenceWindow


class DefaultWindow(IndependenceWindow):
    def __init__(self) -> None:
        super().__init__(1280, 720, "Error Window")