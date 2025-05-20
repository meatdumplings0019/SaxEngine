import pygame

from src.InputSystem.InputAction import InputAction


class InputSystem:
    def __init__(self):
        self.event = None

    def Get(self):
        self.event = pygame.event.get()
        return (InputAction(event) for event in self.event)