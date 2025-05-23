from src.Scene.DefaultScene import DefaultScene
from src.Window import Window


class DefaultWindow(Window):
    def __init__(self):
        super().__init__(1280, 720, "Error Window")

    def scene_init(self):
        super().scene_init()
        self.scene_manager.add("empty", DefaultScene("This is a default window.", "Your window may make a mistake."))