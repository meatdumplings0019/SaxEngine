from typing import TypeVar, Generic

#typevar
_MessageT = TypeVar('_MessageT')

#class
class Message(Generic[_MessageT]):
    def __init__(self, var: _MessageT, msg: Exception | str = None):
        self._var = var
        self._msg = msg

    @property
    def var(self) -> _MessageT:
        return self._var

    @property
    def msg(self) -> Exception | str | None:
        return self._msg

    @staticmethod
    def is_message(msg) -> bool:
        if not msg.msg:
            return True

        return False


    def __iter__(self):
        yield self._var
        yield self._msg

    def __getitem__(self, item):
        return getattr(self, item)

    def __repr__(self):
        return f'<Message var:{self.var} msg:{self.msg}>'