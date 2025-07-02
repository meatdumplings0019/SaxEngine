from src.Application import Application
from src.Editor.Windows.Independence.WindowTestOne import WindowTestOne
from src.Editor.Windows.Independence.WindowTestTwo import WindowTestTwo


class App(Application):
    def __init__(self):
        super().__init__("test1")

    def window_init(self):
        super().window_init()
        self.window_manager.add("test1", WindowTestOne())
        self.window_manager.add("test2", WindowTestTwo())