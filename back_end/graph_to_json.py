# 读取dot文件，转换为json
import networkx as nx
import json
import random
from app import app


def PLCG2json(dot_file, js_path):
    G = nx.DiGraph(nx.nx_pydot.read_dot(dot_file))

    data_list = []
    link_list = []
    categories = [
        {
            "name": "Custom Function"
        },
        {
            "name": "Library Function"
        },
        {
            "name": "Unrecognized Function"
        }
    ]
    for node in G.nodes:
        if node == '\\n':
            continue
        data = {}
        node_info = G.nodes[node]
        name = node_info['label'].replace('"', '').split(': ')[1]
        id = node
        value = node_info['label'].replace('"', '')
        data["name"] = name
        data["id"] = id
        data["symbolSize"] = 45
        if "Library function" in value:
            data["category"] = 1
        elif "Unrecognized File" in value:
            data["category"] = 2
        else:
            data["category"] = 0
        data["value"] = value
        data["fixed"] = False
        data["itemStyle"] = {
            "normal": {
                "opacity": 1
            }
        }
        # 出度
        out_degree = G.out_degree(node)
        data["out_degree"] = out_degree
        # 入度
        in_degree = G.in_degree(node)
        data["in_degree"] = in_degree
        data_list.append(data)
    for edge in G.edges:
        edge_info = G.edges[edge]
        source = edge[0]
        target = edge[1]
        link = {}
        link["source"] = source
        link["target"] = target
        link["symbol"] = [
            "none",
            "arrow"
        ]
        link["lineStyle"] = {
            "normal": {
                "width": 2,
                "curveness": 0.2,
                "type": "solid",
                "opacity": 1
            }
        }
        link_list.append(link)

    # 计算最大的入度和出度，最大调用深度和最小调用深度
    max_in_degree = ("", float('-inf'))
    max_out_degree = ("", float('-inf'))
    max_call_depth = float('-inf')
    min_call_depth = float('inf')
    in_degree_0 = []
    out_degree_0 = []
    for node in G.nodes:
        if node == '\\n':
            continue
        in_degree = G.in_degree(node)
        out_degree = G.out_degree(node)
        if in_degree > max_in_degree[1]:
            name = G.nodes[node]['label'].replace('"', '')
            max_in_degree = (name, in_degree)
        if out_degree > max_out_degree[1]:
            name = G.nodes[node]['label'].replace('"', '')
            max_out_degree = (name, out_degree)
        if in_degree == 0:
            in_degree_0.append(node)
        if out_degree == 0:
            out_degree_0.append(node)
    all_path = []
    for node in in_degree_0:
        for node2 in out_degree_0:
            if node == node2:
                all_path.append([node])
            all_path += list(nx.all_simple_paths(G, source=node, target=node2))
    for path in all_path:
        if len(path) > max_call_depth:
            max_call_depth = len(path)
        if len(path) < min_call_depth:
            min_call_depth = len(path)
    # 将data_list，categories，link_list转换为json
    json_data = {}
    json_data["data"] = data_list
    json_data["categories"] = categories
    json_data["links"] = link_list
    json_data["max_in_degree"] = max_in_degree[0]+"("+str(max_in_degree[1])+")"
    json_data["max_out_degree"] = max_out_degree[0]+"("+str(max_out_degree[1])+")"
    json_data["max_call_depth"] = max_call_depth
    json_data["min_call_depth"] = min_call_depth

    # 写入json文件
    json_file = dot_file.replace('.dot', '.js')
    with open(js_path, 'w') as f:
        # 变量名为graph

        f.write('var graph = ')
        json.dump(json_data, f, indent=4)


def FLCG2json(dot_file, js_path):
    G = nx.DiGraph(nx.nx_pydot.read_dot(dot_file))

    data_list = []
    link_list = []
    categories = [
        {
            "name": "Custom File"
        },
        {
            "name": "Library File"
        },
        {
            "name": "Unrecognized File"
        }
    ]
    for node in G.nodes:
        if node == '\\n':
            continue
        data = {}
        node_info = G.nodes[node]
        name = node_info['label'].replace('"', '').split('/')[-1]
        id = node
        value = node_info['label'].replace('"', '')
        data["name"] = name
        data["id"] = id
        data["symbolSize"] = 45
        if "Library function" in value:
            data["category"] = 1
        elif "Unrecognized File" in value:
            data["category"] = 2
        else:
            data["category"] = 0
        data["value"] = value
        data["fixed"] = False
        data["itemStyle"] = {
            "normal": {
                "opacity": 1
            }
        }
        # 出度
        out_degree = G.out_degree(node)
        data["out_degree"] = out_degree
        # 入度
        in_degree = G.in_degree(node)
        data["in_degree"] = in_degree

        func_num = node_info['func_num'].replace('"', '')
        data["func_num"] = int(func_num)
        data_list.append(data)
    for edge in G.edges:
        edge_info = G.edges[edge]
        source = edge[0]
        target = edge[1]
        link = {}
        link["source"] = source
        link["target"] = target
        link["symbol"] = [
            "none",
            "arrow"
        ]
        link["lineStyle"] = {
            "normal": {
                "width": 2,
                "curveness": 0.2,
                "type": "solid",
                "opacity": 1
            }
        }
        link_list.append(link)

    # 计算最大的入度和出度，最大调用深度和最小调用深度
    max_in_degree = ("", float('-inf'))
    max_out_degree = ("", float('-inf'))
    max_call_depth = float('-inf')
    min_call_depth = float('inf')
    in_degree_0 = []
    out_degree_0 = []
    for node in G.nodes:
        if node == '\\n':
            continue
        in_degree = G.in_degree(node)
        out_degree = G.out_degree(node)
        if in_degree > max_in_degree[1]:
            name = G.nodes[node]['label'].replace('"', '').split('/')[-1]
            max_in_degree = (name, in_degree)
        if out_degree > max_out_degree[1]:
            name = G.nodes[node]['label'].replace('"', '').split('/')[-1]
            max_out_degree = (name, out_degree)
        if in_degree == 0:
            in_degree_0.append(node)
        if out_degree == 0:
            out_degree_0.append(node)
    # 获得所有从入度为0的节点到出度为0的节点的路径, source和target可以相同
    all_path = []
    for node in in_degree_0:
        for node2 in out_degree_0:
            if node == node2:
                all_path.append([node])
            all_path += list(nx.all_simple_paths(G, source=node, target=node2))
    for path in all_path:
        if len(path) > max_call_depth:
            max_call_depth = len(path)
        if len(path) < min_call_depth:
            min_call_depth = len(path)
    # 将data_list，categories，link_list转换为json
    json_data = {}
    json_data["data"] = data_list
    json_data["categories"] = categories
    json_data["links"] = link_list
    json_data["max_in_degree"] = max_in_degree[0]+"("+str(max_in_degree[1])+")"
    json_data["max_out_degree"] = max_out_degree[0]+"("+str(max_out_degree[1])+")"
    json_data["max_call_depth"] = max_call_depth
    json_data["min_call_depth"] = min_call_depth

    # 写入json文件
    json_file = dot_file.replace('.dot', '.js')
    with open(js_path, 'w') as f:
        # 变量名为graph
        f.write('var graph = ')
        json.dump(json_data, f, indent=4)


def compgraph2json(dotfile):
    G = nx.MultiDiGraph(nx.nx_pydot.read_dot(dotfile))
    # 删除\\n节点
    remove_list = []
    for node in G.nodes():
        if node == '\\n':
            remove_list.append(node)
    G.remove_nodes_from(remove_list)
    # 获得cluster
    comp_dic = {}
    # 添加节点
    node_list = []
    relationship_list = []
    nodesize = 45
    nodes_num = len(G.nodes())
    for node in G.nodes():
        temp_node = G.nodes[node]
        if "comp" in temp_node.keys():
            comp = temp_node["comp"].replace("\"", "")
            if ":" in comp:
                comp = comp.split(":")[-1]
            if comp not in comp_dic.keys():
                comp_dic[comp] = []
                comp_dic[comp].append(node)
            else:
                comp_dic[comp].append(node)

    # 添加组件节点
    for key in comp_dic.keys():
        node_name = key
        node_id = key
        category = key
        echarts_node = {"name": node_name[:-2],
                        "id": node_id,
                        "symbolSize": 85,
                        # "value": value,
                        "category": category[:-2],
                        "comp": 1,
                        "fixed": False,
                        # "itemStyle":{"normal":{"color":"#0000FF"}}#blue
                        # 如果类别为1，即为库函数，则隐藏该节点
                        "itemStyle": {"normal": {"opacity": 1}},
                        # 形状为圆角矩形
                        "symbol": "roundRect",
                        }
        node_list.append(echarts_node)
    # 添加函数节点
    for key, value in comp_dic.items():
        for node in value:
            for node1 in G.nodes():
                if node1 == node:
                    temp_node = G.nodes[node1]
                    node_name = temp_node['label'].replace('"', '').split(": ")[-1]
                    node_id = node1
                    value = temp_node['label'].replace('"', '').split(": ")[0]
                    category = key
                    echarts_node = {"name": node_name,
                                    "id": node_id,
                                    "symbolSize": nodesize,
                                    # "value": value,
                                    "category": category[:-2],
                                    "comp": 0,
                                    "fixed": False,
                                    # "itemStyle":{"normal":{"color":"#0000FF"}}#blue
                                    # 如果类别为1，即为库函数，则隐藏该节点
                                    "itemStyle": {"normal": {"opacity": 0}},
                                    }
                    node_list.append(echarts_node)

    # 添加边
    for edge in G.edges()._viewer:
        start_node = edge[0]
        end_node = edge[1]
        style = None
        temp_edge = G.edges[edge]
        if "style" in temp_edge.keys():
            style = temp_edge["style"]
        else:
            style = "solid"
        _, countff = if_exist(relationship_list, start_node, end_node, style)
        # 函数到函数的边
        ff_relationship = {"source": start_node,
                           "target": end_node,
                           "value": 200,
                           # 箭头
                           "symbol": ["none", "arrow"],
                           # 线条样式
                           "lineStyle": {"normal": {"width": 2, "distance": 150, "curveness": 0.1*countff, "type": style, "opacity": 0}},
                           # 线条长度
                           # "label": {"normal": {"show": True, "formatter": "{c}", "position": "middle", "distance": line_length}},
                           }
        relationship_list.append(ff_relationship)
        # 添加组件到函数的边
        start_comp = None
        end_comp = None
        for key, value in comp_dic.items():
            for v in value:
                if start_node == v:
                    start_comp = key
                elif end_node == v:
                    end_comp = key
            if start_comp != None and end_comp != None:
                break
        if start_comp == end_comp:
            continue

        findcf, countcf = if_exist(relationship_list, start_comp, end_node, style)
        findfc, countfc = if_exist(relationship_list, start_node, end_comp, style)
        findcc, countcc = if_exist(relationship_list, start_comp, end_comp, style)
        if findcf == False:
            # 不存在，构建边
            cf_relationship = {"source": start_comp,
                               "target": end_node,
                               # 箭头
                               "symbol": ["none", "arrow"],
                               # 线条样式
                               "lineStyle": {"normal": {"width": 2, "distance": 150, "curveness": 0.1*countcf, "type": style, "opacity": 0}},
                               # 线条长度
                               # "label": {"normal": {"show": True, "formatter": "{c}", "position": "middle", "distance": line_length}},
                               }
            relationship_list.append(cf_relationship)
        if findfc == False:
            # 不存在，构建边
            cf_relationship = {"source": start_node,
                               "target": end_comp,
                               # 箭头
                               "symbol": ["none", "arrow"],
                               # 线条样式
                               "lineStyle": {"normal": {"width": 2, "distance": 150, "curveness": 0.1*countfc, "type": style, "opacity": 0}},
                               # 线条长度
                               # "label": {"normal": {"show": True, "formatter": "{c}", "position": "middle", "distance": line_length}},
                               }
            relationship_list.append(cf_relationship)
        if findcc == False:
            # 不存在，构建边
            cf_relationship = {"source": start_comp,
                               "target": end_comp,
                               # 箭头
                               "symbol": ["none", "arrow"],
                               "value": 200,
                               # 线条样式
                               "lineStyle": {"normal": {"width": 2, "distance": 150, "curveness": 0.1*countcc, "type": style, "opacity": 1}},
                               # 线条长度
                               # "label": {"normal": {"show": True, "formatter": "{c}", "position": "middle", "distance": line_length}},
                               # 设置为折线
                               }
            relationship_list.append(cf_relationship)

    # 构建categories
    categories = []
    for key, value in comp_dic.items():
        categories.append({"name": key[:-2]})

    colors = []
    while len(colors) < len(categories):
        color = "#%06x" % random.randint(0, 0xFFFFFF)
        if color not in colors:
            colors.append(color)

    # 构建echarts的json
    echarts_json = {"data": node_list, "categories": categories, "links": relationship_list, "color": colors}
    # 保存json
    file_name = dotfile.split("/")[-1]
    json_path = app.config.get("EXE_PATH") + "/static/comp.js"
    with open(json_path, "w") as f:
        f.write("var comp = ")
        json.dump(echarts_json, f, indent=4)

    return echarts_json


def if_exist(relationship_list, start, end, style):
    count = 0
    find = False
    for re in relationship_list:
        if re["source"] == start and re["target"] == end:
            count += 1
            if style == re["lineStyle"]["normal"]["type"]:
                find = True
        if re["target"] == start and re["source"] == end:
            count += 1

    if style == "dotted":
        find = False
    return find, count


if __name__ == '__main__':
    # PLCG2json("CUnit_dr\\graphs\\PLCG.dot")
    # FLCG2json("CUnit_dr\\graphs\\FLCG.dot")
    compgraph2json("project/CUnit/graphs/clustered_sdg.dot_GNwithoutcomp.dot")
