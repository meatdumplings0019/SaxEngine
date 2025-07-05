import sys

from src.Vebp.Base import VebpBase
from src.Vebp.Cli.build import CliBuild
from src.Vebp.Cli.create import CliCreate
from src.Vebp.Cli.init import CliInit
from src.Vebp.Cli.pack import CliPack
from src.Vebp.Cli.package import CliPackage
from src.Vebp.CMD import CMD
from src.Vebp.Cli.dev import CliDev
from src.Vebp.Cli.plugin import CliPlugin


class CLI(VebpBase):
    def __init__(self) -> None:
        super().__init__()
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
        elif parsed_args.command == 'dev':
            CliDev.handle(parsed_args)
        elif parsed_args.command == 'plugin':
            CliPlugin.handle(parsed_args)
        else:
            sys.exit(0)