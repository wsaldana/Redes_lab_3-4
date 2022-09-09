import json
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path


class Topology:
    def read(self):
        # Opening JSON file
        path = Path(__file__).parent / "../topologia.txt"
        with open(path) as json_file:
            data = json.load(json_file)
            a = list(data['config'].items())

        DG = nx.DiGraph()
        for f in a:
            for i in range(0, len(f)):
                if i%2 == 0:
                    DG.add_node(f[i])

        '''for f in a:
            for i in range(0, len(f)):
                if i%2 == 1:
                    DG.add_edge(f[i - 1], f[1][i])
                else:
                    DG.add_edge(f[i], f[1][i])'''
        for parent in data['config'].keys():
            for child in data['config'][parent]:
                DG.add_edge(parent, child)
                DG.add_edge(child, parent)

        print(DG.nodes())
        print(DG.edges())

        nx.draw(DG, node_shape = "s", arrows = False)
        plt.show()

        return DG.edges(), DG.nodes(), DG
