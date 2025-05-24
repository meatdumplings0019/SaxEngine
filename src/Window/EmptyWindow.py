from src.Libs.display import Display
from src.Resources.Font import FontResource
from src.Window.IndependenceWindow import IndependenceWindow


class EmptyWindow(IndependenceWindow):
    def render(self) -> None:
        super().render()
        SIZE = Display.get_global_height(48)

        res = FontResource("./Assets/Fonts/JeTBrainsMono.ttf")
        text1 = res.render(SIZE).render("This is a empty window.")
        text1_rect = text1.get_rect(centerx=self.surface_display.get_width() / 2,
                                    centery=self.surface_display.get_height() / 2)
        self.surface_display.blit(text1, text1_rect)