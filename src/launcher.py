import sys
from src.error import ErrorWindow


def launch(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            w = ErrorWindow(e)
            sys.exit(1)

    return wrapper