# -*- coding: utf-8 -*-
import json
import re

def listIter(listFromDict):
    for i in listFromDict:
        if isinstance(i, list):
            listIter(i)
        elif isinstance(i, dict):
            dictIter(i)

def dictIter(d):

    for k, v in d.items():
        if isinstance(v, list):
            listIter(v)
        if isinstance(v, dict):
            dictIter(v)
        else:
            if re.match(r"CIM.*Color", str(v)):
                print("{0} : {1}".format(k, v))

with open('MIIP_Mapa_Emisji_UMWM_SR.mapx', encoding='utf-8') as data_file:
    data = json.load(data_file)

dictIter(data)

