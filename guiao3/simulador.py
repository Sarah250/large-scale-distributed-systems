class Sim:

    def __init__(self, nodes, distances):
        self.nodes = nodes
        self.distances = distances
        self.current_time = 0
        self.pendig = []

    def start(self, initial_msg):
        for i in self.nodes:
            event = (0, (None, i, initial_msg))
            self.pendig.append(event)
        self.run_loop()

    def run_loop(self):
        while len(self.pendig > 0):
            min = min(self.distances, key = self.distances.get)
            value = self.distances.get(min)