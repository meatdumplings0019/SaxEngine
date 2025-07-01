import pygame

from src.Libs.tool import Tool
from src.Libs.window import WindowUtils

WindowUtils.center()

class Application:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Sax Engine')
        pygame.display.set_mode((1280, 720))

        self.surface_display = pygame.display.get_surface()

        self.clock = pygame.time.Clock()

    @staticmethod
    def handle_events():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Tool.exit()

    def update(self):
        ...

    def run(self):
        while True:
            self.handle_events()
            self.update()