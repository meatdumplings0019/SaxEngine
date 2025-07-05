from src.Vebp.Data import VebpData


class PluginConfig(VebpData):
    FILENAME = "vebp-plugin.json"

    @staticmethod
    def generate_default() -> dict:
        return {
            "namespace": "plugin",
            "author": "null"
        }