class Application:
    def __init__(self):
        ...

    def handle_events(self):
        ...

    def update(self):
        ...

    def run(self):
        while True:
            self.handle_events()
            self.update()