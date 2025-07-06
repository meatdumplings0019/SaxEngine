import importlib.util
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Dict, Any, Optional

from src.Libs.file import FolderStream
from src.Vebp.Data.globals import get_config
from src.Vebp.Data.plugin import PluginConfig
from src.Vebp.Plugin import Plugin


class PluginManager:
    def __init__(self):
        """
        插件管理器初始化
        """
        # 插件存储字典: {namespace: Plugin 实例}
        self.plugins: Dict[str, Plugin] = {}
        # 记录插件包名到路径的映射
        self.package_paths: Dict[str, str] = {}

    def load_plugins(self):
        """
        加载指定目录下的所有插件
        """
        plugin_dir = get_config().get("plugins", "plugins")

        plugin_dir_path = Path(plugin_dir)
        FolderStream(plugin_dir_path).create()

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

        meta = PluginConfig(plugin_dir / PluginConfig.FILENAME)

        namespace = meta.get("namespace", None)
        author = meta.get("author", "null")

        if not namespace:
            return

        if namespace in self.plugins:
            return

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

        # 4. 创建并存储 Plugin 实例
        plugin = Plugin(
            namespace=namespace,
            author=author,
            module=main_module,
            package_name=package_name,
            meta=meta.file
        )
        self.plugins[namespace] = plugin
        self.package_paths[package_name] = str(plugin_dir)

        print(f"✅ 插件加载成功: {namespace} by {author}")

    def run_hook(self, namespace: str, hook_name: str, *args, **kwargs) -> Any:
        """
        执行指定插件的钩子函数

        :param namespace: 插件命名空间
        :param hook_name: 钩子名称（不需要带 _hook 后缀）
        :param args: 传递给钩子函数的参数
        :param kwargs: 传递给钩子函数的关键字参数
        :return: 钩子函数的返回值
        """
        if namespace in self.plugins:
            return self.plugins[namespace].run_hook(hook_name, *args, **kwargs)

        print(f"插件未加载: {namespace}")
        return None

    def run_hook_all(self, hook_name: str, *args, **kwargs) -> list[Any]:
        if not self.plugins: return []

        return [n.run_hook(hook_name, *args, **kwargs) for n in self.plugins.values()]

    def get_plugin(self, namespace: str) -> Optional[Plugin]:
        """
        获取插件实例

        :param namespace: 插件命名空间
        :return: Plugin 实例或 None
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
            plugin = self.plugins[namespace]
            package_name = plugin.package_name

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