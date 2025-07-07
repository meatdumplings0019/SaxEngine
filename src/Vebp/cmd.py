from colorama import Fore, Style

from src.Libs.Args import ArgsUtil
from src.Vebp.Command.Create import CommandCreate
from src.Vebp.Command.matches import CommandMatch
from src.Vebp.version import __version__
from src.Vebp.base import VebpBase


class CMD(VebpBase):
    def __init__(self) -> None:
        super().__init__()
        self.input = ""
        self.parser = CommandCreate.create()

    def _get_input(self) -> None:
        self.input = input(f"{Fore.MAGENTA}>>> ")

    def _compile(self) -> None:
        CommandMatch.handle(ArgsUtil.parse_input_args(self.input, self.parser))

    def run(self) -> None:
        print(f"Vebp {__version__}")
        print('Type "help", "copyright", "credits" or "license" for more information.')

        while True:
            self._get_input()
            print(Style.RESET_ALL, end="")
            self._compile()