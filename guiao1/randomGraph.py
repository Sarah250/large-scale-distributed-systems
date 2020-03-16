import networkx as nx
import matplotlib.pyplot as plt
import random

'''
[1] - given V vertices, what's de minimum number of edges that have to be added to make the graph connected?
    R: V-1
[2] - given V vertices, what's de maximum number of edges that can be added before making the graph connected?
    R : V-2
[3] - for which V, are the generated connected graphs complete?
    R : V = 2 ? 
[4] - what's the connection (if any) between the previous two questions? 
    R : have no idea bro
'''


# Calculates the average of a list
def avg(edges):
    return sum(edges) / len(edges)


# Given a number of nodes it generates a random graph
def randomGraph(nodes):
    number_edges = 0

    G = nx.Graph()
    G.add_nodes_from([*range(0, nodes)])

    while nx.number_connected_components(G) != 1:
        v1 = random.randint(0, nodes - 1)
        v2 = random.randint(0, nodes - 1)

        if not nx.Graph.has_edge(G, v1, v2) and v1 != v2:
            G.add_edge(v1, v2)
            number_edges += 1
    return number_edges


def main():
    # 1
    n = int(input("Insert number of vertices: "))
    max2 = int(input('Maximum number of iterations: '))
    i = int(input('Interval number of creations of nodes:  '))
    attempts = int(input('Number of attempts for each group of nodes: '))

    # 4
    x = []      # nodes
    yA = []     # average number of edges

    # 5
    yM = []     # max number of edges
    ym = []     # min number of edges

    # 6
    for value in range(0, max2, i):

        tmp = []

        for _ in range(attempts):
            numberEdges = randomGraph(n)
            tmp.append(numberEdges)
        x.append(n)
        yA.append(avg(tmp))
        ym.append(min(tmp))
        yM.append(max(tmp))
        n += i

    # 7
    plt.xlabel('Number of vertices')
    plt.ylabel('Number of edges')
    plt.plot(x, yA, "-b", label="avg")
    plt.plot(x, yM, "-r", label="max")
    plt.plot(x, ym, "-g", label="min")
    plt.legend(loc="upper left")
    plt.show()

if __name__ == "__main__":
    main()