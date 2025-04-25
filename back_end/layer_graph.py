# calculate the layer architecture graph
import numpy as np
import random
import networkx as nx
import os
import pydot
import pandas as pd
import json

interface_libs = ["stdio.h", "graphics.h", "windows.h", "stdafx.h", "ncurses.h", "curses.h", "lcui.h", "cuiliet.h", "gtk.h", "xlib.h", "socket.h"]
mid_comp_libs = ["ngx_config.h", "ngx_core.h", "ngx_http.h", "rocketmq.h", "rdkafaka.h", "amqp.h", "thrift_binary_protocol.h", "thrift_framed_transport.h", "thrift_socket.h"]
database_libs = ["sql.h", "sqltypes.h", "sqlext.h", "mysql.h", "mongoc.h", "memcache.h", "Neo4j-clint.h", "hiredis.h", "odbcss.h", "odbcinst.h"]


def load_dependency_matrix_from_dot(path: str):
    Graph = nx.nx_pydot.read_dot(path)
    comp_names = []
    for node in Graph.nodes:
        if node != "\\n":
            if Graph.nodes[node]['comp'] not in comp_names:  # and "Library function__" not in Graph.nodes[node]['comp']:
                comp_names.append(Graph.nodes[node]['comp'])
    dependency_matrix = np.zeros((len(comp_names), len(comp_names)))
    for edge in Graph.edges:
        if Graph.nodes[edge[0]]['comp'] != Graph.nodes[edge[1]]['comp']:  # and "Library function__" not in Graph.nodes[edge[0]]['comp'] and "Library function__" not in Graph.nodes[edge[1]]['comp']:
            dependency_matrix[comp_names.index(Graph.nodes[edge[0]]['comp']), comp_names.index(Graph.nodes[edge[1]]['comp'])] += 1
    comp_names = [c_name.strip('"').replace("_", "").strip() for c_name in comp_names]
    return dependency_matrix, comp_names


def load_dependency_matrix_from_csv(csv_path: str, plcg: nx.DiGraph):
    # 加载一个来自csv的层次架构信息
    comps = {}
    csv_data = pd.read_csv(csv_path)
    csv_data = csv_data.dropna()
    # plcg = nx.DiGraph(nx.nx_pydot.read_dot(plcg_path))
    # print(csv_data)
    for index, row in csv_data.iterrows():
        if row["topic"] not in comps.keys():
            comps[row["topic"]] = {"name": [], "headerfile": [], "libs": []}
        comps[row['topic']]["name"].append((row["name"]))
        comps[row['topic']]["headerfile"].append((row["headerfile"]))
        comps[row['topic']]["libs"] += eval(row["libs"])
    # for k in comps.keys():
    #     print(k, len(comps[k]["name"]), len(comps[k]["headerfile"]))
    # 利用PLCG中的边来构造依赖关系
    dependency_matrix = np.zeros((len(list(comps.keys())), len(list(comps.keys()))))

    for i1, k1 in enumerate(list(comps.keys())):
        for i2, k2 in enumerate(list(comps.keys())):
            # 遍历plcg中所有的调用边
            for edge in plcg.edges:
                call1 = False
                call2 = False
                func_name0 = plcg.nodes[edge[0]]['label'].split(":")[-1].strip('"')
                header_name0 = plcg.nodes[edge[0]]['file'].strip('"')
                func_name1 = plcg.nodes[edge[1]]['label'].split(":")[-1].strip('"')
                header_name1 = plcg.nodes[edge[1]]['file'].strip('"')
                for i in range(len(comps[k1]["name"])):
                    if func_name0 == comps[k1]["name"][i] and header_name0 == comps[k1]["headerfile"][i]:
                        call1 = True
                        break
                for i in range(len(comps[k2]["name"])):
                    if func_name1 == comps[k2]["name"][i] and header_name1 == comps[k2]["headerfile"][i]:
                        call2 = True
                        break
                # 如果存在从组件1到组件2的调用
                if call1 and call2:
                    dependency_matrix[i1, i2] = 1
                    break
    return dependency_matrix, list(comps.keys()), comps


class LayerArchitectureGraph:
    def __init__(self, dependency_matrix: np.ndarray, layer_num: int, node_names, comps) -> None:
        self.dependency_matrix = dependency_matrix.copy()
        assert (layer_num > 2)
        self.layer_num = layer_num
        self.node_num = self.dependency_matrix.shape[0]
        self.adj_pen = None
        self.intra_pen = None
        self.skip_pen = None
        self.back_pen = None
        self.node_names = node_names
        self.freeze_comps = []
        self.comps = comps
        for comp in comps.keys():
            if len(comps[comp]["libs"]) > 0:
                print("libs", comp, comps[comp]["libs"])
                if set(comps[comp]["libs"]).intersection(set(interface_libs+mid_comp_libs+database_libs)) != set():
                    self.freeze_comps.append(comp)

        print("self.freeze_comps", self.freeze_comps)

    def set_penalty(self, adj_pen: int, intra_pen: int, skip_pen: int, back_pen: int):
        self.adj_pen = adj_pen
        self.intra_pen = intra_pen
        self.skip_pen = skip_pen
        self.back_pen = back_pen

    def init_random_architecture(self):
        # 根据依赖矩阵随机生成一个分层架构图
        architecture = np.random.randint(2,  self.layer_num+1, size=(self.node_num,))  # 基础设施层无组件
        for i, node in enumerate(self.node_names):
            if set(self.comps[node]["libs"]).intersection(set(interface_libs)) != set():
                architecture[i] = 6
            if set(self.comps[node]["libs"]).intersection(set(mid_comp_libs)) != set():
                architecture[i] = 3
            if set(self.comps[node]["libs"]).intersection(set(database_libs)) != set():
                architecture[i] = 2
        return architecture

    def cal_adj_call_value(self, architecture: np.ndarray, layer: int):
        sum = 0
        for i in range(self.node_num):
            for j in range(self.node_num):
                if architecture[i] == layer and architecture[j] == layer - 1:
                    sum += self.dependency_matrix[i, j]
        return sum

    def cal_intra_call_value(self, architecture: np.ndarray, layer: int):
        sum = 0
        for i in range(self.node_num):
            for j in range(self.node_num):
                if architecture[i] == layer and architecture[j] == layer and i != j:
                    sum += self.dependency_matrix[i, j]
        return sum

    def cal_skip_call_value(self, architecture: np.ndarray, layer: int):
        sum = 0
        for i in range(self.node_num):
            for j in range(self.node_num):
                if architecture[i] == layer and architecture[j] < layer - 1:
                    sum += self.dependency_matrix[i, j]
        return sum

    def cal_back_call_value(self, architecture: np.ndarray, layer: int):
        sum = 0
        for i in range(self.node_num):
            for j in range(self.node_num):
                if architecture[i] == layer and layer < architecture[j]:
                    sum += self.dependency_matrix[i, j]
        return sum

    def cal_layer_fitness(self, architecture: np.ndarray, layer: int):
        return self.adj_pen * self.cal_adj_call_value(architecture, layer) + self.intra_pen * self.cal_intra_call_value(architecture, layer) + self.skip_pen * self.cal_skip_call_value(architecture, layer) + self.back_pen * self.cal_back_call_value(architecture, layer)

    def cal_architecture_fitness(self, architecture: np.ndarray):
        sum = 0
        for l in range(1, self.layer_num+1):
            sum += self.cal_layer_fitness(architecture, l)
        return sum

    def dump_graph(self, path: str):
        # create a graph use nx
        G = nx.from_numpy_array(self.dependency_matrix, create_using=nx.DiGraph)
        if self.node_num == len(self.node_names):
            # rename nodes in G
            nx.relabel_nodes(G, {i: self.node_names[i] for i in range(self.node_num)})
        nx.nx_pydot.write_dot(G, path)
        os.system(f"dot -Tpng {path} -o {path[:-3]+'png'}")

    def dump_layer_graph(self, architecure: np.ndarray, path: str):
        # create a graph use pydot
        G = pydot.Dot(graph_type='digraph', rankdir="LR")  # , splines="line")
        # add nodes to it
        for l in range(1, self.layer_num+1):
            subgraph = pydot.Cluster(f"subG_{l}", rank="same", label=f"layer_{l}")
            for i in range(self.node_num):
                if architecure[i] == l:
                    if self.node_num == len(self.node_names):
                        subgraph.add_node(pydot.Node(self.node_names[i]))
                    else:
                        subgraph.add_node(pydot.Node(i))
            G.add_subgraph(subgraph)
        # add edges to it
        for i in range(self.node_num):
            for j in range(self.node_num):
                if self.dependency_matrix[i, j] != 0:
                    if self.node_num == len(self.node_names):
                        G.add_edge(pydot.Edge(self.node_names[i], self.node_names[j]))
                    else:
                        G.add_edge(pydot.Edge(i, j))
        G.write(path, format='dot')
        os.system(f"dot -Tpng {path} -o {path[:-3]+'png'}")

    def dump_layer_graph_to_js(self, architecure: np.ndarray):  # , path:str): #, keywords: str = "topics_words.json"):
        json_data = []
        colors = ["red", "blue", "green", "yellow", "brown", "pink", "orange", "purple", "brown", "grey"]
        layer_names = list(reversed(["用户接口层", "业务服务层", "基础服务层", "中间件层", "数据层", "基础设施层"]))
        layer_names_eng = list(reversed(["User Interface Layer", "Business Service Layer", "Basic Service Layer", "Middleware Layer", "Data Layer", "Infrastructure Layer"]))
        json_layers = []
        # load keywords from "topics_words.json"
        # try:
        #     with open(keywords, "r") as f:
        #         comps_words = json.load(f)
        # except FileNotFoundError:
        #     print("topic words file not found")
        #     comps_words = {str(node):[] for node in self.node_names}
        comps_words = {str(node): [] for node in self.node_names}

        # print(comps_words)
        # different layers are different in y of value
        for y in range(1, self.layer_num+1):
            c_nodes = []
            for i in range(self.node_num):
                if architecure[i] == y:
                    c_nodes.append(self.node_names[i])

            all_words = []

            x = 2.5 - 0.3 * len(c_nodes) / 2
            for node in c_nodes:
                x += 0.3
                all_words += comps_words[str(node)]
                # add a node into the graph
                json_data.append({
                    "name": node,
                    "id": node,
                    "symbolSize": 55,
                    "node_type": "comp",
                    "funcs_num": len(self.comp_funcs[node]["name"]),
                    "funcs": "(); ".join(self.comp_funcs[node]["name"]) + "();",
                    "words": comps_words[str(node)],
                    "itemStyle": {
                        "normal": {
                            "opacity": 1
                        }
                    }, "z": 3,
                    "symbol": "roundRect",
                    "value": [x, y-1],
                    "layer": f"{layer_names[y-1]}, {layer_names_eng[y-1]}"
                })
            json_layers.append({
                "name": f"{layer_names[y-1]}",
                "eng_name": f"{layer_names_eng[y-1]}",
                "id": f"layer {y} back",
                "symbolSize": [1500, 75],
                "node_type:": "layer",
                "comp_nums": len(c_nodes),
                "words": list(set(all_words)),
                "itemStyle": {
                    "normal": {
                        "color": colors[y-1],
                        "borderWidth": 0,
                        "opacity": 0.2
                    }
                }, "z": 1,
                "symbol": "Rect",
                "value": [2.5, y-1]
            })

        json_links = []
        for i in range(self.node_num):
            for j in range(self.node_num):
                if self.dependency_matrix[i, j] != 0:
                    json_links.append({
                        "source": self.node_names[i],
                        "target": self.node_names[j],
                        "symbol": [
                            "none",
                            "arrow"
                        ], "symbolSize": 10,
                        "lineStyle": {
                            "normal": {
                                "width": 3,
                                "type": "solid",
                                "opacity": 1
                            }
                        }
                    })

        return json.dumps({"data": json_data, "links": json_links, "layer_data": json_layers}, indent=4)

        # with open(path, 'w') as f:
        #     f.write('const data = ')
        #     json.dump(json_data, f, indent=4)
        #     f.write(";\n")
        #     f.write('const links = ')
        #     json.dump(json_links, f, indent=4)
        #     f.write(";\n")
        #     f.write('const layer_data = ')
        #     json.dump(json_layers, f, indent=4)
        #     f.write(";\n")


class GALayerGraph:
    def __init__(self, layer_architecture_graph: LayerArchitectureGraph, size_pop=100, max_iter=202, prob_mut=0.15, keep_ratio=0.1):
        self.lag = layer_architecture_graph
        self.size_pop = size_pop
        self.max_iter = max_iter
        self.prob_mut = prob_mut
        self.keep_ratio = keep_ratio
        self.population = []
        for _ in range(self.size_pop):
            self.population.append(self.lag.init_random_architecture())
        self.population = sorted(self.population, key=lambda x: self.lag.cal_architecture_fitness(x))

    def select(self):
        # random select 2 from first half of population
        index1 = np.random.randint(0, self.size_pop // 2)
        index2 = np.random.randint(0, self.size_pop // 2)
        return index1, index2

    def crossover(self, i1: np.ndarray, i2: np.ndarray):
        newx = self.population[i2].copy()
        for i in range(self.lag.node_num):
            if i < self.lag.node_num // 2:
                if self.lag.node_names[i] not in self.lag.freeze_comps:
                    newx[i] = self.population[i1][i]
        return newx

    def mutation(self, x: np.ndarray):
        # random choose a node in x and change its layer
        if random.random() < self.prob_mut:
            if random.random() < 0.5:
                index1 = np.random.randint(0, self.lag.node_num)
                index2 = np.random.randint(0, self.lag.node_num)
                if self.lag.node_names[index1] not in self.lag.freeze_comps and self.lag.node_names[index2] not in self.lag.freeze_comps:
                    # newl = np.random.randint(2, self.lag.layer_num)
                    x[index1], x[index2] = x[index2], x[index1]
            else:
                index = np.random.randint(0, self.lag.node_num)
                if self.lag.node_names[index] not in self.lag.freeze_comps:
                    x[index] = np.random.randint(2, self.lag.layer_num+1)
        return x

    def run(self, if_cross=True):
        # self.lag.dump_graph("dependency_graph.dot")
        each_iter_best = []
        for i in range(self.max_iter):
            if i == 0:
                each_iter_best.append(self.lag.cal_architecture_fitness(self.population[self.size_pop//2]))
            else:
                each_iter_best.append(self.lag.cal_architecture_fitness(self.population[0]))
            if i % 10 == 1:
                print(i, self.lag.cal_architecture_fitness(self.population[0]))
            for j in range(self.size_pop):
                if if_cross:
                    if j > self.keep_ratio * self.size_pop:
                        i1, i2 = self.select()
                        newx = self.crossover(i1, i2)
                        newx = self.mutation(newx)
                        self.population[j] = newx
                else:
                    newx = self.population[j].copy()
                    count = 0
                    while count < 100 and self.lag.cal_architecture_fitness(newx) >= self.lag.cal_architecture_fitness(self.population[j]):
                        # print(self.lag.cal_architecture_fitness(newx), self.lag.cal_architecture_fitness(self.population[j]))
                        newx = self.mutation(newx)
                        count += 1
                    if count < 100:
                        self.population[j] = newx
        # sort the population
            self.population = sorted(self.population, key=lambda x: self.lag.cal_architecture_fitness(x))
        # self.lag.dump_layer_graph(self.population[0], f"best_layer_graph.dot")
        # self.lag.dump_layer_graph_to_js(self.population[0], "layer.js")
        return self.population[0], each_iter_best


def random_generate_graph():
    k = 200
    layer_num = 10
    max_weight = 5
    # random init a dependency_matrix
    dm = np.zeros((k, k))
    # random set 4 lines rows to be all zero
    for i in range(k):
        i1 = np.random.randint(0, k)
        i2 = np.random.randint(0, k)
        if i1 != i2:
            dm[i1, i2] = np.random.randint(1, max_weight)
    return dm, layer_num


def main(comp_data_csv_path, plcg: nx.DiGraph):
    layer_num = 6
    # dm, node_names = load_dependency_matrix_from_dot("sdg.dot")
    dm, node_names, comps = load_dependency_matrix_from_csv(comp_data_csv_path, plcg)
    # print dm shape
    print(dm.shape, len(node_names))
    # print number of 1 in dm
    print(np.sum(dm == 1))
    # dm[node_names.index("testcunitaddtest"),node_names.index("Library function")] = 2
    print(node_names)
    lag = LayerArchitectureGraph(dm, layer_num, node_names, comps)
    lag.comp_funcs = comps
    lag.set_penalty(1, 15, 25, 10)

    # cm = GALayerGraph(lag, size_pop=1, prob_mut=1)
    # best_a, log_cm = cm.run(if_cross = False)

    ga = GALayerGraph(lag, max_iter=1)
    best_a, log_ga = ga.run()
    return ga.lag.dump_layer_graph_to_js(best_a)


if __name__ == "__main__":
    main()
# main()
