from src.Vebp.Builder.builder import Builder
from src.Vebp.CMD.tool import error


def cmd_build(args):
    if len(args) != 0:
        return error(f"Only 0 args, but has {len(args)} arguments.")
    Builder().from_package().build()