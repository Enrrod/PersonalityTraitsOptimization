#-*- coding: utf-8 -*-

import networkx as nx
import numpy as np
import xlsxwriter as xls
from sklearn.metrics import mean_squared_error as mse
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
    del_ind = np.where(LANDA <= 0.01)[0]
    del_ind = del_ind[0:(len(del_ind) - 1)]
    LANDA = np.delete(LANDA, del_ind)
    PHY = np.delete(PHY, del_ind, 1)
    PHY = PHY.T # Transponemos para que los autovectores se almacenen en filas
    LANDA_ses = LANDA[0:41]
    PHY_ses = PHY[0:41]
    return PHY_ses, LANDA_ses


if __name__=="__main__":
    directory = '/home/enrique/Proyectos/PersonalityTraitsOptimization/Data/DS00071/Graphs'
    refValues = np.genfromtxt('/home/enrique/Proyectos/PersonalityTraitsOptimization/Data/DS00071/meanEigvec.txt', delimiter=',')
    subjects = os.listdir(directory)
    workbookName = '/home/enrique/Proyectos/PersonalityTraitsOptimization/Data/DS00071/eigenVectorsMSE.xlsx'
    workbook = xls.Workbook(workbookName)
    worksheet = workbook.add_worksheet()
    row = 0
    worksheet.write(row, 0, 'ID')
    for i in range(41):
        worksheet.write(row, i + 1 , 'MSE_' + str(i))
    for i in range(41):
        worksheet.write(row, i + 42, 'normMSE_' + str(i))
    row = row + 1
    for i in range(len(subjects)):
        if subjects[i].endswith('.gpickle'):
            ID = subjects[i][4:13]
            results = []
            graph = directory + '/' + subjects[i]
            g = readgraph(graph)
            W = wmatrix(g)
            D = degmatrix(W)
            gL = graphLaplacian(W, D)
            PHY, LANDA = eigen(gL)
            PHY_ses, LANDA_ses = eigen_reduce(PHY, LANDA)
            for j in range(len(PHY_ses)):
                results.append(mse(refValues[j], PHY_ses[j]))
            normResults = results / np.max(results)
            worksheet.write(row, 0, ID)
            for j in range(len(results)):
                worksheet.write(row, j + 1, results[j])
            for j in range(len(normResults)):
                worksheet.write(row, j + 1 + len(results), normResults[j])
            row = row + 1
    workbook.close()



