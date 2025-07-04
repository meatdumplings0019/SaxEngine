import pygame

from src.InputSystem import InputSystem
from src.Libs.tool import Tool
from src.Libs.window import WindowUtils
from src.Window.Manager import WindowManager

WindowUtils.center()

class Application:
    def __init__(self, main: str) -> None:
        pygame.init()

        self.window_manager = WindowManager()
        self.window_init()
        self.window_manager.switch(main)
        self.window_manager.init()

        self.input_system = InputSystem()

        self.surface_display = pygame.display.get_surface()
        self.clock = pygame.time.Clock()

    def window_init(self) -> None: ...

    def handle_events(self) -> None:
        for event in self.input_system.Get():
            if event.quit:
                Tool.exit()
            self.window_manager.handle_event(event)

    def update(self) -> None:
        self.clock.tick(60)
        self.surface_display.fill("black")
        self.window_manager.update()
        self.window_manager.render()
        pygame.display.update()

    def run(self) -> None:
        self.window_manager.enter()
        while True:
            self.handle_events()
            self.update()