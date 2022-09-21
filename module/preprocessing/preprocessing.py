from typing import List, Any

from FlavorGraph.module.util import *
import os
from tqdm import tqdm

mapping = read_json("mapping.json")
not_ing = read_json("not_ingredient.json")


def ing_validation(ingredient: dict) -> bool:
    for ban in not_ing:
        if ban == ingredient['name']:
            return True

    if "생략가능" in ingredient['name']:
        return True
    if "생략 가능" in ingredient['name']:
        return True
    if "생략" in ingredient['name']:
        return True
    if "(선택)" in ingredient['name']:
        return True

    if "생략가능" in ingredient['quantity']:
        return True
    if "생략 가능" in ingredient['quantity']:
        return True
    if "생략" in ingredient['quantity']:
        return True
    return False


def seq_validation(seq: str) -> str:
    seq = seq.replace("\n", "")
    return seq.strip()


def recipe_validation(recipe_data: dict) -> dict:
    ret = {}

    for id, recipe in tqdm(recipe_data.items()):
        ings = []
        for ing in recipe['ingredients']:
            if ing_validation(ing):
                continue
            ings.append({'name': ing_name_validation(ing['name']), 'quantity': ing['quantity']})
        seqs = []
        for seq in recipe['sequences']:
            seqs.append({'sequence': seq['sequence'], 'content': seq_validation(seq['content'])})
        ret[id] = recipe
        ret[id]['ingredients'] = ings

    make_json("result/valid_recipe.json", ret)
    return ret


def ing_name_validation(name: str) -> str:
    """
    식재료명 정제
    input : 식재료명
    output : 식재료명 내의 특정 문자를 삭제
    """
    blacklist = read_json("blacklist.json")

    for b in blacklist:
        if name.find(b) != -1:
            name = name.replace(b, "")

    if name.find("​") != -1:
        name = name.replace("​", "")
    if name.find("﻿") != -1:
        name = name.replace("﻿", "")
    if name.find("!") != -1:
        name = name.replace("!", "")
    if name.find("▶ 재료 : ") != -1:
        name = name.replace("▶ 재료 : ", "")

    name = name.strip()

    if name in mapping.keys():
        name = mapping[name]

    return name


def read_pure_recipe_data() -> dict:
    """
    root_dir(Asite)의 데이터를 dictionary 형태로 변환
    output : recipe_dict = {recipe_id : recipe_data}
                                recipe_data = {title, ings, seqs}
    """
    data = {}

    root_dir = "Asite"
    for filename in os.listdir(root_dir):
        if filename[-5:] != ".json":
            continue
        json_file = read_json(root_dir + "/" + filename)

        for recipe in json_file:
            if "ingredients" in recipe.keys() and len(recipe['ingredients']) > 0:
                data[recipe['recipe_id']] = recipe

    make_json("result/pure_recipe.json", data)
    return data


def making_ing_data(recipe_data: dict) -> List[Any]:
    """
    자주 쓰인 식재료 확인
    input : 레시피 데이터셋
    output : 각 레시피에서 식재료가 사용된 빈도를 내림차순 정렬한 것
    """
    freq_dict = {}
    for id, recipe in recipe_data.items():
        for ing in recipe['ingredients']:
            ing = ing['name']
            if freq_dict.get(ing) is None:
                freq_dict[ing] = 1
            else:
                freq_dict[ing] += 1
    freq_dict = sorted(freq_dict.items(), key=lambda item: item[1], reverse=True)
    make_json("result/ings_occur_freq.json", freq_dict)
    return freq_dict


def make_mapping(ing_list: list) -> dict:
    ret = {}

    if "mapping.json" in os.listdir():
        ret = read_json("mapping.json")

    for ingstr in ing_list:
        if "or" in ingstr:
            ings = ingstr.split('or')
            # for ing in ings:

    return ret


def cut_recipe(th: int, ing_dict: dict) -> dict:
    recipe_dict = read_json("result/pure_recipe.json")
    blacklist = []
    for [k, v] in ing_dict:
        if v < th:
            blacklist.append(k)
    print(blacklist)
    print(len(blacklist))

    ret = {}
    count = 0
    incount = 0
    recipe_tqdm = tqdm(recipe_dict.items())
    for id, recipe in recipe_tqdm:
        ban = False
        count += 1
        for ing in recipe['ingredients']:
            if ing['name'] in blacklist:
                ban = True
                break

        if not ban:
            incount += 1
            ret[id] = recipe

        recipe_tqdm.set_description(f"count : {count}, incount : {incount}, rate : {incount * 100 // count}%")

    make_json(f"result/upper{th}_ings_recipe.json", ret)
    return ret


if __name__ == "__main__":
    if not os.path.exists("result"):
        os.makedirs("result")

    # 수집 레시피 읽어오기
    if "pure_recipe.json" not in os.listdir("result"):
        recipe_dict = read_pure_recipe_data()
    else:
        recipe_dict = read_json("result/pure_recipe.json")

    # 식재료 정제
    if "valid_recipe.json" not in os.listdir("result"):
        recipe_dict = recipe_validation(recipe_dict)
    else:
        recipe_dict = read_json("result/valid_recipe.json")

    # 식재료마다 등장 빈도 체크하여 내림차순 정렬
    if "ings_occur_freq.json" not in os.listdir("result"):
        ing_dict = making_ing_data(recipe_dict)
    else:
        ing_dict = read_json("result/ings_occur_freq.json")

    # threshold 이상 등장한 식재료만 사용한 레시피 뽑아내기
    threshold = 100
    if f"upper{threshold}_ings_recipe.json" not in os.listdir("result"):
        recipe_dict = cut_recipe(threshold, ing_dict)
    else:
        recipe_dict = read_json(f"result/upper{threshold}_ings_recipe.json")
    print(len(recipe_dict))

    # threshold 이상 등장한 식재료 리스트 만들기
    if f"upper{threshold}_ings.json" not in os.listdir("result"):
        ing_list = list(map(lambda x: x[0], list(filter(lambda x: x[1] > threshold, ing_dict))))
        make_json(f"result/upper{threshold}_ings.json", ing_list)
    else:
        ing_list = read_json(f"result/upper{threshold}_ings.json")
