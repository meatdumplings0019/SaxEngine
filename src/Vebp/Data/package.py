from src.Libs.path import MPath, MPath_
from src.Vebp.Data import VebpData


class Package(VebpData):
    FILENAME = "vebp-package.json"

    @staticmethod
    def generate_default() -> dict:
        project_name = MPath_.cwd.name
        return {
            "name": project_name,
            "venv": ".venv",
            "scripts": {}
        }