﻿import argparse
from src.Vebp.Cli.add import CliAdd

class CliCreate:
    @staticmethod
    def create() -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            description='🚀 vebp - 增强的 PyInstaller 打包工具',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog='''示例:
              🔨 vebp build MyProject --src app.py
              🔨 vebp build MyApp -s app.py -i app.ico -c
              🔨 vebp build ProjectX -s main.py -d
              🔨 vebp build Game -s app.py --asset "images;resources" --asset "sfx;resources"
              🔨 vebp build App -s app.py --in_asset "config.json;settings"
              🔨 vebp build App -s app.py --in_asset "templates;ui" --asset "README.md"
              🔨 vebp build  # 使用 vebp-build.json 中的配置
              📦 vebp package # 显示 package 配置
            ''')

        parser.add_argument('--version', '-v', action='store_true',
                            help='ℹ️ 显示版本信息')

        subparsers = parser.add_subparsers(
            title='📋 可用命令',
            dest='command',
            help='👉 选择要执行的操作'
        )

        CliAdd.add_build_command(subparsers)
        CliAdd.add_init_command(subparsers)
        CliAdd.add_package_command(subparsers)
        CliAdd.add_pack_command(subparsers)
        CliAdd.add_dev_command(subparsers)
        CliAdd.add_plugin_command(subparsers)

        return parser