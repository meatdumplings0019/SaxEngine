from typing import TypeVar, Generic

T = TypeVar('T')

class Message(Generic[T]):
    def __init__(self, var: T, msg: Exception | str = None):
        self.var = var
        self.msg = msg

    def __iter__(self):
        yield self.var
        yield self.msg