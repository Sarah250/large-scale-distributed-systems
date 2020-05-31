import numpy as np

from connected import randomGraph
import matplotlib.pyplot as plt
import networkx as nx

from numpy import random

class Node:

    def __init__(self, num, k, t, neighbors):
        self.vector = random.exponential(scale = 1, size = k)
        self.known_msgs = list()
        self.num = num
        self.neighbors = neighbors
        self.msgs = []

        self.k = k
        self.t = t
        self.nonews = 0
        self.converged = False

    def receiveMsg(self, vector):
        oldx = self.vector

        # For each message received
        # determine the minimum between self.x and message vector
        # for i in messages:
        self.vector = np.minimum(self.vector, vector)
            # self.x[i] = min(min(self.x), min(messages[i]))

        # If there Oldx isn't different than X then nonews = 0
        if (oldx != self.vector).all():
            print("OldX = X, there are no news")
            self.nonews = 0
        # Else there is new news
        else:
            self.nonews = self.nonews + 1
            print(f"News: {self.nonews}")

        if self.nonews >= self.t:
            self.converged = True
            # Calculate N and Return it
            result = self.calcN()
            return result

    def calcN(self):
        result = 0
        for i in range(self.k):
            result = result + self.vector[i]

        return (self.k - 1) / result
        # return ( self.k - 1 ) / self.k

    def minimumValue(self):
        return min(self.vector)


    def append(self, msg):
        if msg not in self.known_msgs:
            self.in_queue.append(msg)
            self.known_msgs.append(msg)
            return 1
        return 0

    def get_num(self):
        return self.num

    def next_to_broadcast(self):
        if len(self.in_queue) > 0:
            msg = self.in_queue[0]
            del self.in_queue[0]
            return msg
        return None