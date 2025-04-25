from attack_surface_info import convert_info_format, AttackPattern, attack_pattern_table
import networkx as nx
import os
import json

library_functions = {
    'input': [
        'scanf', 'fread', 'sscanf', 'getchar', 'open'
        ],
    'output': [
        'printf', 'fwrite', 'system', 'fflush', 'open', 'asprintf', 'fprintf', 'fputs'
        ],
    'objects':{
        'printf':'stdout',
        'asprintf':'stdout',
        'scanf':'stdin',
        'sscanf':'stdin',
        'getchar':'stdin',
        'socket':'socket',
        'open':'file',
        'fprintf':'file',
        'fputs':'file',
        'fread':'file',
        'fflush':'file',
        'fwrite':'file',
        'system':'exec',

    }
    }

source_attack_table = {
    "main": [1],
    "stdio.h:scanf": [2],
    "stdio.h:printf": [3],
}

def is_input_node(node_label: str, project_path: str):
    all_path = node_label.strip().strip('"').split(':')[0].strip().strip('"').strip()
    function_name = node_label.strip().strip('"').split(':')[-1].strip().strip('"').strip()
    if os.path.abspath(all_path).startswith(os.path.abspath(project_path)):
        # if current node is not library node
        if function_name == "main":
            return True
    else:
        # find function name:        
        if function_name in library_functions["input"]:
            return True
    return False

def is_output_node(node_label: str, project_path: str):
    all_path = node_label.strip().strip('"').split(':')[0].strip().strip('"').strip()
    function_name = node_label.strip().strip('"').split(':')[-1].strip().strip('"').strip()
    if os.path.abspath(all_path).startswith(os.path.abspath(project_path)):
        # if current node is not library node
        if function_name == "main":
            return True
    else:
        # find function name:        
        if function_name in library_functions["output"]:
            return True
    return False

def find_node_objects(node_label):
    all_path = node_label.strip().strip('"').split(':')[0].strip().strip('"').strip()
    library_name = all_path.split("/")[-1]
    function_name = node_label.strip().strip('"').split(':')[-1].strip().strip('"').strip()
    ud_object = f"{library_functions['objects'][function_name]}::{node_label.split('/')[-1]}"
    return [ud_object]

class AttackSurface:
    def __init__(self):
        self.entry_points_plcg = {}
        self.exit_points_plcg = {}
        self.node_names = {}
        self.node_types = {}
        self.untrusted_items = set()
        self.channels = set()
        self.pipe_filter_graph = None
        self.plcg = None
        self.project_path = None
        self.possible_attacks = None
        self.node_resilience = None

    def attack_surface_detection(self, pipe_filter_graph: nx.DiGraph, plcg: nx.DiGraph, project_path:str):
        self.pipe_filter_graph = pipe_filter_graph
        self.plcg = plcg
        self.project_path = project_path
        for node in plcg.nodes:
            node_label = plcg.nodes[node]['label']
            node_name = node_label.split("/")[-1].strip('"')
            if node not in self.node_names:
                self.node_names[node] = node_name
            if plcg.nodes[node]['file'].strip().strip('"') == "Library function":
                self.node_types[node] = ["Library"]
            else:
                self.node_types[node] = ["Function"]
            if is_input_node(node_label, project_path):
                self.entry_points_plcg[node] = node_name
                if node_name.split(':')[-1] == "main":
                    self.untrusted_items.add(f"cmd::{node_name}")
                if plcg.nodes[node]['file'].strip().strip('"') == "Library function":
                    for ud_object in find_node_objects(node_label):
                        self.untrusted_items.add(ud_object)
                    for call_node in plcg.predecessors(node):
                        call_node_name = plcg.nodes[call_node]['label'].split("/")[-1].strip('"')
                        self.entry_points_plcg[call_node] = f"{node_name}::{call_node_name}"
                        self.node_names[call_node] = f"{node_name}::{call_node_name}"
                        self.channels.add((node_name, call_node_name))
            if is_output_node(node_label, project_path):
                self.exit_points_plcg[node] = node_name                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
                if node_name.split(':')[-1] == "main":
                    self.untrusted_items.add(f"cmd::{node_name}")
                if plcg.nodes[node]['file'].strip().strip('"') == "Library function":
                    for ud_object in find_node_objects(node_label):
                        self.untrusted_items.add(ud_object)
                    for call_node in plcg.predecessors(node):
                        call_node_name = plcg.nodes[call_node]['label'].split("/")[-1].strip('"')
                        self.exit_points_plcg[call_node] = f"{node_name}::{call_node_name}"
                        self.node_names[call_node] = f"{node_name}::{call_node_name}"
                        self.channels.add((call_node_name, node_name))

    def generate_possible_attacks(self):
        possible_attacks = []
        for node in self.entry_points_plcg:
            node_name = self.node_names[node]
            if "::" in node_name:
                library_info = node_name.split("::")[0].split(':')[0] + ":" + node_name.split("::")[0].split(':')[2]
            else:
                library_info = "main"
            if library_info in source_attack_table:
                attacks = source_attack_table[library_info]
            else:
                attacks = []
            possible_attacks.append((node, attacks))
        for node in self.exit_points_plcg:
            node_name = self.node_names[node]
            if "::" in node_name:
                library_info = node_name.split("::")[0].split(':')[0] + ":" + node_name.split("::")[0].split(':')[2]
            else:
                library_info = "main"
            if library_info in source_attack_table:
                attacks = source_attack_table[library_info]
            else:
                attacks = []
            possible_attacks.append((node, attacks))
        self.possible_attacks = possible_attacks

    def cal_node_reliability(self):
        """calculate the reliability for each node in plcg"""
        node_reliability = {}
        for node in self.plcg.nodes:
            node_reliability[node] = 0.2
        self.node_reliability = node_reliability

def generate_attack_graph(attack_surface:AttackSurface):
    attack_graph = {
        "categories": [
            {
                "name": "Normal Node"
            },
            {
                "name": "Entry Node"
            },
            {
                "name": "Exit Node"
            },
            {
                "name": "Potential Attack"
            },
        ]
    }
    # set nodes 

    data_info = []

    for node in attack_surface.plcg.nodes:
        category = 0
        if node in attack_surface.exit_points_plcg:
            category = 2
        if node in attack_surface.entry_points_plcg:
            category = 1
        cur_resilience = attack_surface.node_reliability[node]

        if node in attack_surface.node_resilience:
            cur_resilience = attack_surface.node_resilience[node]

        node_name = attack_surface.node_names[node]
        if "::" in node_name:
            temp_node_name = node_name.split('::')[1]
        else:
            temp_node_name = node_name
        func_name = temp_node_name.split(':')[2]
        file_name = temp_node_name.split(':')[0]
        line_loc = temp_node_name.split(':')[1]

        new_node = {
            "name":func_name+"()",
            "id":"Func:"+node_name,
            "file":file_name+":"+line_loc,
            "category": category,
            "symbolSize": 45,
            "node_resilience":cur_resilience,
            "reliability":attack_surface.node_reliability[node],
            "fixed": False,
            "itemStyle": {
                "normal": {
                    "opacity": 1
                }
            },
        }
        data_info.append(new_node)

    # set edges 

    edge_info = []

    attack_info = {}
    for node, attacks in attack_surface.possible_attacks:
        node_name = attack_surface.node_names[node]
        for attack in attacks:
            if attack not in attack_info:
                atk_name = attack_pattern_table[attack].name
                attack_info[attack] = {
                    "name":atk_name,
                    "id":"Attack:"+atk_name,
                    "file":"activity uml",
                    "category": 3,
                    "symbolSize": 45,
                    "fixed": False,
                    "attack_nums":1,
                    "attack_prob":attack_pattern_table[attack].possiblity,
                    "attack_severity":attack_pattern_table[attack].severity,
                    "itemStyle": {
                        "normal": {
                            "opacity": 1
                        }
                    },
                }
            else:
                attack_info[attack]['attack_nums'] += 1
            cur_edge = {
                "source": "Attack:"+atk_name,
                "target": "Func:"+node_name,
                "symbol": [
                    "none",
                    "arrow"
                ],
                "lineStyle": {
                    "normal": {
                        "width": 2,
                        "curveness": 0.1,
                        "type": "solid",
                        "opacity": 1
                    }
                }
            }
            edge_info.append(cur_edge)


    data_info += list(attack_info.values())

    for edge in attack_surface.plcg.edges:
        source_node = "Func:" + attack_surface.node_names[edge[0]]
        target_node = "Func:" + attack_surface.node_names[edge[1]]
        cur_edge = {
            "source": source_node,
            "target": target_node,
            "symbol": [
                "none",
                "arrow"
            ],
            "lineStyle": {
                "normal": {
                    "width": 2,
                    "curveness": 0.1,
                    "type": "solid",
                    "opacity": 1
                }
            }
        }
        edge_info.append(cur_edge)    

    attack_graph["data"] = data_info
    attack_graph["links"] = edge_info

    return json.dumps(attack_graph, indent=4)


    

def deal_project(plcg:nx.DiGraph, pipe_filter_graph:nx.DiGraph, system_dependency_graph: nx.DiGraph, project_path: str):
    
    all_infos = {"type":"SourceCode"}
    resilience = None
    attack_surface_info = {"node":{}}
    analysis_result_info = {}

    attack_surface = AttackSurface()
    attack_surface.attack_surface_detection(pipe_filter_graph, plcg, project_path)
    attack_surface.generate_possible_attacks()
    attack_surface.cal_node_reliability()
    attack_surface_info["entry_points"] = [{"name":name, "type":attack_surface.node_types[node]} for node,name in attack_surface.entry_points_plcg.items()]
    attack_surface_info["exit_points"] = [{"name":name, "type":attack_surface.node_types[node]} for node,name in attack_surface.exit_points_plcg.items()]
    attack_surface_info["untrusted_data_items"] = attack_surface.untrusted_items
    
    attack_surface_info["channels"] = [(channel[0], channel[1]) for channel in attack_surface.channels]


    resilience = 0
    node_resilience_info = {}
    for node, atks in attack_surface.possible_attacks:
        attack_surface_info["node"][attack_surface.node_names[node]] = [attack_pattern_table[a].id for a in atks]
        node_resilience = 1
        for state in plcg.nodes:
            if node == state:
                if len(atks) > 0:
                    node_resilience = 0
                    for a in atks:
                        node_resilience += attack_surface.node_reliability[state] * attack_pattern_table[a].possiblity
                    node_resilience = node_resilience / len(atks)
                    break
        resilience += node_resilience
        node_resilience_info[attack_surface.node_names[node]] = node_resilience
    resilience = resilience / len(plcg.nodes)

    analysis_result_info["node_resilience"] = node_resilience_info

    all_infos["resilience"] = resilience
    all_infos["attacksurface"] = attack_surface_info
    all_infos["analysisresult"] = analysis_result_info

    attack_surface.node_resilience = node_resilience_info

    attack_graph_str = "var graph = " + generate_attack_graph(attack_surface)

    

    return all_infos, attack_graph_str, convert_info_format(all_infos)

if __name__ == "__main__":
    prop = "/temp_grad/upload/t"
    plcg = nx.nx_pydot.read_dot("/temp_grad/upload/t/code/PLCG.dot")
    pf = None
    sdg = None
    all_info, att_str, c_info = deal_project(plcg, pf, sdg, prop)
    with open("static/attack.js", "w") as f:
        f.write(att_str)
    import pprint
    pprint.pprint(all_info)
    # pprint.pprint(c_info)
