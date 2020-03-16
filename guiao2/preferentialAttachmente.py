import networkx as nx
import matplotlib.pyplot as plt
import random
from guiao2.extras import accumulatedDegrees
from guiao2.extras import choosingNode

def preferentialAttachment(nodes):

    x = list(range(0, nodes))
    degree = []
    listaAcumulativos = []

    G = nx.Graph()
    G.add_nodes_from([*range(0, nodes)])

    i = 0
    accumulateNumber = 0

    while i < nodes:
        accumulateNumber += 1
        listaAcumulativos.insert(i, accumulateNumber)
        degree.insert(i, 1)
        i += 1

    while nx.number_connected_components(G) != 1:
        r1 = random.randint(0, listaAcumulativos[nodes-1])
        r2 = random.randint(0, listaAcumulativos[nodes-1])

        v1 = choosingNode(r1, listaAcumulativos)
        v2 = choosingNode(r2, listaAcumulativos)

        if not nx.Graph.has_edge(G, v1, v2) and v1 != v2:
            G.add_edge(v1, v2)
            degree[v1] += 1
            degree[v2] += 1
            listaAcumulativos = accumulatedDegrees(v1, degree, listaAcumulativos)
            listaAcumulativos = accumulatedDegrees(v2, degree, listaAcumulativos)

    nx.draw(G, with_labels=True, font_weight='bold')
    plt.savefig("graph.png")
    plt.show()

    plt.xlabel('Vertices')
    plt.ylabel('Grau')
    plt.plot(x, degree, "-b", label="degree")
    plt.legend(loc="upper left")
    plt.show()


def main():
    n = int(input("Insert initial number of vertices: "))
    max2 = int(input('Maximum number of vertices: '))
    i = int(input('Interval number of creations of nodes:  '))
    #attempts = int(input('Number of attempts for each group of nodes: '))


    for value in range(0, max2, i):

       # for _ in range(attempts):
        preferentialAttachment(n)
        n += i

if __name__ == "__main__":
    main()