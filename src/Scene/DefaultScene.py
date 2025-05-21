from src.Libs.display import Display
from src.Resources.Font import FontResource
from src.Scene import Scene


class DefaultScene(Scene):
    def render(self):
        SIZE = Display.get_global_height(48)

        res = FontResource("./Assets/Fonts/JeTBrainsMono.ttf")
        text1 = res.render(SIZE).render("This is a default scene.")
        text2 = res.render(SIZE).render("Your scene may make a mistake.")
        text1_rect = text1.get_rect(centerx=self.surface_display.get_width() / 2, centery=self.surface_display.get_height() / 2 - SIZE / 2)
        text2_rect = text2.get_rect(centerx=self.surface_display.get_width() / 2, centery=self.surface_display.get_height() / 2 + SIZE / 2)
        self.surface_display.blit(text1, text1_rect)
        self.surface_display.blit(text2, text2_rect)