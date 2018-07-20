#-*- coding: utf-8 -*-

import numpy as np
import os


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
    LANDA_ses = np.delete(LANDA, del_ind)
    PHY_ses = np.delete(PHY, del_ind, 1)
    return PHY_ses, LANDA_ses


def eigen_aisle(PHY_ses, LANDA_ses):
    landa9 = LANDA_ses[7].real   # Aislamos el 9º par autovalor/vector
    phy9 = np.empty(0)
    for i in range(PHY_ses.shape[0]):
        phy9 = np.hstack((phy9, PHY_ses[i, 7].real))
    return phy9, landa9

if __name__=="__main__":
    path = '/home/enrique/Proyectos/PersonalityTraitsOptimization/Data/DS00071/Wmatrix/highConscientiousness'
    files = os.listdir(path)
    os.chdir(path)
    phy9_list = []
    landa9_list = []
    for i in range(len(files)):
        file = files[i]
        if file.endswith('.txt'):
            W = np.genfromtxt(file, delimiter=",")
            D = degmatrix(W)
            gLap = graphLaplacian(W, D)
            PHY, LANDA = eigen(gLap)
            PHY_ses, LANDA_ses = eigen_reduce(PHY, LANDA)
            phy9, landa9 = eigen_aisle(PHY_ses, LANDA_ses)
            phy9_list.append(phy9)
            landa9_list.append(landa9)
    phy9_mean = np.mean(phy9_list, axis=0)
    landa9_mean = np.array([np.mean(landa9_list)])
    np.savetxt('phy9_mean.txt', phy9_mean, delimiter=',')
    np.savetxt('landa9_mean.txt', landa9_mean)


