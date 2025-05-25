from src.Data.Path import font_path
from src.Resources.Font import FontResource
from src.Scene import Scene

class EmptyScene(Scene):

    def render(self) -> None:
        super().render()

        res = FontResource(font_path)
        text1 = res.render(48).render("This is a empty scene.")
        text1_rect = text1.get_rect(centerx=self.surface_display.get_width() / 2,
                                    centery=self.surface_display.get_height() / 2)
        self.surface_display.blit(text1, text1_rect)