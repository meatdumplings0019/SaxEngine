from src.Libs.file import FileStream
from src.Libs.path import PathUtils


class BuildConfig:
    FILENAME = "vebp-build.json"

    def __init__(self, path):
        self.file = self._read(path)

    def _read(self, path):
        f = FileStream(path)
        if not f.is_name(self.FILENAME):
            raise FileNotFoundError

        return f.read_json()

    @staticmethod
    def generate_default() -> dict:
        return {
            "main": "run.py",
            "console": False
        }

    @classmethod
    def create(cls, path, overwrite=False):
        file_path = FileStream(PathUtils.get_cwd() / path / cls.FILENAME)

        if file_path.exists() and not overwrite:
            print(f"{cls.FILENAME} 已存在。使用 --force 覆盖。")
            return False

        file_path.create()
        config = cls.generate_default()
        file_path.write_json(config)

        print(f"成功创建 {cls.FILENAME}!")

        return True

    def get(self, key, default=None):
        return self.file.get(key, default)