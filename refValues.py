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


def degmatrix(W):
    tam = W.shape[0]
    d = np.zeros((tam, 1))
    I = np.identity(tam)
    for i in range(tam):
        for j in range(tam):
            d[i] = d[i] + W[i, j]
    D = I * d
    return D


def Lmatrix(W, D):
    Lnt = D - W
    Lt = Lnt.transpose()
    L = np.dot(Lt, Lnt)
    L = L / 2
    return L


def eigen(L):
    (LANDA, PHY) = np.linalg.eig(L)  # calculamos los autovalores
    tam = PHY.shape[1]
    ind = np.argsort(LANDA)  # de menor a mayor
    #ind = ind[::-1]         # de mayor a menor
    LANDA = LANDA[ind]
    for i in range(tam):
        PHY[i] = PHY[i][ind]
    return PHY, LANDA


def eigen_reduce(PHY, LANDA):
    del_ind = np.where(LANDA <= 0)[0]
    LANDA_ses = np.delete(LANDA, del_ind)
    PHY_ses = np.delete(PHY, del_ind, 1)
    return PHY_ses, LANDA_ses


def eigen_aisle(PHY_ses, LANDA_ses):
    landa9 = LANDA_ses[7].real   # Aislamos el 9º par autovalor/vector
    phy9 = np.empty(0)
    for i in range(PHY_ses.shape[0]):
        phy9 = np.hstack((phy9, PHY_ses[i, 7].real))
    return phy9, landa9