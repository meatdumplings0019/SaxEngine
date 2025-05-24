from src.Libs.types import vec2


def get_window_resolution() -> vec2:
    import ctypes

    user32 = ctypes.windll.user32
    return vec2(user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))