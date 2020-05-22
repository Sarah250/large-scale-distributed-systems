import networkx as nx
import random as rand
import sys
import matplotlib.pyplot as plt

MAX_NODES = 100
NUM_TESTS = 40
STEP = 5
stats = {}

def add_random_edge(node_list, graph):
    temp = list(node_list)
    rand_val1 = rand.choice(node_list)
    temp.remove(rand_val1)
    rand_val2 = rand.choice(temp)
    graph.add_edge(rand_val1, rand_val2)

def generate_connected_graph(node_count):
    node_list = range(0, node_count)
    graph = nx.Graph()
    graph.add_nodes_from(node_list)
    for i in range(1, node_count):
        add_random_edge(node_list, graph)
    while nx.is_connected(graph) == False:
        add_random_edge(node_list, graph)
    return graph

#########################################

if len(sys.argv) > 1:
    try:
        MAX_NODES = int(sys.argv[1])
    except:
        print("invalid int, using " + str(MAX_NODES))

nodes = STEP
while nodes <= MAX_NODES:
    temp_stats = 0
    for i in range(0, NUM_TESTS):
        graph = generate_connected_graph(nodes)
        temp_stats += graph.number_of_edges()
    stats[nodes] = temp_stats/NUM_TESTS
    nodes += STEP

### Create plot with collected data
fig = plt.figure()
fig.canvas.set_window_title('Connected Graphs')
plt.plot(stats.keys(), stats.values(), 'ro-')
plt.title('Random generation of edges on a graph')
plt.xlabel('number of nodes')
plt.ylabel('random edges generated (average of '
            +str(NUM_TESTS)
            +' tests)')

plt.show()
