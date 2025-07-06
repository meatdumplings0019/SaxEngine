from src.Vebp.Plugin.globals import get_plugin_manager


class VebpBase:
    def __init__(self):
        get_plugin_manager().load_plugins()