from typing import Any

from src.Vebp.Data import VebpData


class Config(VebpData):
    FILENAME = "vebp-config.json"

    @staticmethod
    def generate_default() -> dict:
        return {}

    @staticmethod
    def default() -> dict[str, Any]:
        return {
            "autoRun": True
        }

