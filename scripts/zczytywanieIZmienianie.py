# -*- coding: utf-8 -*-
import simplejson as json
import re
from functools import reduce  # forward compatibility for Python 3
import operator
import csv
import os

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
                if re.match(kwargs['colorModel'], str(v)) and 'values' in isValue:
                    pathWithColorsToChange = path + ['values']
                    pathWithModelToChange = path + ['type']
                    actualColors = getFromDict(data, pathWithColorsToChange)
                    colorModel = getFromDict(data, path + ['type'])
                    try:
                        layerName = str(getFromDict(data, path[:2] + ['name']))
                    except:
                        layerName = ""
                    if layerName != "":
                        change = kwargs['actualCsvRow']
                        try:
                            if (getFromDict(data, pathWithModelToChange)) != "CIMCMYKColor":
                                colorsToChange = [int(change[7]),int(change[8]),int(change[9]),int(change[10])]
                            else:
                                colorsToChange = [int(change[7]), int(change[8]), int(change[9]), int(change[10]), int(change[11])]
                        except:
                            colorsToChange = 0
                        if  str.strip(change[6]) == colorModel and actualColors == colorsToChange and layerName == str.strip(change[5]) and "_".join(pathWithoutListIndexes) == str.strip(change[12]):
                            print(f"Zmieniono kolor dla wiersza nr {kwargs['rowIndex']+1}")
                            setInDict(data, pathWithColorsToChange, [int(change[0]),int(change[1]),int(change[2]),int(change[3])])
                            setInDict(data, pathWithModelToChange, "CIMRGBColor")
    dictIter(data, **kwargs)

nazwaPliku = "NowaKompozycjaBDOT10kV3NightVision.mapx"
sciezka_input = os.path.realpath('..') + os.sep + "input_data" + os.sep + nazwaPliku
with open(sciezka_input, encoding='utf-8') as data_file:
    data = json.load(data_file)

sciezka_output = os.path.realpath('..') + os.sep + "output_data" + os.sep
file_object = open(sciezka_output + "NowaKompozycjaBDOT10kV3NightVision.csv", "r", encoding='utf-8')
csv = csv.reader(file_object, delimiter = ";")
for i, change in enumerate(csv):
    try:
        change[0] = float(change[0])
        change[1] = float(change[1])
        change[2] = float(change[2])
        change[3] = float(change[3])
    except:
        #print("Nie podano liczb dla wiersza nr " + str(i))
        pass
    if i > 1 and isinstance(change[0], (float)) and isinstance(change[1], (float)) and isinstance(change[2], (float)):
        mapxChange(data, colorModel = r"CIM.*Color", actualCsvRow = change, rowIndex = i)
    #else:
        #print("Kolor dla wiersza nr " + str(i) + " nie został zmieniony")

nowaNazwa = nazwaPliku[:-5] + '_zmieniony.mapx'
changedFile = open(sciezka_output + nowaNazwa, "w", encoding='utf-8')
json.dump(data, changedFile, indent = 6, ensure_ascii=False, encoding="utf-8")
changedFile.close()