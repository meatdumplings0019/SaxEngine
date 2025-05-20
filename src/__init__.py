from src.Application import Application
from src.Core.Windows import WindowTestTwo
from src.Core.Windows.WindowTestOne import WindowTestOne
from src.Core.Windows.WindowTestTwo import WindowTestTwo
from src.Resources.Font import FontResource

class App(Application):
    def __init__(self):
        super().__init__("test1")

    def window_init(self):
        super().window_init()
        self.window_manager.add("test1", WindowTestOne())
        self.window_manager.add("test2", WindowTestTwo())