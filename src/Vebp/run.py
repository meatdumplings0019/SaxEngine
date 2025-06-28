#!/usr/bin/env python3
"""
vebp - Enhanced PyInstaller Packaging Tool Entry Point
"""
import argparse
import sys
from .builder import Builder
from . import __version__


def show_version():
    """Display version information"""
    print(f"vebp (Enhanced PyInstaller Packaging Tool) version: {__version__}")
    print("Use 'vebp build --help' to view build help")


def build_command(args):
    """Handle build subcommand"""
    try:
        # Initialize builder
        builder = Builder(
            name=args.name,
            icon=args.icon
        )
        # Set source script (required)
        builder.set_script(args.src)

        # Set console option
        builder.set_console(args.console)

        # Set packaging mode
        builder.set_onefile(not args.onedir)  # Note: --onedir sets onefile to False

        # Add external assets if provided
        if args.asset:
            # Group assets by target path
            assets_by_target = {}

            # Parse asset specifications
            for asset_spec in args.asset:
                # Split source and target
                parts = asset_spec.split(';', 1)
                if len(parts) == 1:
                    source = parts[0].strip()
                    target = ""
                else:
                    source = parts[0].strip()
                    target = parts[1].strip()

                # Add to grouping dictionary
                if target not in assets_by_target:
                    assets_by_target[target] = []
                assets_by_target[target].append(source)

            # Add assets to builder
            for target, sources in assets_by_target.items():
                builder.add_assets(sources, target)

        # Add internal assets if provided
        if args.inasset:
            # Group inassets by target path
            inassets_by_target = {}

            # Parse inasset specifications
            for inasset_spec in args.inasset:
                # Split source and target
                parts = inasset_spec.split(';', 1)
                if len(parts) == 1:
                    source = parts[0].strip()
                    target = ""
                else:
                    source = parts[0].strip()
                    target = parts[1].strip()

                # Add to grouping dictionary
                if target not in inassets_by_target:
                    inassets_by_target[target] = []
                inassets_by_target[target].append(source)

            # Add inassets to builder
            for target, sources in inassets_by_target.items():
                builder.add_inassets(sources, target)

        # Execute build
        success = builder.build()
    except Exception as e:
        print(f"\nInitialization error: {str(e)}", file=sys.stderr)
        sys.exit(2)

    if success:
        sys.exit(0)
    else:
        print("\nOperation failed! Please check error messages", file=sys.stderr)
        sys.exit(1)


def main():
    # Create top-level parser
    parser = argparse.ArgumentParser(
        description='vebp - Enhanced PyInstaller Packaging Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''Examples:
  vebp build MyProject --src app.py
  vebp build MyApp -s app.py -i app.ico -c
  vebp build ProjectX -s main.py -d
  vebp build Game -s app.py --asset "images;resources" --asset "sfx;resources"
  vebp build App -s app.py --inasset "config.json;settings"
  vebp build App -s app.py --inasset "templates;ui" --asset "README.md"
''')

    parser.add_argument('--version', '-v', action='store_true',
                        help='Show version information')

    # Add subcommands
    subparsers = parser.add_subparsers(
        title='Available commands',
        dest='command',
        help='Select an action to perform'
    )

    # Build command
    build_parser = subparsers.add_parser(
        'build',
        help='Build executable',
        description='Package Python script into executable',
        epilog='''Build examples:
  vebp build MyProject --src app.py
  vebp build MyApp -s app.py -i app.ico -c
  vebp build ProjectX -s main.py -d
  vebp build Game -s app.py --asset "images;resources" --asset "sfx;resources"
  vebp build App -s app.py --inasset "config.json;settings"
  vebp build App -s app.py --inasset "templates;ui" --asset "README.md"
''')

    # Required arguments for build command
    build_parser.add_argument('name',
                              help='Project name (required)')
    build_parser.add_argument('--src', '-s', required=True,
                              help='Path to Python script to package (required)')

    # Optional arguments for build command with aliases
    build_parser.add_argument('--icon', '-i',
                              help='Application icon (.ico file)')
    build_parser.add_argument('--console', '-c', action='store_true',
                              help='Show console window (hidden by default)')
    build_parser.add_argument('--onedir', '-d', action='store_true',
                              help='Use directory mode instead of single executable (default: onefile)')

    # Asset arguments
    build_parser.add_argument('--asset', action='append',
                              help='External asset: "source_path;target_relative_path" (copied to output directory)')
    build_parser.add_argument('--inasset', action='append',
                              help='Internal asset: "source_path;target_relative_path" (embedded in executable)')

    # If no arguments provided, show help
    if len(sys.argv) == 1:
        show_version()
        sys.exit(0)

    args = parser.parse_args()

    # Handle --version option
    if args.version:
        show_version()
        sys.exit(0)

    # Handle subcommands
    if args.command == 'build':
        build_command(args)
    else:
        # If command not recognized, show help
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()