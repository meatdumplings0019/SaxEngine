import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Union
import platform


class Builder:
    """PyInstaller Packaging Tool Class"""

    def __init__(self, name, icon=None):
        """
        Initialize the builder

        Parameters:
        name: Project name (required)
        icon: Application icon path (optional)
        """
        self._name = name
        self._icon = Path(icon) if icon else None
        self._script_path = None
        self._console = False  # Hide console by default
        self._onefile = True  # Use onefile mode by default
        self._assets: Dict[str, List[Path]] = {}  # External assets: target_relative_path -> list of sources
        self._inassets: Dict[str, List[Path]] = {}  # Internal assets: target_relative_path -> list of sources

        # Create base output directory
        self._base_output_dir = Path("vebp-build")
        self._base_output_dir.mkdir(exist_ok=True)

        # Project output directory
        self._project_dir = self._base_output_dir / self._name
        self._project_dir.mkdir(exist_ok=True)

    def set_script(self, script_path):
        """Set the script path to package"""
        self._script_path = Path(script_path)
        return self

    def set_console(self, console):
        """Set whether to show console window"""
        self._console = console
        return self

    def set_onefile(self, onefile):
        """
        Set packaging mode (onefile or onedir)

        Parameters:
        onefile: True for single executable file, False for directory with dependencies
        """
        self._onefile = onefile
        return self

    def add_assets(self, sources: List[Union[str, Path]], target_relative_path: str = ""):
        """
        Add external assets (files or directories) to be copied to the output directory

        Parameters:
        sources: List of paths to files or directories to copy
        target_relative_path: Relative path within the project directory to copy assets to
        """
        # Convert string paths to Path objects
        source_paths = [Path(source) for source in sources]

        # Initialize target path if not exists
        if target_relative_path not in self._assets:
            self._assets[target_relative_path] = []

        # Add sources to the target path
        for source in source_paths:
            if not source.exists():
                print(f"Warning: Asset source does not exist: {source}", file=sys.stderr)
            else:
                self._assets[target_relative_path].append(source)

        return self

    def add_inassets(self, sources: List[Union[str, Path]], target_relative_path: str = ""):
        """
        Add internal assets (files or directories) to be embedded in the executable

        Parameters:
        sources: List of paths to files or directories to embed
        target_relative_path: Relative path within the executable to embed assets at
        """
        # Convert string paths to Path objects
        source_paths = [Path(source) for source in sources]

        # Initialize target path if not exists
        if target_relative_path not in self._inassets:
            self._inassets[target_relative_path] = []

        # Add sources to the target path
        for source in source_paths:
            if not source.exists():
                print(f"Warning: Internal asset source does not exist: {source}", file=sys.stderr)
            else:
                self._inassets[target_relative_path].append(source)

        return self

    def validate(self):
        """Validate input parameters"""
        if not self._script_path or not self._script_path.is_file():
            raise ValueError(f"Script file does not exist: {self._script_path}")

        if self._icon and not self._icon.is_file():
            raise ValueError(f"Icon file does not exist: {self._icon}")

        return True

    def _get_add_data_args(self):
        """Generate PyInstaller --add-data arguments for internal assets"""
        add_data_args = []
        separator = ";" if platform.system() == "Windows" else ":"

        for target_relative, sources in self._inassets.items():
            for source in sources:
                # Convert source to absolute path
                abs_source = source.resolve()

                # Format: "source_path[separator]target_path"
                arg = f"{abs_source}{separator}{target_relative}"
                add_data_args.extend(["--add-data", arg])

        return add_data_args

    def _copy_assets(self):
        """Copy all registered external assets to the project directory"""
        if not self._assets:
            return True

        print("\nCopying external assets...")
        success = True

        for target_relative, sources in self._assets.items():
            target_path = self._project_dir / target_relative
            target_path.mkdir(parents=True, exist_ok=True)

            for source in sources:
                try:
                    if source.is_dir():
                        # Copy directory recursively
                        dest_path = target_path / source.name
                        print(f"  Copying directory: {source} -> {dest_path}")

                        # Remove existing directory if exists
                        if dest_path.exists():
                            shutil.rmtree(dest_path)

                        # Copy directory
                        shutil.copytree(source, dest_path)
                    else:
                        # Copy single file
                        dest_path = target_path / source.name
                        print(f"  Copying file: {source} -> {dest_path}")
                        shutil.copy2(source, dest_path)
                except Exception as e:
                    print(f"  Error copying {source}: {str(e)}", file=sys.stderr)
                    success = False

        return success

    def build(self):
        """Execute the build process"""
        try:
            self.validate()
        except ValueError as e:
            print(f"Validation error: {str(e)}", file=sys.stderr)
            return False

        # Build PyInstaller command
        cmd = ['pyinstaller', '--noconfirm']

        # Add packaging mode option
        if self._onefile:
            cmd.append('--onefile')
        else:
            cmd.append('--onedir')

        # Add console option
        if not self._console:
            cmd.append('--noconsole')

        # Add icon if provided
        if self._icon:
            cmd.extend(['--icon', str(self._icon.resolve())])

        # Add internal assets using --add-data
        cmd.extend(self._get_add_data_args())

        # Add script name and path
        cmd.extend(['--name', self._name, str(self._script_path.resolve())])

        # Execute packaging command (hide output)
        try:
            print(f"Starting packaging for project: {self._name}")
            print(f"Script path: {self._script_path}")
            print(f"Packaging mode: {'Single executable' if self._onefile else 'Directory with dependencies'}")

            # Print internal assets info
            if self._inassets:
                print("Internal assets to embed:")
                for target_relative, sources in self._inassets.items():
                    for source in sources:
                        print(f"  {source} -> {target_relative}")

            print("Packaging in progress...")

            # Execute command without showing output
            subprocess.run(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT,
                check=True
            )

        except subprocess.CalledProcessError as e:
            print(f"\nPackaging failed! Error code: {e.returncode}", file=sys.stderr)
            return False
        except FileNotFoundError:
            print("\nError: pyinstaller command not found, please ensure PyInstaller is installed", file=sys.stderr)
            print("Install command: pip install pyinstaller", file=sys.stderr)
            return False

        # Determine output file/directory based on packaging mode
        if self._onefile:
            # Single file mode: dist/project_name.exe
            source_path = Path('dist') / f"{self._name}.exe"
            target_path = self._project_dir / f"{self._name}.exe"
        else:
            # Directory mode: dist/project_name/
            source_path = Path('dist') / self._name
            target_path = self._project_dir / self._name

        # Verify output exists
        if not source_path.exists():
            print(f"\nError: Generated output not found - {source_path}", file=sys.stderr)
            return False

        # Copy output to project directory
        try:
            if self._onefile:
                # Copy single file
                shutil.copy2(source_path, target_path)
            else:
                # Copy entire directory
                if target_path.exists():
                    shutil.rmtree(target_path)
                shutil.copytree(source_path, target_path)

            print(f"\nProject built successfully!")
            print(f"Output directory: {self._project_dir}")
            print(f"Output: {target_path}")

            # Show packaging mode
            mode = "Single executable" if self._onefile else "Directory with dependencies"
            print(f"Packaging mode: {mode}")

            # Show console setting
            console_status = "Console visible" if self._console else "Console hidden"
            print(f"Console setting: {console_status}")

            # Copy external assets
            assets_success = self._copy_assets()

            return assets_success
        except Exception as e:
            print(f"\nOutput copy failed: {str(e)}", file=sys.stderr)
            return False