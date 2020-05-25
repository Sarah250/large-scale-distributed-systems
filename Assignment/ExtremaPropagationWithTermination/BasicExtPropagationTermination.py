from numpy import random
import numpy as np
from ExtremaPropagationWithTermination.connected import randomGraph
import networkx as nx
import matplotlib.pyplot as plt
import operator

class Sim:

    def __init__(self, nodes, distances):
        self.nodes = nodes
        self.distances = distances
        self.currentTime = 0
        self.pending = []
        self.graph = randomGraph(nodes)

    def start(self, initial_msg):
        # schedule first event
        for i in self.nodes:
            event = (self.nodes[i], (None, i, initial_msg))
            self.pending.append(event)

        # run the simulation loop
        self.run_loop()

    def run_loop(self):
        while len(self.pending) > 0 and len(self.distances) > 0:
            # Self pending is the events (0, 1...)
            # Minimum distances Nodes (src, dst)
            minimumTiming = min(self.distances, key=self.distances.get)
            # Distance is timer
            timer = self.distances.get(minimumTiming)

            ton = self.pending[minimumTiming[0]]
            tuple = ton[1]
            msg = tuple[2]

            # handle message
            ton[0].handle(minimumTiming[0], msg, timer)

            self.distances.pop(minimumTiming)
            self.pending.pop(minimumTiming[0])




def calculatingN(vectorX):
    return ((len(vectorX) - 1) / sum(vectorX))


class BasicExtremePropagation:

    def __init__(self, K, T, numberOfNodes, percentage):
        # Generate Network of Random Nodes
        self.graph = randomGraph(numberOfNodes)
        self.nodes = list(self.graph.nodes)
        self.T = T
        self.K = K
        self.listN = list()
        self.converged = list()
        self.numberOfNodes = numberOfNodes
        self.percentage = percentage
        self.dist = {}
        self.queue = []
        # incrementa com o envio
        self.time = 0


    def initialize(self):
        for i in self.nodes:
            # init Nodes
            self.nodes[i] = Node(self.K, self.T, list(self.graph.neighbors(i)), i)
            self.listN.append(self.nodes[i].N)
            self.converged.append(self.nodes[i].converged)
            #dists
            for j in self.nodes[i].neighbors:
                # random tempo
                time = random.randint(0,self.numberOfNodes)
                #inserir
                self.dist[(i,j)] = time


    def start(self):
        current = 0
        # 1. nodo i envia para todos os seus vizinhos
        # 2. o vizinho responde so ao nodo i OU o vizinho envia para todos os seus vizinhos
        for i in range(0, len(self.nodes)):
            #Nodo i envia mensagem para todos os seus vizinhos
            for j in self.nodes[i].neighbors:
                # 1.Nodo i envia msg para j
                timeValueIJ = self.dist[(i, j)]
                current += timeValueIJ
                self.queue.append((i, j, current))
            # Vizinhos respondem ao nodo i
            for j in self.nodes[i].neighbors:
                # j responde a i
                timeValueJI = self.dist[(j,i)]
                current += timeValueJI
                self.queue.append((j, i, current))
            # Nodo i envia mensagem aos vizinhos
            for j in self.nodes[i].neighbors:
                # 1.Nodo i envia msg para j
                timeValueIJ = self.dist[(i, j)]
                current += timeValueIJ


    def run(self):
        round = 0
        numberOfMessages = 0
        numberLost = 0
        numberOfTrues = 0

        while numberOfTrues < self.numberOfNodes:

            for i in range(0, len(self.nodes)):
                # send x to every neighbor
                for j in self.nodes[i].neighbors:
                    # send to node j vectorX and receiving new vectorX from j
                    self.nodes[j].receiveMsg(self.nodes[i].vectorX)
                    numberOfMessages += 1
                    # Messages Lost
                    randomNumber = random.rand()
                    if randomNumber > self.percentage:
                        # ---- So para receber
                        # add N  of node j to list
                        self.listN[j] = self.nodes[j].N
                        # calculating and updating vectorX in node i
                        self.nodes[i].pontwiseMinimum(self.nodes[j].vectorX)
                        # add N  of node i to list
                        self.listN[j] = self.nodes[i].N
                        if self.converged[i] is False and self.nodes[i].converged:
                            self.converged[i] = self.nodes[i].converged
                            numberOfTrues+=1
                            print(f'{self.nodes[i].converged} -> {numberOfTrues}')
                    else:
                        numberLost += 1
            i = 0
            round += 1
        print(f'Round {round} = {self.listN}')
        print(f'Round {round} = {self.converged}')
        print(f'Number of messages lost = {numberLost}; Number of Messages {numberOfMessages}')

    def run_loop(self):
        while len(self.queue) > 0:
            # Minimum distances Nodes ((src, dst), time)
            minimumTiming = sorted(bPropagation.dist.items(), key=lambda x: x[1], reverse=False)
            # handle Nodo i -> j




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

    def receiveMsg(self, msgX, nodeSource):
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
    bPropagation = BasicExtremePropagation(1000, 4, 10, 0.1)
    bPropagation.initialize()
    #bPropagation.run()

    #print(f'{bPropagation.dist}')
    sort_orders = sorted(bPropagation.dist.items(), key=lambda x: x[1], reverse=False)
    for i in sort_orders:
        print(f'dict[({i[0][0]},{i[0][1]})] = {i[1]} ')
    #minimumTiming = min(bPropagation.dist, key=bPropagation.dist.get)
    #print(minimumTiming)
    print(sort_orders[0])
    plt.subplot(121)
    nx.draw(bPropagation.graph, with_labels=True)
    plt.show()
