import pygame

from src.InputSystem import InputSystem
from src.Libs.tool import Tool
from src.Libs.window import WindowUtils
from src.Window.Manager import WindowManager

WindowUtils.center()

class Application:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Sax Engine')
        pygame.display.set_mode((1280, 720))

        self.input_system = InputSystem()

        self.window_manager = WindowManager()

        self.surface_display = pygame.display.get_surface()
        self.clock = pygame.time.Clock()

    def handle_events(self):
        for event in self.input_system.Get():
            if event.quit:
                Tool.exit()
            self.window_manager.handle_events()

    def update(self):
        self.clock.tick(60)
        self.window_manager.update()
        self.window_manager.render()
        self.surface_display.fill("black")
        pygame.display.update()

    def run(self):
        while True:
            self.handle_events()
            self.update()