from src.Vebp.Data.globals import get_config
from src.Vebp.Plugin.globals import get_plugin_manager


class VebpBase:
    def __init__(self):
        get_plugin_manager().load_plugins(get_config().get("plugins", "plugins"))