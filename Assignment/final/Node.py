from numpy import random
import numpy as np

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
        self.expectedResponses = []
        self.dist2 = {}
        self.dist = []
        self.numberOfResponses = 0
        self.pending = []

    def setDist(self, dist):
        self.dist2 = dist
        for key in dist:
            self.dist.append((key, dist[key]))
        self.dist = sorted(self.dist, key=lambda x: x[1])

    def calculatingExpectedResponses_v1(self):
        for j in self.dist:
            self.expectedResponses.append((j[0][1], j[0][0]))

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

    def receive(self, msgX, src, clock):
        pending = []
        # Round 2: recebe mensagem de um nodo qualquer!
        if not ((src, self.myNumber) in self.expectedResponses):
            print(f' Recebi 1 msg {self.myNumber} <- {src}')
            # oldX <- vectorX
            self.oldX = self.vectorX
            # vectorX da mensagem
            vectorX = msgX.vectorX
            # calculate and update vectorX with the pontwiseMinimum
            self.vectorX = np.minimum(self.vectorX, vectorX)
            # adiciono às mensagens esperadas
            self.expectedResponses.append((src, self.myNumber))
            msg = Msg(self.vectorX)
            distTime = self.dist2[(self.myNumber, src)]
            event = ((self.myNumber, src), msg, distTime + clock)
            pending.append(event)
            return pending
        # Round 3:
        elif (src, self.myNumber) in self.expectedResponses:
            # vectorX da mensagem
            msg = msgX.vectorX
            # se for a mensagem final -> Quando um vizinho recebe a resposta final
            if msgX.final:
                #print(f'mensagem final de {src} para {self.myNumber}')
                self.expectedResponses.remove((src, self.myNumber))
                # oldX <- vectorX
                self.oldX = self.vectorX
                # calculate and update vectorX with the pontwiseMinimum
                self.vectorX = np.minimum(self.vectorX, msg)
                return None
            else:
                self.expectedResponses.remove((src, self.myNumber))
                self.oldX = self.vectorX
                # calculate and update vectorX with the pontwiseMinimum
                self.vectorX = np.minimum(self.vectorX, msg)
                #
                self.numberOfResponses += 1
                #

                print(f'Number of Response={self.numberOfResponses}\nNeighbors={self.neighbors}')

                if self.numberOfResponses == len(self.neighbors):
                    self.numberOfResponses = 0

                    if (self.oldX != self.vectorX).all():
                        self.nonews = 0
                    else:
                        self.nonews += 1
                    if self.nonews >= self.T:
                        self.converged = True
                    pending = []

                    print(f'T={self.T}\nNo News={self.nonews}')

                    for nei in self.neighbors:
                        #print(f'Eu {self.myNumber} vou enviar mensagens finais a {nei}')
                        self.expectedResponses.append((nei, self.myNumber))
                        disTime = self.dist2[(self.myNumber, nei)]
                        msg = Msg(self.vectorX)
                        msg.final = True
                        event = ((self.myNumber, nei), msg, disTime + clock)
                        pending.append(event)
                    return pending

    def pontwise(self, msgX):
        # oldX <- vectorX
        self.oldX = self.vectorX
        # calculate and update vectorX with the pontwiseMinimum
        self.vectorX = np.minimum(self.vectorX, msgX)

    def estimating(self):
        return (len(self.vectorX) - 1) / sum(self.vectorX)
