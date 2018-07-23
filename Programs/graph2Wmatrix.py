#-*- coding: utf-8 -*-

import networkx as nx
import numpy as np


def readgraph(x):
    g = nx.read_gpickle(x)
    return g


def wmatrix(gph):
    A = nx.adjacency_matrix(gph)
    W = A.toarray()
    W = W.astype(float)
    peso_max = np.amax(W)
    W = W / peso_max
    return W

if __name__=="__main__":
    # Obtenemos la lista de individuos que queremos procesar
    filedir = '/home/enrique/Proyectos/PersonalityTraitsOptimization/Data/lowConscientiousness.txt'
    archivo = open(filedir, "r")
    names = archivo.readlines()
    archivo.close()
    for i in range(len(names)):
        names[i] = names[i].rstrip("\n")

    # Obtenemos el tipo de individuo que buscamos
    filePart = filedir.split('/')
    typ = filePart[len(filePart) - 1]
    typ = typ.rstrip('.txt')

    # Comprobamos también que grafos no están
    missing = []
    for i in range(len(names)):
        try:
            graph = '/home/enrique/Proyectos/PersonalityTraitsOptimization/Data/DS00071/Graphs/sub-' + names[i] + '_ses-1_dwi_DS00071.gpickle'
            G = readgraph(graph)
            '''
            W = wmatrix(G)
            graphName = 'Wmat_' + names[i] + '.txt'
            route = '/home/enrique/Proyectos/PersonalityTraitsOptimization/Data/DS00071/Wmatrix/' + typ + '/'
            np.savetxt(route + graphName, W, delimiter=',')
            '''
        except(IOError):
            missing.append(names[i])
    missingPath = '/home/enrique/Proyectos/PersonalityTraitsOptimization/Data/DS00071/' + typ + 'MissingFiles.txt'
    archivo = open(missingPath, 'a+')
    for i in range(len(missing)):
        archivo.write(str(missing[i]) + '\n')

