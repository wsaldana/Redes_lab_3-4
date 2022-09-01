import abc

from .models import Node
from .topology import Topology


class Rounting(abc.ABC):
    @abc.abstractmethod
    def route(self, sender: str, receiver: str) -> dict:
        pass


class Flooding(Rounting):
    def route(self, sender: str, receiver: str) -> dict:
        way = {}
        graph = Topology().read()
        for edge in graph:
            way[edge[0]] = []
            way[edge[0]].append(edge[1])
        return way


class DistanceVector(Rounting):
    def route(self, sender: str, receiver: str) -> dict:
        ...


class Dijkstra(Rounting):
    def route(self, sender: str, receiver: str) -> dict:
        ...


class Router:

    alg: Rounting = None
    table: dict = {
        "A": "walt.gfe@alumchat.fun",
        "B": "walt.gfe@alumchat.fun",
        "C": "walt.gfe@alumchat.fun",
        "D": "walt.gfe@alumchat.fun",
        "E": "walt.gfe@alumchat.fun",
        "F": "walt.gfe@alumchat.fun",
    }

    def __init__(self, alg: str) -> None:
        if alg == 'flooding':
            self.alg = Flooding()
        elif alg == 'distance':
            self.alg = DistanceVector()
        else:
            self.alg = Dijkstra()

    def get_route(self, sender, receiver) -> Node:
        return self.alg.route(sender, receiver)
