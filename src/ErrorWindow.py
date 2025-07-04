﻿import pygame
import traceback
import pyperclip
from datetime import datetime

from src.Color import MColor
from src.Data.Fonts import msyh_font


class ErrorWindow:
    def __init__(self, exception, width=600, height=400):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Error occurred!")

        # 颜色配置
        self.theme = {
            'background': MColor(45, 45, 48),
            'primary': MColor(0, 122, 204),
            'secondary': MColor(100, 100, 100),
            'text': MColor(240, 240, 240),
            'warning': MColor(255, 153, 0)
        }

        self.title_font = msyh_font.render(48)
        self.text_font = msyh_font.render(40)
        self.small_font = msyh_font.render(32)

        self.exception = exception
        self.error_type = type(exception).__name__
        self.error_msg = str(exception)
        self.full_traceback = traceback.format_exc()

        self.error_mapping = {
            'FileNotFoundError': {
                'title': "File not found",
                'suggestion': "请检查文件路径是否正确，确认文件存在且程序有访问权限"
            },
            'ZeroDivisionError': {
                'title': "Zero division",
                'suggestion': "不能进行除以零的操作，请检查计算公式的输入值"
            },
            'KeyError': {
                'title': "KeyError",
                'suggestion': "请求的键不存在，请检查数据字典的有效键值"
            },
            'TypeError': {
                'title': "TypeError",
                'suggestion': "检测到不兼容的数据类型操作，请检查变量类型"
            },
            'ValueError': {
                'title': "数值错误",
                'suggestion': "输入值不符合要求，请检查数据范围和格式"
            },
            'ConnectionError': {
                'title': "ConnectionError",
                'suggestion': "无法连接到服务器，请检查网络连接和服务器状态"
            }
        }

        self.panel_rect = pygame.Rect(20, self.screen.get_height() - 80,
                                 self.screen.get_width() - 40, 60)

        self.button_rect_1 = pygame.Rect(
            self.panel_rect.right - 150,
            self.panel_rect.centery - 15,
            140,
            30
        )

        self.button_rect_2 = pygame.Rect(
            self.panel_rect.left + 10,
            self.panel_rect.centery - 15,
            140,
            30
        )

        self.running = True
        self.main_loop()

    def get_friendly_message(self):
        default = {
            'title': "Error",
            'suggestion': "Restart the program"
        }
        info = self.error_mapping.get(self.error_type, default)

        messages = [
            f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Type: {self.error_type}",
            f"Description: {info['title']}",
            "",
            "Suggestion:",
            info['suggestion'],
            "",
            f"Detailed information：{self.error_msg}"
        ]
        return '\n'.join(messages)

    def draw_main_content(self):
        content = self.get_friendly_message()
        y = 70
        line_height = 24

        for line in content.split('\n'):
            if "Time" in line:
                text = self.small_font.render(line, self.theme['secondary'])
            elif "Suggestion" in line:
                text = self.text_font.render(line, self.theme['warning'])
            else:
                text = self.text_font.render(line, self.theme['text'])
            self.screen.blit(text, (30, y))
            y += line_height

    def handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if event.button == 1:
                    if self.button_rect_1.collidepoint(mouse_pos):
                        self.running = False
                    if self.button_rect_2.collidepoint(mouse_pos):
                        try:
                            pyperclip.copy(self.get_friendly_message())
                        except Exception as e:
                            print(f"Error: {e}")

    def render_btn(self):
        pygame.draw.rect(self.screen, self.theme['secondary'].to(), self.panel_rect, border_radius=5)

        btn_color_1 = self.theme['primary']
        btn_color_2 = self.theme["primary"]

        # 绘制切换按钮
        pygame.draw.rect(self.screen, btn_color_1.to(), self.button_rect_1, border_radius=3)
        pygame.draw.rect(self.screen, btn_color_2.to(), self.button_rect_2, border_radius=3)
        text_1 = self.text_font.render("Close", self.theme['text'])
        text_2 = self.text_font.render("Copy", self.theme['text'])
        text_rect_1 = text_1.get_rect(center=self.button_rect_1.center)
        text_rect_2 = text_2.get_rect(center=self.button_rect_2.center)
        self.screen.blit(text_1, text_rect_1)
        self.screen.blit(text_2, text_rect_2)

    def main_loop(self):
        while self.running:
            self.screen.fill(self.theme['background'].to())

            title = self.title_font.render("Error!", self.theme['text'])
            self.screen.blit(title, (30, 20))

            self.draw_main_content()

            self.render_btn()

            self.handle_events()

            pygame.display.update()

        pygame.quit()