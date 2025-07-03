from typing import Any

import pygame
import colorsys
import re


class MColor:
    def __init__(self, *args):
        """
        创建增强版颜色对象，支持多种输入格式：\n
        1. RGB 元组: (255, 100, 50)
        2. RGBA 元组: (255, 100, 50, 200)
        3. 颜色名称: "dodger blue", "crimson"
        4. 十六进制值: "#FF6347" 或 "FF6347"
        5. HSL 元组: (0.05, 0.6, 0.5)
        6. HSV 元组: (0.05, 0.6, 0.8)
        7. 另一个 EnhancedColor 对象
        """
        self._pygame_color = pygame.Color(0, 0, 0)

        if len(args) == 1:
            arg = args[0]
            if isinstance(arg, MColor):
                self._pygame_color = pygame.Color(arg.rgba)
            elif isinstance(arg, pygame.Color):
                self._pygame_color = arg
            elif isinstance(arg, str):
                # 处理颜色名称或十六进制值
                if arg.startswith("#"):
                    self._pygame_color = pygame.Color(arg)
                else:
                    # 尝试匹配十六进制值（不带#）
                    if re.match(r'^[0-9a-fA-F]{6}$', arg) or re.match(r'^[0-9a-fA-F]{8}$', arg):
                        self._pygame_color = pygame.Color(f"#{arg}")
                    else:
                        # 尝试颜色名称
                        try:
                            self._pygame_color = pygame.Color(arg)
                        except ValueError:
                            raise ValueError(f"未知的颜色名称或格式: '{arg}'")
            elif isinstance(arg, tuple) or isinstance(arg, list):
                if len(arg) == 3:  # RGB
                    self._pygame_color = pygame.Color(arg[0], arg[1], arg[2])
                elif len(arg) == 4:  # RGBA
                    self._pygame_color = pygame.Color(arg[0], arg[1], arg[2], arg[3])
                else:
                    raise ValueError("元组长度必须是3(RGB)或4(RGBA)")
            else:
                raise TypeError("不支持的参数类型")
        elif len(args) == 3:  # RGB
            self._pygame_color = pygame.Color(args[0], args[1], args[2])
        elif len(args) == 4:  # RGBA
            self._pygame_color = pygame.Color(args[0], args[1], args[2], args[3])
        else:
            raise ValueError("参数数量错误，应为1个(颜色对象/名称/元组)或3-4个(RGB/RGBA值)")

    # 基本颜色属性
    @property
    def r(self):
        """红色分量 (0-255)"""
        return self._pygame_color.r

    @r.setter
    def r(self, value):
        self._pygame_color.r = max(0, min(255, value))

    @property
    def g(self):
        """绿色分量 (0-255)"""
        return self._pygame_color.g

    @g.setter
    def g(self, value):
        self._pygame_color.g = max(0, min(255, value))

    @property
    def b(self):
        """蓝色分量 (0-255)"""
        return self._pygame_color.b

    @b.setter
    def b(self, value):
        self._pygame_color.b = max(0, min(255, value))

    @property
    def a(self):
        """透明度分量 (0-255)"""
        return self._pygame_color.a

    @a.setter
    def a(self, value):
        self._pygame_color.a = max(0, min(255, value))

    @property
    def rgb(self):
        """RGB元组 (r, g, b)"""
        return self.r, self.g, self.b

    @property
    def rgba(self):
        """RGBA元组 (r, g, b, a)"""
        return self.r, self.g, self.b, self.a

    @property
    def normalized_rgba(self):
        """归一化的RGBA值 (0.0-1.0)"""
        return self.r / 255.0, self.g / 255.0, self.b / 255.0, self.a / 255.0

    # 颜色空间转换
    @property
    def hsl(self):
        """HSL元组 (h, s, l) 所有值在0.0-1.0之间"""
        r, g, b = [x / 255.0 for x in self.rgb]
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        return h, s, l

    @hsl.setter
    def hsl(self, value):
        h, s, l = value
        r, g, b = [int(x * 255) for x in colorsys.hls_to_rgb(h, l, s)]
        self._pygame_color = pygame.Color(r, g, b, self.a)

    @property
    def hsv(self):
        """HSV元组 (h, s, v) 所有值在0.0-1.0之间"""
        r, g, b = [x / 255.0 for x in self.rgb]
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        return h, s, v

    @hsv.setter
    def hsv(self, value):
        h, s, v = value
        r, g, b = [int(x * 255) for x in colorsys.hsv_to_rgb(h, s, v)]
        self._pygame_color = pygame.Color(r, g, b, self.a)

    # 颜色操作
    def lighten(self, amount):
        """增加亮度 (0.0-1.0)"""
        h, s, l = self.hsl
        new_l = min(1.0, l + amount)
        self.hsl = (h, s, new_l)
        return self

    def darken(self, amount):
        """降低亮度 (0.0-1.0)"""
        h, s, l = self.hsl
        new_l = max(0.0, l - amount)
        self.hsl = (h, s, new_l)
        return self

    def saturate(self, amount):
        """增加饱和度 (0.0-1.0)"""
        h, s, l = self.hsl
        new_s = min(1.0, s + amount)
        self.hsl = (h, new_s, l)
        return self

    def desaturate(self, amount):
        """降低饱和度 (0.0-1.0)"""
        h, s, l = self.hsl
        new_s = max(0.0, s - amount)
        self.hsl = (h, new_s, l)
        return self

    def adjust_hue(self, amount):
        """调整色相 (0.0-1.0)"""
        h, s, l = self.hsl
        new_h = (h + amount) % 1.0
        self.hsl = (new_h, s, l)
        return self

    def complement(self):
        """返回补色"""
        return self.copy().adjust_hue(0.5)

    def blend(self, other_color, factor=0.5):
        """混合两种颜色 (factor=0.0 返回当前颜色, 1.0 返回另一个颜色)"""
        factor = max(0.0, min(1.0, factor))
        r = int(self.r * (1 - factor) + other_color.r * factor)
        g = int(self.g * (1 - factor) + other_color.g * factor)
        b = int(self.b * (1 - factor) + other_color.b * factor)
        a = int(self.a * (1 - factor) + other_color.a * factor)
        return MColor(r, g, b, a)

    # 实用方法
    def copy(self):
        """创建颜色的副本"""
        return MColor(self.r, self.g, self.b, self.a)

    def to_hex(self, with_alpha=False):
        """返回十六进制颜色代码"""
        if with_alpha:
            return f"#{self.r:02x}{self.g:02x}{self.b:02x}{self.a:02x}"
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"

    def to(self):
        """转换为原生Pygame颜色对象"""
        return pygame.Color(self.r, self.g, self.b, self.a)

    # 兼容Pygame的Color
    @staticmethod
    def from_name(name):
        """从颜色名称创建颜色对象"""
        return MColor(name)

    # 常用颜色作为类属性
    @staticmethod
    def from_hex(hex_value):
        """从十六进制值创建颜色对象"""
        return MColor(hex_value)

    @staticmethod
    def from_hsl(h, s, l):
        """从HSL值创建颜色对象"""
        color = MColor(0, 0, 0)
        color.hsl = (h, s, l)
        return color

    @staticmethod
    def from_hsv(h, s, v):
        """从HSV值创建颜色对象"""
        color = MColor(0, 0, 0)
        color.hsv = (h, s, v)
        return color

    def __str__(self):
        return f"EnhancedColor(r={self.r}, g={self.g}, b={self.b}, a={self.a})"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        """支持与Pygame颜色对象的比较"""
        if isinstance(other, MColor):
            return self.rgba == other.rgba
        elif isinstance(other, pygame.Color):
            return self.r == other.r and self.g == other.g and self.b == other.b and self.a == other.a
        elif isinstance(other, (tuple, list)) and len(other) in (3, 4):
            # 比较RGB或RGBA元组
            if len(other) == 3:
                return self.r == other[0] and self.g == other[1] and self.b == other[2]
            return self.r == other[0] and self.g == other[1] and self.b == other[2] and self.a == other[3]
        return False

    def __iter__(self):
        """支持解包为(r, g, b, a)"""
        return iter((self.r, self.g, self.b, self.a))

    def __getitem__(self, index):
        """支持索引访问[r, g, b, a]"""
        if index == 0: return self.r
        if index == 1: return self.g
        if index == 2: return self.b
        if index == 3: return self.a
        raise IndexError("Color index out of range. Valid indices: 0-3")

    def __len__(self):
        """支持len()函数"""
        return 4

    def __enter__(self):
        """支持上下文管理器，返回原生Pygame颜色"""
        return self.to()

    def __exit__(self, exc_type, exc_value, traceback):
        """上下文管理器退出时不做特殊处理"""
        pass
