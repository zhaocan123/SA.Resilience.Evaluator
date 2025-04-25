# this file is for construct a cdg for a cfg
import networkx as nx
import numpy as np

def find_dominate_tree(G: nx.DiGraph):
    dominate_nodes = dict()
    dominate_tree = nx.DiGraph()
    if "\\n" in G.nodes:
        G.remove_node("\\n")
    for node in G.nodes:
        if "(EXIT)" in G.nodes[node]['label']:
            exit_node = node
            dominate_tree.add_node(node)
            dominate_tree.nodes[node]['label'] = G.nodes[node]['label']
            dominate_nodes[exit_node] = set()
            break
    for node in G.nodes:
        if node != exit_node:
            dominate_tree.add_node(node)
            dominate_tree.add_edge(exit_node, node)
            dominate_nodes[exit_node].add(node)
            dominate_tree.nodes[node]['label'] = G.nodes[node]['label']

    for node in G.nodes:
        if "(EXIT)" not in G.nodes[node]['label'] and "(ENTRY)" not in G.nodes[node]['label']:
            G_ = G.copy()
            reachable_nodes = set(nx.shortest_path(G, exit_node).keys())
            G_.remove_node(node)
            reachable_nodes_ = set(nx.shortest_path(G_, exit_node).keys())
            dominate_nodes[node] = reachable_nodes - \
                reachable_nodes.intersection(reachable_nodes_) - set([node])

            for d_node in dominate_nodes[node]:
                for edge in list(dominate_tree.edges):
                    if edge[1] == d_node:
                        if edge[0] != edge[1]:
                            dominate_tree.add_edge(node, edge[1])
            for node in list(nx.topological_sort(dominate_tree)):
                # for node in dominate_tree.nodes:
                dominate_tree.nodes[node]['shape'] = 'record'
                while len(list(dominate_tree.predecessors(node))) >= 2:
                    path = nx.shortest_path(dominate_tree, exit_node, node)
                    dominate_tree.remove_edge(path[-2], path[-1])

    return dominate_tree


def find_dominate_frontier(dominate_tree: nx.DiGraph, G: nx.DiGraph):
    # nx.nx_pydot.write_dot(dominate_tree, "dt.dot")
    dominate_frontier = dict()
    for node in G.nodes:
        preds = list(G.predecessors(node))
        if len(preds) > 1:
            # print(node, preds)
            for pred_node in preds:
                runner = pred_node
                # print("runner", runner, list(dominate_tree.predecessors(node)))
                while runner != list(dominate_tree.predecessors(node))[0]:
                    try:
                        dominate_frontier[runner].add(node)
                    except KeyError:
                        dominate_frontier[runner] = set([node])
                    if len(list(dominate_tree.predecessors(runner))) > 0:
                        runner = list(dominate_tree.predecessors(runner))[0]
                    else:
                        break
    return dominate_frontier


def construct_cdg(cfg: nx.DiGraph):
    cfg_ = cfg.copy()
    for edge in list(cfg_.edges):
        cfg_.remove_edge(edge[0], edge[1])
        cfg_.add_edge(edge[1], edge[0])

    dominate_tree = find_dominate_tree(cfg_)
    dominate_frontier = find_dominate_frontier(dominate_tree, cfg_)

    cdg = nx.DiGraph()
    entry_node = None
    exit_node = None
    for node in cfg.nodes:
        if "(ENTRY)" in cfg.nodes[node]['label']:
            cdg.add_node(node)
            cdg.nodes[node]['label'] = cfg.nodes[node]['label']
            cdg.nodes[node]['shape'] = 'record'
            entry_node = node
            break

    for node in cfg.nodes:
        if "(EXIT)" in cfg.nodes[node]['label']:
            cdg.add_node(node)
            cdg.nodes[node]['label'] = cfg.nodes[node]['label']
            cdg.nodes[node]['shape'] = 'record'
            exit_node = node
            break

    for node in cfg.nodes:
        if not "(ENTRY)" in cfg.nodes[node]['label'] and not "(EXIT)" in cfg.nodes[node]['label']:
            cdg.add_node(node)
            cdg.add_edge(entry_node, node)
            cdg.nodes[node]['label'] = cfg.nodes[node]['label']
            cdg.nodes[node]['shape'] = 'record'

    for k, v in dominate_frontier.items():
        for node in v:
            if node != k:
                cdg.add_edge(node, k)

    for edge in list(cdg.edges):
        if edge[1] != entry_node and edge[0] == entry_node:
            cdg.remove_edge(edge[0], edge[1])
            if not nx.has_path(cdg, entry_node, edge[1]):
                cdg.add_edge(edge[0], edge[1])

    cdg.remove_node(exit_node)
    for node in list(cdg.nodes):
        labels = cdg.nodes[node]['label'].split('\\l')
        # print(labels)
        if "ENTRY" in labels[0]:
            cdg.nodes[node]['label'] = "ENTRY"
        elif "EXIT" in labels[0]:
            cdg.nodes[node]['label'] = "EXIT"
        elif len(labels) <= 2 and labels[1].strip() == '}"':
            cdg.remove_node(node)
        else:
            cdg.nodes[node]['label'] = '"{' + '\\l'.join(labels[1:])
    return dominate_tree, cdg

def cfg_dominance_matrix(cfg: nx.DiGraph, dt: nx.DiGraph):
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
    return np.array(dominance_matrix)

def cdg(cfg: nx.DiGraph):
    # return cdg and dominate matrix
    if '\\n' in cfg.nodes:
        cfg.remove_node('\\n')
    dominate_tree, cdg = construct_cdg(cfg)
    # calculate and save dominate matrix
    dm = cfg_dominance_matrix(cfg, dominate_tree)
    for node in list(dominate_tree.nodes):
        label = dominate_tree.nodes[node]['label']
        if "(ENTRY)" in label:
            dominate_tree.nodes[node]['label'] = "ENTRY"
        elif "(EXIT)" in label:
            dominate_tree.nodes[node]['label'] = "EXIT"
        else:
            index = label.find('\\l')
            dominate_tree.nodes[node]['label'] = '"{' + \
                label[index+2:-2] + '}"'
    return cdg, dm