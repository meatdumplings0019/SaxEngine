from src.Libs.fs import get_fs
from src.Libs.path import MPath_



def format_string(string):
    if not isinstance(string, str):
        return string

    return get_fs(string, {
        "cwd": MPath_.cwd.name,
    })