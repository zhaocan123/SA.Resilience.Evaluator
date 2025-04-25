import process_wsd
import datetime
from attack_surface_info import convert_info_format, AttackPattern, attack_pattern_table
import os
import json

class Node:
    def __init__(self, name) -> None:
        self.name = name
        self.resilience = None

    def __repr__(self):
        return self.name

class ComponentNode(Node):
    def __init__(self, name, reliability=None) -> None:
        super().__init__(name)
        self.reliability = reliability
        
    def __repr__(self):
        return "ComponentNode: \"" + self.name + "\", Type: " + self.type + ", Resilience: " + str(self.reliability) + ";"

class ActivityNode(Node):
    def __init__(self, name, object=None, type=None, comps=None) -> None:
        super().__init__(name)
        if object is None:
            self.objects = []
        else:
            self.objects = [object]
        self.type = type
        if comps == None:
            self.comps = []
        else:
            self.comps = comps
        self.reliability = None
    
    def __repr__(self):
        return "ActivityNode: \"" + self.name + "\", Type: " + self.type + ";"

class Link:
    def __init__(self, node1=None, node2=None, direction=None, type=None, name=None) -> None:
        self.name = name
        self.type = type
        self.node1 = node1
        self.node2 = node2
        self.direction = direction
    
    def __repr__(self):
        return "Link of: \"" + str(self.node1) + "\" and \"" + str(self.node2) + "\", Direction: " + str(self.direction) + ", Type: " + str(self.type) + ";"

class Diagram:
    def __init__(self, name) -> None:
        self.name = name
        self.nodes = []
        self.links = []

    def find_node_by_name(self,name):
        for node in self.nodes:
            if node.name == name:
                return node
        return None

    def get_node_index(self,node):
        return self.nodes.index(node)

    def get_adjency_matrix(self):
        matrix = [[0 for _ in range(len(self.nodes))] for _ in range(len(self.nodes))]
        for link in self.links:
            i, j = self.get_node_index(self.find_node_by_name(link.node1)), self.get_node_index(self.find_node_by_name(link.node2))
            if link.direction == "bi":
                matrix[i][j] = 1
                matrix[j][i] = 1
            elif link.direction == "right":
                matrix[i][j] = 1
            elif link.direction == "left":
                matrix[j][i] = 1
            else:
                raise ValueError("Invalid direction for a link!")
        return matrix

class ComponentDiagram(Diagram):
    def read_from_wsd_text(self,text, processed=False):
        if not processed:
            text = self._process_plantUML(text)
            # print("======Processed Component diagram:")
            # print("======Maybe you need to save this==")
            # print(text)
            # print("==================================")
        lines = text.split("\n")
        read_mode = "None"
        com_link = None
        com_node = None
        for line in lines:
            line = line.strip()
            if line.find("node: ") == 0:
                read_mode = "node"
                com_node = ComponentNode(line.split(": ")[1])
            if line.find("link:") == 0:
                read_mode = "link"
                com_link = Link()
            if line.find("type: ") == 0:
                type = line.split(': ')[1]
                if read_mode == "node":
                    if type != "TODO":
                        com_node.type = type
                elif read_mode == "link":
                    if type != "TODO":
                        com_link.type = type
            if line.find("node1: ") == 0:
                com_link.node1 = line.split(': ')[1]
            if line.find("node2: ") == 0:
                com_link.node2 = line.split(': ')[1]
            if line.find("resilience: ") == 0:
                resilience = line.split(': ')[1]
                if resilience != "TODO":
                    com_node.reliability = resilience
                else:
                    com_node.reliability = 0.99
                    if com_node.type == "interface":
                        com_node.reliability = 0.999
            if line.find("end node") == 0:
                self.nodes.append(com_node)
            if line.find("end link") == 0:
                com_link.direction = "bi"
                self.links.append(com_link)

        # print(self.nodes)
        # print(self.links)

    def _process_plantUML(self,text):
        return process_wsd.process_component(text)

class ActivityDiagram(Diagram):
    def read_from_wsd_text(self, text, processed=False):
        if not processed:
            text = self._process_plantUML(text)
            # print("======Processed Activity diagram:")
            # print("======Maybe you need to save this==")
            # print(text)
            # print("==================================")
        lines = text.split("\n")
        for line in lines:
            line = line.strip()
            if line.find("node: ") == 0:
                act_node = ActivityNode(line.strip().split(": ")[1])
                act_node.reliability = 0.5
            if line.find("type: ") == 0:
                type = line.split(': ')[1]
                if type != "TODO":
                    act_node.type = type
            if line.find("object: ") == 0:
                object = line.split(': ')[1]
                if object != "TODO":
                    act_node.objects.append(object)
            if line.find("comp: ") == 0:
                components = line.strip().split(": ")[1]
                if components != "TODO":
                    components = components.split(', ')
                    for component in components:
                        if component != "":
                            act_node.comps.append(component)
            if line.find("end node") == 0:
                self.nodes.append(act_node)
            if line.find("link: ") == 0:
                start,end = line.split(': ')[1].split(" -> ")
                self.links.append(Link(start,end,"right","activity_link"))

        # print(self.nodes)
        # print(self.links)

    def _process_plantUML(self,text) -> str:
        return process_wsd.process_activity(text)
    
# node types in activity diagram
activity_types = ['start_node',
                'end_node',
                'action_node',
                'call_node',
                'send_node',
                'receive_node',
                'decision_node',
                'merge_node',
                'fork_node',
                'join_node']

activtiy_attack_table = {
                        'start_node':[1,6,7,11],
                        'action_node':[2,4],
                        'call_node':[3,4,10,11],
                        'send_node':[2,3,4],
                        'receive_node':[1,8,11],
                        'decision_node':[5,7,9,11],
                        'merge_node':[5,9],
                        'fork_node':[5,9],
                        'join_node':[5,9]}

class ActivityUMLNode:
    def __init__(self,name):
        self.name = name
        self.type = "not_defined"
        self.childs = []
        self.parents = []
        self.objects = []
        self.call = None
    
    def __repr__(self) -> str:
        return f"Node: {self.name} type: {self.type} objects:{self.objects}"

class ActivityUMLDiagram:
    def __init__(self):
        self.nodes = []
        self.links = []

    def find_node(self,name):
        for node in self.nodes:
            if node.name == name:
                return node
        return None

    def add_links(self):
        for link in self.links:
            start,end = self.find_node(link[0]),self.find_node(link[1])
            start.childs.append(end)
            end.parents.append(start)
            
    def read_from_text(self,text):
        lines = text.split("\n")
        for line in lines:
            line = line.strip()
            if line.find("node: ") == 0:
                act_node = ActivityUMLNode(line.strip().split(": ")[1])
            if line.find("type: ") == 0:
                type = line.split(': ')[1]
                if type != "TODO":
                    act_node.type = type
            if line.find("object: ") == 0:
                object = line.split(': ')[1]
                if object != "TODO":
                    act_node.objects.append(object)
            if line.find("end node") == 0:
                self.nodes.append(act_node)
            if line.find("link: ") == 0:
                start,end = line.split(': ')[1].split(" -> ")
                self.links.append([start,end])
        self.add_links()

    def read_from_file(self,pth):
        """
        read an activity diagram from a given file which contains a description
        of an activity diagram.
        example (which is an activity diagram only have one start node and one end node):
        in activity diagram file, we firstly need to define the nodes, then the links, as below.
        >>>
        node: start
        type: start_node
        end node
        node: end
        type: end_node
        end node
        link: start -> end
        """
        with open(pth,"r") as f:
            for line in f:
                line = line.strip()
                if line.find("node: ") == 0:
                    act_node = ActivityUMLNode(line.strip().split(": ")[1])
                if line.find("type: ") == 0:
                    type = line.split(': ')[1]
                    if type != "TODO":
                        act_node.type = type
                if line.find("object: ") == 0:
                    object = line.split(': ')[1]
                    if object != "TODO":
                        act_node.objects.append(object)
                if line.find("end node") == 0:
                    self.nodes.append(act_node)
                if line.find("link: ") == 0:
                    start,end = line.split(': ')[1].split(" -> ")
                    self.links.append([start,end])
        
        self.add_links()                

class AttackSurface:
    def __init__(self):
        self.entry_points = set()
        self.exit_points = set()
        self.untrusted_items = set()
        self.channels = set()

    def attack_surface_detection(self,activity_diagram:ActivityDiagram):
        # print(activity_diagram.nodes)
        for node in activity_diagram.nodes:
            if node.type == "start_node":
                start_node = node
                break
        
        Beh = []
        nodes = []
        visited_node = []
        nodes.append(start_node)
        while len(nodes) > 0:
            current_node = nodes[0]
            nodes = nodes[1:]
            if not current_node in visited_node:
                if current_node.type == "call_node":
                    Beh.append(current_node.call)
                visited_node.append(current_node)

                if len(current_node.childs) != 0:
                    for node in current_node.childs:
                        nodes.append(node)
                
                if len(current_node.objects) != 0:
                    flag = False
                    for node in current_node.parents:
                        for object in current_node.objects:
                            if not object in node.objects:
                                flag = True
                    if flag:
                        self.entry_points.add(current_node)

                if len(current_node.objects) != 0:
                    flag = False
                    for node in current_node.childs:
                        for object in current_node.objects:
                            if not object in node.objects:
                                flag = True
                    if flag:
                        self.exit_points.add(current_node)

                if current_node.type == "send_node":
                    self.exit_points.add(current_node)

                if current_node.type == "receive_node":
                    self.entry_points.add(current_node)
                    for object in current_node.objects:
                        self.untrusted_items.add(object)
                else:
                    flag = False
                    if len(current_node.objects) >= 1:
                        for object in current_node.objects:
                            if object in self.untrusted_items:
                                flag = True
                    if flag:
                        for object in current_node.objects:
                            self.untrusted_items.add(object)
                            self.channels.add((current_node,object))
            
                if current_node.type == "end_node":
                    pass

        for ad in Beh:
            self.attack_surface_detection(ad)

# third part



def generate_possible_attacks(attack_surface:AttackSurface):
    possible_acttacks = []
    items = set()
    items = items.union(attack_surface.entry_points)
    items = items.union(attack_surface.exit_points)

    for item in items:
        try:
            attacks = activtiy_attack_table[item.type]
        except KeyError:
            attacks = []

        possible_acttacks.append([item,attacks])
    return possible_acttacks

def attack_surface_resilience(activity_diagram:ActivityDiagram, possible_attacks):
    resilience = 0.
    for p_attack in possible_attacks:
        attacks = p_attack[1]
        for attack in attacks:
            resilience += attack_pattern_table[attack].possiblity 
    
    total_probility = 0.0
    for id,pattern in attack_pattern_table.items():
        total_probility += pattern.possiblity

    resilience = 1 - resilience / (total_probility * len(activity_diagram.nodes))
    return resilience

def generate_attack_graph(attack_surface: AttackSurface, act_diagram: ActivityDiagram, node_resilience:dict):
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

    for node in act_diagram.nodes:
        category = 0
        if node.name in [nn.name for nn in attack_surface.entry_points]:
            category = 1
        if node.name in [nn.name for nn in attack_surface.exit_points]:
            category = 2
        cur_resilience = node.reliability
        if node.name in node_resilience:
            cur_resilience = node_resilience[node.name]
        new_node = {
            "name":node.name,
            "id":"Node:"+node.name,
            "file":"activity uml",
            "category": category,
            "symbolSize": 45,
            "node_resilience":cur_resilience,
            "reliability":node.reliability,
            "fixed": False,
            "itemStyle": {
                "normal": {
                    "opacity": 1
                }
            },
        }
        data_info.append(new_node)
    # set edges and attacks
    edge_info = []

    attack_info = {}
    for node, atks in generate_possible_attacks(attack_surface):
        for atk in atks:
            if atk not in attack_info:
                atk_name = attack_pattern_table[atk].name
                attack_info[atk] = {
                    "name":atk_name,
                    "id":"Attack:"+atk_name,
                    "file":"activity uml",
                    "category": 3,
                    "symbolSize": 45,
                    "fixed": False,
                    "attack_nums":1,
                    "attack_prob":attack_pattern_table[atk].possiblity,
                    "attack_severity":attack_pattern_table[atk].severity,
                    "itemStyle": {
                        "normal": {
                            "opacity": 1
                        }
                    },
                }
            else:
                attack_info[atk]['attack_nums'] += 1
            cur_edge = {
                "source": "Attack:"+atk_name,
                "target": "Node:"+node.name,
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

     
    
    for edge in act_diagram.links:
        source = "Node:" + edge.node1
        target = "Node:" + edge.node2
        cur_edge = {
            "source": source,
            "target": target,
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

def deal_project(project_path):
    # if project path contain a uml diagram folder
    uml_info = {}
    wsd_uml_folder_path = os.path.join(project_path, "wsd_uml_folder")
    # find activity.wsd and activity.txt in file
    if not os.path.exists(os.path.join(wsd_uml_folder_path, "activity.wsd")):
        raise ValueError("Not activity Diagram found!")
    if not os.path.exists(os.path.join(wsd_uml_folder_path, "activity.txt")):
        raise ValueError("Not activity Diagram found!")
    uml_info["activity_diagram_path"] = os.path.abspath(os.path.join(wsd_uml_folder_path, "activity.wsd"))
    uml_info["activity_text_path"] = os.path.abspath(os.path.join(wsd_uml_folder_path, "activity.txt"))
    # find comp.wsd and comp.txt in file
    if not os.path.exists(os.path.join(wsd_uml_folder_path, "comp.wsd")):
        raise ValueError("Not comp Diagram found!")
    if not os.path.exists(os.path.join(wsd_uml_folder_path, "comp.txt")):
        raise ValueError("Not comp Diagram found!")
    uml_info["comp_diagram_path"] = os.path.abspath(os.path.join(wsd_uml_folder_path, "comp.wsd"))
    uml_info["comp_text_path"] = os.path.abspath(os.path.join(wsd_uml_folder_path, "comp.txt"))
    
    all_infos = {"uml_info": uml_info}
    all_infos["type"] = "UML"
    

    resilience = None
    attack_surface_info = {"node":{}}
    analysis_result_info = {}

    activity_diagram = ActivityUMLDiagram()
    activity_diagram.read_from_file(uml_info["activity_text_path"])

    attack_surface = AttackSurface()
    attack_surface.attack_surface_detection(activity_diagram)
    attack_surface_info["entry_points"] = [{"name":node.name, "type":node.type} for node in attack_surface.entry_points]
    attack_surface_info["exit_points"] = [{"name":node.name, "type":node.type} for node in attack_surface.exit_points]
    attack_surface_info["untrusted_data_items"] = attack_surface.untrusted_items
    
    attack_surface_info["channels"] = [(channel[0].name, channel[1]) for channel in attack_surface.channels]

    act_diagram = ActivityDiagram("act")
    comp_diagram = ComponentDiagram("comp")
    with open(uml_info["comp_text_path"], "r") as f:
        comp_diagram.read_from_wsd_text(f.read(), processed=True)
    with open(uml_info["activity_text_path"], "r") as f:
        act_diagram.read_from_wsd_text(f.read(), processed=True)

    resilience = 0
    node_resilience_info = {}
    for node, atks in generate_possible_attacks(attack_surface):
        attack_surface_info["node"][node.name] = [attack_pattern_table[a].id for a in atks]
        node_resilience = 1
        for state in act_diagram.nodes:
            if node.name == state.name:
                if len(atks) > 0:
                    node_resilience = 0
                    for a in atks:
                        node_resilience += state.reliability * attack_pattern_table[a].possiblity
                    node_resilience = node_resilience / len(atks)
                    break
        resilience += node_resilience
        node_resilience_info[node.name] = node_resilience
    resilience = resilience / len(act_diagram.nodes)

    analysis_result_info["node_resilience"] = node_resilience_info

    all_infos["resilience"] = resilience
    all_infos["attacksurface"] = attack_surface_info
    all_infos["analysisresult"] = analysis_result_info
    # save attack graph
    attack_graph_str = "var graph = " + generate_attack_graph(attack_surface, act_diagram, node_resilience_info)

    return all_infos, attack_graph_str, convert_info_format(all_infos)

if __name__ == "__main__":
    import pprint
    res = deal_project("test1")
    pprint.pprint(res[0])
    with open("static/attack.js", "w") as f:
        f.write(res[1])
    # pprint.pprint(deal_project("test1"))

# def resilience_evaluation(input_activity_text, input_comp_text):
#     current_time = datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S')
#     results = "\n============================"
#     results += "\n攻击面韧性评估结果： "
#     results += "\n评估时间：" + current_time
#     atd = ActivityUMLDiagram()
#     atd.read_from_text(input_activity_text)

#     # print(len(atd.links))

#     ats = AttackSurface()
#     ats.attack_surface_detection(atd)

#     results += "\n++ 攻击面 ++\n"
#     results += "\n#入口节点： \n"
#     results += ', '.join([str(node.name) for node in ats.entry_points])
#     results += "\n#出口节点: \n"
#     results += ', '.join([str(node.name) for node in ats.exit_points])
#     results += "\n#不可信数据元素: \n"
#     results += ', '.join([str(object) for object in ats.untrusted_items])
#     results += "\n#数据通道: \n  "
#     results += ', \n  '.join([str((node.name,object)) for node,object in ats.channels])

#     results += "\n+++++++++++++++++++++++"

#     # generate possible attack

#     atks = generate_possible_attacks(ats)

#     results += "\n潜在攻击集合: "
#     for node,atk in atks:
#         results += "\n 节点: \"" + node.name
#         results += "\" , 潜在攻击ID: " + str(atk)

#     # calculate resilience

#     resilience = 0
#     avcitvity_diagram = ActivityDiagram("activity")
#     avcitvity_diagram.read_from_wsd_text(input_activity_text,processed=True)
#     comp_diagram = ComponentDiagram("comp")
#     comp_diagram.read_from_wsd_text(input_comp_text,processed=False)

#     for node, atk in atks:
#         node_resilience = 1
#         for state in avcitvity_diagram.nodes:
#             if node.name == state.name:
#                 if len(atk) > 0:
#                     node_resilience = 0
#                     for a in atk:
#                         node_resilience += state.reliability * attack_pattern_table[a].possiblity
#                     node_resilience = node_resilience / len(atk)
#                     break
#         resilience += node_resilience
#     resilience = (resilience + len(avcitvity_diagram.nodes) - 2 - len(atks)) / (len(avcitvity_diagram.nodes) - 2)
#     # print(resilience)

#     results += "\n韧性结果: "
#     results += str(round(resilience,4))

#     results += "\n========================\n"

#     print(results)
#     return results

# if __name__ == "__main__":
#     pass