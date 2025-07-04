import os


class WindowUtils:
    @staticmethod
    def center() -> None:
        os.environ['SDL_VIDEO_CENTERED'] = '1'