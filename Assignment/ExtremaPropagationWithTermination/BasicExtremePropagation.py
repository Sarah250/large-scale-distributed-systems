from numpy import random
import numpy as np
from ExtremaPropagationWithTermination.connected import randomGraph
import networkx as nx
import matplotlib.pyplot as plt


def calculatingN(vectorX):
    return ((len(vectorX) - 1) / sum(vectorX))


class BasicExtremePropagation:
    def __init__(self, K, numberOfNodes):
        # Generate Network of Random Nodes
        self.graph = randomGraph(numberOfNodes)
        self.nodes = list(self.graph.nodes)
        self.K = K
        self.listN = list()

    def initialize(self):
        for i in self.nodes:
            # init Nodes
            self.nodes[i] = Node(self.K, list(self.graph.neighbors(i)), i)
            self.listN.append(self.nodes[i].N)

    def run(self):
        round = 0
        numberLost = 0
        numberOfMessages = 0
        while True:
            for i in range(0, len(self.nodes)):
                # send x to every neighbor
                for j in self.nodes[i].neighbors:
                    # send to node j vectorX and receiving new vectorX from j
                    msgX = self.nodes[j].receiveMsg(self.nodes[i].vectorX)
                    numberOfMessages += 1
                    # random number for ms
                    tuple = (msgX, random.rand())
                    if tuple[1] >= 0.9:
                        # add N  of node j to list
                        self.listN[j] = self.nodes[j].N
                        # calculating and updating vectorX in node i
                        self.nodes[i].pontwiseMinimum(msgX)
                        # add N  of node i to list
                        self.listN[j] = self.nodes[i].N
                    else :
                        print("Message Lost")
                        numberLost += 1
            i = 0
            round += 1
            print(f'Round {round} = {self.listN}')
            print(f'Number of messages lost = {numberLost}; Number of Messages {numberOfMessages}')


class Node:

    def __init__(self, K, neighbors, myNumber):
        self.vectorX = random.exponential(scale=1, size=K)
        self.neighbors = neighbors
        self.N = 0
        self.queueMsgs = list()
        self.myNumber = myNumber

    def receiveMsg(self, msgX):
        # calculate and update vectorX with the pontwiseMinimum
        self.vectorX = np.minimum(self.vectorX, msgX)
        # calculating N(x)
        self.N = calculatingN(self.vectorX)
        # returning new vector
        return self.vectorX


    def pontwiseMinimum(self, msgX):
        self.vectorX = np.minimum(self.vectorX, msgX)
        self.N = calculatingN(self.vectorX)
        #print(f' Estimation of Network Size (N) = {self.N}')


if __name__ == '__main__':
    # K
    bPropagation = BasicExtremePropagation(10000, 100)
    bPropagation.initialize()
    bPropagation.run()
    #graph = randomGraph(10)
    #node = Node(12, list(graph.neighbors(2)),2)
    #print(f"{node.neighbors}")
    '''plt.subplot(121)
    nx.draw(bPropagation.graph, with_labels=True)
    plt.show()'''
