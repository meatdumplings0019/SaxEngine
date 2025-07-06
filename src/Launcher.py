import sys
from src.ErrorWindow import ErrorWindow
from src.Libs.Error import get_traceback


def launch(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"{e}: {get_traceback(e)}")
            w = ErrorWindow(e)
            sys.exit(1)

    return wrapper