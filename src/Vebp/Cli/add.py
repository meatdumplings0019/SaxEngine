class CliAdd:
    @staticmethod
    def add_build_command(subparsers):
        build_parser = subparsers.add_parser(
            'build',
            help='构建可执行文件',
            description='将 Python 脚本打包成可执行文件',
            epilog='''构建示例:
                  vebp build MyProject --src app.py
                  vebp build MyApp -s app.py -i app.ico -c
                  vebp build ProjectX -s main.py -d
                  vebp build Game -s app.py --asset "images;resources" --asset "sfx;resources"
                  vebp build App -s app.py --in_asset "config.json;settings"
                  vebp build App -s app.py --in_asset "templates;ui" --asset "README.md"
                  vebp build  # 使用 vebp-build.json 中的配置
                ''')

        build_parser.add_argument('name', nargs='?', default=None,
                                  help='项目名称 (如果在 vebp-build.json 中定义了则为可选)')
        build_parser.add_argument('--src', '-s',
                                  help='要打包的 Python 脚本路径 (如果在 vebp-build.json 中定义了则为可选)')

        build_parser.add_argument('--icon', '-i',
                                  help='应用程序图标 (.ico 文件)')
        build_parser.add_argument('--console', '-c', action='store_true',
                                  help='显示控制台窗口 (默认隐藏)')
        build_parser.add_argument('--onedir', '-d', action='store_true',
                                  help='使用目录模式而不是单文件模式 (默认: 单文件)')

        build_parser.add_argument('--asset', action='append',
                                  help='外部资源: "源路径;目标相对路径" (复制到输出目录)')
        build_parser.add_argument('--in_asset', action='append',
                                  help='内部资源: "源路径;目标相对路径" (嵌入到可执行文件中)')

    @staticmethod
    def add_init_command(subparsers):
        init_parser = subparsers.add_parser(
            'init',
            help='初始化项目配置',
            description='创建 vebp-build.json 和 vebp-config.json 文件'
        )

        init_parser.add_argument('--force', '-f', action='store_true',
                                 help='覆盖现有配置文件')

        init_parser.add_argument('--pack', '-p', action='store_true',
                                 help='添加pack配置文件')

        init_parser.add_argument('path', nargs='?', default=".",
                                  help='生成路径')

    @staticmethod
    def add_pack_command(subparsers):
        pack_parser = subparsers.add_parser(
            'pack',
            help='构建python包',
            description='构建python包'
        )

    @staticmethod
    def add_package_command(subparsers):
        subparsers.add_parser(
            'package',
            help='显示 package 配置详情',
            description='打印 vebp-build.json 文件的详细属性说明'
        )