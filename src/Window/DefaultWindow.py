from src.Scene.DefaultScene import DefaultScene
from src.Window.IndependenceWindow import IndependenceWindow


class DefaultWindow(IndependenceWindow):
    def __init__(self) -> None:
        super().__init__(1280, 720, "Error Window")

    def scene_init(self) -> None:
        super().scene_init()
        self.scene_manager.add("empty", DefaultScene("This is a default window.", "Your window may make a mistake."))