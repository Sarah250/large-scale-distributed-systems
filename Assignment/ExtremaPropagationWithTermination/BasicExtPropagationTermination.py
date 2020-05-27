from numpy import random
import time
import atexit
import numpy as np
from ExtremaPropagationWithTermination.connected import randomGraph
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger


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
        self.time = 0
        self.s = BackgroundScheduler()

    def initialize(self):
        for i in self.nodes:
            # init Nodes
            self.nodes[i] = Node(self.K, self.T, list(self.graph.neighbors(i)), i, self.graph)
            self.listN.append(self.nodes[i].N)
            self.converged.append(self.nodes[i].converged)

            if i == 0:
                event = (self.nodes[i], self.nodes[i].vectorX, 0)
                self.queue.append(event)


            for j in self.nodes[i].neighbors:
                time = random.randint(1, self.numberOfNodes)
                # inserir
                self.dist[(i, j)] = time

    def queueing(self):
        print("Calculating")

        flag = True
        i = 0
        N = 0

        while i < len(self.nodes) and flag:
            if self.nodes[i].converged:
                N = self.nodes[i].estimating()
                flag = False
        print(f"Estimated value = {N}")


    def timer(self):
        self.s.start()
        self.s.add_job(
            func=self.queueing,
            trigger=IntervalTrigger(seconds=10),
            id='printing_time_job',
            name='Print time every 60 seconds',
            replace_existing=True
        )

        # Shut down the scheduler when exiting the app
        atexit.register(lambda: self.s.shutdown())

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
                            numberOfTrues += 1
                            print(f'{self.nodes[i].converged} -> {numberOfTrues}')
                    else:
                        numberLost += 1
            i = 0
            round += 1
        print(f'Round {round} = {self.listN}')
        print(f'Round {round} = {self.converged}')
        print(f'Number of messages lost = {numberLost}; Number of Messages {numberOfMessages}')

    def run_loop(self):
        self.timer()
        r = 0

        while len(self.queue) > 0:
            # 1. Minimum distances Nodes ((src, dst), time)
            result = sorted(self.queue, key=lambda x: x[2])
            node = result[0][0]
            senderNode = node.myNumber
            # fannout?
            numberOfneighbors = len(node.neighbors)
            time = result[0][2]
            msg = result[0][1]
            del result[0]
            self.queue = result

            # 2. envia para todos
            listMsgs = node.handleMsg_1(msg)

            for i in listMsgs:
                self.queue.append((self.nodes[i[0]], i[1], self.dist[(senderNode, i[0])]))


            # 3. vizinhos recebem a mensagem e enviam resposta
            k = 0
            listMsgs2 = []
            while k < numberOfneighbors:
                result = sorted(self.queue, key=lambda x: x[2])
                node = result[0][0]
                # fannout?
                time = result[0][2]
                msg = result[0][1]
                del result[0]
                self.queue = result

                msgReceived = node.handleMsg_2(msg, senderNode)
                listMsgs2.append(msgReceived)
                k +=1

            for y in listMsgs2:
                self.queue.append((self.nodes[y[0]], y[1], self.dist[(y[2], y[0])]))


            # 4. node recebe mensagens dos vizinhos e calcula pontwise:
            k = 0
            while k < numberOfneighbors:
                result = sorted(self.queue, key=lambda x: x[2])
                node = result[0][0]
                # fannout?
                time = result[0][2]
                msg = result[0][1]
                del result[0]
                self.queue = result

                self.nodes[senderNode].pontwise(msg)
                k += 1


            #5. envia resposta para os vizinhos
            listMsgs = self.nodes[senderNode].handleMsg_3()

            for i in listMsgs:
                self.queue.append((self.nodes[i[0]], i[1], self.dist[(senderNode, i[0])]))


            # Vizinhos recebem o resultado
            k = 0
            while k < numberOfneighbors:
                result = sorted(self.queue, key=lambda x: x[2])
                node = result[0][0]
                # fannout?
                time = result[0][2]
                msg = result[0][1]
                del result[0]
                self.queue = result
                node.pontwise(msg)
                k+=1

            r += 1
            if r == self.numberOfNodes:
                r = 0
            event = (self.nodes[r], self.nodes[r].vectorX, 0)
            self.queue.append(event)




class Node:

    def __init__(self, K, T, neighbors, myNumber, graph):
        self.T = T
        self.vectorX = random.exponential(scale=1, size=K)
        self.neighbors = neighbors
        self.N = 0
        self.oldX = self.vectorX
        self.nonews = 0
        self.converged = False
        self.myNumber = myNumber
        self.graph = graph

    # enviar para os viznhos
    def handleMsg_1(self, msgX):

        listMsgs = []
        # oldX <- vectorX
        self.oldX = self.vectorX
        # calculate and update vectorX with the pontwiseMinimum
        self.vectorX = np.minimum(self.vectorX, msgX)

        for j in self.neighbors:
            listMsgs.append((j, self.vectorX))

        return listMsgs

    def handleMsg_2(self, msgX, src):
        # oldX <- vectorX
        self.oldX = self.vectorX
        # calculate and update vectorX with the pontwiseMinimum
        self.vectorX = np.minimum(self.vectorX, msgX)

        return (src,self.vectorX, self.myNumber)

    # recebe dos vizinhos as mensagens
    def handleMsg_3(self):
        listMsgs = []
        if (self.oldX != self.vectorX).all():
            self.nonews = 0
        else:
            self.nonews += 1
        if self.nonews >= self.T:
            self.converged = True
        for j in self.neighbors:
            listMsgs.append((j, self.vectorX))

        return listMsgs

    # enviar o x para todos os viznhos

    def pontwise(self,msgX):
        # oldX <- vectorX
        self.oldX = self.vectorX
        # calculate and update vectorX with the pontwiseMinimum
        self.vectorX = np.minimum(self.vectorX, msgX)

    def estimating(self):
        return calculatingN(self.vectorX)


if __name__ == '__main__':
    # K, T, number of Nodes
    bPropagation = BasicExtremePropagation(1000, 4, 10, 0.1)
    bPropagation.initialize()
    bPropagation.run_loop()


    '''sort_orders = sorted(bPropagation.dist.items(), key=lambda x: x[1], reverse=False)
    for i in sort_orders:
        print(f'dict[({i[0][0]},{i[0][1]})] = {i[1]} ')
    #minimumTiming = min(bPropagation.dist, key=bPropagation.dist.get)
    #print(minimumTiming)
    print(sort_orders[0])
    plt.subplot(121)
    nx.draw(bPropagation.graph, with_labels=True)
    plt.show()'''
