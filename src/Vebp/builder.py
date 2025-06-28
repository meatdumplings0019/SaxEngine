import os
import shutil
import subprocess
import sys
import platform
from pathlib import Path
from typing import Dict, List, Union
from src.Vebp.package import Package
from src.Libs.file import FileStream, FolderStream


class Builder:
    def __init__(self, name=None, icon=None):
        self._project_dir = None
        self._name = name
        self._icon = Path(icon) if icon else None
        self._script_path = None
        self._console = False  # 默认隐藏控制台
        self._onefile = True  # 默认使用单文件模式
        self._assets: Dict[str, List[Path]] = {}  # 外部资源: 目标相对路径 -> 源文件列表
        self._inassets: Dict[str, List[Path]] = {}  # 内部资源: 目标相对路径 -> 源文件列表

        self._base_output_dir = Path("vebp-build")
        FolderStream(str(self._base_output_dir)).create()

    @staticmethod
    def from_package():
        package_config = Package.read_config()
        if not package_config:
            return None

        builder = Builder()

        builder._name = package_config.get('name', None)
        builder.set_script(package_config.get('main', None))
        builder.set_console(package_config.get('console', False))

        icon = package_config.get('icon', None)
        if icon:
            builder._icon = Path(icon)

        onefile = package_config.get('onefile', True)  # 默认 True
        builder.set_onefile(onefile)

        return builder

    def set_script(self, script_path):
        if script_path:
            self._script_path = Path(script_path)
        return self

    def set_console(self, console):
        if console is not None:
            self._console = console
        return self

    def set_onefile(self, onefile):
        if onefile is not None:
            self._onefile = onefile
        return self

    def add_assets(self, sources: List[Union[str, Path]], target_relative_path: str = ""):
        if not sources:
            return self

        source_paths = [Path(source) for source in sources]

        self._assets.setdefault(target_relative_path, [])

        for source in source_paths:
            if not source.exists():
                print(f"警告: 资源源不存在: {source}", file=sys.stderr)
            else:
                self._assets[target_relative_path].append(source)

        return self

    def add_inassets(self, sources: List[Union[str, Path]], target_relative_path: str = ""):
        if not sources:
            return self

        source_paths = [Path(source) for source in sources]

        self._inassets.setdefault(target_relative_path, [])

        for source in source_paths:
            if not source.exists():
                print(f"警告: 内部资源源不存在: {source}", file=sys.stderr)
            else:
                self._inassets[target_relative_path].append(source)

        return self

    def _validate(self):
        if not self._name:
            raise ValueError("项目名称是必需的")

        if not self._script_path or not self._script_path.is_file():
            raise ValueError(f"脚本文件不存在: {self._script_path}")

        if self._icon and not self._icon.is_file():
            raise ValueError(f"图标文件不存在: {self._icon}")

        return True

    def _get_add_data_args(self):
        add_data_args = []
        separator = ";" if platform.system() == "Windows" else ":"

        for target_relative, sources in self._inassets.items():
            for source in sources:
                abs_source = source.resolve()

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
                        dest_path = target_path / source.name
                        print(f"  复制目录: {source} -> {dest_path}")

                        if dest_path.exists():
                            shutil.rmtree(dest_path)

                        FolderStream(str(dest_path)).create()

                        for root, dirs, files in os.walk(source_path):
                            relative_path = Path(root).relative_to(source_path)
                            dest_dir = dest_path / relative_path

                            FolderStream(str(dest_dir)).create()

                            # 复制所有文件
                            for file in files:
                                src_file = Path(root) / file
                                dest_file = dest_dir / file
                                if not FileStream.copy(str(src_file), str(dest_file)):
                                    print(f"    复制文件失败: {src_file} -> {dest_file}", file=sys.stderr)
                                    success = False
                    else:
                        dest_file = target_path / source.name
                        print(f"  复制文件: {source} -> {dest_file}")
                        if not FileStream.copy(str(source_path), str(dest_file)):
                            print(f"    复制文件失败: {source} -> {dest_file}", file=sys.stderr)
                            success = False
                except Exception as e:
                    print(f"  复制 {source} 出错: {str(e)}", file=sys.stderr)
                    success = False

        return success

    def _print_result(self, target_path):
        print(f"\n项目构建成功!")
        print(f"输出目录: {self._project_dir}")
        print(f"输出文件: {target_path}")

        print(f"单文件打包: {self._onefile}")

        print(f"显示控制台: {self._console}")

    def _copy_exe(self, source_path, target_path):
        if self._onefile:
            if FileStream.copy(str(source_path), str(target_path)):
                print(f"  已复制可执行文件到: {target_path}")
                return True
            else:
                print(f"  复制可执行文件失败: {source_path} -> {target_path}", file=sys.stderr)
                return False
        else:
            print(f"  复制目录: {source_path} -> {target_path}")

            for item in source_path.iterdir():
                dest_item = target_path / item.name
                if item.is_dir():
                    shutil.copytree(item, dest_item, dirs_exist_ok=True)
                    return True
                else:
                    if not FileStream.copy(str(item), str(dest_item)):
                        print(f"    复制文件失败: {item} -> {dest_item}", file=sys.stderr)
                        return False

            return True

    def _start_build(self, cmd):
        print(f"开始打包项目: {self._name}")
        print(f"脚本路径: {self._script_path}")
        print(f"打包模式: {'单文件' if self._onefile else '带依赖的目录'}")
        print(f"控制台设置: {'显示' if self._console else '隐藏'}")

        if self._inassets:
            print("要嵌入的内部资源:")
            for target_relative, sources in self._inassets.items():
                for source in sources:
                    print(f"  {source} -> {target_relative}")

        print("打包进行中...")

        subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
            check=True
        )

    def _get_cmd(self):
        cmd = ['pyinstaller', '--noconfirm']

        if self._onefile:
            cmd.append('--onefile')
        else:
            cmd.append('--onedir')

        if not self._console:
            cmd.append('--noconsole')

        if self._icon:
            cmd.extend(['--icon', str(self._icon.resolve())])

        cmd.extend(self._get_add_data_args())

        cmd.extend(['--name', self._name, str(self._script_path.resolve())])

        return cmd

    @staticmethod
    def _run_executable(exe_path: Path):
        try:
            if not exe_path.exists():
                print(f"可执行文件不存在: {exe_path}", file=sys.stderr)
                return

            print(f"\n正在运行程序: {exe_path}")

            # 根据系统决定如何运行
            if platform.system() == 'Windows':
                # Windows系统
                subprocess.Popen([str(exe_path)], creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                # 类Unix系统
                subprocess.Popen([str(exe_path)])
        except Exception as e:
            print(f"运行程序失败: {str(e)}", file=sys.stderr)

    def build(self):
        self._project_dir = self._base_output_dir / self._name
        FolderStream(str(self._project_dir)).create()

        try:
            self._validate()
        except ValueError as e:
            print(f"验证错误: {str(e)}", file=sys.stderr)
            return False

        try:
            self._start_build(self._get_cmd())
        except subprocess.CalledProcessError as e:
            print(f"\n打包失败! 错误代码: {e.returncode}", file=sys.stderr)
            return False
        except FileNotFoundError:
            print("\n错误: 未找到 pyinstaller 命令，请确保已安装 PyInstaller", file=sys.stderr)
            print("安装命令: pip install pyinstaller", file=sys.stderr)
            return False

        if self._onefile:
            source_path = Path('dist') / f"{self._name}.exe"
            target_path = self._project_dir / f"{self._name}.exe"
        else:
            source_path = Path('dist') / self._name
            target_path = self._project_dir

        if not source_path.exists():
            print(f"\n错误: 未找到生成的输出 - {source_path}", file=sys.stderr)
            return False

        try:
            copy = self._copy_exe(source_path, target_path)
            self._print_result(target_path)
            assets = self._copy_assets()

            self._run_executable(target_path)

            return copy and assets
        except Exception as e:
            print(f"\n输出复制失败: {str(e)}", file=sys.stderr)
            return False

    @property
    def onefile(self):
        return self._onefile