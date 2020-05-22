import sys
import networkx as nx
import random as rand
import matplotlib.pyplot as plt
import math

'''
    - Cool improvements:
        make step by step iteration triggered by the user
'''

class NetworkSimulation:
    '''
    reached_nodes is a dictionary that will have the following content:
        - key = step of the simulation (0,1,2,3...)
        - value = number of nodes the gossip has reached
    '''
    def __init__(self, num_nodes, broadcast_percent):
        self.graph = nx.barabasi_albert_graph(num_nodes, 1)
        self.nodes = {}
        self.num_nodes = num_nodes
        self.reached_nodes = {}
        self.broadcasting = []
        self.received_msg = []
        self.current_step = 0
        self.percentage = broadcast_percent

    def __node_broadcast(self, node):
        next_msg = node.next_to_broadcast()
        how_many = 0
        if next_msg is not None:
            neighbors = list(self.graph.neighbors(node.get_num()))
            num = math.ceil(len(neighbors) * self.percentage)
            for i in rand.sample(neighbors, num):
                neighbor = self.nodes[i]
                res = neighbor.append(next_msg)
                self.received_msg.append(neighbor)
                step = self.current_step
                try:
                    self.reached_nodes[step] += res
                except:
                    self.reached_nodes[step] = res
            return True
        return False

    def run(self):
        for i in range(self.num_nodes):
            self.nodes[i] = Node(i)
        init = rand.choice(range(self.num_nodes))
        self.nodes[init].append(init)
        self.reached_nodes[0] = 1
        self.broadcasting.append(self.nodes[init])
        running = 1
        while running > 0:
            running = 0
            for node in self.broadcasting:
                if self.__node_broadcast(node):
                    running += 1
            self.current_step += 1
            step = self.current_step
            before = self.reached_nodes[step - 1]
            self.reached_nodes[step] = before
            self.broadcasting = self.received_msg
            self.received_msg = []
        return self.reached_nodes

    def get_graph(self):
        return self.graph

class Node:
    def __init__(self, num):
        self.in_queue = list()
        self.known_msgs = list()
        self.num = num

    def append(self, msg):
        if msg not in self.known_msgs:
            self.in_queue.append(msg)
            self.known_msgs.append(msg)
            return 1
        return 0

    def get_num(self):
        return self.num

    def next_to_broadcast(self):
        if len(self.in_queue) > 0:
            msg = self.in_queue[0]
            del self.in_queue[0]
            return msg
        return None

###########################################

nodes = 100
percentage = 1.0

if len(sys.argv) > 1:
    try:
        nodes = int(sys.argv[1])
    except:
        print("invalid int, using " + str(nodes))
print("Number of nodes: " + str(nodes))
print("default is 100, configurable by argument")

simulation = NetworkSimulation(nodes, percentage)
stats = simulation.run()

# plot stats

fig = plt.figure()
fig.canvas.set_window_title('(Probabilistic) Broadcast')
plt.plot(list(stats.keys()), list(stats.values()), 'ro-')
plt.title('Broadcast')
plt.xlabel('step')
plt.ylabel('reached nodes')
plt.show()
