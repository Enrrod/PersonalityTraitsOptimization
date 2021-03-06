# -*- coding: utf-8 -*-

import os
import random
import numpy as np
import matplotlib.pyplot as plt
from deap import creator, base, tools, algorithms
from sklearn.metrics import mean_squared_error as mse
from time import time



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


def eigen_aisle(PHY_ses):
    # Aislamos el 9º autovector
    phy9 = np.empty(0)
    for i in range(PHY_ses.shape[0]):
        phy9 = np.hstack((phy9, PHY_ses[i, 7].real))
    return phy9


def fit_function(individual, phy_mean):
    degmat = degmatrix(individual)
    lmat = graphLaplacian(individual, degmat)
    (phys, landas) = eigen(lmat)
    phys_ses, landa_ses = eigen_reduce(phys, landas)
    phy9 = eigen_aisle(phys_ses)
    # Aplicamos el MSE (Error Cuadrático Medio) como función a minimizar
    error_phy = mse(phy_mean, phy9)
    return error_phy,


def matMutFloat(individual, rowindpb, elemindpb, mask):
    size = len(individual)
    for i in range(size):
        rowindMut = random.random()
        if rowindMut < rowindpb:
            for j in range(size):
                elemindMut = random.random()
                if elemindMut < elemindpb:
                    attrMut = random.random()
                    individual[i][j], individual[j][i] = attrMut, attrMut
    np.place(individual, mask, 0)
    return individual,


def patchCx(ind1, ind2):
    n = len(ind1)
    tam = np.random.randint(1, (n / 2) + 1)
    patch1 = ind1[0:tam,(n-tam):n].copy()
    patch2 = ind2[0:tam, (n - tam):n].copy()
    ind1[0:tam, (n - tam):n], ind1[(n - tam):n, 0:tam] = patch2, patch2.T
    ind2[0:tam, (n - tam):n], ind2[(n - tam):n, 0:tam] = patch1, patch1.T
    del patch1
    del patch2
    return ind1, ind2,


def obtainMask(file):
    mask = np.genfromtxt(file, delimiter=",")
    mask = np.where(mask > 0, 0, 1)
    return mask


def graphInd(icls, dim, mask):
    indGenerator = np.random.rand(dim, dim)
    graphInd = (indGenerator + indGenerator.T) / 2
    np.place(graphInd, mask, 0)
    return icls(graphInd)


def main(file,refFile):
    mask = obtainMask(file)
    phy_mean = np.genfromtxt(refFile, delimiter=',')

    creator.create('FitnessMin', base.Fitness, weights=(-1.0,))
    creator.create('Individual', np.ndarray, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    toolbox.register('individual', graphInd, creator.Individual, dim=70, mask=mask)
    toolbox.register('population', tools.initRepeat, list, toolbox.individual)
    toolbox.register('evaluate', fit_function,phy_mean=phy_mean)
    toolbox.register('mate', patchCx)
    toolbox.register('mutate', matMutFloat, rowindpb=0.1, elemindpb=0.1, mask=mask)
    toolbox.register('select', tools.selTournament, tournsize=3)

    mutpb = 0.1
    cxpb = 0.6
    stats = tools.Statistics(key=lambda ind: ind.fitness.values)
    stats.register('min', np.min, axis=0)
    stats.register('avg', np.mean, axis=0)

    logbook = tools.Logbook()
    population = toolbox.population(100)
    NGEN = 15000
    print("Starting optimization with " + str(NGEN) + " generations")
    for gen in range(NGEN):
        offspring = algorithms.varAnd(population, toolbox, cxpb, mutpb)
        fits = toolbox.map(toolbox.evaluate, offspring)
        for fit, ind in zip(fits, offspring):
            ind.fitness.values = fit
        population = toolbox.select(offspring, k=len(population))
        top = tools.selBest(population, k=1)
        record = stats.compile(population)
        logbook.record(gen=gen, **record)
        print("Generation (" + str(gen + 1) + "/" + str(NGEN) + ") completed")

    return logbook, top, phy_mean


if __name__ == "__main__":
    directory = '/home/enrique/Proyectos/PersonalityTraitsOptimization/Data/DS00071/WmatrixGrouped/lowOpenness'
    subjects = os.listdir(directory)
    for i in range(len(subjects)):
        name = subjects[i]
        path = directory + '/' + name + '/'
        file = path + 'Wmat_' + name + '.txt'
        refFile = '/home/enrique/Proyectos/PersonalityTraitsOptimization/Data/DS00071/WmatrixGrouped/highOpenness/phy9_mean.txt'
        logbook, top, phy_mean = main(file, refFile)
        generation = logbook.select('gen')
        fitness_min = logbook.select('min')
        fitness_avg = logbook.select('avg')
        top_ind = top[0]

        w_pat = np.genfromtxt(file, delimiter=",")
        wdiff = top_ind - w_pat
        init_error = fit_function(w_pat, phy_mean)
        init_error = init_error[0]
        fitness_rel = (fitness_min / init_error) * 100
        fitness_avg_rel = (fitness_avg / init_error) * 100

        plt.figure()
        line1 = plt.plot(generation, fitness_rel, "b-", label="Relative fitness")
        line2 = plt.plot(generation, fitness_avg_rel, "r-", label="Relative average Fitness", alpha=0.5)
        plt.axis([0, len(generation), -10, 120])
        plt.xlabel("Generation")
        plt.ylabel("Fitness")
        lines1 = [line1[0], line2[0]]
        labs1 = [line1[0].get_label(), line2[0].get_label()]
        plt.legend(lines1, labs1, loc="upper right")
        plt.title(name + " | cxpb= 0.6 mutpb= 0.1")

        plotPath = path + 'optimizationResults/optPlot.pdf'
        fitAvgPath = path + 'optimizationResults/fitAvg.csv'
        fitMinPath = path + 'optimizationResults/fitMin.csv'
        fitAvgRelPath = path + 'optimizationResults/fitAvgRel.csv'
        fitMinRelPath = path + 'optimizationResults/fitMinRel.csv'
        topIndPath = path + 'optimizationResults/topInd.csv'
        WdiffPath = path + 'optimizationResults/Wdiff.csv'

        np.savetxt(fitAvgPath, fitness_avg, delimiter=',')
        np.savetxt(fitMinPath, fitness_min, delimiter=',')
        np.savetxt(fitAvgRelPath, fitness_avg_rel, delimiter=',')
        np.savetxt(fitMinRelPath, fitness_rel, delimiter=',')
        np.savetxt(topIndPath, top_ind, delimiter=',')
        np.savetxt(WdiffPath, wdiff, delimiter=',')
        plt.savefig(plotPath)




