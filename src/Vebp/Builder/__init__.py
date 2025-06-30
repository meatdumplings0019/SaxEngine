from pathlib import Path
from ...Libs.file import FolderStream
from ...Libs.path import PathUtils


class BaseBuilder:
    def __init__(self, name=None, base_path="."):
        self._name = name
        self._base_path = Path(base_path)
        self._venv = ".venv"

        self._project_dir = None

        self._base_output_dir = PathUtils.get_cwd() / Path("vebp-build")
        FolderStream(self._base_output_dir).create()

    @property
    def name(self):
        return self._name

    @property
    def project_dir(self):
        return self._project_dir

    @property
    def venv(self):
        return self._venv

    @venv.setter
    def venv(self, value):
        self._venv = value

    def _validate(self):
        if not self.name:
            raise ValueError("项目名称是必需的")