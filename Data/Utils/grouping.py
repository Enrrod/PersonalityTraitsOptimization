#-*- coding: utf-8 -*-

from xlrd import open_workbook
from collections import OrderedDict
import unicodedata
import numpy as np

def dataRead(file):
    '''This function reads an xls file and creates a dictionary containing the variable names and the
    data stored in each one.
    INPUT: Xls file route (string).
    OUTPUT: Excel data stored in a dictionary (dict).'''
    book = open_workbook(file)
    sheet = book.sheet_by_index(0)
    cols = sheet.ncols
    data = OrderedDict()
    headers = sheet.row(0)
    for h in range(len(headers)):
        if isinstance(headers[h].value, unicode):
            data[unicodedata.normalize('NFKD', headers[h].value).encode('ascii','ignore')] = []
    for column in range(cols):
        col = sheet.col(column)
        key = col[0].value
        if isinstance(key, unicode):
            key = unicodedata.normalize('NFKD', key).encode('ascii', 'ignore')
        for i in range(1,len(col)):
            value = col[i].value
            if isinstance(value, unicode):
                value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
            data[key].append(value)
    return data

if __name__=="__main__":
    file = '/home/enrique/Escritorio/Templeton114.xlsx'
    data = dataRead(file)

    opens = data['Openness']
    meanOpen = np.mean(opens)
    maxOpen = np.max(opens)
    minOpen = np.min(opens)

    highThreshOpen = ((maxOpen - meanOpen) / 2) + meanOpen
    lowThreshOpen = ((meanOpen - minOpen) / 2) + minOpen



    cons = data['Conscientiousness']
    cons = filter(None, cons)
    meanCons = np.mean(cons)
    maxCons= np.max(cons)
    minCons= np.min(cons)

    highThreshCons = ((maxCons - meanCons) / 2) + meanCons
    lowThreshCons = ((meanCons - minCons) / 2) + minCons

    highOpen = []
    lowOpen = []
    highCons = []
    lowCons = []

    for i in range(len(opens)):
        name = data['URSI'][i]
        if data['Openness'][i] > highThreshOpen:
            highOpen.append(name)
        elif data['Openness'][i] < lowThreshOpen:
            lowOpen.append(name)
        if data['Conscientiousness'][i] > highThreshCons:
            highCons.append(name)
        elif data['Conscientiousness'][i] < lowThreshCons:
            lowCons.append(name)

    route = '/home/enrique/Proyectos/PersonalityTraitsOptimization/Graphs'

    hOpenRoute = '/home/enrique/Proyectos/PersonalityTraitsOptimization/Graphs' + '/highOpenness.txt'
    lOpenRoute = '/home/enrique/Proyectos/PersonalityTraitsOptimization/Graphs' + '/lowOpenness.txt'
    hConsRoute = '/home/enrique/Proyectos/PersonalityTraitsOptimization/Graphs' + '/highConscientiousness.txt'
    lConsRoute = '/home/enrique/Proyectos/PersonalityTraitsOptimization/Graphs' + '/lowConscientiousness.txt'

    hOpen = open(hOpenRoute, 'a+')
    lOpen = open(lOpenRoute, 'a+')
    hCons = open(hConsRoute, 'a+')
    lCons = open(lConsRoute, 'a+')

    for i in range(len(highOpen)):
        hOpen.write(highOpen[i] + '\n')
    for i in range(len(lowOpen)):
        lOpen.write(lowOpen[i] + '\n')
    for i in range(len(highCons)):
        hCons.write(highCons[i] + '\n')
    for i in range(len(lowCons)):
        lCons.write(lowCons[i] + '\n')

    hOpen.close()
    lOpen.close()
    hCons.close()
    lCons.close()