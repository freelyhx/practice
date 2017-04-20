#!/usr/bin/python
# -*- coding:UTF-8 -*-

import json

from treelib import Tree

def list_all_dict(dict_a, data):
    if isinstance(dict_a,dict):
        for x in range(len(dict_a)):
            temp_key = dict_a.keys()[x]
            temp_value = dict_a[temp_key]
            tree.create_node(temp_key, temp_key, parent=data)
            list_all_dict(temp_value, temp_key)
    else:
        tree.create_node(dict_a, dict_a, parent=data)

if __name__ == '__main__':
    f = open("p2.json")
    d = json.load(f)
    tree = Tree()
    tree.create_node("root", "root")
    list_all_dict(d, "root")
    
    print "\nThe json file is: %s \n" % d
    tree.show()
    
    f.close()