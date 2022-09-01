import abc

from .models import Node


class Rounting(abc.ABC):
    @abc.abstractmethod
    def route(self):
        pass


class Flooding(Rounting):
    def route(self):
        ...


class DistanceVector(Rounting):
    def route(self):
        ...


class Dijkstra(Rounting):
    def route(self):
        ...


class Router:

    alg: Rounting = None

    def __init__(self, alg: str) -> None:
        if alg == 'flooding':
            self.alg = Flooding()
        elif alg == 'distance':
            self.alg = DistanceVector()
        else:
            self.alg = Dijkstra()

    def get_next(self, dest: Node) -> Node:
        ...
