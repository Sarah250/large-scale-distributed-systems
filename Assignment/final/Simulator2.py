import atexit
import networkx as nx
import matplotlib.pyplot as plt


from Node2 import Node

from connected import randomGraph
from numpy import random

import sched, time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

class Simulator:
    # - nodes: {0: Node, 1: Node, 2: Node...}
    # - distances: {(0,1): 103, (0,2): 40, ...}
    def __init__(self, K, T, numberOfNodes, percentage):
        """
        Initiate Simulation
        :param K: size of vector X
        :param T: number max of no news
        :param numberOfNodes: number of nodes in simulation
        :param percentage: percentage of message loss
        """
        self.graph = randomGraph(numberOfNodes) # Random Graph
        # plt.subplot(121)
        # nx.draw(self.graph, with_labels=True)
        # plt.show()
        self.nodes = list(self.graph.nodes) # List of Nodes created with Graph
        self.T = T
        self.K = K
        self.numberOfNodes = numberOfNodes
        self.percentage = percentage
        self.dist = {}
        # self.listN = list()
        # self.converged = list()
        self.pending = []
        self.time = 0
        self.sche = sched.scheduler(time.time, time.sleep)
        self.backgroundSchedule = BackgroundScheduler()

        self.initialize()


    def timer(self):
        self.backgroundSchedule.start()
        self.backgroundSchedule.add_job(
            func=self.query,
            trigger=IntervalTrigger(seconds=30),
            id="Printing N estimation every 30 seconds",
            replace_existing=True
        )
        # Shut down the scheduler when exiting the app
        atexit.register(lambda: self.backgroundSchedule.shutdown())

    def initialize(self):
        # Instanciar todos os nós da rede
        for node in self.nodes:
            # (delay, Node)
            # node = (0, Node(self.K, self.T, 0, node, self.percentage))
            self.nodes[node] = Node(self.K, self.T, None, list(self.graph.neighbors(node)), node, self.percentage)

        # Para cada nó da rede
        for node in self.nodes:
            neighbors = []
            #Instanciar o vizinho de index neighbor
            for neighbor in self.nodes[node.myNumber].neighbors:
                if neighbor != node.myNumber:
                    # K, T, parent, neighbors, myNumber, faults
                    n = Node(self.K, self.T, node, self.nodes[neighbor], neighbor, self.percentage)
                    neighbors.append(n)
                    #index = self.nodes[node.myNumber].neighbors.index(neighbor)
                    #self.nodes[node.myNumber].neighbors[index] = n
            node.neighbors.clear()
            node.neighbors = neighbors
            print("added")

                #= neighbors
                # else:
                    # self.nodes[node.myNumber].neighbors.pop
    def start(self):
        # schedule first event
        for i in self.nodes:
            # [(delay, (src, dst, msg))]
            event = (0, (None, i, "initial_msg"))
            self.pending.append(event)
        # run the simulation loop
        self.run_loop()

    def run_loop(self):
        self.timer()
        while len(self.pending) > 0:
            self.pending = sorted(self.pending, key=lambda x: x[0])
            node = self.pending[0][1][1]
            #self.pending

            node.handle()

            self.time += self.pending[0][0]

            self.pending.pop(0)

    '''
    Queries the initial Node for estimator value
    :return: 
    '''
    def query(self):

        result = self.nodes[0].query()

        if result is not None:
            print(result)
        else:
            print("Result isn't ready yet. Convergence is a key!")

if __name__ == '__main__':
    # k, t, number of nodes, fault percentage
    simulator = Simulator(1000, 4, 10, 0.2)
    # simulator.initialize()
    simulator.start()


    #graph = randomGraph(10)
    # plt.subplot(121)
    # nx.draw(graph, with_labels=True)
    # plt.show()
