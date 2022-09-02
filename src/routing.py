import abc

from .models import Node
from .topology import Topology


class Rounting(abc.ABC):
    @abc.abstractmethod
    def route(self, sender: str, receiver: str) -> dict:
        pass


class Flooding(Rounting):
    def __init__(self) -> None:
        self.passed = []
        self.way = {}
        self.graph = Topology().read()

    def route(self, sender: str, receiver: str) -> dict:
        self.passed.append(sender)
        self.flood([sender])
        return self.way

    def flood(self, nodes):
        next_nodes = []

        for node in nodes:
            for edge in self.graph:
                if edge[0] in node:
                    if edge[0] not in self.way.keys():
                        self.way[edge[0]] = []
                    if edge[1] not in self.passed:
                        self.way[edge[0]].append(edge[1])
                        next_nodes.append(edge[1])
                        self.passed += next_nodes

        if(len(next_nodes) > 0):
            self.flood(next_nodes)


class DistanceVector(Rounting):
    def route(self, sender: str, receiver: str) -> dict:
        ...


class Dijkstra(Rounting):
    def __init__(self) -> None:
        self.passed = []
        self.way = {}
        self.edges, self.nodes = Topology().read()
        self.init_graph = self.graph_base()
    
    def graph_base(self):
        init_graph = {}
        for node in self.nodes:
            init_graph[node] = {}
        
        for edge in self.edges:
            init_graph[edge[0]][edge[1]] = 1
        
        return init_graph

    def route(self, sender: str, receiver: str) -> dict:
        ...
    
    def Shortest_path(self):
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
