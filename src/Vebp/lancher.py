﻿import sys

from src.Libs.error import get_traceback
from src.Vebp.Cli import CLI


def launch(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"{e}: {get_traceback(e)}", file=sys.stderr)
            sys.exit(1)

    return wrapper

@launch
def run():
    cli = CLI()
    cli.run()