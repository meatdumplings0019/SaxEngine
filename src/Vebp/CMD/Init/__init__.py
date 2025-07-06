from src.Vebp.CMD.utils import error
from src.Vebp.Data.BuildConfig import BuildConfig
from src.Vebp.Data.Config import Config
from src.Vebp.Data.Package import Package


def cmd_init(args) -> bool:
    if len(args) > 1:
        error(f"Only 1 args, but has {len(args)} arguments.")
        return False
    try:
        path = args[0]
    except IndexError:
        path = ".."

    package_success = Package.create(path)
    build_success = BuildConfig.create(path)
    config_success = Config.create(path)

    return package_success and build_success and config_success