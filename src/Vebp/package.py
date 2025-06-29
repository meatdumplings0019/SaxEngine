import json
import sys
from pathlib import Path


class Package:
    FILENAME = "vebp-package.json"

    PROPERTIES = {
        "name": {
            "description": "项目名称",
            "required": True,
            "default": "当前文件夹名称",
            "example": "my-project"
        },
        "main": {
            "description": "入口脚本文件路径",
            "required": True,
            "default": "无",
            "example": "src/main.py"
        },
        "console": {
            "description": "是否显示控制台窗口",
            "required": False,
            "default": False,
            "example": True
        },
        "icon": {
            "description": "应用程序图标路径 (.ico 文件)",
            "required": False,
            "default": "无",
            "example": "assets/icon.ico"
        },
        "onefile": {
            "description": "是否使用单文件打包模式",
            "required": False,
            "default": True,
            "example": False
        },
        "venv": {
            "description": "虚拟环境目录名称",
            "required": False,
            "default": ".venv",
            "example": "venv"
        }
    }

    @staticmethod
    def generate_default() -> dict:
        project_name = Path.cwd().name
        return {
            "name": project_name,
            "main": "",  # 默认为空
            "console": False,  # 默认不显示控制台
            "venv": ".venv"  # 默认虚拟环境目录
        }

    @classmethod
    def create_config(cls, overwrite=False) -> bool:
        file_path = Path.cwd() / cls.FILENAME

        if file_path.exists() and not overwrite:
            print(f"{cls.FILENAME} 已存在。使用 --force 覆盖。")
            return False

        config = cls.generate_default()
        with open(file_path, 'w') as f:
            json.dump(config, f, indent=2)

        project_name = config.get("name", "未知项目")
        print(f"成功创建 {cls.FILENAME}! 项目名称: {project_name}")
        return True

    @classmethod
    def read_config(cls):
        file_path = Path.cwd() / cls.FILENAME

        if not file_path.exists():
            return None

        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"读取 {cls.FILENAME} 出错: {str(e)}", file=sys.stderr)
            return None

    @classmethod
    def print_config(cls):
        config = cls.read_config()

        print("vebp-package.json 属性说明:")
        print("=" * 60)

        for prop, info in cls.PROPERTIES.items():
            value = config.get(prop, None) if config else None

            if value is None:
                value_str = "未设置"
            elif isinstance(value, (str, int, bool)):
                value_str = str(value)
            else:
                value_str = json.dumps(value, ensure_ascii=False)

            print(f"属性: {prop}")
            print(f"  描述: {info.get('description', '无描述')}")
            print(f"  必需: {'是' if info.get('required', False) else '否'}")
            print(f"  默认值: {info.get('default', '无')}")
            print(f"  当前值: {value_str}")
            print(f"  示例: {info.get('example', '无')}")
            print("-" * 60)

        return True