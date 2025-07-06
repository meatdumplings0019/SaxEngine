import sys

from src.Vebp.Base import VebpBase
from src.Vebp.Cli.Builder import CliBuild
from src.Vebp.Cli.Create import CliCreate
from src.Vebp.Cli.Init import CliInit
from src.Vebp.Cli.Pack import CliPack
from src.Vebp.Cli.Package import CliPackage
from src.Vebp.CMD import CMD
from src.Vebp.Cli.Dev import CliDev
from src.Vebp.Cli.Plugin import CliPlugin


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
            print("🔨 开始构建项目...")
            CliBuild.handle(parsed_args)
        elif parsed_args.command == 'init':
            print("🛠️ 初始化项目...")
            CliInit.handle(parsed_args)
        elif parsed_args.command == 'package':
            print("📦 显示包配置...")
            CliPackage.handle()
        elif parsed_args.command == 'pack':
            print("📦 打包项目...")
            CliPack.handle()
        elif parsed_args.command == 'dev':
            print("🚀 运行开发脚本...")
            CliDev.handle(parsed_args)
        elif parsed_args.command == 'plugin':
            print("🧩 插件工具...")
            CliPlugin.handle(parsed_args)
        else:
            sys.exit(0)