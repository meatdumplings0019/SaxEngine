import sys

from colorama import Fore, Style

from src.Libs.Args import ArgsUtil
from src.Vebp.Command.Create import CommandCreate
from src.Vebp.Command.matches import CommandMatch
from src.Vebp.version import __version__
from src.Vebp.base import VebpBase


class CMD(VebpBase):
    def __init__(self) -> None:
        super().__init__()
        self.parser = CommandCreate.create()

    def run(self) -> None:
        print(f"Vebp {__version__}")
        print('Type "help", "copyright", "credits" or "license" for more information.')

        while True:
            try:
                file = input(f"{Fore.MAGENTA}>>> ")
                print(Style.RESET_ALL, end="")
                CommandMatch.handle(ArgsUtil.parse_input_args(file, self.parser))
            except Exception as e:
                print(e, file=sys.stderr)