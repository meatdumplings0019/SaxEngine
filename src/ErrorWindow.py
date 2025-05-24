import pygame
import traceback
from datetime import datetime


class ErrorWindow:
    def __init__(self, exception, width=600, height=400):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("程序遇到问题")

        # 颜色配置
        self.theme = {
            'background': (45, 45, 48),
            'primary': (0, 122, 204),
            'secondary': (100, 100, 100),
            'text': (240, 240, 240),
            'warning': (255, 153, 0)
        }

        # 字体配置
        self.title_font = pygame.font.SysFont('simhei', 24, bold=True)
        self.text_font = pygame.font.SysFont('simhei', 18)
        self.small_font = pygame.font.SysFont('simhei', 14)

        # 错误信息处理
        self.exception = exception
        self.error_type = type(exception).__name__
        self.error_msg = str(exception)
        self.full_traceback = traceback.format_exc()

        # 友好提示映射
        self.error_mapping = {
            'FileNotFoundError': {
                'title': "文件未找到",
                'suggestion': "请检查文件路径是否正确，确认文件存在且程序有访问权限"
            },
            'ZeroDivisionError': {
                'title': "数学计算错误",
                'suggestion': "不能进行除以零的操作，请检查计算公式的输入值"
            },
            'KeyError': {
                'title': "数据键值错误",
                'suggestion': "请求的键不存在，请检查数据字典的有效键值"
            },
            'TypeError': {
                'title': "类型错误",
                'suggestion': "检测到不兼容的数据类型操作，请检查变量类型"
            },
            'ValueError': {
                'title': "数值错误",
                'suggestion': "输入值不符合要求，请检查数据范围和格式"
            },
            'ConnectionError': {
                'title': "网络连接失败",
                'suggestion': "无法连接到服务器，请检查网络连接和服务器状态"
            }
        }

        # 窗口状态
        self.show_details = False
        self.running = True
        self.main_loop()

    def get_friendly_message(self):
        """生成友好错误信息"""
        default = {
            'title': "程序遇到问题",
            'suggestion': "发生未预期的错误，建议尝试重新启动程序或联系技术支持"
        }
        info = self.error_mapping.get(self.error_type, default)

        messages = [
            f"发生时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"错误类型：{self.error_type}",
            f"问题描述：{info['title']}",
            "",
            "建议操作：",
            info['suggestion'],
            "",
            f"技术描述：{self.error_msg}"
        ]
        return '\n'.join(messages)

    def draw_main_content(self):
        content = self.get_friendly_message()
        y = 70
        line_height = 24

        for line in content.split('\n'):
            if "发生时间" in line:
                text = self.small_font.render(line, True, self.theme['secondary'])
            elif "建议操作" in line:
                text = self.text_font.render(line, True, self.theme['warning'])
            else:
                text = self.text_font.render(line, True, self.theme['text'])
            self.screen.blit(text, (30, y))
            y += line_height

    def handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键点击
                    mouse_pos = pygame.mouse.get_pos()
                    # 切换技术细节显示
                    if (self.screen.get_width() - 170 < mouse_pos[0] < self.screen.get_width() - 30 and
                            self.screen.get_height() - 70 < mouse_pos[1] < self.screen.get_height() - 40):
                        self.show_details = not self.show_details

    def main_loop(self):
        """主循环"""
        while self.running:
            self.screen.fill(self.theme['background'])

            # 绘制标题
            title = self.title_font.render("程序遇到问题", True, self.theme['text'])
            self.screen.blit(title, (30, 20))

            self.draw_main_content()
            self.handle_events()

            pygame.display.update()

        pygame.quit()