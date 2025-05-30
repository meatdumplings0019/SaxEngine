﻿from src.Data.Path import font_path
from src.Libs.display import Display
from src.Resources.Font import FontResource
from src.Scene import Scene


class DefaultScene(Scene):
    def __init__(self, *args) -> None:
        super().__init__()
        if args:
            self.args = args
        else:
            self.args = [
                "This is a default scene.",
                "Your scene may make a mistake."
            ]

    def render(self) -> None:
        super().render()
        SIZE = Display.get_global_height(48)

        res = FontResource(font_path)
        text1 = res.render(48).render(self.args[0])
        text2 = res.render(48).render(self.args[1])
        text1_rect = text1.get_rect(centerx=self.surface_display.get_width() / 2, centery=self.surface_display.get_height() / 2 - SIZE / 2)
        text2_rect = text2.get_rect(centerx=self.surface_display.get_width() / 2, centery=self.surface_display.get_height() / 2 + SIZE / 2)
        self.surface_display.blit(text1, text1_rect)
        self.surface_display.blit(text2, text2_rect)