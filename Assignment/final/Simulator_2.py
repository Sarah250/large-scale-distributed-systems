
from numpy import random
import sched, time

from connected import randomGraph


class Simulator:

    def __init__(self, K, T, numberOfNodes, percentage):
        self.graph = randomGraph(numberOfNodes)
        self.nodes = list(self.graph.nodes)
        self.T = T
        self.K = K
        self.numberOfNodes = numberOfNodes
        self.percentage = percentage
        self.dist = {}
        self.pending = []
        self.time = 0
        self.s = sched.scheduler(time.time, time.sleep)

    def initialize(self):
        for i in self.nodes:
            time = random.randint(1, 10)
            event = ((1, 4), "mensagem1", time)
            self.pending.append(event)

    def receiveMsg(self, msg):
        print(msg)

    def run_loop(self):
        i = 0
        while len(self.pending) > 0:
            # 1. Minimum distances Nodes ((src, dst), time)
            result = sorted(self.pending, key=lambda x: x[2])
            time = result[0][2]
            print(f'{i}. Result = {result[0]}')

            # enviar mensagem:
            msg = "msg" + str(i)
            self.s.enter(time, 0, self.receiveMsg,argument=(msg,))
            # blocking
            self.s.run()

            # remove from pending
            del result[0]
            self.pending = result

            # update time
            self.time += time
            print(f'{i}. Clock = {self.time}')
            print('----------------------------------------------')
            i += 1


if __name__ == '__main__':
    simulator = Simulator(10, 2, 10, 0.2)
    simulator.initialize()
    simulator.run_loop()
