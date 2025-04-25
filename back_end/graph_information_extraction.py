'''
提取CG信息
作者：刘梓轩，韩晓航
时间：2023.4.27
'''
import networkx as nx
import numpy as np
import os
from cfg_information_extraction import *
from utils import get_file_encoding


class graph_information:
    # 存储有向图信息
    def __init__(self, dot_file_path):

        self.graph = graph_read(dot_file_path)

        # 如果节点的id是\\n,删除节点
        remove_list = []
        for node in self.graph.nodes():
            if node == '\\n':
                remove_list.append(node)
        self.graph.remove_nodes_from(remove_list)

        # 节点信息

        # 节点的度
        self.node_degree = {}
        for node in self.graph.nodes():
            self.node_degree[node] = self.graph.degree(node)
        # 节点的入度
        self.node_in_degree = {}
        for node in self.graph.nodes():
            self.node_in_degree[node] = self.graph.in_degree(node)
        # 节点的出度
        self.node_out_degree = {}
        for node in self.graph.nodes():
            self.node_out_degree[node] = self.graph.out_degree(node)

        # 度，入度，出度的按照大小排序
        self.node_degree_sort = sorted(
            self.node_degree.items(), key=lambda x: x[1], reverse=True)
        self.node_in_degree_sort = sorted(
            self.node_in_degree.items(), key=lambda x: x[1], reverse=True)
        self.node_out_degree_sort = sorted(
            self.node_out_degree.items(), key=lambda x: x[1], reverse=True)
        # 节点的最大度
        self.max_degree = self.node_degree_sort[0][1]
        # 节点的最小度
        self.min_degree = self.node_degree_sort[-1][1]
        # 节点的最大入度
        self.max_in_degree = self.node_in_degree_sort[0][1]
        # 节点的最小入度
        self.min_in_degree = self.node_in_degree_sort[-1][1]
        # 节点的最大出度
        self.max_out_degree = self.node_out_degree_sort[0][1]
        # 节点的最小出度
        self.min_out_degree = self.node_out_degree_sort[-1][1]

        # Hopcount 跳数
        self.hopcount = {}
        for node in self.graph.nodes():
            self.hopcount[node] = {}
        for node in self.graph.nodes():
            paths = []
            # 获得到所有其他节点的所有简单路径
            for target in self.graph.nodes():
                if node != target:
                    paths.append(nx.all_simple_paths(self.graph, node, target))

            for gen in paths:
                for path in gen:
                    # 获取每条路最后一个节点的id
                    last_node = path[-1]
                    # 获取每条路的跳数
                    path_length = len(path) - 1
                    # 将每条路的长度和最后一个节点的id存入字典
                    # 判断最后一个节点的id是否已经在字典中
                    if last_node in self.hopcount[node].keys():
                        # 如果已经在字典中，则直接将路径长度加入字典
                        self.hopcount[node][last_node].append(path_length)
                    else:
                        # 如果不在字典中，则将路径长度存入列表
                        self.hopcount[node][last_node] = [path_length]

        # MinHopcount 节点的最小跳数
        self.min_hopcount = {}
        for node in self.graph.nodes():
            self.min_hopcount[node] = {}
            for key in self.hopcount[node]:
                self.min_hopcount[node][key] = min(self.hopcount[node][key])

        # Closeness 紧密度 节点的总跳数的倒数
        self.closeness = {}
        for node in self.graph.nodes():
            self.closeness[node] = 0
            for key in self.hopcount[node]:
                self.closeness[node] += sum(self.hopcount[node][key])
            # 不为0时计算倒数
            if self.closeness[node] != 0:
                self.closeness[node] = 1/self.closeness[node]

        # Eccentricity 离心率 节点的最大跳数
        self.eccentricity = {}
        for node in self.graph.nodes():
            self.eccentricity[node] = 0
            for key in self.hopcount[node]:
                self.eccentricity[node] = max(
                    self.eccentricity[node], max(self.hopcount[node][key]))

        # 度中心性
        self.degree_centrality = nx.degree_centrality(self.graph)
        # 近中心性
        self.closeness_centrality = nx.closeness_centrality(self.graph)
        # 介数中心性
        self.betweenness_centrality = nx.betweenness_centrality(self.graph)
        # 特征向量中心性
        self.eigenvector_centrality = nx.eigenvector_centrality(
            self.graph, max_iter=10000)

        # 节点的介数
        self.betweenness = {}
        for node in self.graph.nodes():
            self.betweenness[node] = self.betweenness_centrality[node] * \
                (self.graph.number_of_nodes()-1) * \
                (self.graph.number_of_nodes()-2)/2

        # 聚类系数
        self.clustering = nx.clustering(self.graph)

        # 图的信息

        # 节点数量
        self.node_num = self.graph.number_of_nodes()
        # 边的数量
        self.edge_num = self.graph.number_of_edges()
        # 获得所有环
        self.cycle = nx.simple_cycles(self.graph)
        # 环的数量
        self.cycle_num = len(list(self.cycle))

        # 图的密度
        self.max_density = self.node_num * (self.node_num - 1)/2
        self.actual_density = self.edge_num / self.max_density

        # 图的直径 最大离心率
        self.diameter = max(self.eccentricity.values())
        # 图的半径 最小离心率
        self.radius = min(self.eccentricity.values())
        # 图的周长 最小环的跳数
        cycle_length = []
        for cycle in nx.simple_cycles(self.graph):
            cycle_length.append(len(cycle))
        if len(cycle_length) > 0:
            self.girth = min(cycle_length)
        else:
            self.girth = None

        # 邻接矩阵
        self.adjacency_matrix = nx.adjacency_matrix(self.graph)
        # 邻接矩阵的特征值
        self.adjacency_matrix_eigenvalue = np.linalg.eigvals(
            self.adjacency_matrix.toarray())
        # 邻接矩阵的特征向量
        self.adjacency_matrix_eigenvector = np.linalg.eig(
            self.adjacency_matrix.toarray())[1]
        # Laplacian 拉普拉斯矩阵 度矩阵减去邻接矩阵
        # 度矩阵
        self.degree_matrix = np.diag(
            np.sum(self.adjacency_matrix.toarray(), axis=1))
        # 拉普拉斯矩阵
        self.laplacian_matrix = self.degree_matrix - self.adjacency_matrix.toarray()
        # 拉普拉斯矩阵的特征值
        self.laplacian_matrix_eigenvalue = np.linalg.eigvals(
            self.laplacian_matrix)
        # 拉普拉斯矩阵的特征向量
        self.laplacian_matrix_eigenvector = np.linalg.eig(
            self.laplacian_matrix)[1]

        # 对拉普拉斯矩阵的特征值进行排序
        sorted_laplacian_matrix_eigenvalue = sorted(
            self.laplacian_matrix_eigenvalue)
        # 代数连通性 拉普拉斯矩阵第二小的特征值
        self.algebraic_connectivity = sorted_laplacian_matrix_eigenvalue[1]
        # 光谱半径 邻接矩阵的最大特征值的绝对值
        self.spectral_radius = max(abs(self.adjacency_matrix_eigenvalue))
        # 菲德勒向量 与拉普拉斯矩阵的第二小特征值对应的特征向量
        index = 0
        for i in range(len(self.laplacian_matrix_eigenvalue)):
            if self.laplacian_matrix_eigenvalue[i] == sorted_laplacian_matrix_eigenvalue[1]:
                index = i
        self.fiedler_vector = self.laplacian_matrix_eigenvector[:, index]
        # 主特征向量 与邻接矩阵的最大特征值对应的特征向量
        self.principal_eigenvector = self.adjacency_matrix_eigenvector[:, np.argmax(
            abs(self.adjacency_matrix_eigenvalue))]

        # 平均跳数
        self.average_hop = 0
        for key, value in self.min_hopcount.items():
            for key1, value1 in value.items():
                if key != key1:
                    self.average_hop = self.average_hop + value1
        self.average_hop = self.average_hop / \
            (self.node_num * (self.node_num - 1))

        # 节点度分布
        self.degree_histogram = nx.degree_histogram(self.graph)
        all_degree = 0
        for i in range(len(self.degree_histogram)):
            all_degree = self.degree_histogram[i]
        self.degree_distribution = [
            i/all_degree for i in self.degree_histogram]
        # 平均度
        self.average_degree = 2 * self.edge_num / self.node_num

        # 图的平均聚类系数
        self.average_clustering = nx.average_clustering(self.graph)

        # 有效直径
        H = 4
        self.effective_diameter = (
            self.node_num**2/(self.node_num+self.edge_num*2))**(1/H)

        # 主导中心点 CPD
        # 获得最大介度
        max_betweenness = max(self.betweenness.values())
        self.cpd = 1/(self.node_num-1) * \
            sum([max_betweenness-i for i in self.betweenness.values()])


def graph_read(graph_path):
    # 读取CG的dot文件
    G = nx.DiGraph(nx.nx_pydot.read_dot(graph_path))
    return G


def print2txt(graph_information, path):
    # 将图的信息写入txt文件
    info = 'The information of the graph is as follows:\r'
    graph = graph_information.graph
    # 节点信息
    # 节点的度
    info = info + 'The degree of each node is as follows:\r'
    for key, value in graph_information.node_degree.items():
        if 'label' not in graph.nodes[key]:
            node_label = key
        else:
            node_label = graph.nodes[key]['label']
        info = info + node_label + ':' + str(value) + '\r'
    info += '\r'
    # 节点的入度
    info = info + 'The in-degree of each node is as follows:\r'
    for key, value in graph_information.node_in_degree.items():
        if 'label' not in graph.nodes[key]:
            node_label = key
        else:
            node_label = graph.nodes[key]['label']
        info = info + node_label + ':' + str(value) + '\r'
    info += '\r'
    # 节点的出度
    info = info + 'The out-degree of each node is as follows:\r'
    for key, value in graph_information.node_out_degree.items():
        if 'label' not in graph.nodes[key]:
            node_label = key
        else:
            node_label = graph.nodes[key]['label']
        info = info + node_label + ':' + str(value) + '\r'
    info += '\r'
    # 节点的最大最小度
    info = info + 'The max degree of the graph is ' + \
        str(graph_information.max_degree) + '\r'
    info = info + 'The min degree of the graph is ' + \
        str(graph_information.min_degree) + '\r'
    info += '\r'
    # 节点的最大最小入度
    info = info + 'The max in-degree of the graph is ' + \
        str(graph_information.max_in_degree) + '\r'
    info = info + 'The min in-degree of the graph is ' + \
        str(graph_information.min_in_degree) + '\r'
    info += '\r'
    # 节点的最大最小出度
    info = info + 'The max out-degree of the graph is ' + \
        str(graph_information.max_out_degree) + '\r'
    info = info + 'The min out-degree of the graph is ' + \
        str(graph_information.min_out_degree) + '\r'
    info += '\r'
    # 节点的跳数
    info = info + 'The hopcount of each node is as follows:\r'
    for key, value in graph_information.hopcount.items():
        if 'label' not in graph.nodes[key]:
            node_label = key
        else:
            node_label = graph.nodes[key]['label']
        for key1, value1 in value.items():
            if 'label' not in graph.nodes[key1]:
                node_label1 = key1
            else:
                node_label1 = graph.nodes[key1]['label']
            for hop in value1:
                info = info + node_label + '->' + \
                    node_label1 + ':' + str(hop) + '\r'
    info += '\r'
    # 节点的最小跳数
    info = info + 'The min hopcount of each node is as follows:\r'
    for key, value in graph_information.min_hopcount.items():
        if 'label' not in graph.nodes[key]:
            node_label = key
        else:
            node_label = graph.nodes[key]['label']
        for key1, value1 in value.items():
            if 'label' not in graph.nodes[key1]:
                node_label1 = key1
            else:
                node_label1 = graph.nodes[key1]['label']
            info = info + node_label + '->' + \
                node_label1 + ':' + str(value1) + '\r'
    info += '\r'
    # 节点的紧密度
    info = info + 'The closeness of each node is as follows:\r'
    for key, value in graph_information.closeness.items():
        if 'label' not in graph.nodes[key]:
            node_label = key
        else:
            node_label = graph.nodes[key]['label']
        info = info + node_label + ':' + str(value) + '\r'
    info += '\r'
    # 节点的介度
    info = info + 'The betweenness of each node is as follows:\r'
    for key, value in graph_information.betweenness.items():
        if 'label' not in graph.nodes[key]:
            node_label = key
        else:
            node_label = graph.nodes[key]['label']
        info = info + node_label + ':' + str(value) + '\r'
    info += '\r'
    # 离心率
    info = info + 'The eccentricity of each node is as follows:\r'
    for key, value in graph_information.eccentricity.items():
        if 'label' not in graph.nodes[key]:
            node_label = key
        else:
            node_label = graph.nodes[key]['label']
        info = info + node_label + ':' + str(value) + '\r'
    info += '\r'
    # 度中心性
    info = info + 'The degree centrality of each node is as follows:\r'
    for key, value in graph_information.degree_centrality.items():
        if 'label' not in graph.nodes[key]:
            node_label = key
        else:
            node_label = graph.nodes[key]['label']
        info = info + node_label + ':' + str(value) + '\r'
    info += '\r'
    # 近中心性
    info = info + 'The closeness centrality of each node is as follows:\r'
    for key, value in graph_information.closeness_centrality.items():
        if 'label' not in graph.nodes[key]:
            node_label = key
        else:
            node_label = graph.nodes[key]['label']
        info = info + node_label + ':' + str(value) + '\r'
    info += '\r'
    # 介数中心性
    info = info + 'The betweenness centrality of each node is as follows:\r'
    for key, value in graph_information.betweenness_centrality.items():
        if 'label' not in graph.nodes[key]:
            node_label = key
        else:
            node_label = graph.nodes[key]['label']
        info = info + node_label + ':' + str(value) + '\r'
    info += '\r'
    # 特征向量中心性
    info = info + 'The eigenvector centrality of each node is as follows:\r'
    for key, value in graph_information.eigenvector_centrality.items():
        if 'label' not in graph.nodes[key]:
            node_label = key
        else:
            node_label = graph.nodes[key]['label']
        info = info + node_label + ':' + str(value) + '\r'
    info += '\r'

    # 聚类系数
    info = info + 'The clustering coefficient of each node is as follows:\r'
    for key, value in graph_information.clustering.items():
        if 'label' not in graph.nodes[key]:
            node_label = key
        else:
            node_label = graph.nodes[key]['label']
        info = info + node_label + ':' + str(value) + '\r'
    info += '\r'

    # 图的信息
    # 图的节点数
    info = info + 'The number of nodes in the graph is ' + \
        str(graph_information.node_num) + '\r'
    # 图的边数
    info = info + 'The number of edges in the graph is ' + \
        str(graph_information.edge_num) + '\r'
    # 环的个数
    info = info + 'The number of cycles in the graph is ' + \
        str(graph_information.cycle_num) + '\r'
    # 图的最大密度
    info = info + 'The max density of the graph is ' + \
        str(graph_information.max_density) + '\r'
    # 图的实际密度
    info = info + 'The actual density of the graph is ' + \
        str(graph_information.actual_density) + '\r'

    # 图的直径
    info = info + 'The diameter of the graph is ' + \
        str(graph_information.diameter) + '\r'
    # 图的半径
    info = info + 'The radius of the graph is ' + \
        str(graph_information.radius) + '\r'
    # 图的周长
    info = info + 'The girth of the graph is ' + \
        str(graph_information.girth) + '\r'
    # 邻接矩阵
    info = info + 'The adjacency matrix of the graph is as follows:\r'
    # print(graph_information.adjacency_matrix.shape)
    for i in range(graph_information.node_num):
        for j in range(graph_information.node_num):
            info = info + \
                str(graph_information.adjacency_matrix.toarray()[i][j]) + ' '
        info += '\r'
    info += '\r'
    # 邻接矩阵特征值
    info = info + 'The eigenvalues of the graph is as follows:\r'
    for i in range(graph_information.node_num):
        info = info + \
            str(graph_information.adjacency_matrix_eigenvalue[i]) + ' '
    info += '\r'
    # 邻接矩阵特征向量
    info = info + 'The eigenvectors of the graph is as follows:\r'
    for i in range(graph_information.node_num):
        for j in range(graph_information.node_num):
            info = info + \
                str(graph_information.adjacency_matrix_eigenvector[i][j]) + ' '
        info += '\r'
    info += '\r'

    # 图的拉普拉斯矩阵
    info = info + 'The Laplacian matrix of the graph is as follows:\r'
    for i in range(graph_information.node_num):
        for j in range(graph_information.node_num):
            info = info + str(graph_information.laplacian_matrix[i][j]) + ' '
        info += '\r'
    info += '\r'
    # 图的拉普拉斯矩阵特征值
    info = info + 'The eigenvalues of the Laplacian matrix of the graph is as follows:\r'
    for i in range(graph_information.node_num):
        info = info + \
            str(graph_information.laplacian_matrix_eigenvalue[i]) + ' '
    info += '\r'
    # 图的拉普拉斯矩阵特征向量
    info = info + 'The eigenvectors of the Laplacian matrix of the graph is as follows:\r'
    for i in range(graph_information.node_num):
        for j in range(graph_information.node_num):
            info = info + \
                str(graph_information.laplacian_matrix_eigenvector[i][j]) + ' '
        info += '\r'
    info += '\r'

    # 代数连通性
    info = info + 'The algebraic connectivity of the graph is ' + \
        str(graph_information.algebraic_connectivity) + '\r'
    # 光谱半径
    info = info + 'The spectral radius of the graph is ' + \
        str(graph_information.spectral_radius) + '\r'
    # 菲德勒向量
    info = info + 'The Fiedler vector of the graph is as follows:\r'
    for i in range(graph_information.node_num):
        info = info + str(graph_information.fiedler_vector[i]) + ' '
    info += '\r'
    # 主特征向量
    info = info + 'The principal eigenvector of the graph is as follows:\r'
    for i in range(graph_information.node_num):
        info = info + str(graph_information.principal_eigenvector[i]) + ' '
    info += '\r'

    # 平均跳数
    info = info + 'The average hop of the graph is ' + \
        str(graph_information.average_hop) + '\r'
    # 节点度分布
    info = info + 'The degree distribution of the graph is as follows:\r'
    for i in range(len(graph_information.degree_distribution)):
        info = info + str(graph_information.degree_distribution[i]) + ' '
    info += '\r'
    # 平均度
    info = info + 'The average degree of the graph is ' + \
        str(graph_information.average_degree) + '\r'
    # 图的平均聚类系数
    info = info + 'The average clustering coefficient of the graph is ' + \
        str(graph_information.average_clustering) + '\r'
    # 有效直径
    info = info + 'The effective diameter of the graph is ' + \
        str(graph_information.effective_diameter) + '\r'
    # 主导中心点
    info = info + 'The CPD of the graph is ' + \
        str(graph_information.cpd) + '\r'
    # 存储info到txt文件
    with open(path, 'w') as f:
        f.write(info)


def cal_Cyclomatic_complexity(G):
    # 计算有向图的圈复杂度
    # 边数
    edge_num = G.number_of_edges()
    # 节点数
    node_num = G.number_of_nodes()
    # p连接组件数目
    p_component_num = nx.number_weakly_connected_components(G)
    # 圈复杂度
    complexity = edge_num - node_num + 2*p_component_num
    return complexity


def cal_Cyclomatic_complexity_PLCG(file_path):
    # 计算函数级调用图的圈复杂度
    # 读取CG的dot文件
    G = graph_read(file_path)

    # 删除库函数节点和\\n节点
    remove_list = []
    for node in G.nodes():
        node_info = G.nodes[node]
        if 'label' in node_info:
            if 'Library function' in node_info['label']:
                remove_list.append(node)

        if node == '\\n':
            remove_list.append(node)
    G.remove_nodes_from(remove_list)

    # 计算图的复杂度
    complexity = cal_Cyclomatic_complexity(G)
    return complexity


def cal_Cyclomatic_complexity_FLCG(file_path):
    # 计算文件级调用图的圈复杂度
    # 读取CG的dot文件
    G = graph_read(file_path)

    # 删除库函数节点和\\n节点
    remove_list = []
    for node in G.nodes():
        node_info = G.nodes[node]
        if 'label' in node_info:
            if 'Library function' in node_info['label']:
                remove_list.append(node)

        if node == '\\n':
            remove_list.append(node)
    G.remove_nodes_from(remove_list)

    # 计算图的复杂度
    complexity = cal_Cyclomatic_complexity(G)
    return complexity


def cal_Cyclomatic_complexity_CFG(CFG):
    # 读取cfg的dot文件
    G = graph_read(CFG)

    # 删除\\n节点
    remove_list = []
    for node in G.nodes():
        if node == '\\n':
            remove_list.append(node)
    G.remove_nodes_from(remove_list)

    # 计算图的复杂度
    complexity = cal_Cyclomatic_complexity(G)
    return complexity


def getfilelist(path):
    # Convert relative path to absolute path
    path = os.path.abspath(path)
    # Get all files in the path
    filelist = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if "unprocessed" not in file and '.cfg.dot' in file:
                filelist.append(os.path.join(root, file).replace('\\', '/'))

    return filelist


def MMo_2_S(CFG, K):
    print("MMo_2_S")
    # K 圈复杂度阈值
    # 计算圈复杂度
    num = 0
    K_list = []
    CFG_list = getfilelist(CFG)
    for file in CFG_list:
        complexity = cal_Cyclomatic_complexity_CFG(file)
        if complexity > K:
            K_list.append(file)
        num += 1

    MMo_2_S = 1-(num/len(CFG_list))
    return MMo_2_S, K_list


def cal_Call_depth(project_name, K):
    file_path = project_name + "/graphs/PLCG.dot"
    print("cal_Call_depth")
    print("调用深度阈值: ", K)
    # 计算函数调用深度
    # 读取CG的dot文件

    # 读取project_name + "/code_file_match.txt"
    code_file_match = {}
    encoding = get_file_encoding(project_name + "/code_file_match.txt")
    with open(project_name + "/code_file_match.txt", 'r', encoding=encoding) as f:
        for line in f.readlines():
            line = line.strip()
            code_file_match[line.split(':: ')[0]] = line.split(':: ')[1]

    # 读取PLCG
    G = nx.DiGraph(nx.nx_pydot.read_dot(file_path))

    # 删除库函数节点和\\n节点
    remove_list = []
    for node in G.nodes():
        node_info = G.nodes[node]

        if 'file' in node_info:
            file = node_info['file'].replace('"', '')
            if file != "Library function":
                G.nodes[node]['file'] = code_file_match[file]

        if node == '\\n':
            remove_list.append(node)
    G.remove_nodes_from(remove_list)

    # 获得入度为0的节点
    in_degree_0 = []
    for node in G.nodes():
        if G.in_degree(node) == 0:
            in_degree_0.append(node)
    # print(in_degree_0)
    # 获得出度为0的节点
    out_degree_0 = []
    for node in G.nodes():
        if G.out_degree(node) == 0:
            out_degree_0.append(node)
    # print(out_degree_0)

    # 获得所有从入度为0的节点到出度为0的节点的路径
    all_path = []
    for node in in_degree_0:
        for node2 in out_degree_0:
            all_path += list(nx.all_simple_paths(G, source=node, target=node2))
    # print(all_path)

    # 获得长度大于等于K的路径
    path = []
    for i in range(len(all_path)):
        if len(all_path[i]) >= K:
            temp_path = []
            for j in range(len(all_path[i])):
                # 获得label
                file = G.nodes[all_path[i][j]]['file'].replace('"', '')
                name = G.nodes[all_path[i][j]]['label'].replace('"', '').split(': ')[
                    1]
                temp_path.append(file+"/"+name+"()")
            path.append(temp_path)
    # print(path)
    return path, all_path


def cal_Reusability_of_assets(file_path):
    print("cal_Reusability_of_assets")
    # 计算资产的可重用性
    # 读取CG的dot文件
    G = graph_read(file_path)
    # 删除库函数节点和\\n节点
    remove_list = []
    for node in G.nodes():
        node_info = G.nodes[node]
        if 'label' in node_info:
            if 'Library function' in node_info['label']:
                remove_list.append(node)

        if node == '\\n':
            remove_list.append(node)
    G.remove_nodes_from(remove_list)

    # 获得所有入度大于1的节点
    in_degree_1 = []
    for node in G.nodes():
        if G.in_degree(node) > 1:
            # 获得label
            label = G.nodes[node]['label']
            in_degree_1.append(label)

    return in_degree_1, len(G.nodes())


# def ComponentRedundancy(cfg1:nx.DiGraph, cfg2:nx.DiGraph, dt1:nx.DiGraph, dt2: nx.DiGraph):
#     dm1 = np.array(cfg_dominance_matrix(cfg1, dt1))
#     dm2 = np.array(cfg_dominance_matrix(cfg2, dt2))
#     return np.array_equal(dm1,dm2)

def ComponentRedundancy(dm1_path: str, dm2_path: str):
    dm1 = np.load(dm1_path)
    dm2 = np.load(dm2_path)
    return np.array_equal(dm1, dm2)


def sysRedundantComponents(project_folder):
    # 读取project_name + "/code_file_match.txt"
    code_file_match = {}
    encoding = get_file_encoding(project_folder + "/code_file_match.txt")
    with open(project_folder + "/code_file_match.txt", 'r', encoding=encoding) as f:
        for line in f.readlines():
            line = line.strip()
            code_file_match[line.split(':: ')[0]] = line.split(':: ')[1]
    print("sysRedundantComponents")
    cfgs = {}
    redundant_comps = []
    cfg_paths = os.path.join(project_folder, "graphs")
    for root, dirs, files in os.walk(cfg_paths):
        for file in files:
            if "unprocessed" not in file and '.cfg.dot' == file[-8:]:

                func_name = file.split('_')[1].split('.')[0]
                cfgs[root + ":" +
                     func_name] = os.path.join(root, file[:-8]+".dm.npy")
    for i in range(len(cfgs.keys())):
        for j in range(len(cfgs.keys())):
            if i != j:
                keyi = list(cfgs.keys())[i]
                keyj = list(cfgs.keys())[j]
                if ComponentRedundancy(cfgs[keyi], cfgs[keyj]) == True:
                    keyi = keyi.replace("\\", "/")
                    # 删去最后一个/后面的内容
                    f_list = keyi.split(':')
                    # 删除最后一个
                    filei = f_list[0] + ":" + f_list[1]
                    filei = filei.replace("/graphs", "/code")
                    # 将最后的_c转换为.c
                    filei = filei[:-2] + "." + filei[-1]
                    # 转换为绝对路径
                    abs_filei = os.path.abspath(filei).replace('\\', '/')
                    keyi = code_file_match[abs_filei] + \
                        "/" + keyi.split(':')[-1]

                    keyj = keyj.replace("\\", "/")
                    # 删去最后一个/后面的内容
                    f_list = keyj.split(':')
                    filej = f_list[0] + ":" + f_list[1]
                    filej = filej.replace("/graphs", "/code")
                    # 将最后的_c转换为.c
                    filej = filej[:-2] + "." + filej[-1]
                    # 转换为绝对路径
                    abs_filej = os.path.abspath(filej).replace('\\', '/')
                    keyj = code_file_match[abs_filej] + \
                        "/" + keyj.split(':')[-1]

                    redundant_comps.append([keyi+"()", keyj+"()"])
    print("sysRedundantComponents 已完成")
    return redundant_comps


def get_degree(file_path, K_in, K_out):
    print("get_degree")
    # 读取CG的dot文件
    G = graph_read(file_path)

    # 删除库函数节点和\\n节点
    remove_list = []
    for node in G.nodes():
        node_info = G.nodes[node]
        if 'label' in node_info:
            if 'Library function' in node_info['label']:
                remove_list.append(node)

        if node == '\\n':
            remove_list.append(node)
    G.remove_nodes_from(remove_list)

    # 获得入度和出度大于等于K的节点
    in_degree_K = []
    out_degree_K = []
    for node in G.nodes():
        if G.in_degree(node) >= K_in:
            # 获得label
            if 'label' in G.nodes[node]:
                label = G.nodes[node]['label']
            in_degree_K.append(label)
        if G.out_degree(node) >= K_out:
            # 获得label
            if 'label' in G.nodes[node]:
                label = G.nodes[node]['label']
            out_degree_K.append(label)

    return in_degree_K, out_degree_K


def get_Standalone_components(file_path):
    file_path = file_path.replace("\\", "/")
    print("get_Standalone_components")
    if not os.path.exists(file_path):
        return [], []
    # 获取独立组件
    # 读取组件图的dot文件
    G = graph_read(file_path)
    # 删除\\n节点
    remove_list = []
    for node in G.nodes():
        if node == '\\n':
            remove_list.append(node)
    G.remove_nodes_from(remove_list)

    comp_list = []
    comp_dic = {}
    # 获取组件
    for node in G.nodes():
        temp_node = G.nodes[node]
        if "comp" in temp_node.keys():
            comp = temp_node["comp"].replace("\"", "")
            if comp not in comp_dic.keys():
                comp_dic[comp] = []
                comp_dic[comp].append(node)
            else:
                comp_dic[comp].append(node)

            if comp not in comp_list:
                comp_list.append(comp)

    # 获取各个组件的父组件
    comp_parent = {}
    for key, value in comp_dic.items():
        # 获取组件的父组件
        temp_parent = []
        for node in value:
            for parent in G.predecessors(node):
                if parent not in value:
                    temp_parent.append(parent)
        comp_parent[key] = []
        for node in temp_parent:
            parent_comp = G.nodes[node]["comp"].replace("\"", "")
            if parent_comp not in comp_parent[key]:
                comp_parent[key].append(parent_comp)

    Standalone_components_list = []
    for key, value in comp_parent.items():
        if len(value) == 0:
            Standalone_components_list.append(key)
    return Standalone_components_list, comp_list


def get_Redundant_components(file_path, project_folder):

    print("get_Redundant_components")
    # 获取冗余组件
    # 读取组件图的dot文件
    print(file_path)
    if not os.path.exists(file_path):
        return [], []
    G = graph_read(file_path)
    # 删除\\n节点

    remove_list = []
    for node in G.nodes():
        if node == '\\n':
            remove_list.append(node)
    G.remove_nodes_from(remove_list)
    # print(1)
    comp_list = []
    comp_dic = {}
    # 获取组件
    for node in G.nodes():
        temp_node = G.nodes[node]
        if "comp" in temp_node.keys():
            comp = temp_node["comp"].replace("\"", "")
            if comp not in comp_dic.keys():
                comp_dic[comp] = []
                node_label = temp_node["label"].replace("\"", "")
                comp_dic[comp].append(node_label)
            else:
                node_label = temp_node["label"].replace("\"", "")
                comp_dic[comp].append(node_label)

            if comp not in comp_list:
                comp_list.append(comp)
    print(2)
    # 获取冗余函数
    redundant_func = []
    redundant_temp = sysRedundantComponents(project_folder)
    for func_list in redundant_temp:
        for func in func_list:
            f = func.split('/')[-1]
            redundant_func.append(f)
    # 获取冗余组件
    print(3)
    redundant_comp = []
    for key, value in comp_dic.items():
        # 判断该组件包含的函数是否全部是冗余函数
        flag = True
        for func in value:
            if func not in redundant_func:
                flag = False
                break
        if flag == True:
            redundant_comp.append(key)
    print(4)
    return redundant_comp, comp_list


def get_info(file_path):
    # 读取CG的dot文件
    info = graph_information(file_path)
    # 存储info到txt文件
    print2txt(info, file_path+'.info')


def get_func_info(project):
    print('get_func_info - in ')
    CG_dot = project + "/graphs/PLCG.dot"
    CG = nx.DiGraph(nx.nx_pydot.read_dot(CG_dot))
    # 读取project_name + "/code_file_match.txt"
    code_file_match = {}
    encoding = get_file_encoding(project + "/code_file_match.txt")
    with open(project + "/code_file_match.txt", 'r', encoding=encoding) as f:
        for line in f.readlines():
            line = line.strip()
            code_file_match[line.split(':: ')[0]] = line.split(':: ')[1]
    # 删除库函数节点和\\n节点
    remove_list = []
    for node in CG.nodes():
        node_info = CG.nodes[node]
        if 'label' in node_info:
            if 'Library function' in node_info['label']:
                remove_list.append(node)

        if 'file' in node_info:
            file = node_info['file'].replace('"', '')
            if file != "Library function" and file != "Unrecognized File":
                CG.nodes[node]['file'] = code_file_match[file]

        if node == '\\n':
            remove_list.append(node)
    CG.remove_nodes_from(remove_list)
    print('get_func_info - 882')
    # 获取函数的信息
    in_degree_info = {}
    # 正无穷
    in_degree_info["minIn"] = float("inf")
    # 负无穷
    in_degree_info["maxIn"] = float("-inf")
    out_degree_info = {}
    out_degree_info["minOut"] = float("inf")
    out_degree_info["maxOut"] = float("-inf")
    func_info = {}
    sum_in_degree = 0
    sum_out_degree = 0
    for node in CG.nodes():
        node_info = CG.nodes[node]
        name = ""
        if 'label' in node_info:
            name = node_info['label'].replace("\"", "").split(": ")[1]

        file = ""
        if 'file' in node_info:
            file = node_info['file'].replace("\"", "")

        in_degree = CG.in_degree(node)
        out_degree = CG.out_degree(node)
        key = file+"/"+name+"()"
        func_info[key] = {"inDegree": in_degree, "outDegree": out_degree}

        # 找最大入度和最小入度
        if in_degree > in_degree_info["maxIn"]:
            in_degree_info["maxIn"] = in_degree
            in_degree_info["maxInFunc"] = name+"()"
            in_degree_info["maxInFuncPath"] = file
        if in_degree < in_degree_info["minIn"]:
            in_degree_info["minIn"] = in_degree
            in_degree_info["minInFunc"] = name+"()"
            in_degree_info["minInFuncPath"] = file

        # 找最大出度和最小出度
        if out_degree > out_degree_info["maxOut"]:
            out_degree_info["maxOut"] = out_degree
            out_degree_info["maxOutFunc"] = name+"()"
            out_degree_info["maxOutFuncPath"] = file
        if out_degree < out_degree_info["minOut"]:
            out_degree_info["minOut"] = out_degree
            out_degree_info["minOutFunc"] = name+"()"
            out_degree_info["minOutFuncPath"] = file

        sum_in_degree += in_degree
        sum_out_degree += out_degree
    print('get_func_info - 932')
    # 获取平均入度和平均出度
    func_num = len(CG.nodes())
    avg_in_degree = sum_in_degree / func_num
    avg_out_degree = sum_out_degree / func_num
    in_degree_info["avgIn"] = avg_in_degree
    out_degree_info["avgOut"] = avg_out_degree

    cycl_info = {}
    # 负无穷
    cycl_info["maxComplex"] = float("-inf")
    # 正无穷
    cycl_info["minComplex"] = float("inf")
    # 获取圈复杂度
    CFG = project + "/graphs"
    CFG_list = getfilelist(CFG)
    cycl_sum = 0
    num = 0
    for file in CFG_list:
        complexity = cal_Cyclomatic_complexity_CFG(file)
        name = file.split("/")[-1][:-8].replace('processed_', '')
        for key in func_info.keys():
            func_name = key.split("/")[-1][:-2]
            file_list = key.split("/")[:-1]
            file_path = ""
            for f in file_list:
                file_path += f+"/"
            if name == func_name:
                func_info[key]["cycl"] = complexity
                cycl_sum += complexity
                num += 1

                if complexity > cycl_info["maxComplex"]:
                    cycl_info["maxComplex"] = complexity
                    cycl_info["maxComplexFunc"] = func_name + "()"
                    cycl_info["maxComplexFuncPath"] = file_path[:-1]
                if complexity < cycl_info["minComplex"]:
                    cycl_info["minComplex"] = complexity
                    cycl_info["minComplexFunc"] = func_name + "()"
                    cycl_info["minComplexFuncPath"] = file_path[:-1]
                break
    print('get_func_info - 974')
    # 获取平均圈复杂度
    avg_cycl = 0 if num == 0 else cycl_sum / num
    cycl_info["avgComplex"] = avg_cycl

    return func_info, in_degree_info, out_degree_info, cycl_info


if __name__ == "__main__":
    forder = "project/CUnit"
    # forder = "flask_back_end/Design_recovery/project/" + projectname
    # file_path = forder + '/graphs/clustered_sdg.dot_GNwithoutcomp.dot'
    # redundant_comp, comp_list = get_Redundant_components(file_path, forder)
    # 读取CG的dot文件
    # file_path = 'project_cases\\wuziqi\\PLCG.dot'
    # graph_information = graph_information('project_cases\\wuziqi\\PLCG.dot')
    # print2txt(graph_information, 'project_cases\wuziqi\PLCG.dot')
    import sys
    # get_info(sys.argv[1])
    # sysRedundantComponents(sys.argv[1])
    # comp_FILE = "wuziqi\\graphs\\PLCG.dot_GNwithoutcomp.dot"
    # get_Standalone_components(comp_FILE)
    # get_Redundant_components(comp_FILE, "wuziqi")

    # get_degree("wuziqi\\graphs\\PLCG.dot", 2, 2)
    # MMo_2_S("wuziqi\\graphs", 2)

    # forder = 'CUnit_dr'
    # file_path = 'CUnit_dr\\graphs\\clustered_sdg.dot_GNwithoutcomp.dot'
    # redundant_comp, comp_list = get_Redundant_components(file_path,forder)
    # # self.matrix["可靠性"]["容错性"]['组件的冗余度'] = len(redundant_comp)/len(comp_list)
    # #
    # Standalone_components_list, comp_list = get_Standalone_components(file_path)
    # # self.matrix['可维护性']['模块化']['组件间的耦合度'] = len(Standalone_components_list)/len(comp_list)
    # #
    # # file_path = 'CUnit_dr\\graphs\\PLCG.dot'
    # in_degree_1, asset_num = cal_Reusability_of_assets(file_path)
    # # self.matrix['可维护性']['可复用性']['资产的可重用性'] = len(in_degree_1)/asset_nu
    # # self.matrix["坏味"] = {"长函数":self.var_assess.var_long_function,
    # #                        "长参数":self.var_assess.var_long_parm,
    # #                        "过多注释比例":self.var_assess.var_long_note}
    #                        # "大扇入扇出":self.var_assess.var_long_fan_in_out
    # file_path = 'CUnit_dr\\graphs\\PLCG.dot'
    # degree_dict = {}
    # degree_dict['扇入'], degree_dict['扇出'] = get_degree(file_path, 2,2)
    # # self.matrix['坏味']['扇入扇出'] = degree_dict
    # #
    # file_path = 'CUnit_dr\\graphs'
    # index,K_list = MMo_2_S(file_path, 2)
    # # self.matrix['坏味']['高圈复杂度'] = index
    # #
    # file_path = 'CUnit_dr\\graphs\\PLCG.dot'
    # deeppaths,_ = cal_Call_depth(file_path,2)
    # deepdict = dict()
    # index = 0
    # for dp in deeppaths:
    #      deepdict[str(index)] = dp
    # # self.matrix['坏味']['深度调用'] = deepdict
    # #
    # file_path = 'CUnit_dr'
    # redundant_comps = sysRedundantComponents(file_path)
    # tempdict = dict()
    # for r in redundant_comps:
    #      tempdict[str(r)] = dict()
    #
    # self.matrix['坏味']['代码克隆'] = tempdict

    get_func_info(
        r"D:\design_reconstruction\week47\C_Quality_Evaluator\app\Design_recovery\project\s2")
    # sysRedundantComponents("E:/C_master/C_app/Design_recovery/project/CUnit_test2")
