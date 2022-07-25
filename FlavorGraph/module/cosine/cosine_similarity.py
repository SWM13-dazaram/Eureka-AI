import json
import numpy as np
import csv

layer = "../viewPickle/csp_layer.json"

with open(layer, "rb") as f:
    data = json.load(f)
veclst_len = max(list(map(lambda x: int(x), data.keys()))) + 1
vec_lst = [[] for _ in range(veclst_len)]
nodes = "../../input/nodes_191120.csv"

f = open(nodes, 'r', encoding='utf-8')
rdr = csv.reader(f)
next(rdr)

ing_lst = {}
for line in rdr:
    num, name, _, node_type, is_hub = line
    ing_lst[num] = [name, node_type, is_hub]

target = input("select ingredient ID : ")
t = data[str(target)]

cos_sim = [0 for _ in range(veclst_len)]


def sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


for (k, v) in data.items():
    if k == target:
        continue
    cos_sim[int(k)] = sim(v, t)

print("similar ingredient")
print("ID : " + str(np.argmax(cos_sim)))
print("similarity : " + str(np.max(cos_sim)))
print("name : " + ing_lst[str(np.argmax(cos_sim))][0])
print("type : " + ing_lst[str(np.argmax(cos_sim))][1])
