from pathlib import Path

from src.Vebp.Data.config import Config


class VebpBase:
    def __init__(self, config_path):
        self._config = Config(Path(config_path) / Config.FILENAME)

    @property
    def config(self) -> Config:
        return self._config