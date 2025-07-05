from src.Editor.Launch import run
from src.Vebp.Plugin.Manager import PluginManager

if __name__ == '__main__':
    # run()
    pm = PluginManager()

    pm.load_plugins("plugins")

    print("\n已加载插件:", pm.list_plugins())

    pm.run_hook("test", "build")