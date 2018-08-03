#-*- coding: utf-8 -*-

import networkx as nx
import numpy as np
import os


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

def degmatrix(W):
    tam = W.shape[0]
    d = np.zeros((tam, 1))
    I = np.identity(tam)
    for i in range(tam):
        for j in range(tam):
            d[i] = d[i] + W[i, j]
    D = I * d
    return D


def graphLaplacian(W, D):
    L = D - W
    sqD = D
    for i in range(len(sqD)):
        if sqD[i,i] != 0:
            sqD[i,i] = 1 / np.sqrt(sqD[i,i])
        else:
            sqD[i, i] = 0
    gLap = np.dot(sqD,np.dot(L,sqD))
    return gLap


def eigen(gLap):
    (LANDA, PHY) = np.linalg.eig(gLap)  # calculamos los autovalores
    tam = PHY.shape[1]
    ind = np.argsort(LANDA)  # de menor a mayor
    #ind = ind[::-1]         # de mayor a menor
    LANDA = LANDA[ind]
    for i in range(tam):
        PHY[i] = PHY[i][ind]
    return PHY, LANDA


def eigen_reduce(PHY, LANDA):
    del_ind = np.where(LANDA <= 0)[0]
    LANDA = np.delete(LANDA, del_ind)
    PHY = np.delete(PHY, del_ind, 1)
    PHY = PHY.T # Trasnsponemos para que los autovectores se almacenen en filas
    LANDA_ses = LANDA[0:40]
    PHY_ses = PHY[0:40]
    return PHY_ses, LANDA_ses


if __name__=="__main__":
    directory = '/home/enrique/Proyectos/PersonalityTraitsOptimization/Data/DS00071/Graphs'
    subjects = os.listdir(directory)
    eigval = []
    eigvec = []
    for i in range(len(subjects)):
        if subjects[i].endswith('.gpickle'):
            graph = directory + '/' + subjects[i]
            g = readgraph(graph)
            W = wmatrix(g)
            D = degmatrix(W)
            gL = graphLaplacian(W, D)
            PHY, LANDA = eigen(gL)
            PHY_ses, LANDA_ses = eigen_reduce(PHY, LANDA)
            eigval.append(LANDA_ses)
            eigvec.append(PHY_ses)
    '''
    meanEigval = np.mean(eigval, axis=0)
    meanEigvec = np.mean(eigvec, axis=0)
    path = '/home/enrique/Proyectos/PersonalityTraitsOptimization/Data/DS00071/'
    np.savetxt(path + '')
    
    HAY QUE TENER CUIDADO, NO TODOS TIENEN UN VALOR MUY CERCANO A 0 PERO SIN SER 0 POR LO QUE EN ESOS SE ELIMINA EL
    ESTADO FUNDAMENTAL. HAY QUE REVISAR COMO SE SESAGAN LOS AUTOVALORES PARA QUEDARNOS SIEMPRE CON UN PRIMER VALOR
    FUNDAMENTAL EXACTAMENTO O APROXIMADAMENTE = 0
    
    '''






