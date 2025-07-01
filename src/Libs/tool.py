from sys import exit as sys_exit
from pygame import quit


class Tool:
    @staticmethod
    def exit():
        quit()
        sys_exit()