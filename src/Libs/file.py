import os
import shutil


class FileStream:
    def __init__(self, file_path):
        self.path = os.path.normpath(file_path)

    def isExists(self):
        return os.path.exists(self.path)

    @staticmethod
    def abs(source):
        if isinstance(source, FileStream):
            return os.path.abspath(source.path)
        elif isinstance(source, str):
            return os.path.abspath(source)
        else:
            raise TypeError("Input must be a string, FileStream or FolderStream instance")

    @staticmethod
    def copy(source, destination):
        src_path = FileStream.abs(source)

        if not os.path.isfile(src_path):
            raise FileNotFoundError(f"Source file not found: {src_path}")

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

    def __repr__(self):
        return f"<FileStream: {self.path}>"


class DirectoryInfo:
    def __init__(self, path, folders, files):
        self._path = os.path.normpath(path)
        self._folders = folders
        self._files = files

    def __iter__(self):
        yield self._path
        yield self._folders
        yield self._files

    def __repr__(self):
        return f"<DirectoryInfo: {self._path}>"

    @property
    def path(self):
        return self._path

    @property
    def folders(self):
        return self._folders

    @property
    def files(self):
        return self._files

class FolderStream:
    def __init__(self, folder_path):
        self.path = os.path.normpath(folder_path)

    def isExists(self):
        return os.path.exists(self.path) and os.path.isdir(self.path)

    def walk(self):
        if not self.isExists(): return None

        folders = []
        files = []

        try:
            with os.scandir(self.path) as entries:
                for entry in entries:
                    if entry.is_dir():
                        sub_folder = FolderStream(entry.path)
                        folders.append(sub_folder)
                    elif entry.is_file():
                        files.append(FileStream(entry.path))
        except PermissionError:
            pass

        return DirectoryInfo(self.path, folders, files)

    @staticmethod
    def abs(source):
        if isinstance(source, FolderStream):
            return os.path.abspath(source.path)
        elif isinstance(source, str):
            return os.path.abspath(source)
        else:
            raise TypeError("Input must be a string, FolderStream or FileStream instance")

    def __repr__(self):
        return f"<FolderStream: {self.path}>"

    def __eq__(self, other):
        if isinstance(other, FolderStream):
            return os.path.normpath(self.path) == os.path.normpath(other.path)
        return False

    def __hash__(self):
        return hash(os.path.normpath(self.path))