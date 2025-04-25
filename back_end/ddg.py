"""
构建数据依赖图

"""
import subprocess
import os
import sys
import json
import chardet
import networkx as nx
from utils import *
from merge_funcInfo import *
import process_project


def run_cmd(cmd_str='', echo_print=1):
    """
    执行cmd命令，不显示执行过程中弹出的黑框
    备注：subprocess.run()函数会将本来打印到cmd上的内容打印到python执行界面上，所以避免了出现cmd弹出框的问题
    :param cmd_str: 执行的cmd命令
    :return: 
    """
    if echo_print == 1:
        print('\n执行cmd指令="{}"'.format(cmd_str))
    # run(cmd_str, shell=True)
    subprocess.run(cmd_str, shell=True)


def getfilelist(path):
    # Convert relative path to absolute path
    path = os.path.abspath(path)
    # Get all files in the path
    filelist = []
    sourcetypelist = (".c", ".C", ".cc", ".CC", ".cp", ".c++", ".C++", ".cxx", ".cpp", ".CPP", ".CXX")
    headertypelist = (".h", ".H", ".hh", ".hpp", ".hxx")
    with open(path + "/analyze_files.json", 'r', encoding="utf-8") as f:
        file_select = json.load(f)
    filelist += file_select['header']
    filelist += file_select['source']
    # for root, dirs, files in os.walk(path):
    #     for file in files:
    #         # if os.path.splitext(file)[1] == '.c' or os.path.splitext(file)[1] == '.h' or os.path.splitext(file)[1] == '.l' or os.path.splitext(file)[1] == '.C' or os.path.splitext(file)[1] == '.H' or os.path.splitext(file)[1] == '.cpp' or os.path.splitext(file)[1] == '.hpp' or os.path.splitext(file)[1] == '.CPP' or os.path.splitext(file)[1] == '.HPP':
    #         if file.endswith(sourcetypelist) or file.endswith(headertypelist):
    #             filelist.append(os.path.join(root, file).replace('\\', '/'))

    # new_filelist = []
    # for file in filelist:
    #     # 先存储头文件
    #     # if (file.find('.h') != -1 or file.find('.H') != -1 or file.find('.hpp') != -1 or file.find('.HPP') != -1) and file.find('ncurses') == -1 and file.find('ncursesw') == -1:
    #     if file.endswith(headertypelist) and file.find('ncurses') == -1 and file.find('ncursesw') == -1:
    #         new_filelist.append(file)
    # for file in filelist:
    #     # 再存储源文件
    #     # if (file.find('.c') != -1 or file.find('.C') != -1 or file.find('.cpp') != -1 or file.find('.CPP') != -1 or os.path.splitext(file)[1] == '.l') and file.find('ncurses') == -1 and file.find('ncursesw') == -1:
    #     if file.endswith(sourcetypelist) and file.find('ncurses') == -1 and file.find('ncursesw') == -1:
    #         new_filelist.append(file)
    return filelist


def run_DDAnalysis(file_list, project_folder):
    # 运行parsing程序
    ctypelist = (".c")
    cpptypelist = (".C", ".cc", ".CC", ".cp", ".c++", ".C++", ".cxx", ".cpp", ".CPP", ".CXX")
    sourcetypelist = (".c", ".C", ".cc", ".CC", ".cp", ".c++", ".C++", ".cxx", ".cpp", ".CPP", ".CXX")
    headertypelist = (".h", ".H", ".hh", ".hpp", ".hxx")
    fanIn, fanOut = projectInclude(file_list, project_folder)
    change_file_list = {}
    for file in fanOut:
        if file.endswith(cpptypelist):
            include_file = fanOut[file]
            for include_f in include_file:
                if include_f.endswith(headertypelist):
                    change_file_list[include_f] = include_f + '.hpp'
    for file in file_list:
        # 如果为头文件，则新建一个同名的.hpp文件，将头文件内容复制到.hpp文件中
        # if file.endswith((".h", ".H", ".hh", ".hpp", ".hxx")):
        #     new_file = file+'.hpp'
        #     with open(file, 'r') as f:
        #         with open(new_file, 'w') as f1:
        #             for line in f.readlines():
        #                 f1.write(line)
        # 基于include来判定是否需要将该文件转换为.hpp文件
        if file in change_file_list:
            new_file = change_file_list[file]
            with open(file, 'r', encoding="utf-8") as f:
                with open(new_file, 'w', encoding="utf-8") as f1:
                    for line in f.readlines():
                        f1.write(line)
            run_cmd('./DDAnalysis/build/DDAnalysis ' + new_file)
            var_define1 = file+'.var_define1'
            with open(new_file+'.var_define1', 'r', encoding="utf-8") as f:
                with open(var_define1, 'a', encoding="utf-8") as f1:
                    for line in f.readlines():
                        f1.write(line.replace(new_file, file))
            var_define2 = file+'.var_define2'
            with open(new_file+'.var_define2', 'r', encoding="utf-8") as f:
                with open(var_define2, 'a', encoding="utf-8") as f1:
                    for line in f.readlines():
                        f1.write(line.replace(new_file, file))
            var_using = file+'.var_using'
            with open(new_file+'.var_using', 'r', encoding="utf-8") as f:
                with open(var_using, 'a', encoding="utf-8") as f1:
                    for line in f.readlines():
                        f1.write(line.replace(new_file, file))

            # 删除新建的.hpp文件
            os.remove(new_file)
        else:
            run_cmd('./DDAnalysis/build/DDAnalysis' + file)


def get_file_encoding(filepath):
    with open(filepath, 'rb') as f:
        file = open(filepath, 'rb')
        # 根据二进制信息判断编码{'encoding': 'ascii', 'confidence': 1.0, 'language': ''}
        encoding_message = chardet.detect(file.read())
        # print(filepath, encoding_message['encoding'])
        file.close()
        if encoding_message["encoding"] is None:
            return None
        if encoding_message['encoding'] == "GB2312":
            encoding_message['encoding'] = "GBK"
        return encoding_message['encoding']

def get_define_macro(macro_loc):
    tmp = macro_loc.split(":")
    if os.path.exists(tmp[0]+':'+tmp[1]):
        with open(tmp[0]+':'+tmp[1], "r", encoding="utf-8") as f:
            lines = f.readlines()
        line_num = int(tmp[-2])
        col_num = int(tmp[-1])
        line = lines[line_num-1]
        txt = line[:col_num-1]
        txt=txt.replace("#define", "")
        txt=txt.replace(" ", "")
        txt=txt.replace("\t", "")
        return txt
    else:
        return ""

def get_var_using_defining(file_list):
    using_dict = {}
    defining_dict = {}
    for file in file_list:
        # 获取变量定义信息
        defining_file = file+'.var_define1'
        # 判断是否存在文件
        if not os.path.exists(defining_file):
            continue
        # 按行读取文件
        lines = []
        encoding = get_file_encoding(defining_file)
        with open(defining_file, 'r', encoding=encoding) as f:
            for line in f.readlines():
                line = line.strip('\n')
                lines.append(line)
        for line in lines:
            infos = line.split(';;')
            var_name = infos[0]
            if ':' in var_name:
                var_name = var_name[var_name.find(' <'):].replace('Spelling=','').replace('>','').replace(' <','')
                var_name = os.path.abspath(var_name).replace('\\', '/')
                var_name = get_define_macro(var_name)
            var_type = infos[1]
            define_loc = infos[2]
            if ' <' in define_loc:
                define_loc = define_loc[:define_loc.find(' <')]
            var_defining = ":".join(infos[2].split(':')[:-1])
            if var_defining not in defining_dict.keys():
                defining_dict[var_defining] = []
            defining_dict[var_defining].append([var_name, var_type, define_loc])

        # 获取变量使用信息
        using_file = file+'.var_using'
        # 判断是否存在文件
        if not os.path.exists(using_file):
            continue

        # 按行读取文件
        lines = []
        encoding = get_file_encoding(using_file)
        with open(using_file, 'r', encoding=encoding) as f:
            for line in f.readlines():
                line = line.strip('\n')
                lines.append(line)

        for line in lines:
            infos = line.split(';;')
            var_name = infos[0]
            if ':' in var_name:
                var_name = var_name[var_name.find(' <'):].replace('Spelling=','').replace('>','').replace(' <','')
                var_name = os.path.abspath(var_name).replace('\\', '/')
                var_name = get_define_macro(var_name)
            var_type = infos[1]
            using_loc = infos[2]
            if ' <' in using_loc:
                using_loc = using_loc[:using_loc.find(' <')]
            var_using = ":".join(infos[2].split(':')[:-1])
            find = 0
            if var_using in defining_dict.keys():
                for var in defining_dict[var_using]:
                    if var[0] == var_name and var[1] == var_type and var[2] == using_loc:
                        find = 1
                        break
            if find == 1:
                continue
            if var_using not in using_dict.keys():
                using_dict[var_using] = []
            using_dict[var_using].append([var_name, var_type, using_loc])

        # 获取变量定义信息
        defining_file = file+'.var_define2'
        # 判断是否存在文件
        if not os.path.exists(defining_file):
            continue
        # 按行读取文件
        lines = []
        encoding = get_file_encoding(defining_file)
        with open(defining_file, 'r', encoding=encoding) as f:
            for line in f.readlines():
                line = line.strip('\n')
                lines.append(line)
        for line in lines:
            infos = line.split(';;')
            var_name = infos[0]
            if ':' in var_name:
                var_name = var_name[var_name.find(' <'):].replace('Spelling=','').replace('>','').replace(' <','')
                var_name = os.path.abspath(var_name).replace('\\', '/')
                var_name = get_define_macro(var_name)
            var_type = infos[1]
            define_loc = infos[2]
            if ' <' in define_loc:
                define_loc = define_loc[:define_loc.find(' <')]
            var_defining = ":".join(infos[2].split(':')[:-1])
            if var_defining not in defining_dict.keys():
                defining_dict[var_defining] = []
            defining_dict[var_defining].append([var_name, var_type, define_loc])

    # point_matched
    point_matched_var = {}
    for loc, vars in defining_dict.items():
        for var in vars:
            if "*" in var[1]:
                if loc in using_dict.keys():
                    using_set = using_dict[loc]
                    for using in using_set:
                        if "[" in using[1] and "]" in using[1]:
                            point_matched_var[loc] = [var, using]
                        else:
                            if using[1] in var[1] and using[0] != var[0]:
                                point_matched_var[loc] = [var, using]

    return using_dict, defining_dict, point_matched_var


class DDG_node:
    def __init__(self):
        self.id = ""
        self.label = ""
        self.loc = ""
        self.using_set = []
        self.defining_set = []
        self.dd = []
        self.using_point = []
        self.defining_point = []


def get_DDGraph(cfg_data, using_dict, defining_dict, point_matched_var):
    print('get DDGraph')
    DDG_dict = {}
    for file, funcs in cfg_data.items():
        print("处理：", file)
        DDG_dict[file] = {}
        if funcs == None:
            continue
        for func, cfg in funcs.items():
            print("处理: ", func)
            DDG_dict[file][func] = []
            node_dict = {}
            # CFG是一个networkx的有向图，节点是基本块，边是基本块之间的跳转关系，遍历节点
            for node in cfg.nodes():
                node_info = cfg.nodes[node]
                # 获取节点信息
                node_id = node
                node_label = node_info['label']
                node_loc = ""
                if 'sourceLoc' in node_info.keys():
                    if node_info['sourceLoc'] != -1:
                        node_loc = file.replace('\\', '/') + ':' + str(node_info['sourceLoc'])

                # 构建DDG节点
                DDG_node_ = DDG_node()
                DDG_node_.id = node_id
                DDG_node_.label = node_label
                DDG_node_.loc = node_loc
                if node_loc in using_dict.keys():
                    for var in using_dict[node_loc]:
                        if var[0] in node_label:
                            DDG_node_.using_set.append(var)
                            if '*' in var[1]:
                                DDG_node_.using_point.append(var)
                if node_loc in defining_dict.keys():
                    for var in defining_dict[node_loc]:
                        if var[0] in node_label and 'for (' not in node_label:
                            DDG_node_.defining_set.append(var)
                            if '*' in var[1]:
                                DDG_node_.defining_point.append(var)

                node_dict[node_id] = DDG_node_

            # 遍历节点，如果节点定义集和使用集中存在相同变量，且++或--不在代码中出现，判断 = 出现的位置，如果变量在 = 左边，将将该变量从使用集中删除，如果变量在 = 右边，将该变量从定义集中删除
            for node_id, node in node_dict.items():
                remove_dict = {}
                remove_dict['using'] = []
                remove_dict['defining'] = []
                for var1 in node.using_set:
                    for var2 in node.defining_set:
                        if var1[0] == var2[0] and var1[1] == var2[1]:
                            if '++' not in node.label and '--' not in node.label:
                                if '=' in node.label:
                                    if var1[0] in node.label.split('=')[0]:
                                        remove_dict['using'].append(var1)
                                    elif var1[0] in node.label.split('=')[1]:
                                        remove_dict['defining'].append(var2)

                for var in remove_dict['using']:
                    if var in node.using_set:
                        node.using_set.remove(var)
                for var in remove_dict['defining']:
                    if var in node.defining_set:
                        node.defining_set.remove(var)
            # 将指针变量替换为其指向的变量
            START_NODE = None
            for node_id, node in node_dict.items():
                if 'ENTRY' in node.label:
                    START_NODE = node_id

            # 从START_NODE开始遍历CFG，将指针变量替换为其指向的变量
            STOCK = list()
            STOCK.append([START_NODE])
            processed_child = {}
            while len(STOCK) != 0:
                path = STOCK.pop()
                node_id = path[-1]
                for var in node_dict[node_id].defining_set:
                    # 判断是否为指针变量
                    if "*" in var[1]:
                        # 判断使用集是否为空
                        if len(node_dict[node_id].using_set) != 0:
                            # 进行了初始化
                            loc = ':'.join(var[2].split(':')[:-1])
                            if loc in point_matched_var.keys():
                                matched_var = point_matched_var[loc][1]
                                # 如果为指针，则倒叙遍历path，找到其指向的变量
                                start = len(path)-1
                                while '*' in matched_var[1] and start >= 0:
                                    # print('指向另一个指针变量1')
                                    while start >= 0:
                                        parent_id = path[start]
                                        find = False
                                        for defined_var in node_dict[parent_id].defining_set:
                                            if matched_var[0] == defined_var[0] and matched_var[1] == defined_var[1]:
                                                loc = ':'.join(defined_var[2].split(':')[:-1])
                                                if loc in point_matched_var.keys():
                                                    matched_var = point_matched_var[loc][1]
                                                    find = True
                                                    break
                                        start -= 1
                                        if find:
                                            break

                                if func == 'rt_strnlen':
                                    print()
                                # 将指针变量替换为其指向的变量
                                Pointer_replace(cfg, node_id, node_dict, var, matched_var, point_matched_var)

                for child in cfg.successors(node_id):
                    if node_id not in processed_child:
                        processed_child[node_id] = []
                    if child not in processed_child[node_id] and child not in path:
                        STOCK.append(path + [child])
                        processed_child[node_id].append(child)

            # 构建数据依赖图
            node_dict = build_DDGraph(cfg, node_dict)
            # 清空cfg中的边
            new_cfg = nx.DiGraph(cfg)
            new_cfg.remove_edges_from(list(cfg.edges()))
            # 在cfg中添加数据依赖边，虚线
            for node_id, node in node_dict.items():
                for dd_node_id in node.dd:
                    new_cfg.add_edge(dd_node_id, node_id, color='blue', style='dashed')

            DDG_dict[file][func] = new_cfg
            # 将cfg写入dot文件，并生成png文件
            dot_file = file.replace('\\', '/') + '_ddg_' + func + '.dot'
            png_file = file.replace('\\', '/') + '_ddg_' + func + '.png'
            # nx.drawing.nx_pydot.write_dot(cfg, dot_file)
            # run_cmd('D:/Graphviz/bin/dot.exe -Tpng ' + dot_file + ' -o ' + png_file)
    return DDG_dict


def Pointer_replace(cfg, start_node, node_dict, pointer, matched_var, point_matched_var, last_matched_var=None):
    # print()
    # print('替换指针变量')
    # 深度优先搜索，将指针变量替换为指向的变量
    # 停止搜索该路径的条件：1.遇到重复节点 2.指针变量被重新赋值 3.指针变量被释放 4.到达(exit)节点
    # 存储访问过的节点
    processed_child = {}
    STOCK = []
    STOCK.append([start_node])
    new_defining_set = set()
    while len(STOCK) != 0:
        # print(STOCK)
        path = STOCK.pop()
        node_id = path[-1]
        if node_id == start_node:
            for child in cfg.successors(node_id):
                STOCK.append(path + [child])
            continue
        # 如果遇到重复节点，则停止搜索该路径
        if path.count(node_id) > 1:
            continue
        # 如果指针变量被重新赋值，获取其匹配的新的变量
        re_define = False
        for var in node_dict[node_id].defining_set:
            if var[0] == pointer[0] and var[1] == pointer[1] and var[2] != pointer[2]:
                pointer = var
                re_define = True
                break
        if re_define:
            new_defining_set.add(node_id)
            loc = ':'.join(pointer[2].split(':')[:-1])
            if loc in point_matched_var.keys():
                new_matched_var = point_matched_var[loc][1]
                # 如果为指针，则倒叙遍历path，找到其指向的变量
                start = len(path)-1
                while '*' in matched_var[1] and start >= 0:
                    # print("指向另一个指针变量2")
                    while start >= 0:
                        parent_id = path[start]
                        find = False
                        for defined_var in node_dict[parent_id].defining_set:
                            if new_matched_var[0] == defined_var[0] and new_matched_var[1] == defined_var[1]:
                                loc = ':'.join(defined_var[2].split(':')[:-1])
                                if loc in point_matched_var.keys():
                                    new_matched_var = point_matched_var[loc][1]
                                    find = True
                                    break
                        start -= 1
                        if find:
                            break
                if last_matched_var!=None:
                    if new_matched_var[0] == last_matched_var[0] and new_matched_var[1] == last_matched_var[1]:
                        return
                # 将指针变量替换为其指向的变量
                Pointer_replace(cfg, node_id, node_dict, pointer, new_matched_var, point_matched_var, matched_var)
                continue

        # 如果到达exit节点，则停止搜索该路径
        if 'EXIT' in node_dict[node_id].label:
            continue

        # 如果指针变量被使用，则将其替换为指向的变量
        find = False
        remove_list = []
        for var in node_dict[node_id].using_point:
            cfg_node = cfg.nodes[node_id]
            if var[0] == pointer[0] and var[1] == pointer[1] and '*' in cfg_node['label']:
                # 判断指针前是否有*，如果没有，则不替换
                index = cfg_node['label'].index(var[0])-1
                if index >= 0 and cfg_node['label'][index] == '*':
                    find = True
                    remove_list.append(var)
        for var in remove_list:
            if var in node_dict[node_id].using_set:
                node_dict[node_id].using_set.remove(var)
        if find:
            node_dict[node_id].using_set.append(matched_var)

        # 如果指针变量被定义，则将其替换为指向的变量
        find = False
        remove_list = []
        for var in node_dict[node_id].defining_point:
            cfg_node = cfg.nodes[node_id]
            if var[0] == pointer[0] and var[1] == pointer[1] and '*' in cfg_node['label']:
                # 判断指针前是否有*，如果没有，则不替换
                index = cfg_node['label'].index(var[0])-1
                if index >= 0 and cfg_node['label'][index] == '*':
                    find = True
                    remove_list.append(var)
        for var in remove_list:
            if var in node_dict[node_id].defining_set:
                node_dict[node_id].defining_set.remove(var)
        if find:
            node_dict[node_id].defining_set.append(matched_var)

        # 将该节点的后继节点加入STOCK
        for child in cfg.successors(node_id):
            new_path = list(path)
            if node_id not in processed_child.keys():
                processed_child[node_id] = []
            if child not in processed_child[node_id] and child not in new_defining_set and child not in new_path:
                processed_child[node_id].append(child)
                STOCK.append(new_path + [child])


def build_DDGraph(cfg, node_dict):
    # print("构建数据依赖图")
    for node_id, node in node_dict.items():
        # if node_id == "B1-7":
        #     print("debug")
        define_node_list = set()
        use_set = set([u[0] for u in node.using_set])
        for var in use_set:
            define_node_list = list()
            processed_parent = dict()

            STOCK = []
            STOCK.append([node_id])
            while len(STOCK) != 0:
                path = STOCK.pop()
                last_node = path[-1]
                for parent_id in cfg.predecessors(last_node):
                    if last_node not in processed_parent.keys():
                        processed_parent[last_node] = []

                    # 如果该节点的父节点不在路径中，且该节点的父节点不在已处理的父节点中，则将该父节点加入路径中
                    # 如果已经处理过该父节点，则不再处理
                    if parent_id not in path and parent_id not in processed_parent[last_node]:
                        temp = [d[0] for d in node_dict[parent_id].defining_set]
                        if var in [d[0] for d in node_dict[parent_id].defining_set]:
                            # 如果该父节点定义了该变量，则将该父节点加入定义节点列表中
                            define_node_list.append(parent_id)
                            processed_parent[last_node].append(parent_id)
                        else:
                            # 如果该父节点没有定义该变量，则将该父节点加入路径中
                            STOCK.append(path+[parent_id])
                            processed_parent[last_node].append(parent_id)
                    elif parent_id == node_id:
                        # 如果该节点的父节点是当前节点，则将该节点加入定义节点列表中
                        if var in [d[0] for d in node_dict[parent_id].defining_set]:
                            define_node_list.append(parent_id)
                            processed_parent[last_node].append(parent_id)
                        else:
                            processed_parent[last_node].append(parent_id)
            node.dd += list(set(define_node_list))

    return node_dict


def DDG_main(file_list, cfg_data, project_folder):
    # 获取代码文件列表
    # file_list = getfilelist(project_path)
    # 运行解析程序
    run_DDAnalysis(file_list, project_folder)
    # 获取变量使用和定义信息
    using_dict, defining_dict, pointer_matched_var = get_var_using_defining(file_list)

    # 构建数据依赖图
    DDG = get_DDGraph(cfg_data, using_dict, defining_dict, pointer_matched_var)

    return DDG


if __name__ == "__main__":
    project_path = r"E:\CPP_master\dev0807\CPP_support\back_end\project\saolei"
    cfg_data, cdg_data, graph_json = process_project.process_project_to_json(project_path)
    DDG_main(project_path, cfg_data)
