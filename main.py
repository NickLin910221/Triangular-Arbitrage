# -*- coding: utf-8 -*-
import datetime
import json
import threading
import time

import Analysize as func

global a, b, c
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

for i in range(len(pairs)):
    globals()[i] = threading.Thread(target = func.main(class_name=i, a = a[i], b = b[i], c = c[i])).start()
    
while True:
    time.sleep(1)
    print("Now time : " + datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
