import sys
from src.Vebp import __version__
from src.Vebp.Cli.build import CliBuild
from src.Vebp.Cli.create import CliCreate
from src.Vebp.Cli.init import CliInit
from src.Vebp.Cli.pack import CliPack
from src.Vebp.Cli.package import CliPackage


class CLI:
    def __init__(self):
        self.parser = CliCreate.create()

    @staticmethod
    def _show_version():
        print(f"vebp (增强的 PyInstaller 打包工具) 版本: {__version__}")
        print("使用 'vebp build --help' 查看构建帮助")
        print("使用 'vebp init' 初始化新项目")
        print("使用 'vebp package' 查看 package 配置详情")

    def run(self, args=None):
        if len(sys.argv) == 1:
            self._show_version()
            sys.exit(0)

        parsed_args = self.parser.parse_args(args)

        if parsed_args.version:
            self._show_version()
            sys.exit(0)

        if parsed_args.command == 'build':
            CliBuild.handle(parsed_args)
        elif parsed_args.command == 'init':
            CliInit.handle(parsed_args)
        elif parsed_args.command == 'package':
            CliPackage.handle()
        elif parsed_args.command == 'pack':
            CliPack.handle()
        else:
            self.parser.print_help()
            sys.exit(1)