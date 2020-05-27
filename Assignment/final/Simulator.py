import atexit

from Node import Node
from connected import randomGraph
from numpy import random
import sched, time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger




class Simulator:

    def __init__(self, K, T, numberOfNodes, percentage):
        self.graph = randomGraph(numberOfNodes)
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
                time = random.random()
                self.dist[(i, j)] = time
                localDist[(i,j)] = time
            self.nodes[i].setDist(localDist)

    def receiveMsg(self, src,dst, msg):
        #print(f"Mensagem de {src} -> {dst}")
        result = self.nodes[dst].receive(msg, src, self.time)
        if result != None:
            self.pending = self.pending + result

    def queueing(self):
        print("Calculating")

        flag = True
        i = 0
        N = 0

        while i < len(self.nodes) and flag:
            if self.nodes[i].converged:
                N = self.nodes[i].estimating()
                flag = False
            i += 1
        print(f"Estimated value = {N}")

    def timer(self):
        self.s.start()
        self.s.add_job(
            func=self.queueing,
            trigger=IntervalTrigger(seconds=10),
            id='printing_time_job',
            name='Print time every 20 seconds',
            replace_existing=True
        )
        # Shut down the scheduler when exiting the app
        atexit.register(lambda: self.s.shutdown())

    def run_loop(self):
        i = 0
        self.timer()
        pending = self.nodes[i].handle(self.time)
        self.pending = self.pending + pending
        while len(self.pending) > 0:
            # 1. Minimum distances Nodes ((src, dst), time)
            result = sorted(self.pending, key=lambda x: x[2])
            src = result[0][0][0]
            dst = result[0][0][1]
            time = result[0][2]
            msg = result[0][1]

            # enviar mensagem:
            self.sched.enter(time, 0, self.receiveMsg,argument=(src,dst,msg))
            # blocking
            self.sched.run()

            # remove from pending
            self.pending.remove(result[0])

            # update time
            self.time += time
            #print(f'{i}. Clock = {self.time}')
            #print('----------------------------------------------')
            i += 1
            if i == self.numberOfNodes:
                i = 0
            pending = self.nodes[i].handle(self.time)
            self.pending = self.pending + pending
    

if __name__ == '__main__':
    simulator = Simulator(10, 4, 10, 0.2)
    simulator.initialize()
    simulator.run_loop()
