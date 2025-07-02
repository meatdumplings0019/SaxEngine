from src.Editor import App
from src.Launcher import launch


@launch
def run():
    app = App()
    app.run()