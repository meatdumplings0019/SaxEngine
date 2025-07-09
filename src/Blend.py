import pygame
from pygame import Surface

from src.Libs.Utils.types import ColorType


class Blend:
    @staticmethod
    def multiply(surface: Surface, color: ColorType):
        """
        将 surface 的每个像素颜色与指定颜色相乘

        参数:
            surface (pygame.Surface): 要处理的图像表面
            color (tuple or str): 混合颜色，支持格式:
                - (R, G, B) 元组 (0-255)
                - (R, G, B, A) 元组 (0-255)
                - 颜色名称字符串 (如 "red")

        返回:
            pygame.Surface: 处理后的新表面（保留原始格式）
        """
        # 将颜色统一转换为 RGBA 元组
        def get_color(f, c):
            if f // 255 == 0:
                return c

            return (f * c) // 255


        if isinstance(color, str):
            color_obj = pygame.Color(color)
            blend_color = (color_obj.r, color_obj.g, color_obj.b, color_obj.a)
        elif isinstance(color, tuple):
            if len(color) == 3:
                blend_color = color + (255,)  # 添加不透明 alpha
            elif len(color) == 4:
                blend_color = color
            else:
                raise ValueError("Color tuple must have 3 (RGB) or 4 (RGBA) elements")
        else:
            raise TypeError("Color must be tuple or string")

        # 创建目标表面（保留原始格式和透明度）
        result = surface.copy()

        # 锁定表面以便像素级操作
        result.lock()

        # 遍历每个像素
        for x in range(result.get_width()):
            for y in range(result.get_height()):
                # 获取原始像素的 RGBA 值
                original = result.get_at((x, y))

                # 计算乘法混合结果（各通道分别相乘）
                r = get_color(original[0], blend_color[0])
                g = get_color(original[1], blend_color[1])
                b = get_color(original[2], blend_color[2])
                a = (original[3] * blend_color[3]) // 255

                # 写入处理后的像素
                result.set_at((x, y), (r, g, b, a))

        # 解锁表面
        result.unlock()

        return result