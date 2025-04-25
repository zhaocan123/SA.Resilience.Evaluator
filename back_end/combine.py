import copy
import json


def combineClasses(codeInfo, classInfo):
    clazzInfo = copy.deepcopy(classInfo)
    cInfo = copy.deepcopy(codeInfo)
    for key in codeInfo.keys():
        for cla in codeInfo[key]["classList"]:
            if cla.split(":")[0] == key:
                for item in codeInfo[key]["fanOut"]:
                    for cl in codeInfo[item]["classList"]:
                        if cla.split(":")[1] == cl.split(":")[1]:
                            combine(clazzInfo, cl, cla)
                            update_path(cInfo, cl, cla)
                            break
                    else:
                        continue
                    break
    return clazzInfo, cInfo


def combine(clazzInfo, x, y):
    combine_list = ["mem_var", "mem_method", "variable_list", "baseClass", "associatedClass", "fanIn", "fanOut"]
    for ci in combine_list:
        for item in clazzInfo[y][ci]:
            for i in clazzInfo[x][ci]:
                if item == i:
                    break
            else:
                clazzInfo[x][ci].append(item)
    del clazzInfo[y]


def update_path(cInfo, x, y):
    for key in cInfo.keys():
        if y in cInfo[key]["classList"]:
            cInfo[key]["classList"].remove(y)
            cInfo[key]["classList"].append(x)


# with open("classInfo.json", "r", encoding="utf-8") as f:
#     cli = json.load(f)
# with open("codeInfo.json", "r", encoding="utf-8") as f:
#     ci = json.load(f)
#
# clazzInfo,cInfo = combineClasses(ci["codeFileInfo"],cli["classInfo"])
# with open("b.json", "w", encoding="utf-8") as file:
#     json.dump(clazzInfo, file, ensure_ascii=False, indent=4)
# with open("c.json", "w", encoding="utf-8") as file:
#     json.dump(cInfo, file, ensure_ascii=False, indent=4)
