from typing import Any

from src.Vebp.Data import VebpData


class Config(VebpData):
    FILENAME = "vebp-config.json"

    PROP_DICT = {
        "autoRun": {},
        "plugins": {},
    }

    @staticmethod
    def default() -> dict[str, Any]:
        return {
            "autoRun": True,
            "plugins": "plugins"
        }

