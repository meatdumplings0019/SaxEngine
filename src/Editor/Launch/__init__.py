from src.Editor import App
from src.Launcher import launch


@launch
def run() -> None:
    app = App()
    app.run()