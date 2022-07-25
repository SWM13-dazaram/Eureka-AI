import pickle
import json

# filename = "../../output/FlavorGraph+CSL-embedding_M11-metapath_300-dim_0.0025-initial_lr_3-window_size_1-iterations_5-min_count-_True-isCSP_0.0001-CSPcoef.pickle"
# filename = "../../output/FlavorGraph+CSL-embedding_M11-metapath_300-dim_0.0025-initial_lr_3-window_size_1-iterations_5-min_count-_True-isCSP_0.0001-CSPcoef_CSPLayer.pickle"

filename = "../../input/node2fp_revised_1120.pickle"

with open(filename, "rb") as f:
    data = pickle.load(f)

print(dir(data))
print(type(data))
print(data.keys())

# with open("node2fp_revised_1120.json", "w") as f:
#     re_data = dict()
#     for (k, v) in data.items():
#         re_data[k] = v.tolist()
#     json.dump(re_data, f)

print(len(data[7103]))