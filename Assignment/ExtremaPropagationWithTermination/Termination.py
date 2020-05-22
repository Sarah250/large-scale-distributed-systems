'''
Extrema Propagation Algorithm with Termination
'''

# from numpy import random
import numpy as np

from connected import randomGraph
import matplotlib.pyplot as plt
import networkx as nx
from node import Node

# self.graph.neighbors(i)
# i -> nº do nodo
class Termination:
    '''
    K: Number of Random Nodes
    T: Precision (?)
    '''
    def __init__(self, K, T):
        # Generate Network of Random Nodes
        self.graph = randomGraph(K)
        self.nodes = list(self.graph.nodes)

        self.K = K
        self.T = T
        self.nonews = 0
        self.converged = False

        self.messages = []
        # self.n -> neighbors ??
        # self.x = np.random.exponential(scale=1, size=self.K)

    def run(self):
        for i in range(self.K):
            # Generate node with Random Exponential Distribution of Rate 1
            self.nodes[i] = Node(i, self.K, self.T, self.graph.neighbors(i))

    '''
    messages: messages received
    '''
    def receive(self, messages):
        oldx = self.x

        # For each message received
        # determine the minimum between self.x and message vector
        for i in messages:
            self.x = np.minimum(self.x, messages[i])
            # self.x[i] = min(min(self.x), min(messages[i]))

        # If there Oldx isn't different than X then nonews = 0
        if oldx != self.x:
            print("OldX = X, there are no news")
            self.nonews = 0
        # Else there is new news
        else:
            self.nonews = self.nonews + 1
            print(f"News: {self.nonews}")

        if self.nonews >= self.T:
            self.converged = True

        # Send X to node
        # Send X to every P of N

    # Send X random exponential vector
    def sendMsgs(self):
        for i in range(self.K):
            neighbors = self.nodes[i].neighbors

            for nei in neighbors:
                print(f"Node {i} envia para {nei}")
                # Node i envia vector para nei (aka vizinho)
                result = self.nodes[nei].receiveMsg(self.nodes[i].vector)
                print(f"N = {result}")
            print('------------------------------------------')


# termination()
x = Termination(10, 2)
x.run()
x.sendMsgs()

# Draw Graph
plt.subplot(121)
nx.draw(x.graph, with_labels=True)
plt.show()
