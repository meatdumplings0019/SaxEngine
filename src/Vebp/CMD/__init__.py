from colorama import Fore, Style
from src.Vebp.CMD.exit import _exit
from src.Vebp import __version__

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
                _exit()
            case other:
                print(f"{Fore.RED}NameError: name '{other}' is not defined")

    def run(self):
        print(f"Vebp {__version__}")
        print('Type "help", "copyright", "credits" or "license" for more information.')

        while True:
            self._get_input()
            self._compile()
            print(Style.RESET_ALL, end="")