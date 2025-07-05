from src.Vebp.Builder.plugin import PluginBuilder
from src.Vebp.Plugin.globals import get_plugin_manager


class CliPlugin:
    @staticmethod
    def handle(args) -> None:
        print("\n🧩 Plugin Tool")

        if args.list:
            print("\n📋 已加载插件列表:")
            plugins = get_plugin_manager().list_plugins()

            if not plugins:
                print("  没有加载任何插件")
                return

            for pn in plugins:
                p = get_plugin_manager().get_plugin(pn)
                print(f"  🔌 {p.namespace}: 作者: {p.author}")
            return

        if args.build:
            if not hasattr(args, "path"):
                print("❌ 错误: 缺少 --path 参数")
                return

            print(f"🔨 构建插件: {args.path}")
            pb = PluginBuilder(args.path)
            pb.build()
            print("✅ 插件构建完成!")