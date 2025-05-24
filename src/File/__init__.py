from typing import Any
from src.Libs.message import Message


class FileManager:
    def __init__(self, path: str):
        self.path = path

    def open(self) -> Message[Any]:
        try:
            with open(self.path, "r", encoding="utf-8") as file:
                return Message(file.read())
        except Exception as e:
            return Message(None, e)

    def write(self, content) -> Message[bool]:
        try:
            with open(self.path, "w", encoding="utf-8") as file:
                file.write(content)
                return Message(True)
        except Exception as e:
            return Message(False, e)