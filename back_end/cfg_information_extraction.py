import networkx as nx

# given a cfg calculate the number of blocks in the cfg
def cfg_blocks(cfg: nx.DiGraph) -> int:
    count = 0
    # if the node's name starts with 'Node' then it is a block
    # else if the node's name starts with a 'B' and continue with a number then it is a part of a block
    node_blocks = set()
    for node in cfg.nodes:
        if node.startswith('Node'):
            count += 1
        else:
            if node.startswith('B'):
                block_name, sub_id = node[1:].split('-')[0], node[1:].split('-')[1]
                if block_name not in node_blocks:
                    node_blocks.add(block_name)
                    count += 1
    return count

# given a cfg calculate the number of back edges in the cfg
def cfg_back_edges(cfg: nx.DiGraph) -> int:
    count = 0
   # firstly need to find the dfs tree of the graph
    dfs_tree = nx.dfs_tree(cfg)
    nx.nx_pydot.write_dot(dfs_tree, "dfs.dot")
    # for all edges in the cfg if the edge starts from a node and ends with its parent in the dfs tree then it is a back edge
    for edge in cfg.edges:
        # if edge[0] is in the dfs tree and edge[1] is the parent of edge[0] in the dfs tree then it is a back edge
        if edge[0] in dfs_tree and nx.has_path(dfs_tree, edge[1], edge[0]):
            count += 1
    return count

# given a cfg calculate the loop connectedness of the cfg
def cfg_loop_connectedness(cfg: nx.DiGraph) -> float:
    # firstly need to find the dfs tree of the graph
    dfs_tree = nx.dfs_tree(cfg)
    start_node = None
    end_node = None
    for node in cfg.nodes:
        # find the start node of the cfg
        if "(ENTRY)" in cfg.nodes[node]['label']:
            start_node = node
        # find the end node of the cfg
        if "(EXIT)" in cfg.nodes[node]['label']:
            end_node = node
    if start_node is None or end_node is None:
        return 0
    # find all paths from the start node to the end node
    paths = nx.all_simple_paths(cfg, start_node, end_node)
    loop_connectedness = 0
    # find the max number of back edges in each path
    for path in paths:
        back_edges = 0
        for i in range(len(path) - 1):
            if path[i] in dfs_tree and nx.has_path(dfs_tree, path[i+1], path[i]):
                back_edges += 1
        if back_edges > loop_connectedness:
            loop_connectedness = back_edges
    return loop_connectedness
    


# given a cfg calculate the connectivity matrix of the cfg
def cfg_connectivity_matrix(cfg: nx.DiGraph) -> list:
    # calculaye the connectivity matrix of the cfg
    connectivity_matrix = []
    # for each node in the cfg
    for node in cfg.nodes:
        temp = []
        # for each node in the cfg
        for node2 in cfg.nodes:
            # if there is an edge from node to node2 then the value is 1 else 0
            if cfg.has_edge(node, node2):
                temp.append(1)
            else:
                temp.append(0)
        connectivity_matrix.append(temp)
    return connectivity_matrix

# given a cfg calculate the precedence matrix of the cfg
def cfg_precedence_matrix(cfg: nx.DiGraph) -> list:
    # calculate the precedence matrix of the cfg
    precedence_matrix = []
    # for each node in the cfg
    for node in cfg.nodes:
        temp = []
        # for each node in the cfg
        for node2 in cfg.nodes:
            # if there is a path from node to node2 then the value is 1 else 0
            if nx.has_path(cfg, node, node2):
                temp.append(1)
            else:
                temp.append(0)
        precedence_matrix.append(temp)
    return precedence_matrix

# given a cfg calculate the dominance matrix of the cfg
def cfg_dominance_matrix(cfg: nx.DiGraph, dt: nx.DiGraph) -> list:
    # calculate the dominance matrix of the cfg
    dominance_matrix = []
    # for each node in the cfg
    for node in cfg.nodes:
        temp = []
        # for each node in the cfg
        for node2 in cfg.nodes:
            # if node is parent node of node2 in dt then the value is 1 else 0
            if node2 in dt.nodes:
                if node in list(dt.predecessors(node2)):
                    temp.append(1)
                else:
                    temp.append(0)
            else:
                temp.append(0)
        dominance_matrix.append(temp)
    return dominance_matrix

# given a pdg calculate the number of control dependence edges in the pdg
def pdg_control_dependence_edges(pdg: nx.MultiDiGraph) -> int:
    # if the edge is not a control dependence edge then it has a style="dotted" attribute
    count = 0
    for edge in pdg.edges:
        try:
            if pdg.edges[edge]['style'] != 'dotted':
                count += 1
        except KeyError:
            count += 1
    return count

# given a pdg calculate the number of data dependence edges in the pdg
def pdg_data_dependence_edges(pdg: nx.MultiDiGraph) -> int:
    # if the edge is a data dependence edge then it has a style="dotted" attribute
    count = 0
    for edge in pdg.edges:
        try:
            if pdg.edges[edge]['style'] == 'dotted':
                count += 1
        except KeyError:
            pass
    return count


# given a pdg calculate the average number of control dependence edges in the pdg
def avg_pdg_control_dependence_edges(pdg: nx.MultiDiGraph) -> float:
    # if the edge is not a control dependence edge then it has a style="dotted" attribute
    count = 0
    for edge in pdg.edges:
        try:
            if pdg.edges[edge]['style'] != 'dotted':
                count += 1
        except KeyError:
            count += 1
    return count / len(pdg.nodes)

# given a pdg calculate the average number of data dependence edges in the pdg
def avg_pdg_data_dependence_edges(pdg: nx.MultiDiGraph) -> float:
    # if the edge is a data dependence edge then it has a style="dotted" attribute
    count = 0
    for edge in pdg.edges:
        try:
            if pdg.edges[edge]['style'] == 'dotted':
                count += 1
        except KeyError:
            pass
    return count / len(pdg.nodes)


if __name__ == "__main__":
    import sys
    cfg_path = sys.argv[1]
    # cfg = nx.DiGraph(nx.nx_pydot.read_dot(cfg_path))
    # print("CFG BLOCKs NUMBERS: ", cfg_blocks(cfg))
    # print("CFG BACK EDGES NUMBERS: ", cfg_back_edges(cfg))
    # print("CFG ABNORMAL EDGES NUMBERS: ", 0)
    # print("CFG IMPOISSIBLE EDGES NUMBERS: ", 0)
    # import pprint
    
    # print("CFG LOOP CONNECTEDNESS: ", cfg_loop_connectedness(cfg))

    # print("CFG CONNECTIVITY MATRIX: ")
    # pprint.pprint(cfg_connectivity_matrix(cfg))
    # print("CFG PRECEDENCE MATRIX: ")
    # pprint.pprint(cfg_precedence_matrix(cfg))
    # dt_path = sys.argv[2]
    # dt = nx.DiGraph(nx.nx_pydot.read_dot(dt_path))
    # print("CFG DOMINANCE MATRIX: ")
    # pprint.pprint(cfg_dominance_matrix(cfg, dt))

    # pdg_path = sys.argv[3]
    # pdg = nx.MultiDiGraph(nx.nx_pydot.read_dot(pdg_path))
    # print("PDG CONTROL DEPENDENCE EDGES: ", pdg_control_dependence_edges(pdg))
    # print("PDG DATA DEPENDENCE EDGES: ", pdg_data_dependence_edges(pdg))
    # print("PDG AVERAGE CONTROL DEPENDENCE EDGES: ", round(avg_pdg_control_dependence_edges(pdg),4))
    # print("PDG AVERAGE DATA DEPENDENCE EDGES: ", round(avg_pdg_data_dependence_edges(pdg),4))


