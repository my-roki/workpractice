import json

with open("xml_to_json.json", "r") as st_json:
    a = json.load(st_json)

# print(json.dumps(a, indent="\t"))


# image1 = a["annotations"]["image"]
id_list = a["annotations"]["image"][0]


del id_list["box"]

# print(image1)
# print(len(image1))  # 리스트의 갯수

print(json.dumps(id_list, indent="\t"))


# for i in range(0,len(image1)):
#     id_list = a["annotations"]["image"][i]
#     print(id_list)



# test1 = dict()
#
# test2 = dict()
# test2["type"] = "bbox"
# test2["copyright"] =
# test2["date"] = a["annotations"]["dumped"]
# test2["verification"] = "false"
# test2["image"] = a["annotations"]["image"][0:3]
#####