import csv
import json


def read_json(filename):
    with open(filename, "rb") as f:
        data = json.load(f)

    return data


def read_csv(filename):
    f = open(filename, 'r', encoding='utf-8')
    rdr = csv.reader(f)
    next(rdr)

    return rdr


def make_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)