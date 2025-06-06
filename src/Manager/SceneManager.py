﻿from src.InputSystem import InputAction
from src.Libs.message import Message
from src.Manager import Manager
from src.Scene import Scene
from src.Scene.DefaultScene import DefaultScene
from src.Scene.EmptyScene import EmptyScene


class SceneManager(Manager):
    def __init__(self) -> None:
        super().__init__()
        self.current_scene = DefaultScene()
        self.scenes = {}
        
    def add(self, name: str, value: Scene) -> Message[bool]:
        if not name in self.scenes.keys():
            try:
                value.manager = self
                self.scenes[name] = value
                return Message(True)
            except Exception as e:
                return Message(False, e)

        return Message(False, f'{name} in!')

    def remove(self, name: str) -> Message[bool]:
        try:
            self.scenes.pop(name)
            return Message(True)
        except Exception as e:
            return Message(False, e)

    def has(self, name: str) -> bool:
        return name in self.scenes

    def get(self, name: str) -> Message[Scene]:
        try:
            return Message(self.scenes[name])
        except Exception as e:
            return Message(DefaultScene(), e)

    def init(self) -> None:
        if not self.scenes:
            self.add("empty", EmptyScene())

        if isinstance(self.current_scene, DefaultScene):
            self.switch(list(self.scenes.keys())[0])
    
    def switch(self, key) -> Message[bool]:
        try:
            self.current_scene.enter()
            self.current_scene, _ = self.get(key)
            self.current_scene.update_surface()
            self.current_scene.exit()
            return Message(True)
        except KeyError as e:
            self.current_scene.enter()
            self.current_scene = DefaultScene()
            self.current_scene.update_surface()
            self.current_scene.exit()
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

    def update_surface(self) -> None:
        self.current_scene.update_surface()