from src.InputSystem import InputAction
from src.InputSystem.KeyCode import KeyCode
from src.Scene.Manager import SceneManager
from src.Window import Window


class IndependenceWindow(Window):
    def __init__(self, width = 0, height = 0, title = "Window", full_key: KeyCode = KeyCode.K_F11) -> None:
        super().__init__(width, height, title)
        self.window_state = 0

        self.is_fullscreen = False
        self.full_key = full_key

        self.scene_manager = SceneManager()
        self.scene_init()
        self.scene_manager.init()

    def scene_init(self) -> None: ...

    def update_surface(self) -> None:
        super().update_surface()
        self.scene_manager.update_surface()

    def handle_event(self, event: InputAction) -> None:
        super().handle_event(event)
        self.scene_manager.handle_event(event)

    def update(self) -> None:
        super().update()
        self.scene_manager.update()

    def render(self) -> None:
        super().render()
        self.scene_manager.render()

    def enter(self) -> None:
        super().enter()
        self.scene_manager.enter()

    def exit(self) -> None:
        super().exit()
        self.scene_manager.exit()