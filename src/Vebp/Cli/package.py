from src.Vebp.Data.package import Package


class CliPackage:
    @staticmethod
    def handle():
        print("显示 package 配置详情...\n")
        success = Package.print_config()

        print("\n说明:")
        print("- 使用 'vebp init' 创建配置文件")
        print("- 编辑 vebp-package.json 设置属性值")
        print("- 默认生成的配置只包含 name, main 和 console 属性")
        print("- 可以手动添加 icon, onefile 属性")
        print("- 运行 'vebp build' 使用配置构建项目")

        return success