from typing import TypeVar, Generic

#typevar
_MessageT = TypeVar('_MessageT')

#class
class Message(Generic[_MessageT]):
    def __init__(self, var: _MessageT, msg: Exception | str = None):
        self.var = var
        self.msg = msg

    def __iter__(self):
        yield self.var
        yield self.msg