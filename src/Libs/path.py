import os
import sys
import inspect
from pathlib import Path


class PathUtils:
    """路径操作工具类，封装常用路径操作方法"""

    @staticmethod
    def get_cwd():
        """
        获取当前工作目录（命令行路径）

        返回:
            str: 当前工作目录的绝对路径
        """
        return Path(os.getcwd())

    @staticmethod
    def get_script_dir():
        """
        获取当前执行脚本所在的目录

        返回:
            str: 当前脚本所在目录的绝对路径
        """
        return Path(os.path.dirname(os.path.abspath(sys.argv[0])))

    @staticmethod
    def get_caller_dir():
        """
        获取调用者所在的目录（在模块中使用时获取导入模块的位置）

        返回:
            str: 调用者所在目录的绝对路径
        """
        # 获取调用栈中上一帧的信息
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        if module and hasattr(module, '__file__'):
            return os.path.dirname(os.path.abspath(module.__file__))
        return Path(PathUtils.get_script_dir())

    @staticmethod
    def change_directory(path):
        """
        改变当前工作目录

        参数:
            path (str): 目标路径
        """
        os.chdir(path)

    @staticmethod
    def resolve_relative_path(relative_path, base_path=None):
        """
        解析相对路径为绝对路径

        参数:
            relative_path (str): 相对路径
            base_path (str, optional): 基础路径，默认为当前工作目录

        返回:
            str: 绝对路径
        """
        base = base_path or PathUtils.get_cwd()
        return Path(os.path.abspath(str(os.path.join(base, relative_path))))

    @staticmethod
    def get_home_dir():
        """
        获取用户主目录

        返回:
            str: 用户主目录路径
        """
        return Path(os.path.expanduser("~"))

    @staticmethod
    def is_absolute_path(path):
        """
        检查路径是否为绝对路径

        参数:
            path (str): 要检查的路径

        返回:
            bool: 如果是绝对路径返回True，否则False
        """
        return os.path.isabs(path)

    @staticmethod
    def get_path_components(path):
        """
        分解路径为各个组成部分

        返回:
            tuple: (目录名, 基本文件名, 扩展名)
        """
        dir_name = os.path.dirname(path)
        base_name = os.path.basename(path)
        file_name, ext = os.path.splitext(base_name)
        return dir_name, file_name, ext