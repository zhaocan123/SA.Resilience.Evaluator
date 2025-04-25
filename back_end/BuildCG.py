"""
构建CPP的CG
作者：刘梓轩
日期：2023年7月19日
"""
# 读取json文件
import json
import os
import networkx as nx
from app import app
import process_project
import GetBadTaste
import change_PLCG
import call_back
import layer_graph
import numpy as np
# import sdg
import subprocess


def run_cmd(cmd_str='', echo_print=1):
    """
    执行cmd命令，不显示执行过程中弹出的黑框
    备注：subprocess.run()函数会将本来打印到cmd上的内容打印到python执行界面上，所以避免了出现cmd弹出框的问题
    :param cmd_str: 执行的cmd命令
    :return: 
    """
    if echo_print == 1:
        print('\n执行cmd指令="{}"'.format(cmd_str))
    # run(cmd_str, shell=True)
    subprocess.run(cmd_str, shell=True)


class funcInfo:
    def __init__(self, name, file, funIn, funOut, Function_identification):
        self.name = name
        self.file = file
        self.funIn = funIn
        self.funOut = funOut
        self.if_lib = 0
        self.Function_identification = Function_identification


def get_json_data(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def get_func_info(data):
    # data为项目信息的字典
    func_info = []
    funcInfo_dict = data
    for func, info in funcInfo_dict.items():
        func_name = info['name']
        func_file = info['locateFile']
        func_in = info['fanIn']
        func_out = info['fanOut']
        func_info.append(funcInfo(func_name, func_file, func_in, func_out, func))

    PLCG = {}
    # 根据路径和函数名生成调用关系
    for func in func_info:
        if func.Function_identification not in PLCG:
            PLCG[func.Function_identification] = []
        for fan in func.funOut:
            if fan not in PLCG[func.Function_identification]:
                PLCG[func.Function_identification].append(fan)

    # 根据PLCG构建FLCG
    FLCG = {}
    for key, value in PLCG.items():
        file_path = key.split(':')[0] + ":" + key.split(':')[1]
        if file_path not in FLCG:
            FLCG[file_path] = []
        for fan in value:
            called_file_path = fan.split(':')[0]+":" + fan.split(':')[1]
            if called_file_path not in FLCG[file_path] and called_file_path != file_path:
                FLCG[file_path].append(called_file_path)

    CG = {}
    CG['PLCG'] = PLCG
    CG['FLCG'] = FLCG

    return CG

# 根据PLCG和FLCG获取js


def get_js_from_PLCG(PLCG, data, js_path):
    data_list = []
    link_list = []
    categories = [
        {
            "name": "C"
        },
        {
            "name": "C++"
        }
    ]
    func_id = 0
    for func, info in data.items():
        temp_dict = {}
        name = info["name"]
        temp_dict["name"] = name
        temp_dict["id"] = func
        temp_dict["file"] = info["locateFile"].split('/')[-1]
        if info['type'] == 'Method':
            temp_dict["name"] = info['locateClass'] + ": " + name
        func_id += 1
        source_file = info['source']
        if source_file[-2:] == ".c" or source_file[-2:] == ".h":
            temp_dict["category"] = 0
        else:
            temp_dict["category"] = 1

        temp_dict["symbolSize"] = 45
        temp_dict["fixed"] = False
        temp_dict["itemStyle"] = {
            "normal": {
                "opacity": 1
            }
        }
        # 出度
        temp_dict["outDegree"] = len(info["fanOut"])
        # 入度
        temp_dict["inDegree"] = len(info["fanIn"])
        data_list.append(temp_dict)

    for key, value in PLCG.items():
        for fan in value:
            temp_dict = {}
            temp_dict["source"] = key
            temp_dict["target"] = fan
            temp_dict["symbol"] = [
                "none",
                "arrow"
            ]
            temp_dict["lineStyle"] = {
                "normal": {
                    "width": 2,
                    "curveness": 0.2,
                    "type": "solid",
                            "opacity": 1
                }
            }
            link_list.append(temp_dict)

    PLCG_G = nx.DiGraph()
    for key, value in PLCG.items():
        PLCG_G.add_node(key)
        for value1 in value:
            if value1 not in PLCG_G.nodes:
                PLCG_G.add_node(value1)
        for fan in value:
            PLCG_G.add_edge(key, fan)

    # 最大出度
    max_out_degree = max(PLCG_G.out_degree, key=lambda x: x[1])[0]+'()'
    max_out_degree_val = max(PLCG_G.out_degree, key=lambda x: x[1])[1]
    # 最小出度
    min_out_degree = min(PLCG_G.out_degree, key=lambda x: x[1])[0]+'()'
    min_out_degree_val = min(PLCG_G.out_degree, key=lambda x: x[1])[1]
    # 平均出度
    avg_out_degree = sum([d[1] for d in PLCG_G.out_degree])/len(PLCG_G.out_degree)
    # 最大入度
    max_in_degree = max(PLCG_G.in_degree, key=lambda x: x[1])[0]+'()'
    max_in_degree_val = max(PLCG_G.in_degree, key=lambda x: x[1])[1]
    # 最小入度
    min_in_degree = min(PLCG_G.in_degree, key=lambda x: x[1])[0]+'()'
    min_in_degree_val = min(PLCG_G.in_degree, key=lambda x: x[1])[1]
    # 平均入度
    avg_in_degree = sum([d[1] for d in PLCG_G.in_degree])/len(PLCG_G.in_degree)

    in_degree_0 = []
    out_degree_0 = []
    for key, value in PLCG_G.out_degree:
        if value == 0:
            out_degree_0.append(key)
    for key, value in PLCG_G.in_degree:
        if value == 0:
            in_degree_0.append(key)
    # 获取所有简单路径，起点为入度为0的节点，终点为出度为0的节点
    simple_path = []
    for in_degree_node in in_degree_0:
        for out_degree_node in out_degree_0:
            simple_path.extend(nx.all_simple_paths(PLCG_G, in_degree_node, out_degree_node))
    # 最长调用路径
    if len(simple_path) == 0:
        max_call_path = []
    else:
        max_call_path = max(simple_path, key=lambda x: len(x))
    # 最短调用路径
    if len(simple_path) == 0:
        min_call_path = []
    else:
        min_call_path = min(simple_path, key=lambda x: len(x))
    # 平均调用路径
    if len(simple_path) == 0:
        avg_call_path = 0
    else:
        avg_call_path = sum([len(x) for x in simple_path])/len(simple_path)

    js_data = {}
    js_data["data"] = data_list
    js_data["links"] = link_list
    js_data["categories"] = categories
    js_data["maxOutFunc"] = max_out_degree.split('/')[-1] + '(' + str(max_out_degree_val) + ')'
    js_data["minOutFunc"] = min_out_degree.split('/')[-1] + '(' + str(min_out_degree_val) + ')'
    js_data["avgOut"] = avg_out_degree
    js_data["maxInFunc"] = max_in_degree.split('/')[-1] + '(' + str(max_in_degree_val) + ')'
    js_data["minInFunc"] = min_in_degree.split('/')[-1] + '(' + str(min_in_degree_val) + ')'
    js_data["avgIn"] = avg_in_degree
    js_data["maxCallPath"] = max_call_path
    js_data["minCallPath"] = min_call_path
    js_data["avgCallPath"] = avg_call_path

    # 写入到js文件中
    return js_data


def get_js_from_FLCG(FLCG, data, js_path):
    data_list = []
    link_list = []
    categories = [
        {
            "name": "Header file"
        },
        {
            "name": "C Source file"
        },
        {
            "name": "C++ Source file"
        }
    ]
    file_id = 0

    for file, info in data.items():
        temp_dict = {}
        temp_dict["name"] = info["name"]
        temp_dict["id"] = file
        file_id += 1
        if file.endswith((".h", ".H", ".hh", ".hpp", ".hxx")):
            temp_dict["category"] = 0
        elif file.endswith((".c")):
            temp_dict["category"] = 1
        else:
            temp_dict["category"] = 2
        temp_dict["symbolSize"] = 45
        temp_dict["fixed"] = False
        temp_dict["itemStyle"] = {
            "normal": {
                "opacity": 1
            }
        }
        # 出度
        temp_dict["outDegree"] = len(info["fanOut"])
        # 入度
        temp_dict["inDegree"] = len(info["fanIn"])
        # 包含函数个数
        temp_dict["funcNum"] = len(info["functionList"])
        data_list.append(temp_dict)

    for key, value in FLCG.items():
        for fan in value:
            temp_dict = {}
            temp_dict["source"] = key
            temp_dict["target"] = fan
            temp_dict["symbol"] = [
                "none",
                "arrow"
            ]
            temp_dict["lineStyle"] = {
                "normal": {
                    "width": 2,
                    "curveness": 0.2,
                    "type": "solid",
                            "opacity": 1
                }
            }
            link_list.append(temp_dict)

    FLCG_G = nx.DiGraph()
    for key, value in FLCG.items():
        FLCG_G.add_node(key)
        for value1 in value:
            if value1 not in FLCG_G.nodes:
                FLCG_G.add_node(value1)
        for fan in value:
            FLCG_G.add_edge(key, fan)

    # 最大出度
    max_out_degree = max(FLCG_G.out_degree, key=lambda x: x[1])[0]
    max_out_degree_val = max(FLCG_G.out_degree, key=lambda x: x[1])[1]
    # 最小出度
    min_out_degree = min(FLCG_G.out_degree, key=lambda x: x[1])[0]
    min_out_degree_val = min(FLCG_G.out_degree, key=lambda x: x[1])[1]
    # 平均出度
    avg_out_degree = sum([d[1] for d in FLCG_G.out_degree])/len(FLCG_G.out_degree)
    # 最大入度
    max_in_degree = max(FLCG_G.in_degree, key=lambda x: x[1])[0]
    max_in_degree_val = max(FLCG_G.in_degree, key=lambda x: x[1])[1]
    # 最小入度
    min_in_degree = min(FLCG_G.in_degree, key=lambda x: x[1])[0]
    min_in_degree_val = min(FLCG_G.in_degree, key=lambda x: x[1])[1]
    # 平均入度
    avg_in_degree = sum([d[1] for d in FLCG_G.in_degree])/len(FLCG_G.in_degree)

    in_degree_0 = []
    out_degree_0 = []
    for key, value in FLCG_G.out_degree:
        if value == 0:
            out_degree_0.append(key)
    for key, value in FLCG_G.in_degree:
        if value == 0:
            in_degree_0.append(key)
    # 获取所有简单路径，起点为入度为0的节点，终点为出度为0的节点
    simple_path = []
    for in_degree_node in in_degree_0:
        for out_degree_node in out_degree_0:
            simple_path.extend(nx.all_simple_paths(FLCG_G, in_degree_node, out_degree_node))
    # 最长调用路径
    if len(simple_path) == 0:
        max_call_path = []
    else:
        max_call_path = max(simple_path, key=lambda x: len(x))
    # 最短调用路径
    if len(simple_path) == 0:
        min_call_path = []
    else:
        min_call_path = min(simple_path, key=lambda x: len(x))
    # 平均调用路径
    if len(simple_path) == 0:
        avg_call_path = 0
    else:
        avg_call_path = sum([len(x) for x in simple_path])/len(simple_path)

    js_data = {}
    js_data["data"] = data_list
    js_data["links"] = link_list
    js_data["categories"] = categories
    js_data["maxOutFunc"] = max_out_degree.split('/')[-1] + '(' + str(max_out_degree_val) + ')'
    js_data["minOutFunc"] = min_out_degree.split('/')[-1] + '(' + str(min_out_degree_val) + ')'
    js_data["avgOut"] = avg_out_degree
    js_data["maxInFunc"] = max_in_degree.split('/')[-1] + '(' + str(max_in_degree_val) + ')'
    js_data["minInFunc"] = min_in_degree.split('/')[-1] + '(' + str(min_in_degree_val) + ')'
    js_data["avgIn"] = avg_in_degree
    js_data["maxCallPath"] = max_call_path
    js_data["minCallPath"] = min_call_path
    js_data["avgCallPath"] = avg_call_path

    return js_data


def get_func_key(func_name, param_list, file_info, type):
    for func_info in file_info['functionList']:
        name = func_info[0].split('(')[0].split(' ')[-1]
        param_list1 = func_info[0].split('(')[1].split(')')[0].split(',')
        if name == func_name:
            # find = 0
            # if type == 1:
            #     if len(param_list) != len(param_list1):
            #         find = 1
            #     else:
            #         for i in range(len(param_list)):
            #             param1 = param_list[i]
            #             param2 = param_list1[i].split(' @@ ')[0]
            #             if param1 != param2:
            #                 find = 1
            #                 break
            # if find == 0:
            func_key = func_info[-2]
            return func_key


# 根据PLCG和FLCG计算信息
def cal_metric_from_CG(dominate_matrixes, cfg_data, func_data, file_data, bad_smell_data, comp_data):  # 新增的参数：函数-》组件对应关系
    print("计算指标1")
    # 系统级函数圈复杂度信息
    func_cyc = {}
    func_cfg = {}
    for key, value in cfg_data.items():
        if value == None:
            continue
        for func, cfg in value.items():
            cyc = nx.number_of_edges(cfg) - nx.number_of_nodes(cfg) + 2
            key = key.replace('\\', '/')
            file_info = file_data[key]
            func_name = func.split('(')[0]
            param_list = []
            type = 0
            if '(' in func:
                param_list = func.split('(')[1].split(')')[0].split(',')
                type = 1

            func_key = get_func_key(func_name, param_list, file_info, type)
            if func_key != None:
                func_cfg[func_key] = cfg
                func_cyc[func_key] = cyc
                # 保存到project_data中
                func_data[func_key]['cyclComplexity'] = func_cyc[func_key]

    # 遍历所有函数，如果没有圈复杂度信息，则将其圈复杂度设为0
    for key, value in func_data.items():
        if 'cyclComplexity' not in value:
            func_data[key]['cyclComplexity'] = 0
    # 计算每个文件的圈复杂度
    for file_key, file_info in file_data.items():
        max_cyc = 0
        for func_info in file_info['functionList']:
            func_key = func_info[-2]
            if func_key in func_data:
                if func_data[func_key]['cyclComplexity'] > max_cyc:
                    max_cyc = func_data[func_key]['cyclComplexity']
        file_data[file_key]['cyclComplexity'] = max_cyc

    print("计算指标2")

    # 代码克隆
    cfg_copy = []
    for key1, cfg1 in func_cfg.items():
        for key2, cfg2 in func_cfg.items():
            if key1 != key2:
                # 为了加快速度，不再重新生成dt和dm
                # 这里需要直接比较dominate_matrixes里的cfg而不是调用函数了
                souce1 = func_data[key1]['source']
                file1 = souce1.replace('/', '\\')
                func1 = key1.split(":")[-1]
                new_key1 = (file1, func1)
                source2 = func_data[key2]['source']
                file2 = source2.replace('/', '\\')
                func2 = key2.split(":")[-1]
                new_key2 = (file2, func2)
                # print(dominate_matrixes.keys())
                # print(new_key1, new_key2)
                # 但是这里的key和domainate_matrixes里的key不一样，所以需要转换一下还没写
                if new_key1 in dominate_matrixes and new_key2 in dominate_matrixes:
                    if np.array_equal(dominate_matrixes[new_key1], dominate_matrixes[new_key2]):
                        matched_func1 = [key1, key2]
                        matched_func2 = [key2, key1]
                        if matched_func1 not in cfg_copy and matched_func2 not in cfg_copy:
                            cfg_copy.append(matched_func1)
                else:
                    print("one of keys not in dominate_matrixes", new_key1, new_key2)

    bad_smell_data["cfg_copy"] = cfg_copy
    # print(cfg_copy)

    # # 计算组件冗余

    # use comp_data (call_back_json)
    # convert comp_data from json to dict
    comp_datas = json.loads(comp_data)["data"]
    comp_links = json.loads(comp_data)["links"]
    comp = {}
    func = {}
    comp_id_dict = {}
    for functioninfo in comp_datas:
        if functioninfo["comp"] == 0:
            comp_name = str(int(functioninfo["category"]))
            function_name = functioninfo["label"]
            if comp_name not in comp:
                comp[comp_name] = []
            comp[comp_name].append(function_name)
            func[function_name] = comp_name
        else:
            comp_id_dict[functioninfo["id"]] = functioninfo["category"]
    # # 用nx读取dot文件
    # comp_nx = nx.MultiDiGraph(nx.nx_pydot.read_dot("_GNwithoutcomp.dot"))
    # comp = {}
    # func = {}
    # for node in comp_nx.nodes:
    #     node_info = comp_nx.nodes[node]
    #     if 'label' not in node_info:
    #         continue
    #     comp_name = ''
    #     if ' __' not in node_info['label']:
    #         comp_name = node_info['label'].replace('"', '')
    #     else:

    #         comp_name = node_info['comp'].replace('"', '')[:-3]
    #     if ':' in comp_name:
    #         comp_name = comp_name.split(':')[-1]
    #     if comp_name not in comp:
    #         comp[comp_name] = []
    #     func_name = node_info['key'].replace('"', '')
    #     comp[comp_name].append(func_name)
    #     func[func_name] = comp_name
    # 计算组件冗余
    comp_redundancy_set = set()
    comp_redundancy = []
    for cfgs in cfg_copy:

        comp1 = func[cfgs[0]]
        comp2 = func[cfgs[1]]
        if comp1 != comp2:
            comp_redundancy.append([comp1, comp2])
            comp_redundancy_set.add(comp1)
            comp_redundancy_set.add(comp2)

    #  # 获取各个组件的父组件
    # comp_parent = {}
    # for key, value in comp.items():
    #     # 获取组件的父组件
    #     temp_parent = []
    #     for node in value:
    #         if node not in comp_nx.nodes:
    #             continue
    #         for parent in comp_nx.predecessors(node):
    #             if parent not in value:
    #                 temp_parent.append(parent)
    #     comp_parent[key] = []
    #     for node in temp_parent:
    #         parent_comp = comp_nx.nodes[node]["comp"].replace("\"", "")
    #         if parent_comp not in comp_parent[key]:
    #             comp_parent[key].append(parent_comp)

    # Standalone_components_list = []
    # for key, value in comp_parent.items():
    #     if len(value) == 0:
    #         Standalone_components_list.append(key)

    Standalone_components_list = set(comp.keys())
    for linkinfo in comp_links:
        if linkinfo["source"] in comp_id_dict and linkinfo["target"] in comp_id_dict:
            source = comp_id_dict[linkinfo["source"]]
            target = comp_id_dict[linkinfo["target"]]
            # remove source and target's comp from Standalone_components_list
            if source in Standalone_components_list:
                Standalone_components_list.remove(source)
            if target in Standalone_components_list:
                Standalone_components_list.remove(target)

    return func_data, bad_smell_data, file_data, [len(comp_redundancy_set), len(comp.keys())], [len(Standalone_components_list), len(comp.keys())]


def build_CG_tree(project_path, project_name, file_list, id_num):
    root = {}
    root["id"] = id_num
    root["label"] = project_name
    root["path"] = project_path.replace('\\', '/')
    root["children"] = []
    # 判断project_path是文件还是目录
    if os.path.isfile(project_path):
        root["type"] = "source"
    else:
        root["type"] = "folder"
        # 获取peoject_path的直接子目录和文件
        for file in os.listdir(project_path):
            file = os.path.join(project_path, file)
            file = file.replace('\\', '/')
            # 判断file是文件还是目录
            if os.path.isdir(file):
                file_name = file.split('/')[-1]
                id_num += 1
                node = build_CG_tree(file, file_name, file_list, id_num)
                if node != None:
                    root["children"].append(node)
            else:
                if file in file_list:
                    file_name = file.split('/')[-1]
                    node = build_CG_tree(file, file_name, file_list, id_num)
                    if node != None:
                        root["children"].append(node)
    return root


def get_info_from_func(func_data):
    # 获取所有入度为0的函数和所有函数的头文件和源文件
    in_degree_0 = []
    func_header_source = {}
    for key, value in func_data.items():
        if len(value['fanIn']) == 0:
            in_degree_0.append(key)
        func_header_source[key] = [value['source'], value['header']]

    return in_degree_0, func_header_source


def BUILDCG_main(file_list, project_path, project_name, nxplcg: nx.DiGraph, in_degree_0, func_header_source, comp_data):
    print("BUILDCG_main", project_path, project_name)
    # 读取json文件
    func_json_file = project_path + "/funcInfo.json"
    func_data = get_json_data(func_json_file)
    CG = get_func_info(func_data)
    print("BUILDCG_main, 1")
    # 根据PLCG和FLCG计算指标
    # cal_metric_from_CG(data['PLCG'], data['FLCG'])
    # 根据PLCG和FLCG生成js
    js_path = os.path.join(os.path.dirname(__file__), 'PLCG.js')
    PLCG = get_js_from_PLCG(CG['PLCG'], func_data, 'PLCG.js')
    file_json_file = project_path + "/codeFileInfo.json"
    file_data = get_json_data(file_json_file)
    js_path = os.path.join(os.path.dirname(__file__), 'FLCG.js')
    FLCG = get_js_from_FLCG(CG['FLCG'], file_data, 'FLCG.js')
    print("BUILDCG_main, 2")
    # 计算信息和坏味
    # 获取CFG信息
    data = {}
    data['funcInfo'] = func_data
    cfg_data, pdg_data, graph_json, dominate_matrixes = process_project.process_project_to_json(file_list, project_path)
    
    graph_json['PLCG'] = PLCG
    # change_PLCG.change_PLCG(func_data,'E:/CPP_master/dev0807/CPP_support/uploads/saoleiqqq/code/code')
    graph_json['FLCG'] = FLCG
    file_tree = []
    root = build_CG_tree(project_path, project_name, file_data.keys(), 1)
    file_tree.append(root)
    graph_json['CG_js'] = str(file_tree)

    print("BUILDCG_main, 2.5")
    # construct sdg and function level sdg

    print("BUILDCG_main, 3")
    func_data, bad_smell_data, file_data, Component_redundancy, Standalone_components = cal_metric_from_CG(dominate_matrixes, cfg_data, func_data, file_data, {}, comp_data)
    print("BUILDCG_main, 4")
    # 输出到json文件中
    with open(func_json_file, 'w', encoding='utf-8') as f:
        json.dump(func_data, f, indent=4)
    with open(file_json_file, 'w', encoding='utf-8') as f:
        json.dump(file_data, f, indent=4)
        bad_smell = GetBadTaste.Bad_smell_from_function(data)
    bad_smell["funcCopy"]['cfg_copy'] = bad_smell_data['cfg_copy']
    bad_smell_json_file = project_path + "/badSmell_fromfunc.json"
    with open(bad_smell_json_file, 'w', encoding='utf-8') as f:
        json.dump(bad_smell, f, indent=4)
    print("BUILDCG_main, 5")
    with open(app.config.get("EXE_PATH") + "/static/PLCG.js", 'w') as f:
        f.write("var graph = ")
        json.dump(PLCG, f, indent=4)

    with open(app.config.get("EXE_PATH") + "/static/FLCG.js", 'w') as f:
        f.write("var graph = ")
        json.dump(FLCG, f, indent=4)
    if not os.path.exists("temp/" + project_name):
        os.makedirs("temp/" + project_name)
    with open("temp/" + project_name + "/PLCG.json", 'w') as f:
        json.dump(CG["PLCG"], f, indent=4)
    print("BuildCG finished")
    return func_data, bad_smell, graph_json, CG, file_data, Component_redundancy, Standalone_components


if __name__ == "__main__":

    project_path = r"E:\CPP_master\dev0815\CPP_support\back_end\project\c-cpp"
    # load json str from
    comp_data = r"static\callback.js"
    # with open(comp_data, 'r', encoding='utf-8') as f:
    #     comp_data = f.read()
    BUILDCG_main(project_path, 'CUnit', None, None, None, comp_data)
