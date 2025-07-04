from sys import exit as sys_exit
from pygame import quit


class Tool:
    @staticmethod
    def exit() -> None:
        quit()
        sys_exit()