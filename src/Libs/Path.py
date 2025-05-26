from pathlib import Path as PathLib
import os
import sys

class Path:
    @staticmethod
    def get() -> str:
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath("")

        return base_path

    @staticmethod
    def join(*args: str) -> str:
        base_path = Path.get()

        return os.path.join(base_path, *args)

    @staticmethod
    def get_full(path: str) -> str:
        return str(PathLib(path).resolve())

    @staticmethod
    def get_absolute(path: str) -> str:
        if getattr(sys, 'frozen', False):  # 检查是否在打包环境中
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(path)

        return base_path