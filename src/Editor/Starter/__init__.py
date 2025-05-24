import sys
import traceback

from src.Editor import App
from src.ErrorWindow import ErrorWindow

def error_handler(func):
    """异常处理装饰器"""

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            w = ErrorWindow(e)
            sys.exit(1)

    return wrapper

@error_handler
def run() -> None:
    app = App()
    app.run()