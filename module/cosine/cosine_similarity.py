import numpy as np
from FlavorGraph.module.util import *


def sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def generate_ing_data(data):
    ing_dict = {}
    for line in data:
        num, name, _, node_type, is_hub = line
        ing_dict[num] = [name, node_type, is_hub]

    return ing_dict


def calc_cos_sim(data):
    veclst_len = max(list(map(lambda x: int(x), data.keys()))) + 1
    cos_sim = [0 for _ in range(veclst_len)]
    for (k, v) in data.items():
        if k == target:
            continue
        cos_sim[int(k)] = sim(v, t)

    return cos_sim


if __name__ == "__main__":
    vec_data = read_json("../viewPickle/csp_layer.json")
    node_data = read_csv("../../input/example/nodes_191120.csv")
    ing_data = generate_ing_data(node_data)

    target = input("select ingredient ID : ")
    t = vec_data[str(target)]

    cos_sim = calc_cos_sim(vec_data)

    print("=======================================================")
    print("Selected Ingredient")
    print(f"ID : {target}")
    print(f"Name : {ing_data[str(target)][0]}")
    print(f"Type : {ing_data[str(target)][1]}")
    print("=======================================================")

    print()

    print("=======================================================")
    print("Similar Ingredient")
    print(f"ID : {str(np.argmax(cos_sim))}")
    print(f"Name : {ing_data[str(np.argmax(cos_sim))][0]}")
    print(f"Type : {ing_data[str(np.argmax(cos_sim))][1]}")
    print()
    print(f"Similarity : {str(np.max(cos_sim))}")
    print("=======================================================")
