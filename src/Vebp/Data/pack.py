import json
from src.Libs.path import PathUtils


class Pack:
    FILENAME = "vebp-pack.json"

    PROPERTIES = {}

    @staticmethod
    def generate_default() -> dict:
        project_name = PathUtils.get_cwd().name
        return {
            "name": project_name,
            "setup": "",  # 默认为空
            "venv": ".venv"  # 默认虚拟环境目录
        }

    @classmethod
    def create_config(cls, overwrite=False) -> bool:
        file_path = PathUtils.get_cwd() / cls.FILENAME

        if file_path.exists() and not overwrite:
            print(f"{cls.FILENAME} 已存在。使用 --force 覆盖。")
            return False

        config = cls.generate_default()
        with open(file_path, 'w') as f:
            json.dump(config, f, indent=2)

        project_name = config.get("name", "未知项目")
        print(f"成功创建 {cls.FILENAME}! 包名称: {project_name}")
        return True

    @classmethod
    def read_config(cls):
        file_path = PathUtils.get_cwd() / cls.FILENAME

        if not file_path.exists():
            return None

        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"读取 {cls.FILENAME} 出错: {str(e)}", file=sys.stderr)
            return None