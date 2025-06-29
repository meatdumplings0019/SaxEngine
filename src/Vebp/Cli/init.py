from pathlib import Path
from src.Vebp.Data.config import Config
from src.Vebp.Data.package import Package


class CliInit:
    @staticmethod
    def handle(args):
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