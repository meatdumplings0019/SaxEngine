import sys

from src.Vebp.CMD.utils import error


def cmd_exit(args) -> None:
    if len(args) != 0:
        error(f"Only 0 args, but has {len(args)} arguments.")
        return

    sys.exit(0)