
class AttackPattern:
    def __init__(self,id,name,severity,possiblity,description=''):
        self.id = id
        self.name = name
        self.severity = severity
        self.possiblity = possiblity
        self.decript = description

attack_pattern_table = {1:AttackPattern('CAPEC-148','ContentSpoofing','high',0.8),
                        2:AttackPattern('CAPEC-151','IdentitySpoofing','high',0.8),
                        3:AttackPattern('CAPEC-116','Excavation','medium',0.5),
                        4:AttackPattern('CAPEC-117','Interception','Low',0.2),
                        5:AttackPattern('CAPEC-125','Flooding','high',0.8),
                        6:AttackPattern('CAPEC-131','ResourceLeak','high',0.8),
                        7:AttackPattern('CAPEC-148','ContentSpoofing','high',0.8),
                        8:AttackPattern('CAPEC-152','Injection','high',0.8),
                        9:AttackPattern('CAPEC-225','ExploitionOfAuthentication','high',0.8),
                        10:AttackPattern('CAPEC-28','Fuzzing','high',0.8),
                        11:AttackPattern('CAPEC-163','SpearPhishing','high',0.8)}

def save_capec_info_to_dict():
    attack_infos = {}
    for id, attack in attack_pattern_table.items():
        name = attack.name
        id = attack.id
        severity = attack.severity
        possibility = str(attack.possiblity)
        description = attack.decript
        attack_infos[id] = {"id":id, "name":name, "severity":severity, "possibility":possibility, "description": description}
    return attack_infos

def convert_info_format(all_infos):
    attack_surface_info_table = {}
    all_nodes_count = len(all_infos["analysisresult"]["node_resilience"])
    entry_points_count = len(all_infos["attacksurface"]["entry_points"])
    exit_points_count = len(all_infos["attacksurface"]["exit_points"])
    untrusted_data_items_count = len(all_infos["attacksurface"]["untrusted_data_items"])
    channels_count = len(all_infos["attacksurface"]["channels"])
    attack_surface_info_table["entry_exit_points_num"] = entry_points_count + exit_points_count
    attack_surface_info_table["untrusted_data_item_nums"] = untrusted_data_items_count
    attack_surface_info_table["data_channel_num"] = channels_count
    attack_surface_info_table["entry_exit_points_prop"] = round((entry_points_count + exit_points_count) / all_nodes_count, 3)
    
    if all_infos["type"] == "UML":
        untrusted_data_items_table = [{"name":ud_item, "location":"Activity UML", "type":"Data Item", "library": "Activity UML"} for ud_item in all_infos["attacksurface"]["untrusted_data_items"]]
    else:
        untrusted_data_items_table = []
        for ud_item in all_infos["attacksurface"]["untrusted_data_items"]:
            if "::" in ud_item:
                location = ":".join(ud_item.split('::')[1].split(":")[:2])
            else:
                location = ":".join(ud_item.split(":")[:2])
            library_text = None
            if "::" in ud_item:
                library_text = ud_item.split('::')[1].split(":")[0]
            else:
                library_text = "User Function"
            cur_item = {"name":ud_item.split('::')[0], "location":location, "type":"Data Item", "library": library_text}
            untrusted_data_items_table.append(cur_item)

    
    entry_exit_points_table = []

    if all_infos["type"] == "UML":
        for node in all_infos["attacksurface"]["entry_points"]:
            new_info = {"type":"entry_points", "location":node["name"], "library":node["type"]}
            entry_exit_points_table.append(new_info)
        for node in all_infos["attacksurface"]["exit_points"]:
            new_info = {"type":"exit_points", "location":node["name"], "library":node["type"]}
            entry_exit_points_table.append(new_info)
    else:
        for node in all_infos["attacksurface"]["entry_points"]:
            location = None
            if "::" in node["name"]:
                location = ":".join(node["name"].split('::')[1].split(":")[:2])
            else:
                location = ":".join(node["name"].split(":")[:2])
            library_text = None
            if "::" in node["name"]:
                library_text = node["name"].split('::')[0].split(":")[0]
            else:
                library_text = "User Function"
            new_info = {"type":"entry_points", "location":location, "library":library_text}
            entry_exit_points_table.append(new_info)
        for node in all_infos["attacksurface"]["exit_points"]:
            location = None
            if "::" in node["name"]:
                location = ":".join(node["name"].split('::')[1].split(":")[:2])
            else:
                location = ":".join(node["name"].split(":")[:2])
            if "::" in node["name"]:
                library_text = node["name"].split('::')[0].split(":")[0]
            else:
                library_text = "User Function"
            new_info = {"type":"exit_points", "location":location, "library":library_text}
            entry_exit_points_table.append(new_info)
    
    capec_attack_info = save_capec_info_to_dict()

    attack_set_detail_table = []
    attacks_catogery_info_table = {}
    total_atk_num = 0
    for node, atks in all_infos["attacksurface"]["node"].items():
        for atk in atks:
            total_atk_num += 1
            new_info = {"standard": atk}
            new_info["severity"] = capec_attack_info[atk]["severity"]
            new_info["prop"] = capec_attack_info[atk]["possibility"]
            if all_infos["type"] == "UML":
                new_info["source"] = "Activity_UML: " + node
            else:
                new_info["source"] = node + "()"
            attack_set_detail_table.append(new_info)
            if atk not in attacks_catogery_info_table:
                attacks_catogery_info_table[atk] = {
                    "attack_catergory_id": atk,
                    "attack_num": 1,
                    "attack_type_prop":-1
                }
            else:
                attacks_catogery_info_table[atk]["attack_num"] += 1
    for atk in attacks_catogery_info_table:
        attacks_catogery_info_table[atk]["attack_type_prop"] = round(attacks_catogery_info_table[atk]["attack_num"] / total_atk_num, 3)

    attacks_catogery_info_table = list(attacks_catogery_info_table.values())
    cardData = {}
    cardData["resilience"] = round(all_infos["resilience"], 3)
    cardData["average_node_resilience"] = round(sum(all_infos["analysisresult"]["node_resilience"].values()) / all_nodes_count, 3)
    cardData["total_attack_num"] = total_atk_num
    cardData["average_attack_num"] = round(total_atk_num / all_nodes_count, 3)
    cardData["entry_exit_points_num"] = entry_points_count + exit_points_count

    resilience_distribution = [0] * 10
    for node, resilience in all_infos["analysisresult"]["node_resilience"].items():
        for i in range(10):
            if resilience > i / 10 and resilience <= (i+1) / 10:
                resilience_distribution[i] += 1
                break

    capec_distribution = [{"name":atk["attack_catergory_id"], "value":atk["attack_num"]} for atk in attacks_catogery_info_table]
    attackSetChartData = [{"name":atk["attack_catergory_id"], "value":atk["attack_num"], "key":atk["attack_catergory_id"]} for atk in attacks_catogery_info_table]
    top10_distribution = [['score', 'amount', 'product']]
    
    top_all_list = []
    for node, node_resilience in all_infos["analysisresult"]["node_resilience"].items():
        if "::" in node:
            node_name = node.split("::")[1]
        else:
            node_name = node
        cur_list = [len(all_infos["attacksurface"]["node"][node]), node_resilience, node_name]
        top_all_list.append(cur_list)

    top10_distribution += sorted(top_all_list, reverse=True)[:10]

    resilience_info = {
        "cardData" : cardData,
        "resilience_distribution": resilience_distribution,
        "capec_distribution": capec_distribution,
        "top10_distribution": top10_distribution
    }
    attackSurfaceInfo = {
        "attackSetChartData": attackSetChartData,
        "attack_surface_info_table": attack_surface_info_table,
        "attacks_catogery_info_table": attacks_catogery_info_table,
        "entry_exit_points_table": entry_exit_points_table,
        "untrusted_data_items_table": untrusted_data_items_table,
        "attack_set_detail_table": attack_set_detail_table
    }

    return resilience_info, attackSurfaceInfo



def attackSurfaceInfoExtract(project_info):

    # project_info["attackSurfaceInfo"] = {
    #     "attackSetChartData":[
    #         {
    #             "value": 1, "name": "CAPEC-123", "key": "CAPEC-123"
    #         },{
    #             "value": 1, "name": "CAPEC-124", "key": "CAPEC-124"
    #         }
    #     ],
    #     "attack_surface_info_table":[
    #         {
    #             "entry_exit_points_num":10,
    #             "untrusted_data_item_nums":5,
    #             "entry_exit_points_prop": 0.5,
    #             "data_channel_num":3
    #         }
    #     ],
    #     "attacks_catogery_info_table":[
    #         {
    #             "attack_catergory_id": "CAPEC-12",
    #             "attack_num": 50,
    #             "attack_type_prop": 0.25
    #         },
    #         {
    #             "attack_catergory_id":  "CAPEC-35",
    #             "attack_num": 150,
    #             "attack_type_prop": 0.75
    #         }
    #     ],
    #     "entry_exit_points_table":[
    #         {
    #             "location":"/temp/test.c:main():22",
    #             "type":"entry_point",
    #             "library":"stdio.h"
    #         },
    #         {
    #             "location":"/temp/test.c:test():32",
    #             "type":"exit_point",
    #             "library":"stdio.h"
    #         }
    #     ],
    #     "untrusted_data_items_table":[
    #         {
    #             "name":"File",
    #             "location":"/temp/test.c:test():32",
    #             "type":"File IO",
    #             "library":"stdio.h"
    #         }
    #     ],
    #     "attack_set_detail_table":[
    #         {
    #             "source": "/temp/test.c:test():32",
    #             "standard": "CAPEC-35",
    #             "severity":"High",
    #             "prop":0.5
    #         }
    #     ]
    # }
    attackSurfaceInfo = project_info["attackSurfaceInfo"]
    # import pprint
    # pprint.pprint(attackSurfaceInfo)
    return attackSurfaceInfo

def resilienceInfoExtacrt(project_info):
    # import pprint
    # pprint.pprint(project_info["resilience_report_info"])
    resilience_info = project_info["resilience_report_info"]
    # attackSurfaceInfo = project_info["attackSurfaceInfo"]
    # resilience_report_info = {
    #     "cardData":{
    #         "resilience": 0.5,
    #         "average_node_resilience": 0.7,
    #         "total_attack_num": 25,
    #         "average_attack_num": 10
    #     },
    #     "resilience_distribution": [10, 15, 5, 30, 40, 60, 20, 15, 30, 20],
    #     "capec_distribution":[
    #         {"name":f"CAPEC-{i+1}", "value":i * 10 + 5} for i in range(10)
    #     ],
    #     "top10_distribution":[
    #         ['score', 'amount', 'product'],
    #         [89.3, 58212, 'Matcha Latte'],
    #         [57.1, 78254, 'Milk Tea'],
    #         [74.4, 41032, 'Cheese Cocoa'],
    #         [50.1, 12755, 'Cheese Brownie'],
    #         [89.7, 20145, 'Matcha Cocoa'],
    #         [68.1, 79146, 'Tea'],
    #         [19.6, 91852, 'Orange Juice'],
    #         [10.6, 101852, 'Lemon Juice'],
    #         [32.7, 20112, 'Walnut Brownie']
    #     ]

    # }
    return resilience_info

