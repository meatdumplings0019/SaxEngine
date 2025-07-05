import importlib.util
import json
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Dict, Any, Optional, List


class PluginManager:
    def __init__(self):
        """
        插件管理器初始化
        """
        # 插件存储字典: {namespace: {"module": module, "meta": dict, "package": package_name}}
        self.plugins: Dict[str, Dict[str, Any]] = {}
        # 记录插件包名到路径的映射
        self.package_paths: Dict[str, str] = {}

    def load_plugins(self, plugin_dir: str):
        """
        加载指定目录下的所有插件

        :param plugin_dir: 插件目录路径
        """
        plugin_dir_path = Path(plugin_dir)
        if not plugin_dir_path.exists():
            print(f"⚠️ 插件目录不存在: {plugin_dir}")
            return

        # 加载ZIP插件
        for zip_file in plugin_dir_path.glob("*.zip"):
            with tempfile.TemporaryDirectory() as tmp_dir:
                try:
                    # 解压ZIP
                    with zipfile.ZipFile(zip_file, 'r') as z:
                        z.extractall(tmp_dir)

                    # 加载插件
                    self._load_single_plugin(Path(tmp_dir))
                except Exception as e:
                    print(f"🔥 ZIP插件加载失败 [{zip_file.name}]: {str(e)}")

        # 加载文件夹插件
        for folder in plugin_dir_path.iterdir():
            if folder.is_dir():
                try:
                    self._load_single_plugin(folder)
                except Exception as e:
                    print(f"🔥 文件夹插件加载失败 [{folder.name}]: {str(e)}")

    def _load_single_plugin(self, plugin_path: Path):
        """
        加载单个插件

        :param plugin_path: 插件路径
        """
        plugin_dir = Path(plugin_path)

        # 1. 读取元数据文件
        meta_file = plugin_dir / "vebp-plugin.json"
        if not meta_file.exists():
            raise FileNotFoundError(f"缺少 vebp-plugin.json 文件")

        try:
            with open(meta_file, 'r', encoding='utf-8') as f:
                meta = json.load(f)
        except json.JSONDecodeError:
            raise ValueError("vebp-plugin.json 格式错误")

        # 验证必要字段
        required_fields = ["namespace", "author"]
        for field in required_fields:
            if field not in meta:
                raise ValueError(f"vebp-plugin.json 缺少字段: {field}")

        namespace = meta["namespace"]

        # 检查是否已加载
        if namespace in self.plugins:
            print(f"⚠️ 插件已加载: {namespace}")
            return

        # 2. 创建插件包
        package_name = f"plugin_{namespace}"

        # 如果包已存在，先卸载
        if package_name in sys.modules:
            self.unload_plugin(namespace)

        # 创建包规格
        spec = importlib.util.spec_from_loader(
            package_name,
            loader=None,
            origin=str(plugin_dir),
            is_package=True
        )
        if spec is None:
            raise ImportError(f"无法创建包规范: {package_name}")

        # 创建包模块
        package_module = importlib.util.module_from_spec(spec)
        sys.modules[package_name] = package_module

        # 设置包路径
        package_module.__path__ = [str(plugin_dir)]
        package_module.__package__ = package_name

        # 3. 加载主模块
        entry_file = plugin_dir / "main.py"
        if not entry_file.exists():
            # 清理包模块
            del sys.modules[package_name]
            raise FileNotFoundError("入口文件 main.py 不存在")

        # 创建主模块规范
        main_module_name = f"{package_name}.main"
        spec = importlib.util.spec_from_file_location(
            main_module_name,
            str(entry_file),
            submodule_search_locations=[str(plugin_dir)]
        )
        if spec is None:
            # 清理包模块
            del sys.modules[package_name]
            raise ImportError(f"无法创建模块规范: {entry_file}")

        main_module = importlib.util.module_from_spec(spec)
        sys.modules[main_module_name] = main_module

        try:
            # 设置主模块的包信息
            main_module.__package__ = package_name
            main_module.__path__ = [str(plugin_dir)]

            # 执行主模块
            spec.loader.exec_module(main_module)
        except Exception as e:
            # 清理
            del sys.modules[main_module_name]
            del sys.modules[package_name]
            raise RuntimeError(f"主模块执行失败: {str(e)}")

        # 4. 存储插件信息
        self.plugins[namespace] = {
            "module": main_module,  # 存储主模块
            "meta": meta,
            "package": package_name
        }
        self.package_paths[package_name] = str(plugin_dir)

        print(f"✅ 插件加载成功: {namespace} by {meta['author']}")

    def run_hook(self, namespace: str, hook_name: str, *args, **kwargs) -> Any:
        """
        执行指定插件的钩子函数

        :param namespace: 插件命名空间
        :param hook_name: 钩子名称（不需要带 _hook 后缀）
        :param args: 传递给钩子函数的参数
        :param kwargs: 传递给钩子函数的关键字参数
        :return: 钩子函数的返回值
        """
        if namespace not in self.plugins:
            raise ValueError(f"插件未加载: {namespace}")

        plugin = self.plugins[namespace]
        module = plugin["module"]

        # 构建完整的钩子函数名
        hook_func_name = f"{hook_name}_hook"

        # 检查钩子函数是否存在
        if not hasattr(module, hook_func_name):
            raise AttributeError(f"插件 {namespace} 未定义钩子函数: {hook_func_name}")

        hook_func = getattr(module, hook_func_name)

        # 检查是否为可调用函数
        if not callable(hook_func):
            raise TypeError(f"插件 {namespace} 的 {hook_func_name} 不是可调用函数")

        try:
            # 执行钩子函数
            return hook_func(*args, **kwargs)
        except Exception as e:
            print(f"⚠️ 钩子执行失败 [{namespace}.{hook_func_name}]: {str(e)}")
            raise

    def get_plugin(self, namespace: str) -> Optional[Dict[str, Any]]:
        """
        获取插件信息

        :param namespace: 插件命名空间
        :return: 插件信息字典或 None
        """
        return self.plugins.get(namespace)

    def list_plugins(self) -> list[str]:
        """
        列出所有已加载插件的命名空间

        :return: 插件命名空间列表
        """
        return list(self.plugins.keys())

    def unload_plugin(self, namespace: str):
        """
        卸载指定插件

        :param namespace: 插件命名空间
        """
        if namespace in self.plugins:
            plugin_info = self.plugins[namespace]
            package_name = plugin_info["package"]

            # 清理所有相关模块
            to_remove = [name for name in sys.modules
                         if name == package_name or name.startswith(f"{package_name}.")]

            for module_name in to_remove:
                del sys.modules[module_name]

            # 清理插件记录
            del self.plugins[namespace]
            if package_name in self.package_paths:
                del self.package_paths[package_name]

            print(f"✅ 插件已卸载: {namespace}")
        else:
            print(f"⚠️ 插件未加载: {namespace}")