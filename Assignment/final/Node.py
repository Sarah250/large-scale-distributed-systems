from numpy import random
import numpy as np
import queue

from Msg import Msg


class Node:
    def __init__(self, K, T, neighbors, myNumber):
        self.T = T
        self.N = 0
        self.vectorX = random.exponential(scale=1, size=K)
        self.neighbors = neighbors
        self.oldX = self.vectorX
        self.nonews = 0
        self.converged = False
        self.myNumber = myNumber
        #
        self.expectedResponses = queue.Queue()
        self.dist2 = {}
        self.dist = []
        self.numberOfResponses = 0
        self.pending = []
        #
        self.all = []
        self.unexpectedRequests = []

    def setDist(self, dist):
        self.dist2 = dist
        for key in dist:
            self.dist.append((key, dist[key]))
        self.dist = sorted(self.dist, key=lambda x: x[1])

    def calculatingExpectedResponses_v1(self):
        list = []
        for j in self.dist:
            list.append((j[0][1], j[0][0]))
            self.all.append((j[0][1], j[0][0]))
        self.expectedResponses.put(list)

    def addResponde(self, response):
        self.expectedResponses.append(response)

    # Round 1: enviar mensagens para os vizinhos
    def handle(self, clock):
        # oldX <- vectorX
        self.oldX = self.vectorX
        pending = []

        self.calculatingExpectedResponses_v1()

        for nei in self.dist:
            disTime = nei[1]
            msg = Msg(self.vectorX)
            event = ((self.myNumber, nei[0][1]), msg, disTime + clock)
            pending.append(event)
        print(f'{self.myNumber} -> {self.expectedResponses}')
        return pending

    # nada à espera
    def function_1(self, src, msgX, clock):
        pending = []
        #print(f'1. ({self.myNumber} Recebi 1 msg {src} -> {self.myNumber} ')
        # oldX <- vectorX
        self.oldX = self.vectorX
        # vectorX da mensagem
        vectorX = msgX.vectorX
        # calculate and update vectorX with the pontwiseMinimum
        self.vectorX = np.minimum(self.vectorX, vectorX)
        # adiciono às mensagens esperadas
        self.all.append((src, self.myNumber))
        self.unexpectedRequests.append((src, self.myNumber))
        msg = Msg(self.vectorX)
        distTime = self.dist2[(self.myNumber, src)]
        event = ((self.myNumber, src), msg, distTime + clock)
        #print(f"1. {self.myNumber} Event = {event}")
        pending.append(event)
        return pending

    def function_2(self, msgX, src):
        #print(f'2. ({self.myNumber}) Recebi 1 msg {src} -> {self.myNumber} ')
        msg = msgX.vectorX
        self.unexpectedRequests.remove((src, self.myNumber))
        self.all.remove((src, self.myNumber))
        # oldX <- vectorX
        self.oldX = self.vectorX
        # calculate and update vectorX with the pontwiseMinimum
        self.vectorX = np.minimum(self.vectorX, msg)
        return None

    def function_3(self, msgX, src, clock):
        # vectorX da mensagem
        #print(f'2. ({self.myNumber}) Recebi 1 msg {src} -> {self.myNumber} ')
        msg = msgX.vectorX

        self.expectedResponses.queue[0].remove((src, self.myNumber))
        self.oldX = self.vectorX
        # calculate and update vectorX with the pontwiseMinimum
        self.vectorX = np.minimum(self.vectorX, msg)
        #
        self.numberOfResponses += 1
        #

        # print(f'Number of Response={self.numberOfResponses}\nNeighbors={self.neighbors}')

        if self.numberOfResponses == len(self.neighbors):
            #print(f"3. ({self.myNumber}) Calculos")
            self.numberOfResponses = 0
            self.expectedResponses.get()

            if (self.oldX != self.vectorX).all():
                self.nonews = 0
            else:
                self.nonews += 1
            if self.nonews >= self.T:
                self.converged = True
            pending = []

            #print(f'4. T={self.T}\nNo News={self.nonews}')

            list = []
            for nei in self.neighbors:
                # print(f'Eu {self.myNumber} vou enviar mensagens finais a {nei}')
                list.append((nei, self.myNumber))
                disTime = self.dist2[(self.myNumber, nei)]
                msg = Msg(self.vectorX)
                msg.final = True
                event = ((self.myNumber, nei), msg, disTime + clock)
                pending.append(event)
            return pending

    def receive(self, msgX, src, clock):
        pending = []
        # Opção 1: recebe mensagem de um que não està à espera!
        if not ((src, self.myNumber) in self.all):
            return self.function_1(src, msgX, clock)

        # Opção 2: recebe mensagem que está à espera mas não do
        elif (src, self.myNumber) in self.unexpectedRequests:
            return self.function_2(msgX, src)

        # Opção 3:
        elif (src, self.myNumber) in self.expectedResponses.queue[0]:
            return self.function_3(msgX,src,clock)

    def pontwise(self, msgX):
        # oldX <- vectorX
        self.oldX = self.vectorX
        # calculate and update vectorX with the pontwiseMinimum
        self.vectorX = np.minimum(self.vectorX, msgX)

    def estimating(self):
        return (len(self.vectorX) - 1) / sum(self.vectorX)
