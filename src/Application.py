import os
import sys
import pygame

from src.InputSystem import InputSystem
from src.Manager.WindowManager import WindowManager

os.environ['SDL_VIDEO_CENTERED'] = '1'

class Application:
    def __init__(self, main: str):
        pygame.init()

        self.window_manager = WindowManager()
        self.window_init()
        self.window_manager.switch(main)

        self.input_system = InputSystem()

        self.surface_display = pygame.display.get_surface()
        self.clock = pygame.time.Clock()

    def window_init(self):
        ...

    def handle_event(self):
        for event in self.input_system.Get():
            if event.IsQuit():
                pygame.quit()
                sys.exit()
            self.window_manager.handle_event(event)

    def update(self):
        self.clock.tick(60)
        self.surface_display.fill("black")
        self.window_manager.update()
        self.window_manager.render()
        pygame.display.update()

    def run(self):
        self.window_manager.enter()
        while True:
            self.handle_event()
            self.update()