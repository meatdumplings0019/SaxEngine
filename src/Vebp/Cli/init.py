from pathlib import Path

from src.Vebp.Data.build_config import BuildConfig
from src.Vebp.Data.config import Config
from src.Vebp.Data.pack import Pack
from src.Vebp.Data.package import Package


class CliInit:
    @staticmethod
    def handle(args) -> bool:
        print("正在初始化 VEBP 项目...")

        path = getattr(args, 'path', ".")

        project_name = Path.cwd().name

        package_success = Package.create(path, args.force)
        build_success = BuildConfig.create(path, args.force)
        config_success = Config.create(path, args.force)

        if args.pack:
            Pack.create(args.force)

        if build_success and config_success and package_success:
            print(f"\n项目 '{project_name}' 初始化成功!")
            print("下一步:")
            print("1. 编辑 vebp-build.json 设置 'main' 属性 (您的入口脚本)")
            print("2. 运行 'vebp build' 打包您的应用")
            return True

        print("\n初始化完成但有警告。")
        return False