from typing import Any
from src.Libs.Utils import Message


class Resource:
    def __init__(self, path, func = None) -> None:
        self.__path = path
        self.__res = None
        self.func = func

        self.__isLoad, self.__errmsg = self.load()

    def load(self) -> Message[bool]:
        try:
            self.__res = self.get_value() if self.func else self.__path
            return Message(True)
        except Exception as e:
            return Message(False, e)

    def get_value(self) -> Any:
        return self.func(self.__path)

    @property
    def res(self) -> Any:
        return self.__res

    @property
    def isLoad(self) -> bool:
        return self.__isLoad

    @property
    def errmsg(self) -> str:
        return self.__errmsg

    @property
    def path(self) -> str:
        return self.__path