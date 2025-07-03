from typing import Union, Tuple

import pygame
from pygame import Vector2, Vector3

from src.Color import MColor

ColorType = Union[
    Tuple[int, int, int],          # RGB
    Tuple[int, int, int, int],     # RGBA
    pygame.Color,                  # Pygame 原生颜色
    MColor,                        # 增强颜色对象
    str                            # 颜色名称或十六进制值
]

vec2 = Vector2
vec3 = Vector3