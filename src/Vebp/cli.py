import argparse
import sys
from pathlib import Path
from src.Vebp.builder import Builder
from src.Vebp import __version__
from src.Vebp.package import Package
from src.Vebp.config import Config


class CLI:
    def __init__(self):
        self.parser = self._create_parser()

    def _create_parser(self):
        parser = argparse.ArgumentParser(
            description='vebp - 增强的 PyInstaller 打包工具',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog='''示例:
              vebp build MyProject --src app.py
              vebp build MyApp -s app.py -i app.ico -c
              vebp build ProjectX -s main.py -d
              vebp build Game -s app.py --asset "images;resources" --asset "sfx;resources"
              vebp build App -s app.py --inasset "config.json;settings"
              vebp build App -s app.py --inasset "templates;ui" --asset "README.md"
              vebp build  # 使用 vebp-package.json 中的配置
              vebp package # 显示 package 配置
            ''')

        parser.add_argument('--version', '-v', action='store_true',
                            help='显示版本信息')

        subparsers = parser.add_subparsers(
            title='可用命令',
            dest='command',
            help='选择要执行的操作'
        )

        self._add_build_command(subparsers)

        self._add_init_command(subparsers)

        self._add_package_command(subparsers)

        return parser

    @staticmethod
    def _add_build_command(subparsers):
        build_parser = subparsers.add_parser(
            'build',
            help='构建可执行文件',
            description='将 Python 脚本打包成可执行文件',
            epilog='''构建示例:
              vebp build MyProject --src app.py
              vebp build MyApp -s app.py -i app.ico -c
              vebp build ProjectX -s main.py -d
              vebp build Game -s app.py --asset "images;resources" --asset "sfx;resources"
              vebp build App -s app.py --inasset "config.json;settings"
              vebp build App -s app.py --inasset "templates;ui" --asset "README.md"
              vebp build  # 使用 vebp-package.json 中的配置
            ''')

        build_parser.add_argument('name', nargs='?', default=None,
                                  help='项目名称 (如果在 vebp-package.json 中定义了则为可选)')
        build_parser.add_argument('--src', '-s',
                                  help='要打包的 Python 脚本路径 (如果在 vebp-package.json 中定义了则为可选)')

        build_parser.add_argument('--icon', '-i',
                                  help='应用程序图标 (.ico 文件)')
        build_parser.add_argument('--console', '-c', action='store_true',
                                  help='显示控制台窗口 (默认隐藏)')
        build_parser.add_argument('--onedir', '-d', action='store_true',
                                  help='使用目录模式而不是单文件模式 (默认: 单文件)')

        build_parser.add_argument('--asset', action='append',
                                  help='外部资源: "源路径;目标相对路径" (复制到输出目录)')
        build_parser.add_argument('--inasset', action='append',
                                  help='内部资源: "源路径;目标相对路径" (嵌入到可执行文件中)')

    @staticmethod
    def _add_init_command(subparsers):
        init_parser = subparsers.add_parser(
            'init',
            help='初始化项目配置',
            description='创建 vebp-package.json 和 vebp-config.json 文件'
        )

        init_parser.add_argument('--force', '-f', action='store_true',
                                 help='覆盖现有配置文件')

    @staticmethod
    def _add_package_command(subparsers):
        subparsers.add_parser(
            'package',
            help='显示 package 配置详情',
            description='打印 vebp-package.json 文件的详细属性说明'
        )

    @staticmethod
    def _show_version():
        print(f"vebp (增强的 PyInstaller 打包工具) 版本: {__version__}")
        print("使用 'vebp build --help' 查看构建帮助")
        print("使用 'vebp init' 初始化新项目")
        print("使用 'vebp package' 查看 package 配置详情")

    @staticmethod
    def _handle_build_command(args):
        try:
            builder = Builder.from_package()

            if builder is None:
                builder = Builder()

            name = getattr(args, 'name', None)
            if name:
                builder._name = name

            src = getattr(args, 'src', None)
            if src:
                builder.set_script(src)

            icon = getattr(args, 'icon', None)
            if icon:
                builder._icon = Path(icon)

            console = getattr(args, 'console', False)
            if console:
                builder.set_console(True)

            one_dir = getattr(args, 'onedir', False)
            if one_dir:
                builder.set_onefile(False)
            elif builder.onefile is None:
                builder.set_onefile(True)

            assets = getattr(args, 'asset', [])
            if assets:
                assets_by_target = {}

                for asset_spec in assets:
                    parts = asset_spec.split(';', 1)
                    source = parts[0].strip()
                    target = parts[1].strip() if len(parts) > 1 else ""

                    assets_by_target.setdefault(target, []).append(source)

                for target, sources in assets_by_target.items():
                    builder.add_assets(sources, target)

            in_assets = getattr(args, 'inasset', [])
            if in_assets:
                in_assets_by_target = {}

                for inasset_spec in in_assets:
                    parts = inasset_spec.split(';', 1)
                    source = parts[0].strip()
                    target = parts[1].strip() if len(parts) > 1 else ""

                    in_assets_by_target.setdefault(target, []).append(source)

                for target, sources in in_assets_by_target.items():
                    builder.add_inassets(sources, target)

            success = builder.build()
        except Exception as e:
            print(f"\n初始化错误: {str(e)}", file=sys.stderr)
            sys.exit(2)

        if success:
            sys.exit(0)
        else:
            print("\n操作失败! 请检查错误信息", file=sys.stderr)
            sys.exit(1)

    @staticmethod
    def _handle_init_command(args):
        print("正在初始化 VEBP 项目...")

        # 获取默认项目名
        project_name = Path.cwd().name

        # 创建配置文件
        package_success = Package.create_config(args.force)
        config_success = Config.create_config(args.force)

        if package_success and config_success:
            print(f"\n项目 '{project_name}' 初始化成功!")
            print("下一步:")
            print("1. 编辑 vebp-package.json 设置 'main' 属性 (您的入口脚本)")
            print("2. 运行 'vebp build' 打包您的应用")
            return True

        print("\n初始化完成但有警告。")
        return False

    @staticmethod
    def _handle_package_command():
        print("显示 package 配置详情...\n")
        success = Package.print_config()

        print("\n说明:")
        print("- 使用 'vebp init' 创建配置文件")
        print("- 编辑 vebp-package.json 设置属性值")
        print("- 默认生成的配置只包含 name, main 和 console 属性")
        print("- 可以手动添加 icon, onefile 属性")
        print("- 运行 'vebp build' 使用配置构建项目")

        return success

    def run(self, args=None):
        if len(sys.argv) == 1:
            self._show_version()
            sys.exit(0)

        parsed_args = self.parser.parse_args(args)

        if parsed_args.version:
            self._show_version()
            sys.exit(0)

        if parsed_args.command == 'build':
            self._handle_build_command(parsed_args)
        elif parsed_args.command == 'init':
            self._handle_init_command(parsed_args)
        elif parsed_args.command == 'package':
            self._handle_package_command()
        else:
            self.parser.print_help()
            sys.exit(1)