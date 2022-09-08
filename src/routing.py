import abc
import sys
import networkx as nx
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
        self.graph, self.nodes, self.dg = Topology().read()

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
    def __init__(self) -> None:
        self.graph, self.nodes, self.dg = Topology().read()
        self.V = len(self.nodes)
        self.nodes = list(self.nodes)
        self.graph = list(self.graph)
        self.graph_table = self.addEdges()
    
    def route(self, sender: str, receiver: str) -> dict:
        self.BellmanFord(sender, receiver)
    
    def addEdges(self):
        listG = []

        for k, v in self.graph:
            listG.append([self.nodes.index(k), self.nodes.index(v), 1])
        
        return listG

    def printArr(self, dist, routes):
        print("VERTICES\tPESO\t\tRUTA")
        for i in range(self.V):
            print("{0}\t\t{1}\t\t{2}".format(self.nodes[i], dist[i], routes[i]))

        return routes

    def BellmanFord(self, src, rcv):
        dist = [float("Inf")] * self.V
        dist[self.nodes.index(src)] = 0

        for _ in range(self.V - 1):
            for u, v, w in self.graph_table:
                if dist[u] != float("Inf") and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
 
        for u, v, w in self.graph_table:
            if dist[u] != float("Inf") and dist[u] + w < dist[v]:
                print("Graph contains negative weight cycle")
                return

        #RUTAS
        routes = []
        for receiver in self.nodes:
            nx.path_graph(self.dg)
            routes.append(nx.bellman_ford_path(self.dg, src, receiver))
        
        routes = self.printArr(dist, routes)
        rutas = {}
        
        for i in routes:
            if src == i[0] and rcv == i[-1]:
                short_route = i

        i = 0
        next_nodes = []
        while i < len(short_route):

            next = []
            try:
                next.append(short_route[i+1])
                next_nodes.append(next)
            except IndexError:
                next_nodes.append(next)

            i += 1
        
        final_dictionary = dict(zip(short_route, next_nodes))

        return final_dictionary


class Dijkstra(Rounting):
    def __init__(self) -> None:
        self.passed = []
        self.way = {}
        self.edges, self.nodes, self.dg = Topology().read()
        self.init_graph = self.graph_base()
        self.graph = self.construct_graph()
        self.rutes = self.all_routes()
    
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
        print("\n")
        print('\033[2;32;40m')
        for routes in self.rutes[sender]:
            print(routes, " with number of steps ->", len(routes)-1)
        print('\033[0;37;40m')

        route = []
        next_nodes = []

        for routes in self.rutes[sender]:
            if routes[-1] == receiver:
                route = routes
        
        i = 0

        while i < len(route):
            next = []
            try:
                next.append(route[i+1])
                next_nodes.append(next)
            except IndexError:
                next_nodes.append(next)
            i += 1
        
        final_dictionary = dict(zip(route, next_nodes))

        return final_dictionary
    
    def all_routes(self):
        defined_rutes = {}
        rutes = []
        for node_sender in self.nodes:
            for node_receiver in self.nodes:
                path = []
                node = node_receiver
                previous_nodes = self.Shortest_path(node_sender)
                
                while node != node_sender:
                    path.append(node)
                    node = previous_nodes[node]
            
                path.append(node_sender)
                rutes.append([path[len(path) - i] for i in range(1, len(path)+1)])

        for node in self.nodes:
            s = []
            for rute in rutes:
                if rute[0] == node:
                    s.append(rute)
            defined_rutes[node] = s
        
        return defined_rutes
    
    def Shortest_path(self, sender):
        unvisited_nodes = list(self.nodes)
 
        shortest_path = {}
    
        previous_nodes = {}
      
        max_value = sys.maxsize
        for node in unvisited_nodes:
            shortest_path[node] = max_value
        
        shortest_path[sender] = 0
        
        while unvisited_nodes:
            current_min_node = None
            for node in unvisited_nodes: 
                if current_min_node == None:
                    current_min_node = node
                elif shortest_path[node] < shortest_path[current_min_node]:
                    current_min_node = node
                    
            neighbors = self.get_outgoing_edges(current_min_node)
            for neighbor in neighbors:
                tentative_value = shortest_path[current_min_node] + self.value(current_min_node, neighbor)
                if tentative_value < shortest_path[neighbor]:
                    shortest_path[neighbor] = tentative_value
                    previous_nodes[neighbor] = current_min_node
    
            unvisited_nodes.remove(current_min_node)
        
        return previous_nodes

class Router:

    alg: Rounting = None
    table: dict = {
        "A": "javier@alumchat.fun",
        "B": "19324@alumchat.fun",
        "C": "19111@alumchat.fun",
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

    def get_next(self, me, sender, receiver):
        route = self.get_route(sender, receiver)
        try:
            return route[me]
        except KeyError:
            return []
