﻿from src.Vebp.Data import VebpData


class BuildConfig(VebpData):
    FILENAME = "vebp-build.json"

    @staticmethod
    def generate_default() -> dict:
        return {
            "main": "dev.py",
            "console": False
        }