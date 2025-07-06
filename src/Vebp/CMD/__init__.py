from colorama import Fore, Style

from src.Vebp.version import __version__
from src.Vebp.base import VebpBase
from src.Vebp.CMD.Builder import cmd_build
from src.Vebp.CMD.Exit import cmd_exit
from src.Vebp.CMD.Init import cmd_init
from src.Vebp.CMD.utils import error


class CMD(VebpBase):
    def __init__(self) -> None:
        super().__init__()
        self.input = ""

    def _get_input(self) -> None:
        self.input = input(f"{Fore.MAGENTA}>>> ")

    def _compile(self) -> None:
        command, *args = self.input.split(" ")
        # noinspection PyUnreachableCode
        match command:
            case "exit":
                cmd_exit(args)
            case "build":
                cmd_build(args)
            case "init":
                cmd_init(args)
            case other:
                error(f"Unknown command {other}")

    def run(self) -> None:
        print(f"Vebp {__version__}")
        print('Type "help", "copyright", "credits" or "license" for more information.')

        while True:
            self._get_input()
            print(Style.RESET_ALL, end="")
            self._compile()