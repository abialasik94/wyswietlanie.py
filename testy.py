# -*- coding: utf-8 -*-
import json
import re

path = []
def listIter(listFromDict):
    for num, i in enumerate(listFromDict):
        if isinstance(i, list):
            global path
            path.append(num)
            listIter(i)
            path = path[:-1]
        elif isinstance(i, dict):
            path.append(num)
            dictIter(i)
            path = path[:-1]

def dictIter(d):
    for k, v in d.items():
        if isinstance(v, list):
            global path
            path.append(k)
            listIter(v)
            path = path[:-1]
        if isinstance(v, dict):
            path.append(k)
            dictIter(v)
            path = path[:-1]
        else:
            if re.match(r"CIM.*Color", str(v)):
                a=0
                #print("{0} : {1}".format(k, v))
                print("Ścieżka: " + str(path))


with open('MIIP_Mapa_Emisji_UMWM_SR.mapx', encoding='utf-8') as data_file:
    data = json.load(data_file)

dictIter(data)

a=0