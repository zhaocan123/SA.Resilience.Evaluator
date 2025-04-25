# -*- coding: utf-8 -*-
import os
import subprocess
import networkx as nx
import numpy as np
import json
import process_c_cfg
import process_cpp_cfg
import cdg
import ddg

pwd = os.getcwd()
pwd = pwd.replace("\\", "/")
print("process_project.py: pwd = ", pwd)
with open(pwd + "/config.json", "r", encoding="utf-8") as f:
    content = json.load(f)
DOT_EXE_FILE_PATH = content["DOT_EXE_FILE_PATH"]
CLANG_PATH = content["CLANG_PATH"]


def handle_folder(file_list, folder_path):
    all_cfgs = {}
    all_cdgs = {}
    for (root, dirs, files) in os.walk(folder_path):
        for current_file in files:
            current_path = os.path.join(root, current_file).replace("//", "/").replace("\\", "/")
            if current_path[-2:] == '.c' and current_path in file_list:  # or current_path[-2:] == '.h':
                print(f"Handling {current_path}")
                result = generate_and_process_c(
                    current_path)
                if result != "Failed":
                    result_cfgs, result_cdgs = result[0], result[1]
                    print()
                    all_cfgs[current_path.replace("\\", '/')] = result_cfgs
                    all_cdgs[current_path.replace("\\", '/')] = result_cdgs
                else:
                    print(f"Failed to process {current_path}")
            if current_path[-4:] == '.cpp' and current_path in file_list:
                print(f"Handling {current_path}")
                result = generate_and_process_cpp(
                    current_path)
                if result != "Failed":
                    result_cfgs, result_cdgs = result[0], result[1]
                    all_cfgs[current_path] = result_cfgs
                    all_cdgs[current_path] = result_cdgs
                else:
                    print(f"Failed to process {current_path}")
    return all_cfgs, all_cdgs


def generate_and_process_c(code_file_path):
    if code_file_path[-2:] == '.c' or code_file_path[-2:] == '.h':
        cfgs = {}
        cdgs = {}
        ret = 0
        if ret == 0:
            function_names = []
            count = 0
            cmd_str = CLANG_PATH + " " + code_file_path + \
                f" -isystem {os.path.split(code_file_path)[0]}" + \
                " --analyze -Xclang -analyzer-checker=debug.ViewCFG -Xclang -analyzer-config -Xclang max-nodes=3 -Xclang -analyzer-display-progress"
            ret = 1
            include_cmd = " "
            while ret != 0:
                # print(cmd_str)
                ret, val = subprocess.getstatusoutput(
                    cmd_str, encoding='UTF-8')
                # print(ret,val)
                if ret == 1:
                    temp = val
                    if "#include" in temp:
                        temp = temp[temp.find("#include"):]
                        if '"' in temp:
                            header_file = temp[temp.find(
                                '"') + 1:temp.find('"', temp.find('"') + 1)]
                        if '<' in temp:
                            header_file = temp[temp.find(
                                '<') + 1:temp.find('>', temp.find('<') + 1)]
                        # print(header_file, c_header_files_path[header_file])
                        try:
                            header_abs_path = os.path.abspath(os.path.join(os.path.split(code_file_path)[0], header_file)).replace("\\", '/').replace("//", "/")
                            include_cmd += " -isystem " + \
                                           os.path.split(header_abs_path)[0] + " "
                            cmd_str = CLANG_PATH + " " + code_file_path + include_cmd + \
                                "--analyze -Xclang -analyzer-checker=debug.ViewCFG -Xclang -analyzer-config -Xclang max-nodes=3 -Xclang -analyzer-display-progress"
                        except KeyError:
                            break  # print(cmd_str)
                    else:
                        break
                elif ret == 0:
                    val = val.split('\n')
                    for line in val:
                        if 'Writing ' in line and 'done' in line:
                            # print(line)
                            function_writing = line.split()[3]
                            file_place = line.split()[2]
                            if os.path.abspath(file_place) == os.path.abspath(code_file_path):
                                function_name = function_writing.replace(
                                    "Writing", "")
                                function_names.append(function_name)
                                # print(function_name)
                                start_index = line.find("'")
                                end_index = line.find("'", start_index + 1)
                                cfg_path = line[start_index + 1:end_index]
                                print(f"[C] Successfully find cfg of {function_name} at {cfg_path}")
                                un_processed_cfg = nx.DiGraph(nx.nx_pydot.read_dot(cfg_path))
                                # temp_folder = "temp/" + function_name
                                # write original cfg
                                # try:
                                #     nx.nx_pydot.write_dot(un_processed_cfg, temp_folder + ".original.dot")
                                # except Exception as e:
                                #     print(e)
                                # convert to png
                                # os.system(
                                #     f'{DOT_EXE_FILE_PATH} -Tpng {temp_folder + ".original.dot"} -o {temp_folder + ".original.png"}')
                                cfgs[function_name] = process_c_cfg.process_cfg(un_processed_cfg)
                                # try:
                                #     cfgs[function_name] = process_c_cfg.process_cfg(un_processed_cfg)
                                # except Exception as e:
                                #     print(e)
                                #     cfgs[function_name] = un_processed_cfg
                                # construct cdg
                                cdgs[function_name] = cdg.cdg(cfgs[function_name])
                                # write processed cfg and cdg
                                # nx.nx_pydot.write_dot(cfgs[function_name], temp_folder + ".processed.cfg.dot")
                                # nx.nx_pydot.write_dot(cdgs[function_name], temp_folder + ".processed.cdg.dot")
                                # os.system(
                                #     f'{DOT_EXE_FILE_PATH} -Tpng {temp_folder + ".processed.cfg.dot"} -o {temp_folder + ".processed.cfg.png"}')
                                # os.system(
                                #     f'{DOT_EXE_FILE_PATH} -Tpng {temp_folder + ".processed.cdg.dot"} -o {temp_folder + ".processed.cdg.png"}')
                                print(f"[C] Successfully processed cfg and cdg of {function_name} at {cfg_path}")
                                # delet dot while cfg process is finished
                                while os.path.exists(cfg_path):
                                    os.remove(cfg_path)
                                print(f"[C] Successfully delete temp file of cfg at {cfg_path}")
                                count += 1
                else:
                    break

            if ret == 0:
                return cfgs, cdgs
            else:
                return "Failed"


def generate_and_process_cpp(code_file_path):
    if code_file_path[-4:] == '.cpp' or code_file_path[-2:] == '.h':
        cfgs = {}
        cdgs = {}
        ret = 0
        if ret == 0:
            function_names = []
            count = 0
            cmd_str = CLANG_PATH + " " + code_file_path + \
                f" -isystem {os.path.split(code_file_path)[0]}" + \
                " --analyze -Xclang -analyzer-checker=debug.ViewCFG -Xclang -analyzer-config -Xclang max-nodes=3 -Xclang -analyzer-display-progress"
            ret = 1
            include_cmd = " "
            while ret != 0:
                # print(cmd_str)
                ret, val = subprocess.getstatusoutput(
                    cmd_str, encoding='UTF-8')
                # print(val)
                # print(ret, val)
                if ret == 1:
                    temp = val
                    if "#include" in temp:
                        temp = temp[temp.find("#include"):]
                        if '"' in temp:
                            header_file = temp[temp.find(
                                '"') + 1:temp.find('"', temp.find('"') + 1)]
                        if '<' in temp:
                            header_file = temp[temp.find(
                                '<') + 1:temp.find('>', temp.find('<') + 1)]
                        # print(header_file, c_header_files_path[header_file])
                        try:
                            header_abs_path = os.path.abspath(os.path.join(os.path.split(code_file_path)[0], header_file)).replace("\\", '/').replace("//", "/")
                            include_cmd += " -isystem " + \
                                           os.path.split(header_abs_path)[0] + " "
                            cmd_str = CLANG_PATH + " " + code_file_path + include_cmd + \
                                "--analyze -Xclang -analyzer-checker=debug.ViewCFG -Xclang -analyzer-config -Xclang max-nodes=3 -Xclang -analyzer-display-progress"
                        except KeyError:
                            break  # print(cmd_str)
                    else:
                        break
                elif ret == 0:
                    val = val.split('\n')
                    for line in val:
                        if 'Writing ' in line and 'done' in line:
                            function_writing = " ".join(line.split()[3:-2])
                            function_name = function_writing.replace(
                                "Writing", "").replace("()", "").replace("::", ".")
                            file_place = line.split()[2]
                            if os.path.abspath(file_place) == os.path.abspath(code_file_path):
                                function_names.append(function_name)
                                # print(function_name)
                                start_index = line.find("'")
                                end_index = line.find("'", start_index + 1)
                                cfg_path = line[start_index + 1:end_index]
                                print(f"[CPP] Successfully find cfg of {function_name} at {cfg_path}")
                                un_processed_cfg = nx.DiGraph(nx.nx_pydot.read_dot(cfg_path))
                                # temp_folder = "temp/" + function_name.replace("*", "_").replace(" ", "@")
                                # write original cfg
                                # nx.nx_pydot.write_dot(un_processed_cfg, temp_folder + ".original.dot")
                                # convert to png
                                # os.system(
                                #     f'{DOT_EXE_FILE_PATH} -Tpng {temp_folder + ".original.dot"} -o {temp_folder + ".original.png"}')
                                cfgs[function_name] = process_cpp_cfg.process_cfg(un_processed_cfg)
                                # construct cdg
                                cdgs[function_name] = cdg.cdg(cfgs[function_name])
                                # write processed cfg
                                # nx.nx_pydot.write_dot(cfgs[function_name], temp_folder + ".processed.cfg.dot")
                                # nx.nx_pydot.write_dot(cdgs[function_name][0], temp_folder + ".processed.cdg.dot")
                                # os.system(
                                #     f'{DOT_EXE_FILE_PATH} -Tpng {temp_folder + ".processed.cfg.dot"} -o {temp_folder + ".processed.cfg.png"}')
                                # os.system(
                                #     f'{DOT_EXE_FILE_PATH} -Tpng {temp_folder + ".processed.cdg.dot"} -o {temp_folder + ".processed.cdg.png"}')
                                print(f"[CPP] Successfully processed cfg and cdg of {function_name} at {cfg_path}")
                                # delet dot while cfg process is finished
                                while os.path.exists(cfg_path):
                                    os.remove(cfg_path)
                                print(f"[CPP] Successfully delete temp file of cfg at {cfg_path}")
                                count += 1
                else:
                    break

            if ret == 0:
                return cfgs, cdgs
            else:
                return "Failed"


def process_project(file_list, project_folder):
    # # 首先递归找到所有.c .cpp文件和.h文件的相对路径
    # c_source_files_path = dict()
    # c_header_files_path = dict()

    # def find_all_code_files(folder_path):
    #     nonlocal c_source_files_path
    #     nonlocal c_header_files_path
    #     for path in os.listdir(folder_path):
    #         current_path = os.path.join(folder_path, path)
    #         if os.path.isdir(current_path):
    #             find_all_code_files(current_path)
    #         else:
    #             if current_path[-4:] == '.cpp' or current_path[-2:] == '.c':
    #                 index = 0
    #                 index = current_path.find("\\", index)
    #                 while index != -1:
    #                     name = current_path[index + 1:]
    #                     path = current_path[:index]
    #                     name = name.replace('\\', '/')
    #                     try:
    #                         c_source_files_path[name].append(path)
    #                     except KeyError:
    #                         c_source_files_path[name] = [path]
    #                     index = current_path.find("\\", index + 1)
    #             elif current_path[-2:] == '.h':
    #                 index = 0
    #                 index = current_path.find("\\", index)
    #                 while index != -1:
    #                     name = current_path[index + 1:]
    #                     path = current_path[:index]
    #                     name = name.replace('\\', '/')
    #                     # print(name,path)
    #                     try:
    #                         c_header_files_path[name].append(path)
    #                     except KeyError:
    #                         c_header_files_path[name] = [path]
    #                     index = current_path.find("\\", index + 1)

    # find_all_code_files(project_folder)
    # all_cfgs, all_cdgs = handle_folder(file_list, project_folder, c_header_files_path)
    all_cfgs, all_cdgs = handle_folder(file_list, project_folder)

    for path in os.listdir():
        if path[-6:] == '.plist':
            os.remove(path)
    return all_cfgs, all_cdgs


def main(file_list, project_folder):
    # os.environ['path'] = ";".join([ospath for ospath in os.environ['path'].split(';') if
    #                                os.path.abspath(DOT_EXE_FILE_PATH[:-8]) != os.path.abspath(ospath)])
    return process_project(file_list, project_folder)


def compare_cfg(cfg1: nx.DiGraph, cfg2: nx.DiGraph):
    dt1 = cdg.find_dominate_tree(cfg1)
    dt2 = cdg.find_dominate_tree(cfg2)
    dm1 = cdg.cfg_dominance_matrix(cfg1, dt1)
    dm2 = cdg.cfg_dominance_matrix(cfg2, dt2)
    return np.array_equal(dm1, dm2)


def build_pdg(cdg: nx.DiGraph, ddg: nx.DiGraph):
    pdg = nx.MultiDiGraph(ddg)
    if "\\n" in pdg.nodes:
        pdg.remove_node("\\n")
    # add edges from ddg
    for edge in cdg.edges:
        if edge[0] in pdg.nodes and edge[1] in pdg.nodes:
            pdg.add_edge(edge[0], edge[1], color='red')
    return pdg


def create_cfg_tree_json(project_path, results_cfg):
    # create json for cfg file tree
    count = 0
    # get all function nodes
    cfg_function_nodes = []
    # have class flag
    class_flag = False
    all_classes = {}
    for file_path, cfgs in results_cfg.items():
        for function_name, cfg in cfgs.items():
            adj_function_name = function_name
            if "(" not in function_name and ")" not in function_name:
                adj_function_name = function_name + "()"
            current_info = {"id": count, "name": adj_function_name, "label": function_name, "type": "func", "path": file_path}
            count += 1
            if "." in function_name:
                class_flag = True
                classname = function_name.split(".")[0]
                if file_path+classname in all_classes:
                    all_classes[file_path+classname]["children"].append(current_info)
                else:
                    all_classes[file_path+classname] = {"id": count, "name": classname, "label": classname, "type": "class", "path": file_path, "children": [current_info]}
                count += 1
            else:
                cfg_function_nodes.append(current_info)

    # build file tree
    cfg_tree = []
    for file_path in results_cfg.keys():
        rel_path = os.path.relpath(file_path, project_path)
        current_folders = rel_path.split('\\')
        # print(current_folders)
        current_tree = cfg_tree
        for i in range(len(current_folders)):
            # find current level folder in cfg_tree
            # if current level folder already exist, goes to next level
            found = False
            for c in current_tree:
                if c["name"] == current_folders[i]:
                    current_tree = c["children"]
                    found = True
                    break
            if not found:
                # create a current level folder
                temp_folder = {"id": count, "name": current_folders[i], "label": current_folders[i],
                               "type": "folder" if i != len(current_folders) - 1 else "source", "children": []}
                current_tree.append(temp_folder)
                current_tree = current_tree[-1]["children"]
                count += 1

    # add all function nodes into the tree
    for function_node in cfg_function_nodes:
        file_path = function_node["path"]
        rel_path = os.path.relpath(file_path, project_path)
        current_folders = rel_path.split('\\')
        current_tree = cfg_tree
        for i in range(len(current_folders)):
            found = False
            for c in current_tree:
                if c["name"] == current_folders[i]:
                    current_tree = c["children"]
                    found = True
                    break
        # print(function_node, "current_tree", current_tree)
        current_tree.append(function_node)

    # if has class
    if class_flag:
        for class_node in all_classes.values():
            file_path = class_node["path"]
            rel_path = os.path.relpath(file_path, project_path)
            current_folders = rel_path.split('\\')
            current_tree = cfg_tree
            for i in range(len(current_folders)):
                found = False
                for c in current_tree:
                    if c["name"] == current_folders[i]:
                        current_tree = c["children"]
                        found = True
                        break
            current_tree.append(class_node)

    return json.dumps(cfg_tree)


# convert a cfg to a dot string
def convert_to_string(cfg: nx.DiGraph):
    """将一个networkx形式的图转换成字符串的dot格式，便于前端再转换成svg并显示"""
    P_graph = nx.nx_pydot.to_pydot(cfg)
    # write to dot
    # P_graph.write("temp.dot")
    svg_string = P_graph.create_svg(prog=DOT_EXE_FILE_PATH)
    return svg_string


def process_project_to_json(file_list, project_folder):
    return {}, {}, {}, {}
    """处理指定文件夹下的所有C和CPP源文件，并将所有获取的CFG放在一个json字符串中"""
    result_cfgs, result_cdgs = main(file_list, project_folder)
    results_dot = {'cfg': {}, 'pdg': {}, "cfg_js": create_cfg_tree_json(project_folder, result_cfgs),
                   "pdg_js": create_cfg_tree_json(project_folder, result_cdgs)}
    for k, v in result_cfgs.items():
        temp_result = {}
        if v is not None:
            for k1, v1 in v.items():
                temp_result[k1] = convert_to_string(v1)
            results_dot['cfg'][k] = temp_result

    # create ddgs
    ddgs = ddg.DDG_main(file_list, result_cfgs, project_folder)
    # result_pdgs
    result_pdgs = {}
    # dm matrixes
    dominate_matrixes = {}
    # for pdgs, combine cdgs and ddgs
    for k, v in result_cdgs.items():
        temp_result = {}
        temp_file = {}
        if v is not None:
            for k1, v1 in v.items():
                print("build pdg for ", k, k1)
                # if k1 == "test_CU_add_suite":
                #     print("test_CU_add_suite")
                pdg = build_pdg(v1[0], ddgs[k][k1])
                dominate_matrixes[(k.replace('/', '\\'), k1)] = v1[1]
                temp_file[k1] = pdg
                temp_result[k1] = convert_to_string(pdg)
            results_dot['pdg'][k] = temp_result
            result_pdgs[k] = temp_file

    file_tree_data = {}
    count = 0

    # json_str = json.dumps(results_dot)
    
    return result_cfgs, result_pdgs, results_dot, dominate_matrixes


if __name__ == "__main__":
    project_folder = r'D:\Code\test_project\saolei'
    # results= main(project_folder)
    # print()
    # a,b,c =process_project_to_json(project_folder)
    # print(a)
    # print(b)
    # print(c)
    # a, b, c, d = process_project_to_json(project_folder)
    # print(c["cfg_js"])
    # import pprint
    # pprint.pprint(c)
    # print("测试一下转换成 dot string")
    # for k, v in a.items():
    #     for k1, v1 in v.items():
    #         cfg = v1
    #         # 测试一下转换成string
    #         with open("../web/static/graph_show.svg", 'w') as f:
    #             f.write(convert_to_string(cfg).decode())
    #         break
    #     break

    # cfg1 = None
    # cfg2 = None
    # for k, v in results.items():
    #     for k1,v1 in v.items():
    #         if cfg1 == None:
    #             cfg1 = (k,k1,v1)
    #         elif cfg2 == None:
    #             cfg2 = (k,k1,v1)
    #         else:
    #             break

    # print(f"Comparing {cfg1[0]} {cfg1[1]} and {cfg2[0]} {cfg2[1]}")
    # print(compare_cfg(cfg1[2], cfg2[2]))

    c_source_files_path = dict()
    c_header_files_path = dict()

    def find_all_code_files(folder_path):
        for path in os.listdir(folder_path):
            current_path = os.path.join(folder_path, path)
            if os.path.isdir(current_path):
                find_all_code_files(current_path)
            else:
                if current_path[-4:] == '.cpp' or current_path[-2:] == '.c':
                    index = 0
                    index = current_path.find("\\", index)
                    while index != -1:
                        name = current_path[index + 1:]
                        path = current_path[:index]
                        name = name.replace('\\', '/')
                        try:
                            c_source_files_path[name].append(path)
                        except KeyError:
                            c_source_files_path[name] = [path]
                        index = current_path.find("\\", index + 1)
                elif current_path[-2:] == '.h':
                    index = 0
                    index = current_path.find("\\", index)
                    while index != -1:
                        name = current_path[index + 1:]
                        path = current_path[:index]
                        name = name.replace('\\', '/')
                        # print(name,path)
                        try:
                            c_header_files_path[name].append(path)
                        except KeyError:
                            c_header_files_path[name] = [path]
                        index = current_path.find("\\", index + 1)

    find_all_code_files(project_folder)
    print(c_source_files_path)
    print("------------------")
    print(c_header_files_path)
