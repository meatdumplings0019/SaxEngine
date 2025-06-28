import argparse
import sys
from pathlib import Path
from .builder import Builder
from . import __version__
from .package import Package
from .config import Config


class CLI:
    """vebp 打包工具的命令行界面"""

    def __init__(self):
        """初始化 CLI"""
        self.parser = self._create_parser()

    def _create_parser(self):
        """创建主参数解析器"""
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

        # 添加子命令
        subparsers = parser.add_subparsers(
            title='可用命令',
            dest='command',
            help='选择要执行的操作'
        )

        # 构建命令
        self._add_build_command(subparsers)

        # 初始化命令
        self._add_init_command(subparsers)

        # 添加 package 命令
        self._add_package_command(subparsers)

        return parser

    def _add_build_command(self, subparsers):
        """添加 build 子命令"""
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

        # 使用配置时名称和源文件路径是可选的
        build_parser.add_argument('name', nargs='?', default=None,
                                  help='项目名称 (如果在 vebp-package.json 中定义了则为可选)')
        build_parser.add_argument('--src', '-s',
                                  help='要打包的 Python 脚本路径 (如果在 vebp-package.json 中定义了则为可选)')

        # 构建命令的可选参数和别名
        build_parser.add_argument('--icon', '-i',
                                  help='应用程序图标 (.ico 文件)')
        build_parser.add_argument('--console', '-c', action='store_true',
                                  help='显示控制台窗口 (默认隐藏)')
        build_parser.add_argument('--onedir', '-d', action='store_true',
                                  help='使用目录模式而不是单文件模式 (默认: 单文件)')

        # 资源参数
        build_parser.add_argument('--asset', action='append',
                                  help='外部资源: "源路径;目标相对路径" (复制到输出目录)')
        build_parser.add_argument('--inasset', action='append',
                                  help='内部资源: "源路径;目标相对路径" (嵌入到可执行文件中)')

    def _add_init_command(self, subparsers):
        """添加 init 子命令"""
        init_parser = subparsers.add_parser(
            'init',
            help='初始化项目配置',
            description='创建 vebp-package.json 和 vebp-config.json 文件'
        )

        init_parser.add_argument('--force', '-f', action='store_true',
                                 help='覆盖现有配置文件')

    def _add_package_command(self, subparsers):
        """添加 package 子命令"""
        package_parser = subparsers.add_parser(
            'package',
            help='显示 package 配置详情',
            description='打印 vebp-package.json 文件的详细属性说明'
        )

    def _show_version(self):
        """显示版本信息"""
        print(f"vebp (增强的 PyInstaller 打包工具) 版本: {__version__}")
        print("使用 'vebp build --help' 查看构建帮助")
        print("使用 'vebp init' 初始化新项目")
        print("使用 'vebp package' 查看 package 配置详情")

    def _handle_build_command(self, args):
        """处理 build 子命令"""
        try:
            # 尝试从 package.json 创建构建器
            builder = Builder.from_package()

            # 如果从配置文件创建失败，则创建新的构建器实例
            if builder is None:
                builder = Builder()

            # 使用 getattr 获取命令行参数，提供默认值 None
            name = getattr(args, 'name', None)
            if name:
                builder._name = name

            src = getattr(args, 'src', None)
            if src:
                builder.set_script(src)

            icon = getattr(args, 'icon', None)
            if icon:
                builder._icon = Path(icon)

            # 设置控制台选项（命令行参数优先）
            console = getattr(args, 'console', False)
            if console:
                builder.set_console(True)

            # 设置打包模式
            onedir = getattr(args, 'onedir', False)
            if onedir:
                builder.set_onefile(False)  # --onedir 表示不使用单文件模式
            elif builder._onefile is None:  # 如果配置文件没有设置，使用默认值
                builder.set_onefile(True)  # 默认为单文件模式

            # 添加外部资源（如果提供了）
            assets = getattr(args, 'asset', [])
            if assets:
                # 按目标路径分组资源
                assets_by_target = {}

                # 解析资源规范
                for asset_spec in assets:
                    # 分割源和目标
                    parts = asset_spec.split(';', 1)
                    source = parts[0].strip()
                    target = parts[1].strip() if len(parts) > 1 else ""

                    # 添加到分组字典
                    assets_by_target.setdefault(target, []).append(source)

                # 将资源添加到构建器
                for target, sources in assets_by_target.items():
                    builder.add_assets(sources, target)

            # 添加内部资源（如果提供了）
            inassets = getattr(args, 'inasset', [])
            if inassets:
                # 按目标路径分组内部资源
                inassets_by_target = {}

                # 解析内部资源规范
                for inasset_spec in inassets:
                    # 分割源和目标
                    parts = inasset_spec.split(';', 1)
                    source = parts[0].strip()
                    target = parts[1].strip() if len(parts) > 1 else ""

                    # 添加到分组字典
                    inassets_by_target.setdefault(target, []).append(source)

                # 将内部资源添加到构建器
                for target, sources in inassets_by_target.items():
                    builder.add_inassets(sources, target)

            # 执行构建
            success = builder.build()
        except Exception as e:
            print(f"\n初始化错误: {str(e)}", file=sys.stderr)
            sys.exit(2)

        if success:
            sys.exit(0)
        else:
            print("\n操作失败! 请检查错误信息", file=sys.stderr)
            sys.exit(1)

    def _handle_init_command(self, args):
        """处理 init 子命令"""
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

    def _handle_package_command(self, args):
        """处理 package 子命令"""
        print("显示 package 配置详情...\n")
        success = Package.print_config()

        # 添加额外说明
        print("\n说明:")
        print("- 使用 'vebp init' 创建配置文件")
        print("- 编辑 vebp-package.json 设置属性值")
        print("- 默认生成的配置只包含 name, main 和 console 属性")
        print("- 可以手动添加 icon, onefile 属性")
        print("- 运行 'vebp build' 使用配置构建项目")

        return success

    def run(self, args=None):
        """使用给定参数运行 CLI"""
        # 如果未提供参数，显示版本信息
        if len(sys.argv) == 1:
            self._show_version()
            sys.exit(0)

        # 解析参数
        parsed_args = self.parser.parse_args(args)

        # 处理 --version 选项
        if parsed_args.version:
            self._show_version()
            sys.exit(0)

        # 处理子命令
        if parsed_args.command == 'build':
            self._handle_build_command(parsed_args)
        elif parsed_args.command == 'init':
            self._handle_init_command(parsed_args)
        elif parsed_args.command == 'package':
            self._handle_package_command(parsed_args)
        else:
            # 如果命令未识别，显示帮助
            self.parser.print_help()
            sys.exit(1)