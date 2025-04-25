"""
根据输入的文件名，修改PLCG的参数
"""

import os
import networkx as nx

def change_PLCG(c,e,file):
    print('change_PLCG')
    # 读取js文件
    PLCG_data = e['PLCG']
    # 遍历节点
    for node in PLCG_data['data']:
        func_key = node['id']
        funcinfo = c[func_key]
        if file in funcinfo['header'] or file in funcinfo['source']:
            # 显示节点
            node['itemStyle']['normal']['opacity'] = 1
        else:
            # 隐藏节点
            node['itemStyle']['normal']['opacity'] = 0
    
    # 遍历边,如果边的两个节点都显示，则显示边
    for edge in PLCG_data['links']:
        source = edge['source']
        target = edge['target']
        for node in PLCG_data['data']:
            if source == node['id']:
                source_opacity = node['itemStyle']['normal']['opacity']
            if target == node['id']:
                target_opacity = node['itemStyle']['normal']['opacity']
        if source_opacity == 1 and target_opacity == 1:
            edge['lineStyle']['normal']['opacity'] = 1
        else:
            edge['lineStyle']['normal']['opacity'] = 0
    
    # 新建networkx图
    PLCG_G = nx.DiGraph()
    # 添加节点
    for node in PLCG_data['data']:
        # 如果节点隐藏，则不添加
        if node['itemStyle']['normal']['opacity'] == 0:
            continue
        PLCG_G.add_node(node['id'], name=node['name'], file=node['file'], size=node['symbolSize'])
    # 添加边
    for edge in PLCG_data['links']:
        # 如果边隐藏，则不添加
        if edge['lineStyle']['normal']['opacity'] == 0:
            continue
        PLCG_G.add_edge(edge['source'], edge['target'])

    
    # 最大出度
    if len(PLCG_G.out_degree) == 0:
        max_out_degree = 'None'
        max_out_degree_val = 0
    else:
        max_out_degree = max(PLCG_G.out_degree, key=lambda x: x[1])[0]+'()'
        max_out_degree_val = max(PLCG_G.out_degree, key=lambda x: x[1])[1]
    # 最小出度
    if len(PLCG_G.out_degree) == 0:
        min_out_degree = 'None'
        min_out_degree_val = 0
    else:
        min_out_degree = min(PLCG_G.out_degree, key=lambda x: x[1])[0]+'()'
        min_out_degree_val = min(PLCG_G.out_degree, key=lambda x: x[1])[1]
    # 平均出度
    if len(PLCG_G.out_degree) == 0:
        avg_out_degree = 0
    else:
        avg_out_degree = sum([d[1] for d in PLCG_G.out_degree])/len(PLCG_G.out_degree)
    # 最大入度
    if len(PLCG_G.in_degree) == 0:
        max_in_degree = 'None'
        max_in_degree_val = 0
    else:
        max_in_degree = max(PLCG_G.in_degree, key=lambda x: x[1])[0]+'()'
        max_in_degree_val = max(PLCG_G.in_degree, key=lambda x: x[1])[1]
    # 最小入度
    if len(PLCG_G.in_degree) == 0:
        min_in_degree = 'None'
        min_in_degree_val = 0
    else:
        min_in_degree = min(PLCG_G.in_degree, key=lambda x: x[1])[0]+'()'
        min_in_degree_val = min(PLCG_G.in_degree, key=lambda x: x[1])[1]
    # 平均入度
    if len(PLCG_G.in_degree) == 0:
        avg_in_degree = 0
    else:
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
        max_call_path = 'None'
    else:
        max_call_path = max(simple_path, key=lambda x: len(x))
    # 最短调用路径
    if len(simple_path) == 0:
        min_call_path = 'None'
    else:
        min_call_path = min(simple_path, key=lambda x: len(x))
    # 平均调用路径
    if len(simple_path) == 0:
        avg_call_path = 0
    else:
        avg_call_path = sum([len(x) for x in simple_path])/len(simple_path)

    PLCG_data["maxOutFunc"] = max_out_degree.split('/')[-1] +'('+ str(max_out_degree_val) +')'
    PLCG_data["minOutFunc"] = min_out_degree.split('/')[-1] +'('+ str(min_out_degree_val) +')'
    PLCG_data["avgOut"] = avg_out_degree
    PLCG_data["maxInFunc"] = max_in_degree.split('/')[-1] +'('+ str(max_in_degree_val) +')'
    PLCG_data["minInFunc"] = min_in_degree.split('/')[-1] +'('+ str(min_in_degree_val) +')'
    PLCG_data["avgIn"] = avg_in_degree
    PLCG_data["maxCallPath"] = max_call_path
    PLCG_data["minCallPath"] = min_call_path
    PLCG_data["avgCallPath"] = avg_call_path

    return PLCG_data
