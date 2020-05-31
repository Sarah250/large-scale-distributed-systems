from numpy import random
import numpy as np
import queue

from Msg import Msg

class Node:
    """
    Initialize a Node with Parameters
    :param K: size of vector X
    :param T: number max of no news on consecutive rounds
    :param parent: Parent Node or None
    :param neighbors: list of neighbor nodes
    :param myNumber: Node id
    :param faults: percentage max of faults
    """
    def __init__(self, K, T, parent, neighbors, myNumber, faults):
        self.T = T
        self.N = 0
        self.vectorX = random.exponential(scale=1, size=K)
        self.parent = parent
        self.neighbors = neighbors
        self.oldX = self.vectorX
        self.nonews = 0
        self.converged = False
        self.myNumber = myNumber
        self.faults = faults
        self.distance = []
        #
        # Destination Node, responded
        self.sentMessages = []
        self.receivedMessages = []


    # Node Envia para os Vizinhos
    def handle(self):
        for i in self.neighbors:
            print(f'{self.myNumber} -> {i.myNumber}')
            i.receive(self.myNumber, self.vectorX)
            # Adicionar a Mensagens enviadas o numero do vizinho e um boolean
            # i.receive(self.parent, self.vectorX)
            # self.sentMessages.append((i, False)) # false indica que não recebeu resposta ainda
            # enviar o self.X para cada vizinho

    def handleNeighbors(self):
        for i in self.neighbors.neighbors:
            print(f'{self.myNumber} -> {i.myNumber}')
            i.receive(self.myNumber, self.vectorX)


    '''
    Receives a message from neighbor
    :param src: Sender Node
    :param msg: Received Vector X
    :return:
    '''
    def receive(self, src, msg):

        self.receivedMessages.append((src, msg))

        # print(f'{len(self.neighbors)}')
        # Se não não houver mais vizinhos a quem enviar o vector X...
        if len(self.neighbors) > 0:
            self.handleNeighbors()
            # Lógica do algoritmo
            #return self.handleMessage()
        else:
            return self.handleMessage()
            # Continuar a enviar para os vizinhos
            #self.handle()


        #for i in self.sentMessages:
            #if i[0] == src:
                #i[1] = True
                #self.totalReceived = self.totalReceived + 1
                #receivedMessages.append(msg)

        # Calcular quantas faltas posso ter
        #maxLost = round(self.faultPercentage * len(self.neighbors))

        # adicionar um timer
        #if len(self.receivedMessages) >= (len(self.neighbors) - maxLost):
            #self.handleMessage(receivedMessages)


        # Ver das faltas
        # handleMessage()

    '''
    Handle vector received
    :param msg: received vector
    :return:
    '''
    def handleMessage(self):

        self.oldX = self.vectorX

        # Calcular o Pointwise minimum
        for i in msgList:
            self.vectorX = np.minimum(self.vectorX, i)

        if (self.oldX != self.vectorX).all():
            self.nonews = 0
        else:
            self.nonews += 1

        if self.nonews >= self.T:
            self.converged = True

        return self.vectorX
        # após receber todas as mensagens, enviar o resultado do X a todos os vizinhos

    def query(self):
        if self.converged:
            return estimator()
        else:
            # Ainda não acabei !!!
            return None

    def estimator(self):
        return (len(self.vectorX) - 1) / sum(self.vectorX)

    def __len__(self):
        return len(self.neighbors)
