def accumulatedDegrees(node, listaDegree, listaAcumulativos):

    indice = node
    while indice < len(listaDegree):
        if indice == 0:
            listaAcumulativos[indice] = listaDegree[indice]
            indice += 1
        listaAcumulativos[indice] = listaAcumulativos[indice-1] + listaDegree[indice]
        indice += 1
    return listaAcumulativos


def choosingNode(number, listaAcumulativos):

    flag = True
    i = 0
    node = 0
    while i<len(listaAcumulativos) and flag:
        if listaAcumulativos[i] >= number:
            node = i
            flag = False
        i += 1
    return node
