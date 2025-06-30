import sys
from .build import CliBuild
from .create import CliCreate
from .init import CliInit
from .pack import CliPack
from .package import CliPackage
from ..CMD import CMD


class CLI:
    def __init__(self):
        self.parser = CliCreate.create()

    def run(self, args=None):

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