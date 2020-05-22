from connected import randomGraph
from numpy import random
import matplotlib.pyplot as plt
import networkx as nx



class ExtremePropagation:


    def __init__(self, k):
        self.graph = randomGraph(k)
        self.nodes = list(self.graph.nodes)
        self.k = k
        self.results = []
        self.x = 0



    def run(self):
        for i in range(self.k):
            self.nodes[i] = Node(i, self.k, self.graph.neighbors(i))

    def sendMsgs(self):
        for i in range(self.k):
            # vizinhos do node i
            neighbors = self.nodes[i].neighbors

            for nei in neighbors:
                print(f"Node {i} envia para {nei}")
                # Node i envia vector para nei (aka vizinho)
                self.nodes[nei].receiveMsg(self.nodes[i].vector)
            print('------------------------------------------')

    '''   def __node_broadcast(self, node):
        next_msg = node.next_to_broadcast()
        how_many = 0
        if next_msg is not None:
            neighbors = list(self.graph.neighbors(node.get_num()))
            num = math.ceil(len(neighbors) * self.percentage)
            for i in rand.sample(neighbors, num):
                neighbor = self.nodes[i]
                res = neighbor.append(next_msg)
                self.received_msg.append(neighbor)
                step = self.current_step
                try:
                    self.reached_nodes[step] += res
                except:
                    self.reached_nodes[step] = res
            return True
        return False

    def run(self):
        # para cada nodo inicializar o vector v
        for i in range(self.num_nodes):
            self.nodes[i] = Node(i)
        init = rand.choice(range(self.num_nodes))
        self.nodes[init].append(init)
        self.reached_nodes[0] = 1
        self.b    
    def sendMSgs(self):
        for i in self.vector:
            roadcasting.append(self.nodes[init])
        running = 1
        while running > 0:
            running = 0
            fo    
    def sendMSgs(self):
        for i in self.vector:
            r node in self.broadcasting:
                if self.__node_broadcast(node):
                    running += 1
            self.current_step += 1
            step = self.current_step
            before = self.reached_nodes[step - 1]
            self.reached_nodes[step] = before
            self.broadcasting = self.received_msg
            self.received_msg = []
        return self.reached_nodes

    def get_graph(self):
        return self.graph
    '''




class Node:

    def __init__(self, num, k, neighbors):
        self.vector = random.exponential(scale = 1, size = k)
        self.known_msgs = list()
        self.num = num
        self.neighbors = neighbors
        self.msgs = []

    def receiveMsg(self, vector):
        if vector[self.num] < self.vector[self.num]:
            self.vector[self.num] = vector[self.num]
            print(f"Alterou --> {self.vector}  ---\n {self.vector[self.num]} < {self.vector[self.num]}")
            return True
        print(f"Não alterou --> {self.vector}")
        return False

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

'''
node2 = Node(1, 10)
node = Node(2, 10)
print(node.receiveMsg(node2.vector))
'''

x = ExtremePropagation(10)
x.run()
x.sendMsgs()

# Draw Graph
plt.subplot(121)
nx.draw(x.graph, with_labels=True)
plt.show()
