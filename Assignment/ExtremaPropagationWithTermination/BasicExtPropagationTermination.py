from numpy import random
import numpy as np
from ExtremaPropagationWithTermination.connected import randomGraph
import networkx as nx
import matplotlib.pyplot as plt


def calculatingN(vectorX):
    return ((len(vectorX) - 1) / sum(vectorX))


class BasicExtremePropagation:
    def __init__(self, K, T, numberOfNodes):
        # Generate Network of Random Nodes
        self.graph = randomGraph(numberOfNodes)
        self.nodes = list(self.graph.nodes)
        self.T = T
        self.K = K
        self.listN = list()
        self.converged = list()

    def initialize(self):
        for i in self.nodes:
            # init Nodes
            self.nodes[i] = Node(self.K, self.T, list(self.graph.neighbors(i)), i)
            self.listN.append(self.nodes[i].N)
            self.converged.append(self.nodes[i].converged)

    def run(self):
        round = 0
        while (True):
            for i in range(0, len(self.nodes)):
                # send x to every neighbor
                for j in self.nodes[i].neighbors:
                    # send to node j vectorX and receiving new vectorX from j
                    self.nodes[j].receiveMsg(self.nodes[i].vectorX)
                # ---- So para receber
                    # add N  of node j to list
                    self.listN[j] = self.nodes[j].N
                    # add converged of node j to list
                    self.converged[j] = self.nodes[j].converged
                    # calculating and updating vectorX in node i
                    self.nodes[i].pontwiseMinimum(self.nodes[j].vectorX)
                    # add N  of node i to list
                    self.listN[j] = self.nodes[i].N
            i = 0
            round += 1
            print(f'Round {round} = {self.listN}')
            print(f'Round {round} = {self.converged}')


class Node:

    def __init__(self, K, T, neighbors, myNumber):
        self.T = T
        self.vectorX = random.exponential(scale=1, size=K)
        self.neighbors = neighbors
        self.N = 0
        self.oldX = self.vectorX
        self.nonews = 0
        self.converged = False
        self.myNumber = myNumber

    def receiveMsg(self, msgX):
        # oldX <- vectorX
        self.oldX = self.vectorX
        # calculate and update vectorX with the pontwiseMinimum
        self.vectorX = np.minimum(self.vectorX, msgX)
        # calculating N(x)
        self.N = calculatingN(self.vectorX)

        if (self.oldX != self.vectorX).all():
            self.nonews = 0
        else:
            self.nonews += 1
        if self.nonews >= self.T:
            self.converged = True

    def pontwiseMinimum(self, msgX):
        self.vectorX = np.minimum(self.vectorX, msgX)
        self.N = calculatingN(self.vectorX)
        #print(f' Estimation of Network Size (N) = {self.N}')


if __name__ == '__main__':
    # K, T, number of Nodes
    bPropagation = BasicExtremePropagation(100,4, 100)
    bPropagation.initialize()
    bPropagation.run()

    #print(f"{node.neighbors}")
    '''plt.subplot(121)
    nx.draw(bPropagation.graph, with_labels=True)
    plt.show()'''
