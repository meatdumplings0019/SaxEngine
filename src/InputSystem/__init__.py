import pygame
from typing import Generator, Any
from src.InputSystem.InputAction import InputAction


class InputSystem:
    def __init__(self):
        self.event = None

    def Get(self) -> Generator[InputAction, Any, None]:
        self.event = pygame.event.get()
        return (InputAction(event) for event in self.event)