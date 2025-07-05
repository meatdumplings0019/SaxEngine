from src.Vebp.Builder.plugin import PluginBuilder
from src.Vebp.Plugin.globals import get_plugin_manager


class CliPlugin:
    @staticmethod
    def handle(args) -> None:
        print()
        print("Plugin Tool")
        print()

        if args.list:
            for pn in get_plugin_manager().list_plugins():
                p = get_plugin_manager().get_plugin(pn)
                print(f"{p.namespace}: author: {p.author}")

            return

        if args.build:
            if not hasattr(args, "path"):
                raise AttributeError("Dont path argument")
            pb = PluginBuilder(args.path)
            pb.build()