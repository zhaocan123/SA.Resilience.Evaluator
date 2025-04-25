import networkx as nx
import itertools
import matplotlib.pyplot as plt
from networkx.algorithms import community
from subprocess import run
import os
# from sklearn.metrics import silhouette_score

# from pyecharts_CG import EchartsGraphComponent_diagram
from graph_to_json import compgraph2json

import json
pwd = os.getcwd()
pwd = pwd.replace("\\", "/")
print("Design_recovery/Component_recovery.py: pwd = ", pwd)
with open(pwd + "/config.json", "r", encoding="utf-8") as f:
    content = json.load(f)
DOT_EXE_FILE_PATH = content["DOT_EXE_FILE_PATH"]


def run_cmd(cmd_str='', echo_print=1):
    """
    执行cmd命令，不显示执行过程中弹出的黑框
    备注：subprocess.run()函数会将本来打印到cmd上的内容打印到python执行界面上，所以避免了出现cmd弹出框的问题
    :param cmd_str: 执行的cmd命令
    :return: 
    """
    if echo_print == 1:
        print('\n执行cmd指令="{}"'.format(cmd_str))
    run(cmd_str, shell=True)


def dot2png(dot_file_name, png_file_name):
    # Call command line to convert dot to png
    cmd_str = f'{DOT_EXE_FILE_PATH} -Tpng ' + \
        dot_file_name + ' -o ' + png_file_name
    run_cmd(cmd_str)


class file_information:
    def __init__(self, label, file_path):
        self.label = label
        self.file_path = file_path
        self.file_name = file_path.split('/')[-1]
        self.file_type = file_path.split('.')[-1]

        self.header = ""  # 获取文件头部信息
        self.source = ""  # 获取文件源代码

        # 获取文件所在所在文件夹
        self.folder = ""
        for temp in file_path.split('/')[:-1]:
            self.folder += temp + '/'
        self.folder = self.folder[:-1]

        self.children = []


class func_information:
    def __init__(self, label, func_name, func_file):
        self.id = ""
        self.label = label
        self.func_name = ""
        self.func_file = func_file
        self.key = func_name
        if ":" in func_name:
            self.func_name = func_name.split(":")[-1]
        else:
            self.func_name = func_name

        self.if_lib = False  # 如果为True，则表示该函数为库函数
        if 'Library function' in self.func_file:
            self.if_lib = True

        self.if_sdg = False  # 如果为True，则表示该模块已经生成了SDG

        self.deleted = False  # 如果为True，则表示该函数为test或example函数或未识别函数，需要删除
        # if 'test' in self.func_file.lower() or 'example' in self.func_file.lower() or 'Unrecognized' in self.func_file:
        #     self.deleted = True

        self.children = []
        self.parents = []

        self.header_file = ""  # 获取文件头部信息
        self.source_file = ""  # 获取文件源代码


class Modular:
    def __init__(self):
        self.label = ''
        self.id = ''
        # self.folder = folder
        self.if_lib = False
        self.func_set = set()
        self.children = []
        self.parents = []

        self.if_sdg = False  # 如果为True，则表示该模块已经生成了SDG


def get_func_information(G, dot_file, func_header_source):
    # 获取函数信息
    func_information_list = []
    fun_id = 1
    for node in G.nodes:
        node_info = G.nodes[node]
        if 'label' in node_info:
            func_name = G.nodes[node]['label'].replace('"', '')
            if 'file' in node_info:
                func_file = G.nodes[node]['file'].replace(
                    '"', '').replace('\\', '/')
            elif 'code_file_path' in node_info:
                func_file = G.nodes[node]['code_file_path'].replace(
                    '"', '').replace('\\', '/')
            else:
                func_file = func_name.split(": ")[0].replace('\\', '/')
            if func_file != "Unrecognized File":
                func_information_list.append(
                    func_information(node, func_name, func_file))
                func_information_list[-1].id = node
                fun_id += 1
            if 'file' not in node_info:
                func_information_list[-1].if_sdg = True
    # 删除test和example函数
    # remove_list = []
    # for func in func_information_list:
    #     if func.deleted:
    #         remove_list.append(func)
    # for func in remove_list:
    #     func_information_list.remove(func)

    exist_edge = []
    # print(G.edges(data=True))
    for edge in G.edges()._viewer:
        start_node = edge[0]
        end_node = edge[1]
        style = None
        temp_edge = G.edges[edge]
        if "style" in temp_edge.keys():
            style = temp_edge["style"]
        else:
            style = "solid"

        weight = None
        if "count" in temp_edge.keys():
            weight = int(temp_edge["count"])
        else:
            weight = 1

        parent = (start_node, style, weight)
        child = (end_node, style, weight)
        for func in func_information_list:
            if parent[0] == func.label and child[0] in [f.label for f in func_information_list]:
                # 判断是否存在该子节点，如果存在则增加权重，否则添加子节点
                find = False
                for child_node in func.children:
                    if child_node[0] == child[0] and child_node[1] == child[1]:
                        temp = child_node[2] + child[2]
                        new_child = (child_node[0], child_node[1], temp)
                        func.children.remove(child_node)
                        func.children.append(new_child)
                        find = True
                        break
                if not find:
                    func.children.append(child)
            if child[0] == func.label and parent[0] in [f.label for f in func_information_list]:
                # 判断是否存在该父节点，如果存在则增加权重，否则添加父节点
                find = False
                for parent_node in func.parents:
                    if parent_node[0] == parent[0] and parent_node[1] == parent[1]:
                        temp = parent_node[2] + parent[2]
                        new_parent = (parent_node[0], parent_node[1], temp)
                        func.parents.remove(parent_node)
                        func.parents.append(new_parent)
                        find = True
                        break
                if not find:
                    func.parents.append(parent)

    if dot_file == 1:
        return func_information_list

    fun_definitions_dict = {}

    for func_name, files in func_header_source.items():
        source_file = files[0]
        header_file = files[1]
        key = func_name
        fun_definitions_dict[key] = [header_file, source_file]

    for func in func_information_list:
        if func.id == "test_cunit_end_tests":
            print("debug")
        if func.func_file != "Unrecognized File":
            func_name = func.key
            # 将第一个'/'之前的字符串改为CUnit_dr
            header_file = func.func_file
            # source_file = "CUnit_dr" + '/' + '/'.join(source_file)
            key = func_name
            if key in fun_definitions_dict.keys():
                func.source_file = fun_definitions_dict[key][1]
            func.header_file = header_file

    return func_information_list


def modularization(func_information_list):
    Modular_list = []
    for func in func_information_list:
        modular = Modular()
        modular.func_set.add(func)
        modular.if_sdg = func.if_sdg
        modular.if_lib = func.if_lib
        Modular_list.append(modular)

    # 获得子节点
    for modular in Modular_list:
        for func in modular.func_set:
            for child in func.children:
                for modular2 in Modular_list:
                    if child[0] in [f.label for f in modular2.func_set]:
                        # 判断是否存在该子节点，如果存在则增加权重，否则添加子节点
                        find = False
                        for c in modular.children:
                            if c[0] == modular2 and c[1] == child[1]:
                                find = True
                                temp = c[2] + child[2]
                                new_child = (c[0], c[1], temp)
                                modular.children.remove(c)
                                modular.children.append(new_child)
                                break
                        if not find:
                            modular.children.append(
                                (modular2, child[1], child[2]))

            for parent in func.parents:
                for modular2 in Modular_list:
                    if parent[0] in [f.label for f in modular2.func_set]:
                        # 判断是否存在该父节点，如果存在则增加权重，否则添加父节点
                        find = False
                        for p in modular.parents:
                            if p[0] == modular2 and p[1] == parent[1]:
                                find = True
                                temp = p[2] + parent[2]
                                new_parent = (p[0], p[1], temp)
                                modular.parents.remove(p)
                                modular.parents.append(new_parent)
                                break
                        if not find:
                            modular.parents.append(
                                (modular2, parent[1], parent[2]))

    # 将所有的lib模块合并到第一个lib模块中
    start_lib = None
    for modular in Modular_list:
        if modular.if_lib:
            start_lib = modular
            break
    find = True
    while find:
        find = False
        for modular in Modular_list:
            if modular.if_lib and modular != start_lib:
                find = True
                node_merge(Modular_list, start_lib, modular)

    return Modular_list


def Preliminary_merger(Modular_list):

    # 模块按fun.source_file分组
    Modular_dict = {}
    for modular in Modular_list:
        for fun in modular.func_set:
            if fun.source_file not in Modular_dict.keys():
                Modular_dict[fun.source_file] = []
            Modular_dict[fun.source_file].append(modular)
    # 将同一组的模块合并
    for key in Modular_dict.keys():
        if len(Modular_dict[key]) > 1:
            start_modular = Modular_dict[key][0]
            for modular in Modular_dict[key][1:]:
                node_merge(Modular_list, start_modular, modular)

    # 将每个Modular的函数存到networkx的图中，求联通子图
    for modular in Modular_list:
        G = nx.DiGraph()
        for func in modular.func_set:
            G.add_node(func.id)
        for func in modular.func_set:
            for child in func.children:
                G.add_edge(func.id, child[0])
        subgraphs = list(G.subgraph(c)
                         for c in nx.weakly_connected_components(G))
        # 如果联通子图大于1，则将该模块拆分
        new_modular_list = []
        if len(subgraphs) > 1:
            for subgraph in subgraphs:
                new_modular = Modular()
                for node in subgraph.nodes:
                    for func in modular.func_set:
                        if node == func.id:
                            new_modular.func_set.add(func)
                new_modular.if_sdg = modular.if_sdg
                new_modular.if_lib = modular.if_lib
                new_modular.id = modular.id+str(subgraphs.index(subgraph))
                new_modular_list.append(new_modular)
            Modular_list.remove(modular)
            Modular_list.extend(new_modular_list)

    for modular in Modular_list:
        modular.children = []
        modular.parents = []
        for func in modular.func_set:
            for child in func.children:
                for modular2 in Modular_list:
                    if child[0] in [f.label for f in modular2.func_set]:
                        # 判断是否存在该子节点，如果存在则增加权重，否则添加子节点
                        find = False
                        for c in modular.children:
                            if c[0] == modular2 and c[1] == child[1]:
                                find = True
                                temp = c[2] + child[2]
                                new_child = (c[0], c[1], temp)
                                modular.children.remove(c)
                                modular.children.append(new_child)
                                break
                        if not find:
                            modular.children.append(
                                (modular2, child[1], child[2]))

            for parent in func.parents:
                for modular2 in Modular_list:
                    if parent[0] in [f.label for f in modular2.func_set]:
                        # 判断是否存在该父节点，如果存在则增加权重，否则添加父节点
                        find = False
                        for p in modular.parents:
                            if p[0] == modular2 and p[1] == parent[1]:
                                find = True
                                temp = p[2] + parent[2]
                                new_parent = (p[0], p[1], temp)
                                modular.parents.remove(p)
                                modular.parents.append(new_parent)
                                break
                        if not find:
                            modular.parents.append(
                                (modular2, parent[1], parent[2]))

    return Modular_list


def Preliminary_merger_2(Modular_list):
    # 获得所有header和source文件相同的模块，该模块及其父模块分为一组
    new_Modular_list = []
    for modular in Modular_list:
        for func in modular.func_set:
            if func.header_file == func.source_file:
                new_list = set()
                for parent in modular.parents:
                    new_list.add(parent[0])
                new_list.add(modular)
                # 判断new_list与Modular_list中的元素是否有交集，有的话合并
                find = False
                for modular2 in new_Modular_list:
                    inter = modular2 & new_list
                    if len(list(inter)) > 0:
                        find = True
                        for modular3 in new_list:
                            modular2.add(modular3)

                        break
                if not find:
                    new_Modular_list.append(new_list)

    # 将有交集的模块合并
    find = True
    while find == True:
        find = False
        for modular_set1 in new_Modular_list:
            for modular_set2 in new_Modular_list:
                inter = modular_set1 & modular_set2
                if len(list(inter)) > 0 and modular_set1 != modular_set2:
                    find = True
                    for modular in modular_set2:
                        modular_set1.add(modular)
                    new_Modular_list.remove(modular_set2)
                    break

    # 将同一组的模块合并
    for modular_set in new_Modular_list:
        if len(list(modular_set)) == 1:
            continue
        start_modular = modular_set.pop()
        for modular in modular_set:
            node_merge(Modular_list, start_modular, modular)

    for modular in Modular_list:
        modular.children = []
        modular.parents = []
        for func in modular.func_set:
            for child in func.children:
                for modular2 in Modular_list:
                    if child[0] in [f.label for f in modular2.func_set]:
                        # 判断是否存在该子节点，如果存在则增加权重，否则添加子节点
                        find = False
                        for c in modular.children:
                            if c[0] == modular2 and c[1] == child[1]:
                                find = True
                                temp = c[2] + child[2]
                                new_child = (c[0], c[1], temp)
                                modular.children.remove(c)
                                modular.children.append(new_child)
                                break
                        if not find:
                            modular.children.append(
                                (modular2, child[1], child[2]))
            for parent in func.parents:
                for modular2 in Modular_list:
                    if parent[0] in [f.label for f in modular2.func_set]:
                        # 判断是否存在该父节点，如果存在则增加权重，否则添加父节点
                        find = False
                        for p in modular.parents:
                            if p[0] == modular2 and p[1] == parent[1]:
                                find = True
                                temp = p[2] + parent[2]
                                new_parent = (p[0], p[1], temp)
                                modular.parents.remove(p)
                                modular.parents.append(new_parent)
                                break
                        if not find:
                            modular.parents.append(
                                (modular2, parent[1], parent[2]))

    return Modular_list


def Modular_splitting(Modular_list):
    print("Modular_splitting")
    # 遍历所有模块，如果模块中存在函数度大于40的函数，则将该函数切除，形成新的模块，再应用单依赖和紧耦合原则进行组件化
    new_Modular_list = []
    for modular in Modular_list:
        if modular.id == "testrun":
            print("testrun")
        average_degree = 0
        degree_dict = {}
        for func in modular.func_set:
            degree_dict[func] = 0
            # for child in func.children:
            #     degree_dict[func] += child[2]
            for parent in func.parents:
                degree_dict[func] += parent[2]
            average_degree += degree_dict[func]
        average_degree = average_degree / len(modular.func_set)
        for func in modular.func_set:
            if func.func_name == "test_message_handlers":
                print("test_message_handlers")
            if degree_dict[func] > average_degree * 2:
                new_func_set = set()
                new_func_set.add(func)

                # 判断该模块中是否存在函数与被切除的函数有单依赖关系，如果有则将该函数添加到该模块中，并从原模块中删除
                for func2 in modular.func_set:
                    depen_set = set()
                    for child in func2.children:
                        depen_set.add(child[0])
                    for parent in func2.parents:
                        depen_set.add(parent[0])

                    if len(depen_set) == 1 and func.func_name in depen_set:
                        # print("单依赖")
                        new_func_set.add(func2)

                # 判断该模块中是否存在函数与被切除的函数有紧耦合关系，如果有则将该函数添加到该模块中，并从原模块中删除
                for func2 in modular.func_set:
                    for child in func2.children:
                        if child[0] == func.func_name and child[1] == 'solid':
                            for parent in func2.parents:
                                if parent[0] == func.func_name and parent[1] == 'solid':
                                    # print("紧耦合")
                                    new_func_set.add(func2)
                                    break
                            break

                if len(new_func_set) == 1:
                    continue
                new_modular = Modular()
                new_modular.func_set = new_func_set
                modular.func_set = modular.func_set - new_func_set
                new_modular.if_sdg = modular.if_sdg
                new_Modular_list.append(new_modular)

    # 将新生成的模块添加到原模块列表中
    remove_list = []
    for modular in new_Modular_list:
        Modular_list.append(modular)

    for modular in Modular_list:
        if len(modular.func_set) == 0:
            remove_list.append(modular)
    for modular in remove_list:
        Modular_list.remove(modular)

    for modular in Modular_list:
        modular.children = []
        modular.parents = []
        for func in modular.func_set:
            for child in func.children:
                for modular2 in Modular_list:
                    if child[0] in [f.label for f in modular2.func_set]:
                        # 判断是否存在该子节点，如果存在则增加权重，否则添加子节点
                        find = False
                        for c in modular.children:
                            if c[0] == modular2 and c[1] == child[1]:
                                find = True
                                temp = c[2] + child[2]
                                new_child = (c[0], c[1], temp)
                                modular.children.remove(c)
                                modular.children.append(new_child)
                                break
                        if not find:
                            modular.children.append(
                                (modular2, child[1], child[2]))
            for parent in func.parents:
                for modular2 in Modular_list:
                    if parent[0] in [f.label for f in modular2.func_set]:
                        # 判断是否存在该父节点，如果存在则增加权重，否则添加父节点
                        find = False
                        for p in modular.parents:
                            if p[0] == modular2 and p[1] == parent[1]:
                                find = True
                                temp = p[2] + parent[2]
                                new_parent = (p[0], p[1], temp)
                                modular.parents.remove(p)
                                modular.parents.append(new_parent)
                                break
                        if not find:
                            modular.parents.append(
                                (modular2, parent[1], parent[2]))
    set_name(Modular_list)

    return Modular_list, new_Modular_list


def Componentization(Modular_list):
    # 根据组件化原则对模块进行组件化
    # 1.模块只依赖于另一个模块，且该模块不被其他模块依赖
    # 2.紧耦合
    # 3.闭环依赖
    # 4.开环依赖
    # 5.传递依赖
    # Modular_list = Modular_splitting(Modular_list)

    find = False
    print("组件化前模块数：", len(Modular_list))
    # 递归处理模块，直到不满足组件化原则
    # 1.模块只依赖于另一个模块，且该模块不被其他模块依赖
    find_1 = True
    while find_1:
        find_1 = False
        for modular in Modular_list:
            if modular.if_lib:
                continue

            # 判断与该模块有依赖关系的模块是否只有一个
            node_list = set()
            for parent in modular.parents:
                node_list.add(parent[0])
            for child in modular.children:
                node_list.add(child[0])
            if len(node_list) != 1:
                continue

            # 如果与该模块有依赖关系的模块只有一个，将该模块合并到相依赖的模块中
            node = node_list.pop()
            if node == modular:
                continue
            node_merge(Modular_list, node, modular)
            print("单依赖")
            find_1 = True
            find = True

    # 2.紧耦合，某个模块的父节点和子节点都是同一个模块
    find_2 = True
    while find_2:
        find_2 = False

        for modular in Modular_list:
            if modular.if_lib == True:
                # 如果原模块的if_fixed为True，则不组件化，直接跳过
                continue
            # 遍历父节点
            for parent in modular.parents:
                # 遍历子节点
                for child in modular.children:
                    if parent[0] == child[0] and parent[0] != modular:
                        if child[0].if_lib == True or parent[1] == 'dotted' or child[1] == 'dotted':
                            # 如果父节点或子节点是lib模块，则不组件化，直接跳过 如果是依赖边，则不组件化，直接跳过
                            continue
                        # 将该模块合并到父节点中，再将该模块从模块列表中删除
                        print("紧耦合")
                        node_merge(Modular_list, parent[0], modular)
                        find_2 = True
                        find = True

                    # 如果处理了该模块，则跳出循环
                    if find_2:
                        break
                if find_2:
                    break
            if find_2:
                break

    # # 3.闭环依赖，环中的模块都是紧耦合的
    # find_3 = True
    # while find_3:
    #     find_3 = False
    #     start_modular = Modular_list[0]
    #     if start_modular.if_lib == True or start_modular.if_sdg == True:
    #         break
    #     circle_list = []
    #     get_circle(Modular_list, start_modular, circle_list)
    #     if len(circle_list) > 2:
    #         print("规则3")
    #         find_3 = True
    #         find = True
    #         start_modular = None
    #         start_modular_index = 0
    #         for modular in circle_list:
    #             if modular.if_sdg == True or modular.if_lib == True:
    #                 start_modular = modular
    #                 start_modular_index = circle_list.index(modular)
    #                 break
    #         # 将环中的模块合并到环中的第一个模块中
    #         for modular in circle_list[start_modular_index+1:]:
    #             if modular.if_sdg == True or modular.if_lib == True:
    #             # 如果原模块的if_fixed为True，则不组件化，直接跳过
    #                 continue
    #             node_merge(Modular_list, start_modular, modular)

    # # 4.开环依赖，传递依赖
    # find_4 = True
    # while find_4:
    #     find_4 = False
    #     regin_modular_list = get_regin_modular(Modular_list)
    #     for modular in regin_modular_list:
    #         if modular.if_lib == True:
    #             continue
    #         if modular.if_sdg == True:
    #             break
    #         # 将模块列表存到networkx的有向图中
    #         if len(modular.children) >= 2:
    #             for child_1 in modular.children:
    #                 for child_2 in modular.children:
    #                     if child_1[0] != child_2[0] and child_1[0]!=modular and child_2[0]!=modular and child_1[0].if_lib == False and child_2[0].if_lib == False:
    #                         # 判断两个子节点之间是否存在依赖关系
    #                         if_depend = False
    #                         for p in child_1[0].parents:
    #                             if child_2[0] == p[0]:
    #                                 # child_2是child_1的父节点，存在依赖关系
    #                                 if_depend = True
    #                                 break
    #                         for p in child_2[0].parents:
    #                             if child_1[0] == p[0]:
    #                                 # child_1是child_2的父节点，存在依赖关系
    #                                 if_depend = True
    #                                 break
    #                         if if_depend == True:
    #                             # 如果两个子节点之间存在依赖关系，则不组件化，直接跳过
    #                             continue

    #                         modular_graph = nx.DiGraph()
    #                         for modular_2 in Modular_list:
    #                             if modular_2.if_lib != True:
    #                                 modular_graph.add_node(modular_2.id, label=modular_2.label)
    #                         for modular_2 in Modular_list:
    #                             if modular_2.if_lib != True:
    #                                 for child in modular_2.children:
    #                                     if child[0].if_lib != True:
    #                                         modular_graph.add_edge(modular_2.id, child[0].id)

    #                         # 判断两个子节点是否存在开环依赖，即两个子节点之间是否只存在一条路径,如果存在路径，则获得路径
    #                         path1 = nx.all_simple_paths(modular_graph, child_1[0].id, child_2[0].id)
    #                         path2 = nx.all_simple_paths(modular_graph, child_2[0].id, child_1[0].id)
    #                         # 合并两个路径
    #                         path = []
    #                         for p in path1:
    #                             path.append(p)
    #                         for p in path2:
    #                             path.append(p)
    #                         if len(path) > 0 and len(path) <= 2:
    #                             # 如果两个子节点之间存在开环依赖，组件化
    #                             #选择最短路径
    #                             path.sort(key=lambda x:len(x))
    #                             p = path[0]

    #                             # 如果modular是p中的节点，则不组件化，直接跳过
    #                             if modular.id in p:
    #                                 continue

    #                             print("开环依赖")
    #                             find_4 = True
    #                             find = True
    #                             start_modular = None
    #                             modular_merge_list = []
    #                             for modular_id in p:
    #                                 for m in Modular_list:
    #                                     if m.id == modular_id:
    #                                         modular_merge_list.append(m)

    #                             start_modular = modular_merge_list[0]
    #                             for modular_2 in modular_merge_list[1:]:
    #                                 node_merge(Modular_list, start_modular, modular_2)

    #                             # 有开环依赖，停止处理child_1和child_2
    #                             break
    #                     # 如果两个子节点之间不存在开环依赖，判断两个子节点是否存在传递依赖
    #                         else:
    #                             # 判断child_1和child_2是否有公共子节点
    #                             common_child = []
    #                             child1_child_set = set([child[0] for child in child_1[0].children])
    #                             child2_child_set = set([child[0] for child in child_2[0].children])
    #                             common_child_set = child1_child_set & child2_child_set
    #                             if len(common_child_set) > 0:
    #                                 # 如果有公共子节点，则判断公共子节点是否有传递依赖
    #                                 child3 = None
    #                                 for child in common_child_set:
    #                                     if child.if_lib == False and child != modular and child != child_1[0] and child != child_2[0]:
    #                                         child3 = child
    #                                         break
    #                                 if child3 != None:
    #                                     # 存在传递依赖
    #                                     print("传递依赖")
    #                                     find_4 = True
    #                                     find = True
    #                                     start_modular = None
    #                                     temp_list = [child_1[0], child_1[0], child3]
    #                                     modular_merge_list = []
    #                                     for modular_2 in temp_list:
    #                                         for m in Modular_list:
    #                                             if m.id == modular_2.id:
    #                                                 modular_merge_list.append(m)

    #                                     start_modular = modular_merge_list[0]
    #                                     for modular_2 in modular_merge_list:
    #                                         if modular_2 != start_modular:
    #                                             node_merge(Modular_list, start_modular, modular_2)

    #                                     print("传递依赖")

    #                                 # 有传递依赖，停止处理child_1和child_2
    #                         if find_4 == True:
    #                             break
    #             # 如果应用了传递依赖或开环依赖，重新计算regin_modular
    #             if find_4 == True:
    #                 break

    if find:
        # 递归调用
        Modular_list = Componentization(Modular_list)
    return Modular_list


def get_regin_modular(Modular_list, k):
    # 获得域模块
    # 域模块即为对其他模块依赖程度较高的模块
    # 域模块的依赖程度由模块内函数的子节点数量和父节点数量决定
    # 计算每个模块的依赖程度
    # 依赖程度 = 模块内的函数的子节点数量 + 模块内的函数的父节点数量
    Dependency = {}
    for modular in Modular_list:
        if modular.if_lib != True:
            Dependency[modular.id] = 0
            for func in modular.func_set:
                for child in func.children:
                    Dependency[modular.id] += child[2]
                for parent in func.parents:
                    Dependency[modular.id] += parent[2]

    # 从大到小排序
    sorted_Dependency = sorted(
        Dependency.items(), key=lambda x: x[1], reverse=True)
    Dependency = {}
    for i in range(len(sorted_Dependency)):
        Dependency[sorted_Dependency[i][0]] = sorted_Dependency[i][1]
    # 计算依赖程度的平均值
    # 依赖程度的平均值 = 所有模块的依赖程度之和 / 模块数量
    sum = 0
    modular_num = 0
    for modular in Modular_list:
        if modular.if_lib != True:
            sum += Dependency[modular.id]
            modular_num += 1
    average = sum / modular_num

    # 中位数
    median = sorted_Dependency[len(sorted_Dependency) // 2][1]

    # 依赖程度大于依赖程度的平均值的模块为域模块
    # 将域模块添加到域模块列表中
    regin_modular_list = []
    for modular in Modular_list:
        if modular.if_lib != True:
            if Dependency[modular.id] > 40:
                regin_modular_list.append(modular)

    return regin_modular_list


def node_merge(Modular_list, start_modular, modular):
    # 将模块中的文件添加到环中的第一个模块中
    start_modular.func_set.update(modular.func_set)
    # 将模块从模块列表中删除
    Modular_list.remove(modular)
    # 将模块从父节点的子节点列表中删除
    for parent in modular.parents:
        for child in parent[0].children:
            if child[0] == modular:
                parent[0].children.remove(child)
    # 将模块从子节点的父节点列表中删除
    for child in modular.children:
        for parent in child[0].parents:
            if parent[0] == modular:
                child[0].parents.remove(parent)
    # 将模块的子节点添加到环中的第一个模块的子节点列表中
    for child in modular.children:
        if child[0] != start_modular and child[0] != modular:
            start_modular.children.append(child)
            # 更新子节点的父节点列表
            # child.parents.remove(modular)
            # 判断是否存在该父节点，如果存在则增加权重，否则添加父节点
            find = False
            for parent in child[0].parents:
                if parent[0] == start_modular and parent[1] == child[1]:
                    temp = parent[2] + child[2]
                    new_parent = (start_modular, child[1], temp)
                    child[0].parents.remove(parent)
                    child[0].parents.append(new_parent)
                    find = True
                    break
            if find == False:
                child[0].parents.append((start_modular, child[1], child[2]))
    # 将模块的父节点添加到环中的第一个模块的父节点列表中
    for parent in modular.parents:
        if parent[0] != start_modular and parent[0] != modular:
            start_modular.parents.append(parent)
            # 更新父节点的子节点列表
            # parent.children.remove(modular)
            # 判断是否存在该子节点，如果存在则增加权重，否则添加子节点
            find = False
            for child in parent[0].children:
                if child[0] == start_modular and child[1] == parent[1]:
                    temp = child[2] + parent[2]
                    new_child = (start_modular, parent[1], temp)
                    parent[0].children.remove(child)
                    parent[0].children.append(new_child)
                    find = True
                    break
            if find == False:
                parent[0].children.append(
                    (start_modular, parent[1], parent[2]))


def get_circle(Modular_list, modular, circle_list):
    # 深度优先搜索找到一个闭环
    circle_list.append(modular)
    for child in modular.children:
        if child[0] in circle_list:
            # 找到闭环
            return

        else:
            get_circle(Modular_list, child[0], circle_list)

    # 如果没有找到闭环，则将该模块从闭环列表中删除
    circle_list.remove(modular)


def GN(Modular_list):

    Modular_list, regin_modular_list = Modular_splitting(Modular_list)

    if len(Modular_list) == 1:
        return Modular_list, {}, {}

    # set_name(Modular_list)

    # 获取关键模块
    # regin_modular_list = get_regin_modular(Modular_list, 40)

    # 构建有向图
    G = nx.MultiDiGraph()
    for modular in Modular_list:
        if modular.if_lib == False and modular not in regin_modular_list:
            # 添加节点
            G.add_node(modular.id, label=modular.id)

    for modular in Modular_list:
        for child in modular.children:
            # 添加有向边
            if child[0].if_lib == False and child[0] not in regin_modular_list and modular not in regin_modular_list:
                node1 = modular.id
                node2 = child[0].id
                style = child[1]
                weight = child[2]
                G.add_edge(node1, node2, style=style, weight=weight)

    for edge in G.edges()._viewer:
        temp_edge = G.edges[edge]
        start = edge[0]
        end = edge[1]
        style = G.edges[edge]['style']
        # weight = exist_edge_num[(start, end), style]
        # G.edges[edge]['weight'] = weight

    # 画图
    nx.draw(G, with_labels=True)
    sub_graphs_num = 1
    Silhouette_Coefficient_map = {}
    result_map = GN_CAL(G, G, sub_graphs_num, 10, Silhouette_Coefficient_map)
    # 按照轮廓系数从大到小排序
    result_map = sorted(result_map.items(), key=lambda x: x[1], reverse=True)
    modularity_map = {}
    if len(result_map) == 0:
        return Modular_list, {}, {}
    bestresult = result_map[0][0]
    max = 0
    for result in result_map:
        sub_graphs_num = len(list(result[0].subgraph(
            c) for c in nx.weakly_connected_components(result[0])))
        modularity_map[sub_graphs_num] = result[1]
        if sub_graphs_num >= int(len(Modular_list)*0.9) and result[1] > max:
            bestresult = result[0]
            max = result[1]
    # 选取轮廓系数最大的结果
    # 计算子图数量
    # sub_graphs_num = len(list(result.subgraph(c) for c in nx.weakly_connected_components(result)))

    sub_graphs = list(bestresult.subgraph(c)
                      for c in nx.weakly_connected_components(bestresult))

    best_comm = []
    for sub_graph in sub_graphs:
        best_comm.append(list(sub_graph.nodes))

    # 添加关键模块
    for modular in regin_modular_list:
        best_comm.append([modular.id])

    # 带权重的GN算法
    # #comp = community.girvan_newman(G, weight='weight') # Girvan-Newman算法，返回迭代器
    # comp = community.girvan_newman(G) # Girvan-Newman算法，返回迭代器
    # k = int(G.number_of_nodes()*0.15) # 最大类簇数量
    # limited = itertools.takewhile(lambda c: len(c) <= k, comp) # 迭代器
    # max_mod = float("-inf")
    # max_sc = float("-inf")
    # best_comm = None
    # modularity_map = {} # 模块度字典
    # Silhouette_Coefficient_map = {} # 轮廓系数字典
    # start_comm = [set()]
    # for node in G.nodes:
    #     start_comm[0].add(node)
    # best_comm = start_comm
    # print("迭代次数为:",0,"; 聚类结果为:",start_comm,"; 轮廓系数为:",0)
    # if len(G.edges) != 0:
    #     for communities in limited:
    #         if len(communities)< int(G.number_of_nodes()*0.1):
    #             continue
    #         # 遍历每个聚类结果，计算模块度，取最大值
    #         # print(list(set(sorted(c)) for c in communities))
    #         communities = list(set(sorted(c)) for c in communities)

    #         mod = cal_modularity(G, communities)
    #         #mod = community.modularity(G, communities)
    #         modularity_map[len(communities)] = mod
    #         Silhouette_Coefficient = cal_Silhouette_Coefficient(G, communities)
    #         Silhouette_Coefficient_map[len(communities)] = Silhouette_Coefficient
    #         print("迭代次数为:",len(communities)-1,"; 聚类结果为:",communities,"; 轮廓系数为:",Silhouette_Coefficient)
    #         if Silhouette_Coefficient >= max_sc:
    #             max_sc = Silhouette_Coefficient
    #             best_comm = communities
    # else:
    #     best_comm = [{node} for node in G.nodes]
    #     max_sc = 0
    # #print(max_mod)
    # #print(best_comm)

    # comm = []
    # print("最大轮廓系数为：", max_sc)
    # print("最佳聚类结果为：", best_comm)

    # 将同一类的模块合并
    # 遍历每一类，将每一类的模块合并
    for i in range(len(best_comm)):
        # 将每一类的模块合并
        new_modular = None
        for j in range(len(best_comm[i])):
            if j == 0:
                for modular in Modular_list:
                    if modular.id == list(best_comm[i])[j]:
                        new_modular = modular
                        break
            else:
                for modular in Modular_list:
                    if modular.id == list(best_comm[i])[j]:
                        node_merge(Modular_list, new_modular, modular)
                        break

    return Modular_list, modularity_map, Silhouette_Coefficient_map


def GN_CAL(start_G, G, last_sub_graphs_num, max_clusters_num, Silhouette_Coefficient_map):
    # 如果边的数量为0，直接返回
    if len(G.edges) == 0:
        return Silhouette_Coefficient_map
    # 计算每条边的边介数
    edge_betweenness = nx.edge_betweenness_centrality(
        G, normalized=True, weight=None, seed=None)

    temp_edge_betweenness = sorted(
        edge_betweenness.items(), key=lambda x: x[1], reverse=True)

    # new_edge_betweenness = {}
    # 计算每条边的边介数除以边的权重
    for edge in edge_betweenness:
        weight = G.edges[edge]['weight']
        edge_betweenness[edge] = edge_betweenness[edge]/G.edges[edge]['weight']

    # 边介数从大到小排序
    edge_betweenness = sorted(edge_betweenness.items(),
                              key=lambda x: x[1], reverse=True)

    max_edge_list = []
    max_edge_list.append(edge_betweenness[0])
    for i in range(1, len(edge_betweenness)):
        if edge_betweenness[i][1] == edge_betweenness[0][1]:
            max_edge_list.append(edge_betweenness[i])
        else:
            break

    # 从G中删除边介数最大的边
    # for max_edge in max_edge_list:
    temp_edge = max_edge_list[0][0]
    G.remove_edge(temp_edge[0], temp_edge[1], key=temp_edge[2])

    edge_num = len(G.edges)

    # 获取clusters

    # 获得G的子图
    sub_graphs = list(G.subgraph(c) for c in nx.weakly_connected_components(G))
    # 如果子图的数量没有变化,则递归调用
    if len(sub_graphs) == last_sub_graphs_num:
        return GN_CAL(start_G, G, last_sub_graphs_num, max_clusters_num, Silhouette_Coefficient_map)
    # 如果子图的数量变化了，则根据子图对节点进行聚类，然后计算轮廓系数并存储在Silhouette_Coefficient_map中,然后递归调用
    else:
        cluster_list = []
        for sub_graph in sub_graphs:
            cluster_list.append(list(sub_graph.nodes))
        Silhouette_Coefficient = cal_Silhouette_Coefficient(
            start_G, cluster_list)
        new_G = G.copy()
        Silhouette_Coefficient_map[new_G] = Silhouette_Coefficient
        return GN_CAL(start_G, G, len(sub_graphs), max_clusters_num, Silhouette_Coefficient_map)


def cal_Silhouette_Coefficient(G, communities):
    # 根据聚类结果和图计算轮廓系数
    # communities是聚类结果，是一个列表，列表中的每个元素是一个集合，集合中的元素是模块的label
    # G是图
    # 返回轮廓系数
    # 将communities转换成字典
    communities_dict = {}
    for i in range(len(communities)):
        communities_dict[i] = set()
    for i in range(len(communities)):
        for j in range(len(communities[i])):
            communities_dict[i].add(list(communities[i])[j])
    # 遍历每个模块，计算每个节点的轮廓系数，然后求平均值
    Silhouette_Coefficient = 0
    for key, value in communities_dict.items():
        cluster = value
        # 如果该类只有一个模块，则跳过
        if len(cluster) == 1:
            continue
        # 计算该类的轮廓系数
        # a是该类中模块1到其他模块的平均距离
        # b是该类中模块1到其他类的其他模块的平均距离的最小值
        for modelar1 in cluster:
            # 计算a
            a = 0
            for modelar2 in cluster:
                if modelar1 != modelar2:
                    # 如果模块1和模块2之间有最小路径，则计算最小路径的长度
                    if nx.has_path(G, modelar1, modelar2):
                        a += nx.shortest_path_length(G, modelar1, modelar2)
                    elif nx.has_path(G, modelar2, modelar1):
                        a += nx.shortest_path_length(G, modelar2, modelar1)
                    else:
                        a += 100000
            a = a / (len(cluster) - 1)

            # 计算b
            b = float("inf")
            for key2, value2 in communities_dict.items():
                if key2 != key:
                    temp_b = 0
                    for modelar3 in value2:

                        # 如果模块1和模块3之间有最小路径，则计算最小路径的长度
                        if nx.has_path(G, modelar1, modelar3):
                            temp_b += nx.shortest_path_length(
                                G, modelar1, modelar3)
                        elif nx.has_path(G, modelar3, modelar1):
                            temp_b += nx.shortest_path_length(
                                G, modelar3, modelar1)
                        else:
                            temp_b += 100000

                    temp_b = temp_b / len(value2)
                    if temp_b < b:
                        b = temp_b

            # 计算轮廓系数
            Silhouette_Coefficient += (b - a) / max(a, b)

    Silhouette_Coefficient = Silhouette_Coefficient / len(G.nodes)

    return Silhouette_Coefficient


def Modular_list2dot(Modular_list, dot_file):
    for modular in Modular_list:
        modular.id = "Component" + str(Modular_list.index(modular)+1)
        # modular.label = modular.folder + "_" + str(Modular_list.index(modular)+1)

    dot = 'digraph Component_diagram {\n'
    dot += '\tlabel = \"Component_diagram of the project\";\n'
    component_index = 1
    for modular in Modular_list:
        label = "Component" + str(component_index) + "\l"
        # label
        for func in modular.func_set:
            file = func.func_file.split("/")[-1]
            label += file+": " + func.func_name + "\l"
        component_index += 1
        dot += '\t' + modular.id + ' [label=\"' + label + '\"];\n'
        for child in modular.children:
            line = '\t' + modular.id + ' -> ' + \
                child[0].id + ' [style='+child[1]+'];\n'
            if line not in dot:
                dot += line
            # dot+='\t' + modular.id + ' -> ' + child[0].id + ' [style='+child[1]+'];\n'
    dot += '}'
    with open(dot_file, 'w') as f:
        f.write(dot)

    # 生成png文件
    dot2png(dot_file, dot_file+'.png')


def modular_list2dot(Modular_list, dot_file):
    # for modular in Modular_list:
    #     if modular.id =="":
    #         modular.id = "Component" + str(Modular_list.index(modular)+1)
    # modular.label = modular.folder + "_" + str(Modular_list.index(modular)+1)
    Modular_list = set_name(Modular_list)
    dot = 'digraph Component_diagram {\n'
    dot += '\tlabel = \"Component_diagram of the project\";\n'
    dot += '\trankdir=RL;\n'
    dot += '\tgraph [compound=true];\n'
    component_index = 1
    for modular in Modular_list:
        comp = ""
        if modular.if_lib:
            subgraph = '\tsubgraph cluster_lib' + ' {\n'
            comp = "Library function component"
            subgraph += '\t\tlabel = \"Library function' + '\";\n'
        else:
            subgraph = '\tsubgraph cluster' + str(component_index) + ' {\n'
            comp = "Component" + str(component_index)
            subgraph += '\t\tlabel = \"' + modular.id + '\";\n'
            component_index += 1
        for func in modular.func_set:
            if "\\" in func.header_file:
                file = func.header_file.split("\\")[-1]
            else:
                file = func.header_file.split("/")[-1]
            subgraph += '\t\t' + func.id + \
                ' [label=\"' + file + ": " + func.func_name + \
                '\", comp = \"' + comp + '\"];\n'

        subgraph += '\t\tstyle=\"setlinewidth(2)\"'

        # 生成子图的边
        subgraph += '\t}\n'
        dot += subgraph
        # dot+='\t' + modular.id + ' -> ' + child[0].id + ' [style='+child[1]+'];\n'
    existence_line = []
    # 构建边
    for modular in Modular_list:
        for func1 in modular.func_set:
            for child in func1.children:
                line = '\t\t' + func1.id + ' -> ' + \
                    child[0] + ' [style='+child[1]+'];\n'
                dot += line

    dot += '}'
    with open(dot_file, 'w') as f:
        f.write(dot)

    # 生成png文件
    # dot2png(dot_file, dot_file+'.png')


def modular_list2dotwithoutcomp(Modular_list, dot_file):

    dot = 'digraph Component_diagram {\n'
    dot += '\tlabel = \"Component_diagram of the project\";\n'
    # dot+='\trankdir=RL;\n'
    # dot+='\tgraph [compound=true];\n'
    component_index = 1
    for modular in Modular_list:
        comp = ""
        subgraph = ""
        if modular.if_lib:
            comp = modular.id+"__"
        else:
            comp = modular.id+"__"
            component_index += 1

        for func in modular.func_set:
            file = func.func_file.split("/")[-1]
            key = func.key
            subgraph += '\t' + func.id + \
                ' [label=\"' + file + ": " + func.func_name + \
                '\", comp = \"' + comp + '\", key = \"' + key + '\"];\n'

        # 生成子图的边
        # subgraph += '\t}\n'
        dot += subgraph
        # dot+='\t' + modular.id + ' -> ' + child[0].id + ' [style='+child[1]+'];\n'
    existence_line = []
    # 构建边
    for modular in Modular_list:
        for func1 in modular.func_set:
            for child in func1.children:
                line = '\t\t' + func1.id + ' -> ' + \
                    child[0] + ' [style='+child[1]+'];\n'
                dot += line

    dot += '}'
    with open(dot_file, 'w') as f:
        f.write(dot)

    # 生成png文件
    # dot2png(dot_file, dot_file+'.png')


def Line_chart(num_map, Silhouette_Coefficient_map, file_name):
    # 根据字典绘制折线图
    # num_map是字典，key是聚类数量，value是该聚类数量下的模块化度
    # Silhouette_Coefficient_map是字典，key是聚类数量，value是该聚类数量下的轮廓系数
    # file_name是保存图片的文件名
    # 两个字典的key是一样的，两个折线图的x轴是一样的，只是y轴不一样，一个是模块化度，一个是轮廓系数
    # 画在一张图上
    # 使x轴的范围是1到最大的聚类数量
    x = range(1, len(num_map)+2)
    # 使y轴的范围是0到1
    y1 = []
    y2 = []
    for i in range(1, len(num_map)+2):
        if i in num_map:
            y1.append(num_map[i])
            y2.append(Silhouette_Coefficient_map[i])
        else:
            y1.append(0)
            y2.append(0)
    # plt.plot(x, y1, color='r', label='Modularity')
    plt.plot(x, y2, color='b', label='Silhouette_Coefficient')
    plt.legend()
    plt.xlabel('Number of clusters')
    plt.ylabel('Silhouette_Coefficient')
    plt.title('Silhouette_Coefficient of the project')
    plt.savefig(file_name)
    # 清空画布
    plt.clf()


def cal_modularity(G, clusters):
    # 计算模块度
    # 获得所有边
    edges = G.edges()
    # 获得所有节点
    nodes = G.nodes()
    # 获得所有节点的度
    degrees = G.degree()
    # 获得所有节点的度的和
    sum = 2 * G.number_of_edges()

    # 计算模块度
    modularity = 0
    temp_sum = 0
    for node1 in nodes:
        for node2 in nodes:
            temp = 0
            A = 0
            k1 = degrees[node1]
            k2 = degrees[node2]
            if node1 != node2:
                if (node1, node2) in edges or (node2, node1) in edges:
                    A = 1
                cluster1_index = -1
                cluster2_index = -1
                for cluster in clusters:
                    if node1 in cluster:
                        cluster1_index = clusters.index(cluster)
                    if node2 in cluster:
                        cluster2_index = clusters.index(cluster)
                if cluster1_index == cluster2_index:
                    temp = 1
                else:
                    temp = 0
                temp_sum += temp*(A-(k1*k2)/sum)
    modularity = temp_sum/sum
    return modularity


def set_name(Modular_list):
    # 给每个模块设置名字
    # 如果是库函数模块，名字为Library function component

    # 按Modular_list中函数数量从大到小排序
    Modular_list.sort(key=lambda x: len(x.func_set), reverse=True)

    # 获得所有模块内函数的文件夹
    # FILE = ""
    file_set = set()
    for modular in Modular_list:
        for func in modular.func_set:
            if func.func_file != "Library function":
                file_set.add(func.func_file.lower())
                # FILE = func.func_file
            else:
                modular.id = "Library function"

    # print(file_set)
    file_list = list(file_set)
    # 获取字符串的最长公共前缀

    def Solution(list):
        str = ''
        temp = zip(*list)
        for i in zip(*list):
            if len(set(i)) == 1:
                str += i[0]
            else:
                return str

    prefix = Solution(file_list)
    # prefix = FILE[:len(prefix)]

    comp_name_list = []
    # 文件夹次数字典
    for modular in Modular_list:
        if modular.id == "Library function":
            continue
        if len(modular.func_set) == 1:
            modular_name = list(modular.func_set)[0].func_name+" "
            modular.id = modular_name.split(':')[-1]
            comp_name_list.append(modular_name)
            continue

        filenum_dict = {}
        func_dict = {}
        for func in modular.func_set:
            if func.func_file != "Library function":
                # 删除公共前缀
                file = ""
                if prefix != None:
                    file = func.func_file.lower().replace(prefix, '') + "/" + func.func_name
                else:
                    file = func.func_file.lower() + "/" + func.func_name
                # 按照/分割
                temp_list = file.split('/')

                # 获得各级文件夹的名字
                file_name_list = []
                for i in range(len(temp_list)):
                    temp = ''
                    for j in range(i+1):
                        temp += temp_list[j] + '/'
                    file_name_list.append(temp[:-1])

                # 按照/数量从大到小排序
                file_name_list.sort(key=lambda x: len(
                    x.split("/")), reverse=True)

                # 获得各级文件夹的次数
                for file_name in file_name_list:
                    if file_name in filenum_dict and file_name.split('/')[-1].replace('.c', '').replace('.h', '')+" " not in comp_name_list:
                        filenum_dict[file_name] += 1
                    elif file_name.split('/')[-1].replace('.c', '').replace('.h', '')+" " not in comp_name_list:
                        filenum_dict[file_name] = 1
                    if file_name in func_dict and func not in func_dict[file_name]:
                        func_dict[file_name].append(func)
                    elif file_name not in func_dict:
                        func_dict[file_name] = [func]

        # 先按照次数从大到小排序再按照key长度从大到小排序
        filenum_dict = sorted(filenum_dict.items(),
                              key=lambda x: x[1], reverse=True)
        # 获得所有次数最大的文件夹名字
        name_list = []
        name_list.append(filenum_dict[0][0])
        for i in range(1, len(filenum_dict)):
            if filenum_dict[i][1] == filenum_dict[0][1]:
                if filenum_dict[i][0].split('/')[-1].replace('.c', '').replace('.h', '')+" " not in comp_name_list:
                    name_list.append(filenum_dict[i][0])
            else:
                break
        # 如果有多个次数最大的文件夹名字，选择包含的函数度最大的
        max_degree = 0
        max_name = ''
        if len(name_list) > 1:
            for name in name_list:
                degree = 0
                for func in func_dict[name]:
                    degree += len(func.children)+len(func.parents)
                if degree > max_degree and name.split('/')[-1].replace('.c', '').replace('.h', '')+" " not in comp_name_list:
                    max_degree = degree
                    max_name = name
            # comp_name_list.append(max_name)
        elif len(name_list) == 1:
            if name_list[0].split('/')[-1].replace('.c', '').replace('.h', '')+" " not in comp_name_list:
                max_name = name_list[0]
            else:
                max_name = name_list[0] + '_1'
            # comp_name_list.append(name_list[0])

        # 如果max_name为空，则选择模块中度最大的函数
        if max_name == '':
            max_degree = 0
            for func in modular.func_set:
                degree = len(func.children)+len(func.parents)
                if degree > max_degree:
                    max_degree = degree
                    max_name = func.func_name

        modular.id = max_name.split(
            '/')[-1].replace('.c', '').replace('.h', '')+" "
        comp_name_list.append(modular.id)

    return Modular_list


def get_lib_comp(PLCG_Modular_list, SDG_Modular_list):
    # 将PLCG中的库函数模块添加到SDG中

    # 存储SDG中的函数
    SDG_func_list = []
    for comp in SDG_Modular_list:
        for func in comp.func_set:
            SDG_func_list.append(func)
    lib_comp = None
    func_list = []
    for comp in PLCG_Modular_list:
        if comp.id == "Library function":
            lib_comp = comp

        for func in comp.func_set:
            func_list.append(func)
    if lib_comp != None:
        SDG_Modular_list.append(lib_comp)
    else:
        return SDG_Modular_list

    # 修改库函数模块中的函数的父子关系
    for func in lib_comp.func_set:
        new_parent_list = []
        for parent in func.parents:
            # 获取父函数信息
            parent_id = parent[0]
            parent_func = None
            for func1 in func_list:
                if func1.id == parent_id:
                    parent_func = func1
                    break
            parent_name = parent_func.func_name
            new_parent_func = None
            for func2 in SDG_func_list:
                if func2.func_name == parent_name:
                    new_parent_func = func2
                    break
            if new_parent_func == None:
                continue
            # 修改父函数的子函数
            new_parent_func.children.append((func.id, "solid"))
            # 修改子函数的父函数
            new_parent_list.append((new_parent_func.id, "solid"))
        func.parents = new_parent_list

    return SDG_Modular_list


def graph_read(graph_path):
    # 读取CG的dot文件
    G = nx.MultiDiGraph(nx.nx_pydot.read_dot(graph_path))

    return G


def cr(SDG, PLCG_Modular_list, func_header_source, project_name):
    # dot_file = 'PLCG\\tanchishe\\PLCG.dot'
    # G = graph_read(dot_file)
    func_information_list = get_func_information(SDG, 0, func_header_source)
    Modular_list = modularization(func_information_list)

    # modular_list2dot(Modular_list, dot_file+"_Modular_processing.dot")
    set_name(Modular_list)
    Modular_list = Preliminary_merger(Modular_list)
    # modular_list2dot(Modular_list, dot_file+"_Preliminary_merger.dot")
    set_name(Modular_list)
    Modular_list = Componentization(Modular_list)
    # modular_list2dot(Modular_list, dot_file+"_Componentization.dot")
    set_name(Modular_list)
    # Modular_list2dot(Modular_list, 'test/FLCG_Componentization.dot')
    Modular_list, modularity_map, Silhouette_Coefficient_map = GN(Modular_list)
    # Modular_list = set_name(Modular_list)
    # modular_list2dot(Modular_list, dot_file+"_GN.dot")
    # modular_list2dotwithoutcomp(Modular_list, dot_file+"_GNwithoutcomp.dot")
    set_name(Modular_list)
    # Line_chart(modularity_map, Silhouette_Coefficient_map, dot_file+"_Line_chart.png")
    # EchartsGraphComponent_diagram(dot_file+"_GNwithoutcomp.dot", dot_file+"_GNwithoutcomp.dot.html")
    SDG_Modular_list = get_lib_comp(PLCG_Modular_list, Modular_list)
    if not os.path.exists('temp/'+project_name):
        os.makedirs('temp/'+project_name)
    modular_list2dot(SDG_Modular_list, 'temp/'+project_name+"/_GN.dot")
    modular_list2dotwithoutcomp(
        SDG_Modular_list, 'temp/'+project_name+"/_GNwithoutcomp.dot")
    # EchartsGraphComponent_diagram(dot_file+"_GNwithoutcomp.dot", dot_file+"_GNwithoutcomp.dot.html")
    echarts_json = compgraph2json('temp/'+project_name+"/_GNwithoutcomp.dot")

    return Modular_list, echarts_json


def cr_cg(PLCG, func_header_source):
    # G = graph_read(dot_file)
    func_information_list = get_func_information(PLCG, 1, func_header_source)
    Modular_list = modularization(func_information_list)
    set_name(Modular_list)
    return Modular_list


def getdotfilelist(path):
    # 获取PLCG.dot文件列表
    dot_file_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file == 'PLCG.dot':
                dot_file_list.append(os.path.join(root, file))
    return dot_file_list


def deal_sdg(PLCG, SDG, func_header_source, project_name):
    # 处理SDG
    PLCG_Modular_list = cr_cg(PLCG, func_header_source)
    SDG_Modular_list, echarts_json = cr(SDG, PLCG_Modular_list, func_header_source, project_name)
    # dot2html
    return echarts_json


if __name__ == '__main__':
    # dot_file_list = ['PLCG\\saolei\\PLCG.dot','PLCG\\tanchishe\\PLCG.dot','PLCG\\wannianli\\PLCG.dot','PLCG\\wuziqi\\PLCG.dot','PLCG\\xiangqi\\PLCG.dot']
    # dot_file_list = getdotfilelist('PLCG')
    # for dot_file in dot_file_list:
    import sys
    # cr(sys.argv[1])
    deal_sdg(r"E:\C_master\C_app_0710\app\Design_recovery\project\Supercalendar")
    # deal_sdg("project/CUnit")
