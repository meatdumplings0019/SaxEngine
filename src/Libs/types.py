from typing import Sequence
from pygame import Color, Vector2, Vector3

color_type = Color | int | str | tuple[int, int, int] | tuple[int, int, int, int] | Sequence[int]
vec2 = Vector2
vec3 = Vector3