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
        self.graph = self.construct_graph()
    
    def graph_base(self):
        init_graph = {}
        for node in self.nodes:
            init_graph[node] = {}
        
        for edge in self.edges:
            init_graph[edge[0]][edge[1]] = 1
        
        return init_graph
    
    def construct_graph(self):
        graph = {}
        for node in self.nodes:
            graph[node] = {}
        
        graph.update(self.init_graph)
        
        for node, edges in graph.items():
            for adjacent_node, value in edges.items():
                if graph[adjacent_node].get(node, False) == False:
                    graph[adjacent_node][node] = value
                    
        return graph
    
    def get_outgoing_edges(self, node):
        connections = []
        for out_node in self.nodes:
            if self.graph[node].get(out_node, False) != False:
                connections.append(out_node)
        return connections
    
    def value(self, node1, node2):
        return self.graph[node1][node2]

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
