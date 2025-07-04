from src.Libs.types import vec2

class Resolution:
    @property
    def windowResolution(self) -> vec2:
        import ctypes

        user32 = ctypes.windll.user32
        return vec2(user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))

resolution = Resolution()