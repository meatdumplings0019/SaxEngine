import sys

from src.Vebp.Cli.build import CliBuild
from src.Vebp.Cli.create import CliCreate
from src.Vebp.Cli.init import CliInit
from src.Vebp.Cli.pack import CliPack
from src.Vebp.Cli.package import CliPackage
from src.Vebp.CMD import CMD


class CLI:
    def __init__(self) -> None:
        self.parser = CliCreate.create()

    def run(self, args=None) -> None:

        if len(sys.argv) == 1:
            cmd = CMD()
            cmd.run()
            sys.exit(0)

        parsed_args = self.parser.parse_args(args)

        if parsed_args.command == 'build':
            CliBuild.handle(parsed_args)
        elif parsed_args.command == 'init':
            CliInit.handle(parsed_args)
        elif parsed_args.command == 'package':
            CliPackage.handle()
        elif parsed_args.command == 'pack':
            CliPack.handle()
        else:
            sys.exit(0)