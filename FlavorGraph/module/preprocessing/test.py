from FlavorGraph.module.util import *
from tqdm import tqdm

if __name__ == "__main__":
    ings = read_json("result/ings_occur_freq.json")
    blacklist = list()

    thresholds = [1,2,5,10,30,50,100,300,500,1000,1500,3000]
    for threshold in thresholds:
        for ing in ings:
            if ing[1] <= threshold:
                blacklist.append(ing[0])
        blacklist = list(set(blacklist))
        print(f"threshold {threshold} - blacklist {len(blacklist)} - alive {len(ings)-len(blacklist)} - ratio {len(blacklist)/len(ings)}")

        # all_count = 0
        # black_count = 0
        # recipe_dict = read_json("result/pure_recipe.json")
        # recipe_tqdm = tqdm(recipe_dict.items())
        # for id, recipe in recipe_tqdm:
        #     ban = False
        #     for ing in recipe['ingredients']:
        #         all_count += 1
        #         if ing in blacklist:
        #             black_count += 1
        #     #         ban = True
        #     #         break
        #     #
        #     # if not ban:
        #     #     count += 1
        #     recipe_tqdm.set_description(f"Thres[{threshold}] Current Count = {black_count}/{all_count}, Ratio = {black_count*100//all_count}%")
        #     if all_count > 25000:
        #         break
