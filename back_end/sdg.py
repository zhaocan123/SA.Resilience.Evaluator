# sdg all in one
import multiprocessing
from typing import List, Dict
import networkx as nx
import sys
import os
import re
import random
import json
import copy
import pydot
from math import ceil
from pyecharts.commons.utils import JsCode
import pyecharts.charts
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode

from utils import get_file_encoding

pwd = os.getcwd()
pwd = pwd.replace("\\", "/")
print("sdg.py: pwd = ", pwd)
with open(pwd + "//config.json", "r", encoding="utf-8") as f:
    content = json.load(f)
DOT_EXE_FILE_PATH = content["DOT_EXE_FILE_PATH"]
RESERVED_WORDS = content["RESERVED_WORDS"]
GET_CALL_EXE = content["GET_CALL_EXE"]
GET_FUNCTION_EXE = content["GET_FUNCTION_EXE"]


def code_preprocess(project_path: str):
    """
    analysis every code file in this project for their call info and parameter info
    """
    # iterate every code file in the code folder under the project path folder
    for root, dirs, files in os.walk(os.path.join(project_path, "code")):
        for file in files:
            if file[-2:] == ".c":
                code_file_path = os.path.join(root, file)
                # print(code_file_path)
                # check if call info file exists
                if not os.path.exists(code_file_path + ".call"):
                    # generate call info file
                    os.system(GET_CALL_EXE + " " + code_file_path)
                # check if parameter info file exists
                if not os.path.exists(code_file_path + ".parameter"):
                    # generate parameter info file
                    os.system(GET_FUNCTION_EXE + " " + code_file_path)


def preprocess_pdg(pdg: nx.MultiDiGraph, code_file_path: str, function_name: str):
    """
    preprocess each pdg's call node to add additional information for further analysis
    """
    calling_info = {}
    try:
        pdg.remove_node("\\n")
    except:
        pass
    one_flag = "_" + code_file_path.replace("/", "_").replace(
        "\\", "_").replace(".", "_").replace(":", "_") + "_" + function_name
    relabel = {}
    for node in list(pdg.nodes):
        relabel[node] = node + one_flag
        # if node starts does not with "Node", randomly generate a node name
        # if not node.startswith("Node"):
        #     # set the node id to a random string
        #     # print(node)
        #     pdg = nx.relabel_nodes(pdg, {node: node.strip('"').replace("-","_")})
    pdg = nx.relabel_nodes(pdg, relabel)
    for node in list(pdg.nodes):
        # set node's code_file_path = code_file_path
        pdg.nodes[node]['code_file_path'] = code_file_path
    for node in pdg.nodes:
        re_expression = r"[a-zA-Z_][a-zA-Z0-9_]*\(.*\)"
        node_type = "expression"
        code_text = pdg.nodes[node]["label"].strip().strip(
            '"').strip().strip('{').strip('}').strip('\l').split('\l')[-1]
        if "ENTRY" in code_text:
            node_type = "entry"
        if code_text.split()[0] == "return":
            node_type = "return"
            pdg.nodes[node]["variable_name"] = '"' + code_text.split()[1] + '"'
        current_info = []
        match = re.search(re_expression, code_text)
        all_matches = []
        if match:
            all_matches = [match]
        matches_num = 0
        while len(all_matches) > 0:
            match = all_matches.pop()
            # print(code_text, match)
            # get the function name before "("
            function_name = match.group(0).split("(")[0]

            if function_name not in RESERVED_WORDS:
                matches_num += 1
                node_type = "call"
                current_call = {}
                # set call informations for this node
                current_call["function_name"] = function_name
                # get the parameters
                start_index = match.group(0).find("(")+1
                count = 1
                end_index = start_index
                while end_index < len(match.group(0)):
                    if match.group(0)[end_index] == ")":
                        count -= 1
                    if match.group(0)[end_index] == "(":
                        count += 1
                    if count == 0:
                        break
                    end_index += 1

                parameter_text = match.group(0)[start_index:end_index].strip()
                # print(function_name, parameter_text)
                current_parameters = []
                l_index = 0
                r_index = 0
                count = 0
                while r_index < len(parameter_text):
                    if parameter_text[r_index] == ")":
                        count -= 1
                    if parameter_text[r_index] == "(":
                        count += 1
                    if count == 0 and parameter_text[r_index] == ',':
                        current_parameters.append(
                            parameter_text[l_index:r_index])
                        l_index = r_index + 1
                    r_index += 1
                if l_index < r_index:
                    current_parameters.append(parameter_text[l_index:r_index])
                current_call["parameters"] = current_parameters
                # get the return value
                if match.span()[1] > 1 and "=" in code_text[:match.span()[0]]:
                    var_index = code_text[:match.span()[0]].find("=")
                    current_call["return_variable"] = code_text[:var_index]
                else:
                    if matches_num > 1:
                        current_call["return_variable"] = "TEMP"
                    else:
                        current_call["return_variable"] = None
            # print(current_call)
                current_info.append(current_call)

            # print(code_text)
            code_text = code_text[code_text.find("(", match.span()[0])+1:]
            match = re.search(re_expression, code_text)
            if match:
                all_matches.append(match)
            # print(code_text)

        pdg.nodes[node]["type"] = node_type

        calling_info[node] = current_info
    # nx.nx_pydot.write_dot(pdg, "pdg.dot")
    # raise ValueError
    return pdg, calling_info


def find_pdg_according_to_code_file_path(all_pdgs: dict, code_file_path: str, function_name: str, project_path: str):
    """
    find the pdg according to the code file path
    """
    # 直接从all_pdgs中寻找对应的函数的pdg而不是和之前一样从文件夹中寻找pdg的dot文件
    # 返回pdg和pdg中的调用信息
    if code_file_path not in all_pdgs.keys():
        return None
    if function_name not in all_pdgs[code_file_path].keys():
        return None
    return preprocess_pdg(all_pdgs[code_file_path][function_name], code_file_path, function_name)
    # relative_path = os.path.join("graphs", os.path.relpath(
    #     code_file_path, os.path.join(project_path, "code")))
    # relative_path = relative_path.replace("\\", '/')
    # folder_path = relative_path.split(".c")[0] + "_c"
    # file_path = "processed_" + function_name + ".pdg.dot"
    # pdg_file_path = os.path.join(project_path, folder_path, file_path)
    # if not os.path.exists(pdg_file_path):
    #     return None
    # pdg = nx.MultiDiGraph(nx.nx_pydot.read_dot(pdg_file_path))
    # pdg, calling_info = preprocess_pdg(pdg, code_file_path, function_name)
    # # nx.nx_pydot.write_dot(pdg, "pdg.dot")
    # return pdg, calling_info


def find_call_info_according_to_code_file_path(code_file_path: str):
    """
    find the call info file path according to the code file path
    """
    call_info_file_path = code_file_path + ".call"
    return call_info_file_path


def find_parameter_info_according_to_code_file_path(code_file_path: str, function_name: str):
    """
    find the parameter info file path according to the code file path
    """
    parameter_info_file_path = code_file_path + ".parameter"
    parameter_infos = []
    encoding = get_file_encoding(parameter_info_file_path)
    with open(parameter_info_file_path, 'r', encoding=encoding) as f:
        for line in f:
            temp = line.split(";")
            if temp[0].strip() == function_name:
                if len(temp) > 4:
                    # get useful info from the 5th, 7th, ... to the last element of temp
                    parameter_infos = temp[5::2]
    return parameter_infos


def decode_call_info_file(call_info_file: str, function_name: str, func_def_dict: dict):
    """
    find the call info according to the call info file path
    Return: 
        call_infos: dict
            key: called function name
            value: called function code file path
    """
    call_infos = dict()
    encoding = get_file_encoding(call_info_file)
    with open(call_info_file, "r", encoding=encoding) as f:
        for line in f:
            if len(line.strip()) > 2:
                # remove the "{" and "}"
                line = line.strip()[1:-1]
                # split the line by ","
                temp = line.split(",")[:-1]
                if len(temp) > 1:
                    for i, t in enumerate(temp):
                        # remove the "[" and "]"
                        current_call = t.strip()[1:-1]
                        # split by "::"
                        current_info = current_call.split(";;")
                        # print("current_info",function_name,'\n',current_info)
                        if i == 0:
                            if current_info[2].strip() != function_name:
                                break
                        else:
                            # get the path from current_info[0] before second ":"
                            if current_info[0].count(":") > 1:
                                path = current_info[0].split(
                                    ":")[0] + ":" + current_info[0].split(":")[1]
                                # print(path)
                                # this is absolute path, we need to convert it to relative path
                                # if this is a header file
                                if path[-2:] == ".h":
                                    # find the corrsponding source file according to header-source table
                                    try:
                                        path = func_def_dict[current_info[2].strip(
                                        ) + ":" + os.path.abspath(path)]
                                    except KeyError:
                                        print("Not fuound header file KeyError: ", current_info[2].strip(
                                        ) + ":" + os.path.abspath(path))
                                    # with open("CUnit/graphs/fun_definitions.txt", "r") as f:
                                    #     lines = f.readlines()
                                    #     for line in lines:
                                    #         if len(line.strip()) > 1:
                                    #             temp = line.strip().split("::")
                                    #             if current_info[2].strip() == temp[0]:
                                    #                 if os.path.samefile(temp[1], path):
                                    #                     path = temp[2]

                                # # get current absolute path
                                # current_path = os.getcwd()
                                # # use os module to get the relative path
                                # try:
                                #     path = os.path.relpath(path, current_path)
                                #     path = path.replace("\\", "/")
                                # except ValueError:
                                #     continue
                                path = os.path.abspath(path).replace("\\", "/")

                            else:
                                path = current_info[0]
                            call_infos[current_info[2].strip()] = path
    return call_infos


def add_pgd_to_sdg(sdg: nx.MultiDiGraph, pdg: nx.MultiDiGraph, call_node: str, parameters: List[str], call_function_name: str, pdg_calling_info: Dict, call_file_path: str, called_file_path: str, is_expanded=False):
    """
    This function add a pdg to the sdg
    """
    # copy sdg
    # sdg = sdg.copy()
    # find entry node of pdg
    entry_node = None
    for node in pdg.nodes:
        if pdg.nodes[node]['type'] == 'entry':
            entry_node = node
            break

    # add pdg into sdg
    if not is_expanded:
        sdg.add_nodes_from(pdg.nodes(data=True))
        sdg.add_edges_from(pdg.edges(data=True))
    # then find the reture node of pdg
    return_node = None
    entry_node = None
    for node in pdg.nodes:
        if pdg.nodes[node]['type'] == 'return':
            return_node = node
        if pdg.nodes[node]['type'] == 'entry':
            entry_node = node
        else:
            sdg.nodes[node]['label'] = '"{' + pdg_calling_info['function_name'] + \
                ":" + pdg.nodes[node]['label'].strip('"')[1:-1] + '}"'

    # re-name entry node
    sdg.nodes[entry_node]['label'] = '"{' + \
        pdg_calling_info['function_name'] + ":ENTRY" + '}"'

    # sdg add edge from call node to entry node
    sdg.add_edge(call_node, entry_node)

    actual_in_nodes = []
    # add actual-in nodes to the sdg

    call_node_flag = "_" + call_file_path.replace("/", "_").replace(
        "\\", "_").replace(".", "_") + "_" + call_function_name

    for index, parameter in enumerate(parameters):
        # random generate 12bit hex id
        actual_in_id = "Node0x" + \
            str(hex(random.randint(0, 2**48))) + call_node_flag
        actual_in_nodes.append(actual_in_id)
        try:
            sdg.add_node(actual_in_id, type="actual_in", code_file_path=call_file_path,
                         label='"{'+call_function_name+":"+parameter+"_in="+pdg_calling_info['parameters'][index]+'}"', shape="record")
        except:
            print("unrecognized function call",
                  pdg_calling_info['function_name'])
            # print(call_function_name, pdg_calling_info['function_name'], parameters, pdg_calling_info['parameters'])
        # these are control dependency edges
        sdg.add_edge(call_node, actual_in_id)

    if pdg_calling_info["return_variable"] != None:

        # add actual-out nodes to the pdg
        if return_node != None:
            actual_out_id = "Node0x" + \
                str(hex(random.randint(0, 2**48))) + call_node_flag
            sdg.add_node(actual_out_id, type="actual_out", code_file_path=call_file_path,
                         label='"{'+call_function_name+":"+pdg_calling_info["return_variable"]+"=out" + '}"', shape="record")
            sdg.add_edge(call_node, actual_out_id)

    called_node_flag = "_" + called_file_path.replace("/", "_").replace(
        "\\", "_").replace(".", "_") + "_" + pdg_calling_info['function_name']

    formal_in_nodes = []
    # add formal-in nodes to the pdg
    for parameter in parameters:
        formal_in_id = "Node0x" + \
            str(hex(random.randint(0, 2**48))) + called_node_flag
        formal_in_nodes.append(formal_in_id)
        sdg.add_node(formal_in_id, type="formal_in", code_file_path=called_file_path,
                     label='"{'+pdg_calling_info['function_name']+":"+parameter+"="+parameter+"_in" + '}"', shape="record")
        # these are control dependency edges
        sdg.add_edge(entry_node, formal_in_id)

    if pdg_calling_info["return_variable"] != None:
        # add formal-out nodes to the pdg
        if return_node != None:
            formal_out_id = "Node0x" + \
                str(hex(random.randint(0, 2**48))) + called_node_flag
            sdg.add_node(formal_out_id, type="formal_out", code_file_path=called_file_path,
                         label='"{' + pdg_calling_info['function_name'] + ":out="+pdg.nodes[return_node]["variable_name"].strip('"')+'}"', shape="record")
            sdg.add_edge(return_node, formal_out_id)
            sdg.add_edge(formal_out_id, actual_out_id, style="dotted")

    # for node in formal_in_nodes add data dependency edge to the actual_in_nodes
    for index, formal_in_node in enumerate(formal_in_nodes):
        sdg.add_edge(actual_in_nodes[index], formal_in_node, style="dotted")

    return sdg


def generate_sdg(all_pdgs: Dict, sdg: nx.MultiDiGraph, pdg: nx.MultiDiGraph, pdg_calling_info: Dict, call_info_file: str, function_name: str, project_path: str, func_def_dict: dict, expanded_functions: dict, call_file_path: str, in_flag=False):
    """
    This function generate SDG according to the PDG and call info file
    """
    # if function_name == "main":
    #     print()
    # print(len(expanded_functions))
    if sdg == None:
        expanded_functions = {}
        sdg = pdg.copy()
        # find the entry node of sdg
        for node in sdg.nodes:
            if sdg.nodes[node]['type'] == 'entry':
                sdg.nodes[node]['label'] = '"{' + \
                    function_name + ":ENTRY" + '}"'
            else:
                sdg.nodes[node]['label'] = '"{' + function_name + \
                    ":" + sdg.nodes[node]['label'].strip('"')[1:-1] + '}"'
    if in_flag:
        for node in pdg.nodes:
            if pdg.nodes[node]['type'] == 'entry':
                pdg.nodes[node]['label'] = '"{' + \
                    function_name + ":ENTRY" + '}"'
            else:
                pdg.nodes[node]['label'] = '"{' + function_name + \
                    ":" + pdg.nodes[node]['label'].strip('"')[1:-1] + '}"'
        sdg.add_nodes_from(pdg.nodes(data=True))
        sdg.add_edges_from(pdg.edges(data=True))
    call_infos = decode_call_info_file(
        call_info_file, function_name, func_def_dict)
    for node in pdg.nodes:
        if pdg.nodes[node]['type'] == 'call':
            for calling_info in pdg_calling_info[node]:
                called_function_name = calling_info["function_name"]
                if called_function_name in call_infos.keys():
                    if call_infos[called_function_name] != "<invalid loc> ":
                        called_file_path = call_infos[called_function_name]
                        # print(called_function_name, called_file_path)
                        try:
                            # if pdg is already in sdg, we don't need to recursively check this pdg again
                            if called_function_name in expanded_functions.keys():
                                called_pdg = expanded_functions[called_function_name][0]
                                called_parameters = expanded_functions[called_function_name][1]
                                sdg = add_pgd_to_sdg(sdg, called_pdg, node, called_parameters, function_name,
                                                     calling_info, call_file_path, called_file_path, is_expanded=True)
                            else:
                                print(call_infos[called_function_name], called_function_name)
                                result = find_pdg_according_to_code_file_path(
                                    all_pdgs, call_infos[called_function_name], called_function_name, project_path)
                                print(result)
                                if result is not None:
                                    called_pdg, called_pdg_calling_info = result[0], result[1]
                                    called_parameters = find_parameter_info_according_to_code_file_path(
                                        call_infos[called_function_name], called_function_name)
                                    expanded_functions[called_function_name] = [
                                        called_pdg, called_parameters]
                                    sdg = add_pgd_to_sdg(sdg, called_pdg, node, called_parameters,
                                                         function_name, calling_info, call_file_path, called_file_path)
                                    called_info_file = find_call_info_according_to_code_file_path(
                                        call_infos[called_function_name])
                                    sdg, expanded_functions = generate_sdg(
                                        all_pdgs, sdg, called_pdg, called_pdg_calling_info, called_info_file, called_function_name, project_path, func_def_dict, expanded_functions, called_file_path)
                        except FileNotFoundError:
                            # pass
                            # print()
                            print(f"FileNotFoundError: {called_function_name}")
    return sdg, expanded_functions


def remove_repeated_edges(sdg: nx.MultiDiGraph):
    edge_dict = []
    for n1, n2, key in list(sdg.edges):
        try:
            style = sdg.edges[n1, n2, key]['style']
        except:
            style = "control_dep"
        if (n1, n2, style) in edge_dict:
            sdg.remove_edge(n1, n2, key)
        else:
            edge_dict.append((n1, n2, style))
    return sdg


def merge_nodes(G: nx.MultiDiGraph, nodes, new_node, **attr):
    """
    Merges the selected `nodes` of the graph G into one `new_node`,
    meaning that all the edges that pointed to or from one of these
    `nodes` will point to or from the `new_node`.
    """

    G.add_node(new_node, **attr)  # Add the 'merged' node
    for n1, n2, key in list(G.edges):
        # For all edges related to one of the nodes to merge,
        # make an edge going to or coming from the `new gene`.
        try:
            style = G.edges[n1, n2, key]['style']
            if n1 in nodes:
                G.add_edge(new_node, n2, style=style)
            elif n2 in nodes:
                G.add_edge(n1, new_node, style=style)
        except KeyError:
            if n1 in nodes:
                G.add_edge(new_node, n2)
            elif n2 in nodes:
                G.add_edge(n1, new_node)
    code_file_path = G.nodes[nodes[0]]['code_file_path']
    G.nodes[new_node]['label'] = new_node
    G.nodes[new_node]['code_file_path'] = code_file_path

    for n in nodes:  # remove the merged nodes
        G.remove_node(n)


def sdg_clustering(psdg: nx.MultiDiGraph):
    sdg = psdg.copy()
    try:
        sdg.remove_node("\\n")
    except:
        pass
    functions = {}
    for node in sdg.nodes:
        function = sdg.nodes[node]['label'].strip('"').strip('{').split(':')[0]
        if function not in functions.keys():
            functions[function] = [node]
        else:
            functions[function].append(node)
    for function, nodes in functions.items():
        if len(nodes) >= 1:
            merge_nodes(sdg, nodes, function)

    for node in sdg.nodes:
        print(sdg.nodes(data=True)[node])

    adjenct_dict = copy.deepcopy(sdg.adjacency())
    for node, nbrdict in adjenct_dict:
        for nbrnode, keys in nbrdict.items():
            start_edge = True
            count_key = 0
            for key, attrs in keys.items():
                if start_edge:
                    # keep the edge and set count to 1
                    sdg.edges[node, nbrnode, key]["count"] = 1
                    start_edge = False
                else:
                    try:
                        style = sdg.edges[node, nbrnode, key]['style']
                        if count_key == 0:
                            count_key == key
                            start_edge == True
                    except:
                        pass
                    sdg.remove_edge(node, nbrnode, key)
                    sdg.edges[node, nbrnode, count_key]["count"] += 1

    # for node in sdg.nodes:
    #     calls = []
    #     for n1,n2,key in list(sdg.edges):
    #         try:
    #             style = sdg.edges[n1,n2,key]['style']
    #         except:
    #             if n1 == node:
    #                 calls.append([n1,n2])
    #     for k1, k2 in calls:
    #         count = 0
    #         r_count = 0
    #         for n1,n2,key in list(sdg.edges):
    #             try:
    #                 style = sdg.edges[n1,n2,key]['style']
    #                 if n1 == k2 and n2 == k1:
    #                     if r_count > 0:
    #                         sdg.remove_edge(n1,n2,key)
    #                     r_count += 1
    #             except:
    #                 if n1 == k1 and n2 == k2:
    #                     if count > 0:
    #                         sdg.remove_edge(n1,n2,key)
    #                     count += 1
    #         p_count = 0
    #         for n1,n2,key in list(sdg.edges):
    #             try:
    #                 style = sdg.edges[n1,n2,key]['style']
    #                 if n1 == k1 and n2 == k2:
    #                     p_count += 1
    #             except:
    #                 pass
    #         k_count = p_count // count
    #         for n1,n2,key in list(sdg.edges):
    #             try:
    #                 style = sdg.edges[n1,n2,key]['style']
    #                 if n1 == k1 and n2 == k2 and style == "dotted":
    #                     if k_count < 1:
    #                         sdg.remove_edge(n1,n2,key)
    #                     k_count -= 1
    #             except:
    #                 pass
    return sdg


def process_graph(g: nx.MultiDiGraph, project_floder_name: str):
    try:
        g.remove_node("\\n")
        g.remove_node("\\N")
    except:
        pass
    P = pydot.Dot(graph_type='digraph', rankdir="TD")
    for node in g.nodes:
        P.add_node(pydot.Node(
            node, label=g.nodes[node]["label"], shape="box", style="filled"))
    for edge in g.edges:
        # add a label "Pipe" to the edge
        P.add_edge(pydot.Edge(edge[0], edge[1]))
    P.write(pwd+"/temp/processed.dot",
            format='dot', prog=DOT_EXE_FILE_PATH)
    pos_g = nx.MultiDiGraph(nx.nx_pydot.read_dot(
        pwd+"/temp/processed.dot"))
    P = pydot.graph_from_dot_file(
        pwd+"/temp/processed.dot")
    shape = P[0].obj_dict['nodes']['graph'][0]['attributes']['bb'].strip(
        '"').split(',')
    for node in g.nodes:
        x, y = pos_g.nodes[node]["pos"].strip('"').split(',')
        g.nodes[node]['pos_x'] = int(ceil(float(x)))
        g.nodes[node]['pos_y'] = int(ceil(float(y)))
        g.nodes[node]['width'] = float(pos_g.nodes[node]["width"])
        g.nodes[node]['mx'] = float(shape[-2])
        g.nodes[node]['my'] = float(shape[-1])
    return g


def getGraph(graph: nx.MultiDiGraph, project_floder_name):
    G = process_graph(graph, project_floder_name)
    # 删除\\n节点
    remove_list = []
    for node in G.nodes():
        if node == '\\n':
            remove_list.append(node)
    G.remove_nodes_from(remove_list)
    # 添加节点
    node_list = []
    for node in G.nodes():
        temp_node = G.nodes[node]

        # 函数级调用图
        try:
            node_name = temp_node['label'].replace(
                '"', '').strip("{").strip("}").replace("\l", " ")
        except:
            node_name = node
        node_id = node
        mx_length = max(temp_node['mx'], temp_node['my'])
        symbolsize = [25000/mx_length, 20000/mx_length]
        category = 0
        echarts_node = {"name": node_name,
                        "id": node_id,
                        "symbolSize": symbolsize,
                        "x": -temp_node['pos_x'],
                        "y": -temp_node['pos_y'],
                        # "value": value,
                        "category": category,
                        "fixed": False,
                        "symbol": "rect",
                        "itemStyle": {"normal": {"color": "lightblue"}},
                        "label_opts": {},
                        }
        node_list.append(echarts_node)

    relationship_list = []
    for edge in G.edges()._viewer:
        start_node = edge[0]
        end_node = edge[1]
        style = None
        temp_edge = G.edges[edge]
        if "style" in temp_edge.keys():
            style = temp_edge["style"]
            color = "red"
        else:
            style = "solid"
            color = "green"
        count = -1
        for i in range(len(relationship_list)):
            if (relationship_list[i]["source"] == start_node and relationship_list[i]["target"] == end_node) or (relationship_list[i]["source"] == end_node and relationship_list[i]["target"] == start_node):
                count += 1
        echarts_relationship = {"source": start_node,
                                "target": end_node,
                                # 箭头
                                "symbol": ["none", "arrow"],
                                # 线条样式
                                "lineStyle": {"normal": {"width": 1, "curveness": 0.1*count, "type": style, "color": color}},
                                # 显示重复边：
                                "labelLayout": {"hideOverlap": True},
                                # 线条长度
                                # "label": {"normal": {"show": True, "formatter": f"{start_node} to {end_node}", "position": "middle"}},
                                # "label":f"{type_dep} from {start_node} to {end_node}",
                                }
        relationship_list.append(echarts_relationship)
    return node_list, relationship_list


def create_sdg_js(graph_path, project_floder_name):
    nodes, links = getGraph(graph_path, project_floder_name)
    graph_data = {}
    graph_data["data"] = nodes
    graph_data["links"] = links
    return json.dumps(graph_data, fp=f, indent=4)


def main(all_pdgs, project_path, func_def_dict_in, start_functions):  # 直接传入函数定义信息和系统入口函数信息字典
    func_def_dict = {}
    for function, (source, header) in func_def_dict_in.items():
        func_def_dict[function.split(":")[-1]+":"+header] = source
    # # multiprocessing.freeze_support()
    # open header-source code file
    # func_def_dict = {}
    # with open(f"{project_path}/graphs/fun_definitions.txt", "r") as f:
    #     lines = f.readlines()
    #     for line in lines:
    #         if len(line.strip()) > 1:
    #             temp = line.strip().split('::')
    #             func_def_dict[temp[0] + ":" +
    #                           os.path.abspath(temp[1])] = temp[2]

    # start_functions = {}
    # with open(f"{project_path}/graphs/start_functions.txt", "r") as f:
    #     lines = f.readlines()
    #     for line in lines:
    #         if len(line.strip()) > 1:
    #             temp = line.strip().split('::')
    #             start_functions[temp[0]] = temp[2]
    sys_sdg = None
    expanded_functions = {}
    print("generating sdg...")
    for function_info in start_functions:
        function_path = ":".join(function_info.split(":")[:2])
        function_name = function_info.split(":")[-1]
        function_path = function_path.replace("\\", "/")
        print(function_name, function_path)
        main_call_info_file = find_call_info_according_to_code_file_path(
            function_path)
        result = find_pdg_according_to_code_file_path(
            all_pdgs, function_path, function_name, project_path)
        if result is not None:
            main_pdg, main_pdg_calling_info = result[0], result[1]
            sys_sdg, expanded_functions = generate_sdg(all_pdgs, sys_sdg, main_pdg, main_pdg_calling_info, main_call_info_file,
                                                       function_name, project_path, func_def_dict, expanded_functions, function_path, in_flag=True)
            expanded_functions[function_name] = [main_pdg, []]

    if sys_sdg != None:
        for node in list(sys_sdg.nodes):
            try:
                l = sys_sdg.nodes[node]['label']
            except KeyError:
                sys_sdg.remove_node(node)
        # nx.nx_pydot.write_dot(sys_sdg, "sdg.dot")
        print("sdg slustering...")
        cl_sdg = sdg_clustering(sys_sdg)
        # cl_sdg_path = os.path.join(project_path, "graphs", "clustered_sdg.dot")
        # # save the sys_sdg to dot file
        # nx.nx_pydot.write_dot(cl_sdg, cl_sdg_path)
        # convert dot file to png file
        # os.system(f"{DOT_EXE_FILE_PATH} -Tpng {cl_sdg_path} -o {cl_sdg_path}.png")

        # # remove repeat edges in sdg
        sys_sdg = remove_repeated_edges(sys_sdg)
        # save the sys_sdg to dot file
        # sdg_path = os.path.join(project_path, "graphs", "sdg.dot")
        # nx.nx_pydot.write_dot(sys_sdg, sdg_path)
        # # convert dot file to png file
        # os.system(f"{DOT_EXE_FILE_PATH} -Tpng {sdg_path} -o {sdg_path}.png")
        return sys_sdg, cl_sdg  # return system level sdg, and system function level sdg
    else:
        print("sys_sdg is None")
