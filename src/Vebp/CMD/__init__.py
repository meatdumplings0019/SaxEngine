from colorama import Fore, Style

from src.Vebp import __version__
from src.Vebp.CMD.build import cmd_build
from src.Vebp.CMD.exit import cmd_exit
from src.Vebp.CMD.init import cmd_init
from src.Vebp.CMD.tool import error


class CMD:
    def __init__(self):
        self.input = ""

    def _get_input(self):
        self.input = input(f"{Fore.MAGENTA}>>> ")

    def _compile(self):
        command, *args = self.input.split(" ")
        # noinspection PyUnreachableCode
        match command:
            case "exit":
                cmd_exit(args)
            case "build":
                cmd_build(args)
            case "init":
                print(f"{cmd_init(args)}")
            case other:
                error(f"Unknown command {other}")

    def run(self):
        print(f"Vebp {__version__}")
        print('Type "help", "copyright", "credits" or "license" for more information.')

        while True:
            self._get_input()
            print(Style.RESET_ALL, end="")
            self._compile()