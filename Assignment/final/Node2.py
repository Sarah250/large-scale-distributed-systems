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
        # Destination Node, response
        self.responses = []
        # Source Node, VectorX
        self.receivedMessages = []

    # Node Envia para os Vizinhos
    def handle(self):
        # Enquanto tiver vizinhos vizinhos
        if len(self.neighbors) > 0:
            # Enviar o meu vector
            for i in self.neighbors:
                print(f"Sending from {self.myNumber} -> {i.myNumber}")
                # TODO: Implementar um timout para perda de mensagens

                receivedMessage = i.send(self.myNumber, self.vectorX)

                self.receivedMessages.append(receivedMessage)

                print(self.receivedMessages)
                # print(self.receivedMessages)
        else:
            if len(self.receivedMessages) == len(self.neighbors):
                # Não Existem mais vizinhos, lógica do algoritmo
                return self.handleMessage()

    '''
    Receives a message from parent neighbor
    :param src: Sender Node
    :param msg: Received Vector X
    :return:
    '''
    def send(self, src, msg):
        # Recebi uma mensagem do pai vizinho, o que fazer?

        # Adicionar à lista de mensagens
        self.receivedMessages.append((src, msg))

        # Enviar para os meus vizinhos
        # retornar quando já não há mais vizinhos desse vizinho
        return self.handle()

        #self.receivedMessages.append((src, msg))

        #if len(self.neighbors) == 0:
            # Se não houver vizinhos a enviar mensagens, retorna as respostas
#            msg = (self.myNumber, self.handleMessage())

 #           return msg
  #      else:
   #         for neighbor in self.neighbors:
    #            neighbor.handle()

    '''
    Handle vector received
    :param msg: received vector
    :return:
    '''
    def handleMessage(self):

        self.oldX = self.vectorX

        # Calcular o Pointwise minimum
        for i in self.receivedMessages:
            self.vectorX = np.minimum(self.vectorX, i[1])

        if (self.oldX != self.vectorX).all():
            self.nonews = 0
        else:
            print(f"No news {self.nonews}")
            self.nonews += 1

        if self.nonews >= self.T:
            self.converged = True

        # return self.vectorX
        # após receber todas as mensagens, enviar o resultado do X a todos os vizinhos

    def query(self):
        if self.converged:
            return self.estimator()
        else:
            # Ainda não acabei !!!
            return None

    def estimator(self):
        return (len(self.vectorX) - 1) / sum(self.vectorX)

    def __len__(self):
        return len(self.neighbors)
