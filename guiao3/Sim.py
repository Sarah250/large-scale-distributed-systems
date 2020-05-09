import time


class Node:
    # handle `msg` by process `src` at time `t`
    def __init__(self, neighbours):
        self.neighbours = neighbours

    def handle(self, src, msg, t):
        # returns e.g. [(dst0, msg0), (dst1, msg1), ..]
        # pass
        print msg


class Sim:

    def __init__(self, nodes, distances):
        self.nodes = nodes
        self.distances = distances
        self.currentTime = 0
        self.pending = []

    def start(self, initial_msg):
        # schedule first event
        for i in self.nodes:
            event = (self.nodes[i], (None, i, initial_msg))
            self.pending.append(event)

        # run the simulation loop
        self.run_loop()

    def run_loop(self):
        while len(self.pending) > 0 and len(self.distances) > 0:
            # Self pending is the events (0, 1...)
            # Minimum distances Nodes (src, dst)
            minimumTiming = min(self.distances, key=self.distances.get)
            # Distance is timer
            timer = self.distances.get(minimumTiming)

            ton = self.pending[minimumTiming[0]]
            tuple = ton[1]
            msg = tuple[2]

            # handle message
            ton[0].handle(minimumTiming[0], msg, timer)

            self.distances.pop(minimumTiming)
            self.pending.pop(minimumTiming[0])


# nodes = {0: (0, 1), 1: (0, 2)}
# nodes = {0, 1, 2}
nodes = {0: Node({1, 2}), 1: Node({0}), 2: Node({0})}

distances = {(0, 1): 103, (0, 2): 40}

simulador = Sim(nodes, distances)

simulador.start("msg0")

# (dst, src): distance
# distances = {(0,1): 2, }
# distances = {(0,1): 130, (0,10): 10, (0,5): 900}
# t = Sim(distances, {130, 10, 900})
# - nodes: {0: Node, 1: Node, 2: Node...}
# - distances: {(0,1): 103, (0,2): 40, ...}
