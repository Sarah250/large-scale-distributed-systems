import time


class Sim:

    def __init__(self, nodes, distances):
        self.nodes = nodes
        self.distances = distances
        self.currentTime = 0
        self.pending = []

    def start(self, initial_msg):
        # schedule first event
        for i in self.nodes:
            event = (0, (None, i, initial_msg))
            self.pending.append(event)

        # run the simulation loop
        self.run_loop()

    def run_loop(self):
        while len(self.pending) > 0:
            minimumTiming = min(self.distances, key=self.distances.get)
            timer = self.distances.get(minimumTiming)
            time.sleep(timer)
            self.distances.pop(minimumTiming)

distances = {(0,1): 130, (0,10): 10, (0,5): 900}
t = Sim()