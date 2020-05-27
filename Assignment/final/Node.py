from numpy import random
import numpy as np

from Msg import Msg


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
        self.expectedResponses = []
        self.dist = {}
        self.numberOfResponses = 0

    def setDist(self, dist):
        self.dist = dist

    def addResponde(self, response):
        self.expectedResponses.append(response)

    # Round 1: enviar mensagens para os vizinhos
    def handle(self, clock):
        # oldX <- vectorX
        self.oldX = self.vectorX
        pending = []

        for nei in self.neighbors:
            self.expectedResponses.append((nei, self.myNumber))
            disTime = self.dist[(self.myNumber, nei)]
            msg = Msg(self.vectorX)
            event = ((self.myNumber, nei), msg, disTime + clock)
            pending.append(event)
        return pending

    def receive(self, msgX, src, clock):
        pending = []
        # Round 2: recebe mensagem de um nodo
        if len(self.expectedResponses) == 0:
            # oldX <- vectorX
            self.oldX = self.vectorX
            # vectorX da mensagem
            vectorX = msgX.vectorX
            # calculate and update vectorX with the pontwiseMinimum
            self.vectorX = np.minimum(self.vectorX, vectorX)
            # adiciono às mensagens esperadas
            self.expectedResponses.append((src, self.myNumber))
            msg = Msg(self.vectorX)
            distTime = self.dist[(self.myNumber, src)]
            event = ((self.myNumber, src), msg, distTime + clock)
            pending.append(event)
            return pending
        # Round 3:
        if len(self.expectedResponses) > 0:
            # vectorX da mensagem
            vectorX = msgX.vectorX
            # se for a mensagem final
            if msgX.final:
                self.expectedResponses.remove((src, self.myNumber))
                # oldX <- vectorX
                self.oldX = self.vectorX

                # calculate and update vectorX with the pontwiseMinimum
                self.vectorX = np.minimum(self.vectorX, vectorX)
                return None
            else:
                print(f'{(src, self.myNumber)}')
                print(f'{(self.expectedResponses)}')
                self.expectedResponses.remove((src, self.myNumber))
                self.oldX = self.vectorX
                # calculate and update vectorX with the pontwiseMinimum
                self.vectorX = np.minimum(self.vectorX, vectorX)
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
                        self.expectedResponses.append((nei, self.myNumber))
                        disTime = self.dist[(self.myNumber, nei)]
                        msg = Msg(self.vectorX)
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
