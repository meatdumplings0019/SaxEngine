﻿from pathlib import Path
from src.Vebp.Data.build_config import BuildConfig
from src.Vebp.Data.config import Config
from src.Vebp.Data.pack import Pack
from src.Vebp.Data.package import Package


class CliInit:
    @staticmethod
    def handle(args) -> bool:
        print("🛠️ 正在初始化 VEBP 项目...")

        path = getattr(args, 'path', ".")
        project_name = Path.cwd().name

        package_success = Package.create(path, args.force)
        build_success = BuildConfig.create(path, args.force)
        config_success = Config.create(path, args.force)

        if args.pack:
            print("📦 创建打包配置文件...")
            Pack.create(args.force)

        if build_success and config_success and package_success:
            print(f"\n✅ 项目 '{project_name}' 初始化成功!")
            print("👉 下一步:")
            print("1. 📝 编辑 vebp-build.json 设置 'main' 属性 (您的入口脚本)")
            print("2. 📝 编辑 vebp-package.json 添加自定义脚本到 'scripts' 部分")
            print("3. 🚀 运行 'vebp dev <脚本名>' 执行自定义脚本")
            print("4. 🔨 运行 'vebp build' 打包您的应用")
            return True

        print("\n⚠️ 初始化完成但有警告。")
        return False