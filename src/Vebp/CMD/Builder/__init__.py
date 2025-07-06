from src.Vebp.Builder.Builder import Builder
from src.Vebp.CMD.utils import error


def cmd_build(args) -> None:
    if len(args) != 0:
        error(f"Only 0 args, but has {len(args)} arguments.")
        return

    Builder().from_package().build()