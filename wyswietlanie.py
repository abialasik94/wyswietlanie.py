# -*- coding: utf-8 -*-
import json
import re
from functools import reduce  # forward compatibility for Python 3
import operator

path = []
output = "Do wpisania| wartości| nowego koloru|(1.-4. obowiązkowe|, 5. opcjonalna)|Nazwa warstwy|Model koloru|Wartości| starego| koloru (1.-4.| obowiązkowe,| 5. opcjonalna)|Ścieżka po węzłach| \n"
pathWithoutListIndexes = []
pathsWithoutListIndexes = []
def mapxPrint(data, **kwargs):
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
                if re.match(kwargs['colorModel'], str(v)) and 'values' in isValue :
                    #print(pathWithoutListIndexes)
                    #print(pathsWithoutListIndexes)
                    pathWithColorsToChange = path + ['values']
                    #setInDict(data, pathWithColorsToChange, kwargs['colorValues'])
                    actualColors = getFromDict(data, pathWithColorsToChange)
                    colorModel = getFromDict(data, path + ['type'])
                    try:
                        layerName = "|||||" + str(getFromDict(data, path[:2] + ['name'])) + " | "
                    except:
                        layerName = "|||||"
                    pathWithoutCModelAColors = pathWithoutListIndexes + ['values'] + [str(colorModel)] + [str(actualColors)] + [layerName]
                    if pathWithoutCModelAColors not in pathsWithoutListIndexes:
                        pathsWithoutListIndexes.append(pathWithoutCModelAColors)
                        try:
                            fiftcolor = str(actualColors[4])
                        except:
                            fiftcolor = ""
                        global output
                        output += layerName + str(colorModel) + "|" + str(actualColors[0]) + "|" + str(actualColors[1]) + "|" + str(actualColors[2]) + "|" + str(actualColors[3]) + "|" + fiftcolor + "|" + "_".join(pathWithoutListIndexes) + "|".join(pathWithoutListIndexes)  + "\n"

    dictIter(data, **kwargs)
    global output
    with open("ABNowaKompozycjaBDOT10k_ścieżki_kolory2.csv", "w", encoding='utf-8') as text_file:
        text_file.write(str(output))

nazwaPliku = "ABNowaKompozycjaBDOT10k.mapx"
with open(nazwaPliku, encoding='utf-8') as data_file:
    data = json.load(data_file)

mapxPrint(data, colorModel = r"CIM.*Color")
