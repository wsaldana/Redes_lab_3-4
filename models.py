import abc
from dataclasses import dataclass, asdict


class Serializable(abc.ABC):
    @abc.abstractmethod
    def serialize(self):
        dictionary = self.deserialize()
        return str(dictionary)

    @abc.abstractmethod
    def deserialize(self):
        return {k: str(v) for k, v in asdict(self).items()}


@dataclass
class Node(Serializable):
    name: str
    direction: str


@dataclass
class Message(Serializable):
    message: str
    sender: Node
    receiver: Node