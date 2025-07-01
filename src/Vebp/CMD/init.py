from src.Vebp.CMD.tool import error
from src.Vebp.Data.build_config import BuildConfig
from src.Vebp.Data.config import Config
from src.Vebp.Data.package import Package


def cmd_init(args):
    if len(args) > 1:
        error(f"Only 1 args, but has {len(args)} arguments.")
        return False
    try:
        path = args[0]
    except IndexError:
        path = "."

    package_success = Package.create(path)
    build_success = BuildConfig.create(path)
    config_success = Config.create(path)

    return package_success and build_success and config_success