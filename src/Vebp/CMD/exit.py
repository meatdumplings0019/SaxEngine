import sys

from src.Vebp.CMD.tool import error


def cmd_exit(args):
    if len(args) != 0:
        error(f"Only 0 args, but has {len(args)} arguments.")
        return

    sys.exit(0)