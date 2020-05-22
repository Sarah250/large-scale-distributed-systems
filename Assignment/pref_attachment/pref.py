'''
Generate edges on a graph using preferential
attachment. The first node is selected randomly and
the second is selected using preferential attachment.
'''

import networkx as nx
import random as rand
import sys
import matplotlib.pyplot as plt

NODES = 100
STEP = 5
list_to_randomize = []

def add_preferential_edge(node_list, graph):
    global list_to_randomize
    rand_val1 = rand.choice(node_list)
    rand_val2 = rand_val1
    while rand_val2 == rand_val1:
        rand_val2 = rand.choice(list_to_randomize)
    if graph.has_edge(rand_val1, rand_val2) is False:
        list_to_randomize.append(rand_val1)
        list_to_randomize.append(rand_val2)
    graph.add_edge(rand_val1, rand_val2)

def generate_connected_graph(node_count):
    global list_to_randomize
    node_list = range(0, node_count)
    list_to_randomize = list(node_list)
    graph = nx.Graph()
    graph.add_nodes_from(node_list)
    for i in range(1, node_count):
        add_preferential_edge(node_list, graph)
    while nx.is_connected(graph) == False:
        add_preferential_edge(node_list, graph)
    return graph

#########################################

if len(sys.argv) > 1:
    try:
        NODES = int(sys.argv[1])
    except:
        print("invalid int, using " + str(NODES))
print("Number of nodes: "+str(NODES))
print("default is 100, configurable by argument")

### Configure plot
fig = plt.figure()
fig.canvas.set_window_title('Preferential attachment')
plt.title('Generation of edges on a graph')
plt.xlabel('# of nodes')
plt.ylabel('degree')

stats = {}
graph = generate_connected_graph(NODES)
for (i, j) in graph.degree():
    try:
        stats[j] += 1
    except:
        stats[j] = 1

coords = []
for i in stats:
    coords.append((i, stats[i]))
coords.sort(key = lambda x : x[0], reverse = False)

keys, values = zip(*coords)
plt.plot(values, keys, 'ro-')
plt.show()
