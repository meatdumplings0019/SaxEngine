import sys

from src.Vebp.Command.matches import CommandMatch
from src.Vebp.base import VebpBase
from src.Vebp.Command.Create import CommandCreate
from src.Vebp.cmd import CMD


class CLI(VebpBase):
    def __init__(self) -> None:
        super().__init__()
        self.parser = CommandCreate.create()

    def run(self, args=None) -> None:
        if len(sys.argv) == 1:
            cmd = CMD()
            cmd.run()
            sys.exit(0)

        CommandMatch.handle(self.parser.parse_args(args))