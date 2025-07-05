from pathlib import Path

from src.Libs.file import FolderStream
from src.Libs.path import MPath_
from src.Vebp.Base import VebpBase


class BaseBuilder(VebpBase):
    def __init__(self, name=None, base_path=".", config_path=".") -> None:
        super().__init__(config_path)
        self._name = name
        self._base_path = Path(base_path)
        self._venv = ".venv"

        self._project_dir = None

        self._base_output_dir = MPath_.cwd / Path("vebp-build")
        FolderStream(self._base_output_dir).create()

    @property
    def name(self) -> str:
        return self._name

    @property
    def project_dir(self) -> Path:
        return self._project_dir

    @property
    def venv(self) -> str:
        return self._venv

    @venv.setter
    def venv(self, value) -> None:
        self._venv = value

    def _validate(self) -> None:
        if not self.name:
            raise ValueError("项目名称是必需的")