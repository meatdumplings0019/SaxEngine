import sys
from pathlib import Path
from ..Builder.builder import Builder


class CliBuild:
    @staticmethod
    def handle(args):
        try:
            builder = Builder.from_package()

            if not builder:
                builder = Builder()

            name = getattr(args, 'name', None)
            if name:
                builder._name = name

            src = getattr(args, 'src', None)
            if src:
                builder.set_script(src)

            icon = getattr(args, 'icon', None)
            if icon:
                builder._icon = Path(icon)

            console = getattr(args, 'console', False)
            if console:
                builder.set_console(True)

            one_dir = getattr(args, 'onedir', False)
            if one_dir:
                builder.set_onefile(False)
            elif builder.onefile is None:
                builder.set_onefile(True)

            assets = getattr(args, 'asset', [])
            if assets:
                assets_by_target = {}

                for asset_spec in assets:
                    parts = asset_spec.split(';', 1)
                    source = parts[0].strip()
                    target = parts[1].strip() if len(parts) > 1 else ""

                    assets_by_target.setdefault(target, []).append(source)

                for target, sources in assets_by_target.items():
                    builder.add_assets(sources, target)

            in_assets = getattr(args, 'in_asset', [])
            if in_assets:
                in_assets_by_target = {}

                for in_asset_spec in in_assets:
                    parts = in_asset_spec.split(';', 1)
                    source = parts[0].strip()
                    target = parts[1].strip() if len(parts) > 1 else ""

                    in_assets_by_target.setdefault(target, []).append(source)

                for target, sources in in_assets_by_target.items():
                    builder.add_in_assets(sources, target)

            success = builder.build()
        except Exception as e:
            print(f"\n初始化错误: {str(e)}", file=sys.stderr)
            sys.exit(2)

        if success:
            sys.exit(0)
        else:
            print("\n操作失败! 请检查错误信息", file=sys.stderr)
            sys.exit(1)