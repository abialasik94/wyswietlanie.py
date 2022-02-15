# -*- coding: utf-8 -*-
import json
#import re

nazwaPliku = "ABNowaKompozycjaBDOT10k.mapx"

def jsonExtract(jsonData):
    for i, j in jsonData.items(): #iteracja bez listy
        if i == "mapDefinition":
            for k, l in j.items():
                if k == "elevationSurfaces":
                    a=0
        if i =="layerDefinitions": #iteracja z listą
            for a in range(len(j)):
                for m, n in j[a].items():
                    if m == "labelClasses": #iteracja z listą
                        for b in range(len(n)):
                            for o, p in n[b].items():
                                if o == "textSymbol":
                                    for r, s in p["symbol"].items():
                                        if r == "haloSymbol":
                                            for t in range(len(s["symbolLayers"])):
                                                #print(jsonData[i][a][m][b][o]["symbol"][r]["symbolLayers"])
                                                if "color" in s["symbolLayers"][t].keys() and s["symbolLayers"][t]["color"]["type"] == "CIMRGBColor":
                                                    colorValues = jsonData[i][a][m][b][o]["symbol"][r]["symbolLayers"][t]["color"]["values"]
                                                    if jsonData[i][a][m][b][o]["symbol"][r]["symbolLayers"][t]["color"]["values"] == [255, 255, 255, 100]:
                                                        jsonData[i][a][m][b][o]["symbol"][r]["symbolLayers"][t]["color"]["values"] = [157, 158, 159, 160]
                                                        print(jsonData[i][a][m][b][o]["symbol"][r]["symbolLayers"][t]["color"])
    return jsonData

with open('ABNowaKompozycjaBDOT10k.mapx', encoding='utf-8') as data_file:
    data = json.load(data_file)

jsonDataChanged = jsonExtract(data)

nowaNazwa = nazwaPliku[:-5] + '_zmieniony.mapx'
changedFile = open(nowaNazwa, "w", encoding='utf-8')
json.dump(jsonDataChanged, changedFile, indent = 6)
changedFile.close()