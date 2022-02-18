# -*- coding: utf-8 -*-
import json
import re
from functools import reduce  # forward compatibility for Python 3
import operator

path = []
output = ""
pathWithoutListIndexes = []
pathsWithoutListIndexes = []
def zmienKolory(data, **kwargs):
    #if not all(elem in kwargs.keys() for elem in ['pathParameters', 'colorModel', 'colorValues']):
    #    print('Nie został wprowadzony co najmniej 1 parametr z pathParameters, colorModel, colorValues')
    #else:z
    def getFromDict(dataDict, mapList):
        return reduce(operator.getitem, mapList, dataDict)
    def setInDict(dataDict, mapList, value):
        changedValue = getFromDict(dataDict, mapList[:-1])[mapList[-1]] = value
        return changedValue
    def listIter(listFromDict, **kwargs):
        for num, i in enumerate(listFromDict):
            if isinstance(i, list):
                global path
                path.append(num)
                listIter(i, **kwargs)
                path = path[:-1]
            elif isinstance(i, dict):
                path.append(num)
                dictIter(i, **kwargs)
                path = path[:-1]

    def dictIter(d, **kwargs ):
        for k, v in d.items():
            if isinstance(v, list):
                global path
                global pathWithoutListIndexes
                path.append(k)
                pathWithoutListIndexes.append(k)
                listIter(v, **kwargs)
                path = path[:-1]
                pathWithoutListIndexes = pathWithoutListIndexes[:-1]
            if isinstance(v, dict):
                path.append(k)
                pathWithoutListIndexes.append(k)
                dictIter(v, **kwargs)
                path = path[:-1]
                pathWithoutListIndexes = pathWithoutListIndexes[:-1]
            else:
                global pathsWithoutListIndexes
                isValue = getFromDict(data, path)
                if re.match(kwargs['colorModel'], str(v)) and 'values' in isValue:
                    #print(pathWithoutListIndexes)
                    #print(pathsWithoutListIndexes)
                    pathWithColorsToChange = path + ['values']
                    #setInDict(data, pathWithColorsToChange, kwargs['colorValues'])
                    actualColors = getFromDict(data, pathWithColorsToChange)
                    colorModel = getFromDict(data, path + ['type'])
                    pathWithoutCModelAColors = pathWithoutListIndexes + ['values'] + [str(colorModel)] + [str(actualColors)]
                    if pathWithoutCModelAColors not in pathsWithoutListIndexes:
                        pathsWithoutListIndexes.append(pathWithoutCModelAColors)
                        global output
                        output +="Ścieżka(nazwy otwartych węzłów): " + str(path) + " | Model barw: " + str(colorModel) + " | Aktualny kolor: " + str(actualColors) + "\n"
    dictIter(data, **kwargs)
    global pathsWithoutListIndexes
    with open("ABNowaKompozycjaBDOT10k_ścieżki_kolory.txt", "w") as text_file:
        text_file.write(str(pathsWithoutListIndexes))

nazwaPliku = "ABNowaKompozycjaBDOT10k.mapx"
with open(nazwaPliku, encoding='utf-8') as data_file:
    data = json.load(data_file)

zmienKolory(data, pathParameters = ['layerDefinitions', 'renderer', 'symbol', 421],
         colorModel = r"CIM.*Color", colorValues = [212, 505, 505, 0])

# nowaNazwa = nazwaPliku[:-5] + '_zmieniony.mapx'
# changedFile = open(nowaNazwa, "w", encoding='utf-8')
# json.dump(data, changedFile, indent = 6)
# changedFile.close()

#Potrzebne uzupełnienia:
#1. wyprintować ścieżki ze znalezionymi kolorami