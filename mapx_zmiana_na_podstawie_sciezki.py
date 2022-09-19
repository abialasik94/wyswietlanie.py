# -*- coding: utf-8 -*-

#Skrypt wczytuje z mapxa wartości kolorów dla podanych parametrów, zmienia je i zapisuje do nowego mapxa

import json
import re
from functools import reduce  # forward compatibility for Python 3
import operator

path = []
def zmienKolory(data, **kwargs):
    if not all(elem in kwargs.keys() for elem in ['pathParameters', 'colorModel', 'colorValues']):
        print('Nie został wprowadzony co najmniej 1 parametr z pathParameters, colorModel, colorValues')
    else:
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
                    path.append(k)
                    listIter(v, **kwargs)
                    path = path[:-1]
                if isinstance(v, dict):
                    path.append(k)
                    dictIter(v, **kwargs)
                    path = path[:-1]
                else:
                    if re.match(kwargs['colorModel'], str(v)) and all(elem in path for elem in kwargs['pathParameters']):
                        pathWithColorsToChange = path + ['values']
                        setInDict(data, pathWithColorsToChange, kwargs['colorValues'])
                        print('Zmieniono kolor dla ścieżki ' + str(path))

        dictIter(data, **kwargs)

nazwaPliku = "ABNowaKompozycjaBDOT10k.mapx"
with open(nazwaPliku, encoding='utf-8') as data_file:
    data = json.load(data_file)

zmienKolory(data, pathParameters = ['layerDefinitions', 'renderer', 'symbol', 421],
         colorModel = r"CIM.*Color", colorValues = [212, 515, 505, 0])

nowaNazwa = nazwaPliku[:-5] + '_zmieniony.mapx'
changedFile = open(nowaNazwa, "w", encoding='utf-8')
json.dump(data, changedFile, indent = 6)
changedFile.close()

