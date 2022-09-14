from FlavorGraph.module.preprocessing.preprocessing import *

"""
식재료 이름을 입력하면 해당 식재료를 사용하는 레시피의 id와 레시피를 보여줌
"""
if __name__ == "__main__":
    # Asite의 데이터 깔끔하게 정리
    if "pure_recipe.json" not in os.listdir("result"):
        recipe_dict = read_pure_recipe_data()
    else:
        recipe_dict = read_json("result/pure_recipe.json")

    target = input()

    for id, recipe in recipe_dict.items():
        for ing in recipe['ingredients']:
            if ing == target:
                print(id)
                print(recipe['title'])
                print(recipe['ingredients'])
                for s in recipe['sequences']:
                    print(str(s['sequence']) + " : "+s['content'])
                exit(0)
