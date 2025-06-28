import json
import sys
from pathlib import Path


class Config:
    """管理 vebp-config.json 配置文件"""
    FILENAME = "vebp-config.json"

    @staticmethod
    def generate_default() -> dict:
        """生成默认的 build 配置"""
        # 返回空对象
        return {}

    @classmethod
    def create_config(cls, overwrite=False) -> bool:
        """创建 build 配置文件"""
        file_path = Path.cwd() / cls.FILENAME

        if file_path.exists() and not overwrite:
            print(f"{cls.FILENAME} 已存在。使用 --force 覆盖。")
            return False

        config = cls.generate_default()
        with open(file_path, 'w') as f:
            json.dump(config, f, indent=2)

        print(f"成功创建 {cls.FILENAME}! (空配置)")
        return True

    @classmethod
    def read_config(cls):
        """读取 config 配置"""
        file_path = Path.cwd() / cls.FILENAME

        if not file_path.exists():
            return None

        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"读取 {cls.FILENAME} 出错: {str(e)}", file=sys.stderr)
            return None