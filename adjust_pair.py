# -*- coding: utf-8 -*-
from datetime import date
import json
import pandas as pd

def func():
    file_name = "pair.json"
    with open(file_name, "r") as f:
        data = json.load(f)

    pairs = []

    for i in range(len(data)):
        pairs.append({"a" : data[i]['a'], "b" : data[i]['b'], "c" : data[i]['c']})

    a, b, c = [], [], []

    for i in range(len(pairs)):
        a.append(pairs[i]['a'])
        b.append(pairs[i]['b'])
        c.append(pairs[i]['c'])

    data = pd.DataFrame({ "a": a ,
                        "b" : b , 
                        "c" : c }, 
                        columns=["a","b","c"] )

    print(data)
    print("Select want to add pairs or delete pairs")
    print("1) ADD")
    print("2) DELETE")

    select = input()
    if select == '1':
        a = input("input a\n")
        b = input("input b\n")
        c = input("input c\n")
        pairs.append({"a" : a, "b" : b, "c" : c})

    if select == '2':
        index = input("input the pairs want to delete (index) :")
        del pairs[int(index)]

    with open("pair.json", 'w') as f:
        json.dump(pairs, f)

if __name__ == '__main__':
    func()
