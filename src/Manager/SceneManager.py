from src.InputSystem import InputAction
from src.Libs.message import Message
from src.Manager import Manager
from src.Scene import Scene
from src.Scene.DefaultScene import DefaultScene


class SceneManager(Manager):
    def __init__(self) -> None:
        super().__init__()
        self.current_scene = DefaultScene()
        self.scenes = {}
        
    def add(self, name: str, value: Scene) -> Message[bool]:
        try:
            var = self.scenes[name]
            return Message(False, f'{name} in!')
        except KeyError:
            try:
                value.manager = self
                self.scenes[name] = value
                return Message(True)
            except Exception as e:
                return Message(False, e)

    def remove(self, name: str) -> Message[bool]:
        try:
            self.scenes.pop(name)
            return Message(True)
        except Exception as e:
            return Message(False, e)

    def has(self, name: str) -> bool:
        return name in self.scenes
    
    def switch(self, key) -> Message[bool]:
        try:
            self.current_scene = self.scenes[key]
            self.current_scene.update_surface()
            return Message(True)
        except KeyError as e:
            self.current_scene = DefaultScene()
            self.current_scene.update_surface()
            return Message(False, e)
        
    def enter(self) -> None:
        self.current_scene.enter()

    def update(self) -> None:
        self.current_scene.update()

    def render(self) -> None:
        self.current_scene.render()

    def handle_event(self, event: InputAction) -> None:
        self.current_scene.handle_event(event)

    def exit(self) -> None:
        self.current_scene.exit()