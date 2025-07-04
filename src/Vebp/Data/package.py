from src.Libs.path import MPath, mPath
from src.Vebp.Data import VebpData


class Package(VebpData):
    FILENAME = "vebp-package.json"

    @staticmethod
    def generate_default() -> dict:
        project_name = mPath.cwd.name
        return {
            "name": project_name,
            "venv": ".venv"
        }