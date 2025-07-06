from src.Data.Fonts import msyh_font
from src.Libs.Window.display import Display
from src.Window.Independence import IndependenceWindow


class EmptyWindow(IndependenceWindow):
    def render(self) -> None:
        super().render()
        SIZE = Display.get_global_height(48)

        text1 = msyh_font.render(SIZE).render("This is a empty window.")
        text1_rect = text1.get_rect(centerx=self.surface_display.get_width() / 2,
                                    centery=self.surface_display.get_height() / 2)
        self.surface_display.blit(text1, text1_rect)