import networkx as nx
import random

def randomGraph(nodes):
    number_edges = 0

    G = nx.Graph()
    G.add_nodes_from([*range(0, nodes)])

    while nx.number_connected_components(G) != 1:
        v1 = random.randint(0, nodes - 1)
        v2 = random.randint(0, nodes - 1)

        if not nx.Graph.has_edge(G, v1, v2) and v1 != v2:
            G.add_edge(v1, v2)
            number_edges += 1
    return G