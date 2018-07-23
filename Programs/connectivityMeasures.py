#-*- coding: utf-8 -*-

# -----IMPORTACIÓN DE LOS MÓDULOS NECESARIOS----------------------------------------------------------------------------

import networkx as nx
import numpy as np
import xlsxwriter as xls
import os

# -----DEFINICIÓN DE LAS FUNCIONES NECESARIAS---------------------------------------------------------------------------

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

# -----EJECUCIÓN---------------------------------------------------------------------------
if __name__=="__main__":
    path = '/home/enrique/Proyectos/PersonalityTraitsOptimization/Data/DS00071/Graphs'
    files = os.listdir(path)
    workbookName = '/home/enrique/Proyectos/PersonalityTraitsOptimization/Data/DS00071/connectMeasures.xlsx'
    workbook = xls.Workbook(workbookName)
    worksheet = workbook.add_worksheet()
    row = 0
    headers = ['ID', 'nEdges', 'meanWeight', 'stdWeight', 'avgShPath', 'avgClust', 'tree', 'leafNum', 'meanEcc',
               'maxBC', 'TH']
    for i in range(len(headers)):
        worksheet.write(row, i, headers[i])
    row = row + 1
    for k in range(len(files)):
        if files[k].endswith('.gpickle'):
            ID = files[k][4:13]
            graph = '/home/enrique/Proyectos/PersonalityTraitsOptimization/Data/DS00071/Graphs/' + files[k]
            G = readgraph(graph)
            W = wmatrix(G)
            D = degmatrix(W)
            T = nx.minimum_spanning_tree(G,weight='weight')

            weights = W[W>0]
            nEdges = len(weights) / 2
            meanWeight = np.mean(weights)
            stdWeight = np.std(weights)
            try:
                avgPath = nx.average_shortest_path_length(G,weight='weight')    # Longitud media de camino más corto
            except (nx.NetworkXError):
                avgPath = 'Not connected'
            avgClust = nx.average_clustering(G,weight='weight')   # Coeficiente de clustering medio
            if nx.is_tree(T):
                tree = 'True'   # Is tree
                nodes = list(T.nodes())
                m = len(nodes) - 1
                nLeaves = 0
                for i in range(len(nodes)):
                    if T.degree(nodes[i]) == 1:
                        nLeaves = nLeaves + 1
                leafNumber = float(nLeaves) / m    # Leaf number
                meanEcc = np.mean(list(nx.eccentricity(T).values()))    # Mean eccentricity of the tree
                bc = nx.betweenness_centrality(T, weight='weight')
                bcVal = list(bc.values())
                bcMax = np.amax(bcVal)  # Maximum betweenness centrality
                TH = nLeaves / (2 *  (len(nodes) - 1) * bcMax)    # Tree hierarchy
            else:
                tree = 'False'
                leafNumber = 'Not tree'
                meanEcc = 'Not tree'
                bcMax = 'Not tree'
                TH = 'Not tree'
            results = [ID, nEdges, meanWeight, stdWeight, avgPath, avgClust, tree, leafNumber, meanEcc, bcMax, TH]
            for i in range(len(results)):
                worksheet.write(row, i, results[i])
            row = row + 1
    workbook.close()
