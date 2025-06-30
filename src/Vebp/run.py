from colorama import init
from src.Vebp.Cli import CLI

init()

if __name__ == "__main__":
    cli = CLI()
    cli.run()