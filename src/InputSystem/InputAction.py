﻿import pygame
from pygame import Rect
from src.InputSystem.KeyCode import KeyCode
from src.Libs.types import vec2


class InputAction:
    def __init__(self, event: pygame.event.Event):
        self.event = event

    def IsQuit(self) -> bool:
        return self.event.type == pygame.QUIT

    def IsKeyDown(self, key: KeyCode) -> bool:
        if self.event.type == pygame.KEYDOWN:
            return self.event.key == key.value

        return False

    def IsKeyUp(self, key: KeyCode) -> bool:
        if self.event.type == pygame.KEYUP:
            return self.event.key == key.value

        return False

    def IsMouseDown(self, button: int = 1) -> bool:
        if self.event.type == pygame.MOUSEBUTTONDOWN:
            return self.event.button == button

        return False

    def IsMouseUp(self, button: int = 1) -> bool:
        if self.event.type == pygame.MOUSEBUTTONUP:
            return self.event.button == button

        return False

    @staticmethod
    def GetMousePosition() -> vec2:
        return vec2(pygame.mouse.get_pos())

    def IsMouseWheel(self, wheel: int = 0) -> bool:
        if self.event.type == pygame.MOUSEWHEEL:
            if wheel == 0:
                return True
            elif wheel > 0 and self.event.y > 0:
                return True
            elif wheel < 0 and self.event.y < 0:
                return True
        return False

    def GetMouseWheel(self) -> int:
        if self.event.type == pygame.MOUSEWHEEL:
            return self.event.y

        return 0

    def IsBtnDown(self, rect: Rect, btn: int = 1) -> bool:
        if self.IsMouseDown(btn):
            return rect.collidepoint(self.event.pos)

        return False

    def IsBtnUp(self, rect: Rect, btn: int = 1) -> bool:
        if self.IsMouseUp(btn):
            return rect.collidepoint(self.event.pos)

        return False

    def IsMouseMotion(self) -> bool:
        return self.event.type == KeyCode.MOUSEMOTION.value