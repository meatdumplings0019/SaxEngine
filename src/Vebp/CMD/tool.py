from colorama import Fore


def error(value) -> None:
    print(f"{Fore.RED}ERROR: {value}")