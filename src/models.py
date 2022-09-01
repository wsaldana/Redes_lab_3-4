from dataclasses import dataclass


@dataclass
class Node():
    name: str
    direction: str


class Message():
    def __init__(self, message: str, sender: str, receiver: str) -> None:
        self.message = message
        self.sender = sender
        self.receiver = receiver

    def serialize(self):
        dictionary = self.deserialize()
        return str(dictionary)

    def deserialize(self):
        return {
            "message": self.message,
            "sender": self.sender,
            "receiver": self.receiver
        }
