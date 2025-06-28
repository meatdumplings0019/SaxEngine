import os
import shutil
from typing import Iterator, Any


class FileStream:
    def __init__(self, file_path) -> None:
        self._path = os.path.normpath(file_path)

    @property
    def path(self) -> str:
        return self._path

    def create(self, value: str = "") -> bool:
        if not os.path.exists(self._path):
            self.write(value)
            return True

        return False

    def write(self, value: str) -> bool:
        try:
            with open(self._path, 'w') as file:
                file.write(value)
            return True
        except Exception:
            return False

    def read(self) -> Any:
        if not self.isExists(): return None

        try:
            with open(self._path, 'r') as file:
                return file.read()
        except Exception:
            return None

    def isExists(self) -> bool:
        return os.path.exists(self._path)

    @staticmethod
    def abs(source) -> str | None:
        if isinstance(source, FileStream):
            return os.path.abspath(source.path)
        elif isinstance(source, str):
            return os.path.abspath(source)
        else:
            return None

    @staticmethod
    def copy(source, destination):
        src_path = FileStream.abs(source)

        if not os.path.isfile(src_path):
            return None

        dest_abs = FileStream.abs(destination)

        if isinstance(destination, FolderStream) or os.path.isdir(dest_abs):
            dest_path = os.path.join(dest_abs, os.path.basename(src_path))
        else:
            dest_path = dest_abs

        dest_dir = os.path.dirname(dest_path)
        if dest_dir and not os.path.exists(dest_dir):
            os.makedirs(dest_dir, exist_ok=True)

        shutil.copy2(src_path, dest_path)

        return FileStream(dest_path)

    def __repr__(self) -> str:
        return f"<FileStream: {self._path}>"


class DirectoryInfo:
    def __init__(self, path, folders, files) -> None:
        self._path = os.path.normpath(path)
        self._folders = folders
        self._files = files

    def __iter__(self) -> Iterator:
        yield self._path
        yield self._folders
        yield self._files

    def __repr__(self) -> str:
        return f"<DirectoryInfo: {self._path}>"

    @property
    def path(self) -> str:
        return self._path

    @property
    def folders(self) -> list["FolderStream"]:
        return self._folders

    @property
    def files(self) -> list[FileStream]:
        return self._files

class FolderStream:
    def __init__(self, folder_path) -> None:
        self._path = os.path.normpath(folder_path)

    @property
    def path(self) -> str:
        return self._path

    def create(self) -> bool:
        try:
            os.makedirs(self._path, exist_ok=True)
            return True
        except Exception as e:
            return False

    def isExists(self) -> bool:
        return os.path.exists(self._path) and os.path.isdir(self._path)

    def walk(self) -> DirectoryInfo | None:
        if not self.isExists(): return None

        folders = []
        files = []

        try:
            with os.scandir(self._path) as entries:
                for entry in entries:
                    if entry.is_dir():
                        sub_folder = FolderStream(entry.path)
                        folders.append(sub_folder)
                    elif entry.is_file():
                        files.append(FileStream(entry.path))
        except PermissionError:
            pass

        return DirectoryInfo(self._path, folders, files)

    @staticmethod
    def abs(source) -> str | None:
        if isinstance(source, FolderStream):
            return os.path.abspath(source.path)
        elif isinstance(source, str):
            return os.path.abspath(source)
        else:
            return None

    def __repr__(self) -> str:
        return f"<FolderStream: {self._path}>"

    def __eq__(self, other) -> bool:
        if isinstance(other, FolderStream):
            return os.path.normpath(self._path) == os.path.normpath(other._path)
        return False

    def __hash__(self) -> int:
        return hash(os.path.normpath(self._path))