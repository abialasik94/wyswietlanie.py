# -*- coding: utf-8 -*-
import json
import re
from functools import reduce  # forward compatibility for Python 3
import operator
import csv

path = []
output = ""
pathWithoutListIndexes = []
pathsWithoutListIndexes = []
def mapxChange(data, **kwargs):
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
                if re.match(kwargs['colorModel'], str(v)) and 'values' in isValue and kwargs['actualCsvRow']:
                    pathWithColorsToChange = path + ['values']
                    actualColors = getFromDict(data, pathWithColorsToChange)
                    colorModel = getFromDict(data, path + ['type'])
                    try:
                        layerName = str(getFromDict(data, path[:2] + ['name']))
                    except:
                        layerName = ""
                    if layerName != "":
                        #print(layerName)
                        change = kwargs['actualCsvRow']
                        #pathWithoutCModelAColors = pathWithoutListIndexes + ['values'] + [str(colorModel)] + [str(actualColors)] + [layerName]
                        try:
                            colorsToChange = [int(change[9]),int(change[10]),int(change[11]),int(change[12])]
                        except:
                            colorsToChange = 0
                        #pathOfColorToChange = ''
                        #for pathElement in change[14:]:
                        #    pathOfColorToChange += str.strip(pathElement)
                        if  len(change)>14 and str.strip(change[7]) == colorModel and actualColors == colorsToChange and layerName == str.strip(change[5]) and "_".join(pathWithoutListIndexes) == str.strip(change[14]):
                            print("zmieniam")
                            setInDict(data, pathWithColorsToChange, [int(change[0]),int(change[1]),int(change[2]),int(change[3])])
    dictIter(data, **kwargs)

nazwaPliku = "ABNowaKompozycjaBDOT10k.mapx"
with open(nazwaPliku, encoding='utf-8') as data_file:
    data = json.load(data_file)

file_object = open("ABNowaKompozycjaBDOT10k_ścieżki_kolory2.csv", "r", encoding='utf-8')
csv = csv.reader(file_object, delimiter = ";")
for change in csv:
    mapxChange(data, colorModel = r"CIM.*Color", actualCsvRow = change)

nowaNazwa = nazwaPliku[:-5] + '_zmieniony.mapx'
changedFile = open(nowaNazwa, "w", encoding='utf-8')
json.dump(data, changedFile, indent = 6)
changedFile.close()