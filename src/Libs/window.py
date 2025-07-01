import os


class WindowUtils:
    @staticmethod
    def center():
        os.environ['SDL_VIDEO_CENTERED'] = '1'