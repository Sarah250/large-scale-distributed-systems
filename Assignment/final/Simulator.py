import atexit
import networkx as nx
import matplotlib.pyplot as plt
from Node import Node
from connected import randomGraph
from numpy import random
import sched, time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger


class Simulator:

    def __init__(self, K, T, numberOfNodes, percentage):
        self.graph = randomGraph(numberOfNodes)
        plt.subplot(121)
        nx.draw(self.graph, with_labels=True)
        plt.show()
        self.nodes = list(self.graph.nodes)
        self.T = T
        self.K = K
        self.numberOfNodes = numberOfNodes
        self.percentage = percentage
        self.dist = {}
        self.listN = list()
        self.converged = list()
        self.pending = []
        self.time = 0
        self.sched = sched.scheduler(time.time, time.sleep)
        self.s = BackgroundScheduler()

    def initialize(self):
        for i in self.nodes:
            self.nodes[i] = Node(self.K, self.T, list(self.graph.neighbors(i)), i)
            self.listN.append(self.nodes[i].N)
            self.converged.append(self.nodes[i].converged)

            localDist = {}

            for j in self.nodes[i].neighbors:
                #time = random.randint(1, 10)
                time = random.random()
                self.dist[(i, j)] = time
                localDist[(i, j)] = time
            self.nodes[i].setDist(localDist)

    def receiveMsg(self, src, dst, msg):
        # print(f"Mensagem de {src} -> {dst}")
        result = self.nodes[dst].receive(msg, src, self.time)
        if result != None:
            self.pending = self.pending + result

    def queueing(self):
        print("Calculating")

        flag = True
        i = 0
        N = 0
        list = []

        while i < len(self.nodes) and flag:
            #if self.nodes[i].converged:
            list.append((self.nodes[i].myNumber,self.nodes[i].converged, self.nodes[i].estimating()))
            # flag = False
            i += 1
        print(f"Estimated value = {list}")

    def timer(self):
        self.s.start()
        self.s.add_job(
            func=self.queueing,
            trigger=IntervalTrigger(seconds=30),
            id='printing_time_job',
            name='Print time every 20 seconds',
            replace_existing=True
        )
        # Shut down the scheduler when exiting the app
        atexit.register(lambda: self.s.shutdown())

    def updatePending(self):
        pending = []
        for p in self.pending:
            pending.append((p[0], p[1], p[2] + self.time))
        self.pending = pending

    def run_loop(self):
        i = 0
        self.timer()

        pending = self.nodes[i].handle(self.time)
        self.pending = self.pending + pending
        while len(self.pending) > 0:
            # 1. Minimum distances Nodes ((src, dst), time)
            result = sorted(self.pending, key=lambda x: x[2])
            #print(result[0])
            src = result[0][0][0]
            dst = result[0][0][1]
            time2 = self.dist[(src,dst)]
            msg = result[0][1]

            # enviar mensagem:
            print(f"SCHED - {src} -> {dst} : {time2}")
            self.sched.enter(time2, 1, self.receiveMsg, argument=(src, dst, msg))
            # blocking
            self.sched.run()

            # remove from pending
            if result[0] in self.pending:
                self.pending.remove(result[0])

            # update time
            self.time += time2
            # update self.pending
            #self.updatePending()
            # print(f'{i}. Clock = {self.time}')
            # print('----------------------------------------------')
            i += 1
            if i < self.numberOfNodes:
                pending = self.nodes[i].handle(self.time+1)
                self.pending = self.pending + pending
        self.queueing()


if __name__ == '__main__':
    simulator = Simulator(1000, 4, 10, 0.2)
    simulator.initialize()
    simulator.run_loop()

