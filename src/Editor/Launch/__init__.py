from src.Editor import App
from src.launcher import launch


@launch
def run():
    app = App()
    app.run()