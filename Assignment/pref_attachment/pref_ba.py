'''
Similar to v1 but this time we start with one node
and add a new node for each new edge
until it reaches the required number.
The edge links the new node to an existing node,
this node is selected using preferential attachment
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
    node_list.remove(rand_val1)
    rand_val2 = rand.choice(list_to_randomize)
    list_to_randomize.append(rand_val1)
    list_to_randomize.append(rand_val2)
    graph.add_edge(rand_val1, rand_val2)

def generate_connected_graph(node_count):
    global list_to_randomize
    node_list = list(range(1, node_count))
    list_to_randomize = [0]
    graph = nx.Graph()
    for i in range(1, node_count):
        add_preferential_edge(node_list, graph)
    while len(node_list) > 0:
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

### Configure figure
fig = plt.figure()
fig.canvas.set_window_title('Preferential attachment')

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
plt.subplot(1, 2, 1)
plt.plot(values, keys, 'ro-')
plt.title('Generation of edges on a graph')
plt.xlabel('# of nodes')
plt.ylabel('degree')

plt.subplot(1, 2, 2)
nx.draw(graph)
plt.show()
