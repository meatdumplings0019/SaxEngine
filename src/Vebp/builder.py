import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Union
import platform
from .package import Package  # 导入 Package 类
from ..Libs.file import FileStream, FolderStream  # 导入文件操作工具类


class Builder:
    """PyInstaller 打包工具类"""

    def __init__(self, name=None, icon=None):
        """
        初始化构建器

        参数:
        name: 项目名称 (可选)
        icon: 应用图标路径 (可选)
        """
        self._name = name
        self._icon = Path(icon) if icon else None
        self._script_path = None
        self._console = False  # 默认隐藏控制台
        self._onefile = True  # 默认使用单文件模式
        self._assets: Dict[str, List[Path]] = {}  # 外部资源: 目标相对路径 -> 源文件列表
        self._inassets: Dict[str, List[Path]] = {}  # 内部资源: 目标相对路径 -> 源文件列表

        # 创建基础输出目录
        self._base_output_dir = Path("vebp-build")
        # 使用FolderStream确保目录存在
        FolderStream(str(self._base_output_dir)).create()

    @staticmethod
    def from_package():
        """
        从 vebp-package.json 创建构建器实例

        返回:
        Builder 实例，如果配置有效则返回实例，否则返回 None
        """
        # 读取 package 配置
        package_config = Package.read_config()
        if not package_config:
            return None

        # 创建构建器实例
        builder = Builder()

        # 使用 get 方法获取配置值，提供默认值
        builder._name = package_config.get('name', None)
        builder.set_script(package_config.get('main', None))
        builder.set_console(package_config.get('console', False))  # 默认为 False

        # 使用 get 方法获取 icon 属性
        icon = package_config.get('icon', None)
        if icon:
            builder._icon = Path(icon)

        # 使用 get 方法获取 onefile 属性
        onefile = package_config.get('onefile', True)  # 默认 True
        builder.set_onefile(onefile)

        return builder

    def set_script(self, script_path):
        """设置要打包的脚本路径"""
        if script_path:
            self._script_path = Path(script_path)
        return self

    def set_console(self, console):
        """设置是否显示控制台窗口"""
        if console is not None:
            self._console = console
        return self

    def set_onefile(self, onefile):
        """
        设置打包模式 (单文件或目录模式)

        参数:
        onefile: True 表示单可执行文件，False 表示带依赖的目录
        """
        if onefile is not None:
            self._onefile = onefile
        return self

    def add_assets(self, sources: List[Union[str, Path]], target_relative_path: str = ""):
        """
        添加外部资源 (文件或目录) 到输出目录

        参数:
        sources: 要复制的文件或目录路径列表
        target_relative_path: 项目目录中复制资源的相对路径
        """
        if not sources:
            return self

        # 将字符串路径转换为 Path 对象
        source_paths = [Path(source) for source in sources]

        # 如果目标路径不存在则初始化
        self._assets.setdefault(target_relative_path, [])

        # 将源添加到目标路径
        for source in source_paths:
            if not source.exists():
                print(f"警告: 资源源不存在: {source}", file=sys.stderr)
            else:
                self._assets[target_relative_path].append(source)

        return self

    def add_inassets(self, sources: List[Union[str, Path]], target_relative_path: str = ""):
        """
        添加内部资源 (文件或目录) 嵌入到可执行文件中

        参数:
        sources: 要嵌入的文件或目录路径列表
        target_relative_path: 可执行文件中嵌入资源的相对路径
        """
        if not sources:
            return self

        # 将字符串路径转换为 Path 对象
        source_paths = [Path(source) for source in sources]

        # 如果目标路径不存在则初始化
        self._inassets.setdefault(target_relative_path, [])

        # 将源添加到目标路径
        for source in source_paths:
            if not source.exists():
                print(f"警告: 内部资源源不存在: {source}", file=sys.stderr)
            else:
                self._inassets[target_relative_path].append(source)

        return self

    def validate(self):
        """验证输入参数"""
        if not self._name:
            raise ValueError("项目名称是必需的")

        if not self._script_path or not self._script_path.is_file():
            raise ValueError(f"脚本文件不存在: {self._script_path}")

        if self._icon and not self._icon.is_file():
            raise ValueError(f"图标文件不存在: {self._icon}")

        return True

    def _get_add_data_args(self):
        """为内部资源生成 PyInstaller 的 --add-data 参数"""
        add_data_args = []
        separator = ";" if platform.system() == "Windows" else ":"

        for target_relative, sources in self._inassets.items():
            for source in sources:
                # 将源转换为绝对路径
                abs_source = source.resolve()

                # 格式: "源路径[分隔符]目标路径"
                arg = f"{abs_source}{separator}{target_relative}"
                add_data_args.extend(["--add-data", arg])

        return add_data_args

    def _copy_assets(self):
        """使用FileStream和FolderStream复制所有外部资源到项目目录"""
        if not self._assets:
            return True

        print("\n复制外部资源...")
        success = True

        for target_relative, sources in self._assets.items():
            # 创建目标目录
            target_path = self._project_dir / target_relative
            target_folder = FolderStream(str(target_path))

            # 确保目标目录存在
            if not target_folder.create():
                print(f"  创建目录失败: {target_path}", file=sys.stderr)
                success = False
                continue

            for source in sources:
                try:
                    source_path = source.resolve()
                    if source.is_dir():
                        # 复制整个目录
                        dest_path = target_path / source.name
                        print(f"  复制目录: {source} -> {dest_path}")

                        # 如果目标目录已存在则删除
                        if dest_path.exists():
                            shutil.rmtree(dest_path)

                        # 使用FolderStream创建目标目录
                        FolderStream(str(dest_path)).create()

                        # 递归复制目录内容
                        for root, dirs, files in os.walk(source_path):
                            relative_path = Path(root).relative_to(source_path)
                            dest_dir = dest_path / relative_path

                            # 确保子目录存在
                            FolderStream(str(dest_dir)).create()

                            # 复制所有文件
                            for file in files:
                                src_file = Path(root) / file
                                dest_file = dest_dir / file
                                if not FileStream.copy(str(src_file), str(dest_file)):
                                    print(f"    复制文件失败: {src_file} -> {dest_file}", file=sys.stderr)
                                    success = False
                    else:
                        # 复制单个文件
                        dest_file = target_path / source.name
                        print(f"  复制文件: {source} -> {dest_file}")
                        if not FileStream.copy(str(source_path), str(dest_file)):
                            print(f"    复制文件失败: {source} -> {dest_file}", file=sys.stderr)
                            success = False
                except Exception as e:
                    print(f"  复制 {source} 出错: {str(e)}", file=sys.stderr)
                    success = False

        return success

    def build(self):
        """执行构建过程"""
        # 创建项目输出目录
        self._project_dir = self._base_output_dir / self._name
        FolderStream(str(self._project_dir)).create()

        try:
            self.validate()
        except ValueError as e:
            print(f"验证错误: {str(e)}", file=sys.stderr)
            return False

        # 构建 PyInstaller 命令
        cmd = ['pyinstaller', '--noconfirm']

        # 添加打包模式选项
        if self._onefile:
            cmd.append('--onefile')
        else:
            cmd.append('--onedir')

        # 添加控制台选项
        if not self._console:
            cmd.append('--noconsole')

        # 如果提供了图标则添加
        if self._icon:
            cmd.extend(['--icon', str(self._icon.resolve())])

        # 使用 --add-data 添加内部资源
        cmd.extend(self._get_add_data_args())

        # 添加脚本名称和路径
        cmd.extend(['--name', self._name, str(self._script_path.resolve())])

        # 执行打包命令 (隐藏输出)
        try:
            print(f"开始打包项目: {self._name}")
            print(f"脚本路径: {self._script_path}")
            print(f"打包模式: {'单文件' if self._onefile else '带依赖的目录'}")
            print(f"控制台设置: {'显示' if self._console else '隐藏'}")

            # 打印内部资源信息
            if self._inassets:
                print("要嵌入的内部资源:")
                for target_relative, sources in self._inassets.items():
                    for source in sources:
                        print(f"  {source} -> {target_relative}")

            print("打包进行中...")

            # 执行命令但不显示输出
            subprocess.run(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT,
                check=True
            )

        except subprocess.CalledProcessError as e:
            print(f"\n打包失败! 错误代码: {e.returncode}", file=sys.stderr)
            return False
        except FileNotFoundError:
            print("\n错误: 未找到 pyinstaller 命令，请确保已安装 PyInstaller", file=sys.stderr)
            print("安装命令: pip install pyinstaller", file=sys.stderr)
            return False

        # 根据打包模式确定输出文件/目录
        if self._onefile:
            # 单文件模式: dist/项目名称.exe
            source_path = Path('dist') / f"{self._name}.exe"
            target_path = self._project_dir / f"{self._name}.exe"
        else:
            # 目录模式: dist/项目名称/
            source_path = Path('dist') / self._name
            target_path = self._project_dir / self._name

        # 验证输出是否存在
        if not source_path.exists():
            print(f"\n错误: 未找到生成的输出 - {source_path}", file=sys.stderr)
            return False

        # 将输出复制到项目目录
        try:
            if self._onefile:
                # 复制单个文件
                if FileStream.copy(str(source_path), str(target_path)):
                    print(f"  已复制可执行文件到: {target_path}")
                else:
                    print(f"  复制可执行文件失败: {source_path} -> {target_path}", file=sys.stderr)
                    return False
            else:
                # 复制整个目录
                print(f"  复制目录: {source_path} -> {target_path}")

                # 创建目标目录
                FolderStream(str(target_path)).create()

                # 递归复制目录内容
                for item in source_path.iterdir():
                    dest_item = target_path / item.name
                    if item.is_dir():
                        shutil.copytree(item, dest_item, dirs_exist_ok=True)
                    else:
                        if not FileStream.copy(str(item), str(dest_item)):
                            print(f"    复制文件失败: {item} -> {dest_item}", file=sys.stderr)
                            return False

            print(f"\n项目构建成功!")
            print(f"输出目录: {self._project_dir}")
            print(f"输出文件: {target_path}")

            # 显示打包模式
            mode = "单文件" if self._onefile else "带依赖的目录"
            print(f"打包模式: {mode}")

            # 显示控制台设置
            console_status = "显示控制台" if self._console else "隐藏控制台"
            print(f"控制台设置: {console_status}")

            # 复制外部资源
            assets_success = self._copy_assets()

            return assets_success
        except Exception as e:
            print(f"\n输出复制失败: {str(e)}", file=sys.stderr)
            return False