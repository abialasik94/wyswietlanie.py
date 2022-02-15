from treelib import Node, Tree
import json

with open('ABNowaKompozycjaBDOT10k.mapx', encoding='utf-8') as data_file:
    dict_ = json.load(data_file)

added = set()
tree = Tree()
while dict_:

    for key, value in dict_.items():
        if value['parent'] in added:
            tree.create_node(key, key, parent=value['parent'])
            added.add(key)
            dict_.pop(key)
            break
        elif value['parent'] is None:
            tree.create_node(key, key)
            added.add(key)
            dict_.pop(key)
            break

tree.show()

