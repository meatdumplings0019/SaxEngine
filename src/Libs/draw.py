import pygame
from pygame import Surface


def draw_antialiased_x(rect_c, color=(255, 0, 0), width=3) -> Surface:
    srf = Surface((rect_c[0], rect_c[1]), pygame.SRCALPHA)
    rect = srf.get_rect()

    pygame.draw.line(srf, color, rect.topleft, rect.bottomright, width)
    pygame.draw.line(srf, color, rect.topright, rect.bottomleft, width)

    return srf

def draw_rect(rect_c, color=(255, 0, 0), width=3) -> Surface:
    srf = pygame.Surface((rect_c[0], rect_c[1]), pygame.SRCALPHA)
    rect = srf.get_rect()

    pygame.draw.rect(srf, color, rect, width)

    return srf