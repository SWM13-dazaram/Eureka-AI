import csv
import json


def read_json(filename: str) -> dict:
    with open(filename, "rb") as f:
        data = json.load(f)

    return data


def read_csv(filename: str):
    f = open(filename, 'r', encoding='utf-8')
    rdr = csv.reader(f)
    next(rdr)

    return rdr


def make_json(filename: str, data) -> None:
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)
