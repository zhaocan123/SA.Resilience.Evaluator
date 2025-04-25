# 管道过滤器风格架构图 For c
import multiprocessing
import subprocess

import networkx as nx
import re
import sys
import pydot
import os
import time
import json

from utils import get_file_encoding

pwd = os.getcwd()
pwd = pwd.replace("\\", "/")
with open(pwd + "/config.json", "r", encoding="utf-8") as f:
    content = json.load(f)
DOT_EXE_FILE_PATH = content["DOT_EXE_FILE_PATH"]


def pointer_parameters_info(file_list, project_path: str) -> dict:
    # construct a list to store all functions whose parameters has pointers
    # the elements are the '[file name]: [function name]'
    pointer_parameters_functions = []
    not_parameter_functions = []
    # iterative all files in the project
    for file in os.listdir(project_path):
        tmp = os.path.join(project_path, file).replace("\\", "/").replace("//", "/")
        if file.endswith(".c") and tmp in file_list:
            # run the "GET_FUNCTION_INFO" command to get the function information
            # and store the information in a file
            # if the file is not exist, then create it
            if not os.path.exists(os.path.join(project_path, file) + '.txt'):
                raise Exception("[Pre-process Error] The file " + os.path.join(project_path, file) + '.txt' + " is not exist")
            # open the file
            # print(project_path, file)
            encoding = get_file_encoding(os.path.join(project_path, file) + '.txt')
            with open(os.path.join(project_path, file) + '.txt', "r", encoding=encoding) as f:
                functions = f.readlines()
                is_pointer = False
                for function in functions:
                    if len(function.strip()) > 1:
                        temp = function.strip()[:-1].split(";")
                        name = temp[0]
                        parameters = temp[3:]
                        # print(name, parameters)
                        if len(parameters) <= 4:
                            not_parameter_functions.append(file + ": " + name)
                        else:
                            for parameter in parameters:
                                if parameter.strip().endswith("*"):
                                    is_pointer = True
                                    break
                    if is_pointer:
                        pointer_parameters_functions.append(file + ": " + name)

        # elif this is a folder, then recursive call this function
        elif os.path.isdir(os.path.join(project_path, file)):
            ppf, npf = pointer_parameters_info(file_list,
                                               os.path.join(project_path, file))
            pointer_parameters_functions = pointer_parameters_functions + ppf
            not_parameter_functions = not_parameter_functions + npf

    return pointer_parameters_functions, not_parameter_functions


def pipe_filter(plcg: nx.DiGraph, library_functions: dict, pointer_parameters_functions: list, no_parameter_functions: list):
    if "\\n" in plcg.nodes:
        plcg.remove_node('\\n')
    for node in list(plcg.nodes):
        # if this node has not in edge and no out edge, just remove it from pipe filter graph
        if len(list(plcg.predecessors(node))) == 0 and len(list(plcg.successors(node))) == 0:
            plcg.remove_node(node)
    pipe_filter_graph = plcg.copy()
    modified_plcg = plcg.copy()
    for node in list(pipe_filter_graph.nodes):
        if pipe_filter_graph.nodes[node]["file"].strip().strip('"').strip() != "Library function":
            call_infos = pipe_filter_graph.nodes[node]["call_code"]
            function_calls = call_infos.split("|||")
            for function_call in function_calls:
                if function_call.strip().strip('"') != "":
                    function_name = function_call.strip().strip('"').split(":")[0]

                    calls = function_call[function_call.find(':')+1:].split("@@@")

                    # find the corresponding node of the function_name in pipe_filter_graph
                    return_call = False
                    # check all call in calls to see if there is a return value
                    # use regex to match if this is a simple function call with out return value
                    # a simple function call is like function1(para1, para2, ...);
                    # and it must have ");" at the end
                    # and shall start with a letter or "_", and can only contain letters, numbers, and "_" as the function name
                    # then a "(" shall follow
                    # between the "(" and ")" there can be any a string of any length and any character
                    for call in calls:
                        if call.strip().strip('"') == "":
                            continue
                        re_expression = r"^[a-zA-Z_][a-zA-Z0-9_]*\((.*)\);$"

                        # try to mathc the re_expression
                        match = re.match(re_expression, call.strip().strip('"'))
                        if not match:
                            return_call = True
                        else:
                            # additionaly, if we can match a function all inside a existing function call, this is also means there is a return value
                            # for example, if we have a function call like function1(function2(para1, para2, ...), para3, ...);
                            # then we can match function2(para1, para2, ...) as a function call
                            # and we can also match function1(function2(para1, para2, ...), para3, ...) as a function call
                            # so we need to check if the function call is inside another function call
                            re_expression_2 = r"[a-zA-Z_][a-zA-Z0-9_]*\((.*)\)"
                            # try to match the re_expression_2 in the parameter of the function call
                            function_call_str = call.strip().strip('"')
                            match_2 = re.search(
                                re_expression_2, function_call_str[function_call_str.find("(")+1:-2])

                            if match_2:
                                # print(match_2, function_name, match_2.group(0))
                                # then check if the function call is current funciton
                                if match_2.group(0).split("(")[0] == function_name:
                                    # print(match_2.group(0).split("(")[0])
                                    return_call = True

                    # if there is a return value, add a back edge from the called node to current node
                    if return_call:
                        for called_node in list(pipe_filter_graph.nodes):
                            label = pipe_filter_graph.nodes[called_node]["label"]
                            called_node_name = label.split(
                                ":")[1].strip().strip('"').strip()
                            if called_node_name == function_name:
                                pipe_filter_graph.add_edge(called_node, node)
                                pipe_filter_graph.edges[called_node,
                                                        node]["pftype"] = "back"
                                break

    # then check all libraries functions about input and output functions
    # actually we only concern about the input nodes like scanf() or fread()
    for node in plcg.nodes:
        # get the function name
        label = plcg.nodes[node]["label"]
        library_name = plcg.nodes[node]["file"].strip().strip('"').strip()
        function_name = label.split(":")[-1].strip().strip('"').strip()
        # print(label, library_name, function_name)
        # check if this is a library function
        if library_name != "Library function":
            # check if this node has an pointer parameter
            if label.strip().strip('"').strip() in pointer_parameters_functions:
                # if it is, check if there are call edges to this node
                for edge in plcg.in_edges(node):
                    # and add a back edge in pipe_filter_graph
                    pipe_filter_graph.add_edge(node, edge[0])
            elif label.strip().strip('"').strip() in no_parameter_functions:
                # if it is, check if there are call edges to this node
                for edge in plcg.in_edges(node):
                    # remove the edge from pipe_filter_graph
                    pipe_filter_graph.remove_edge(edge[0], edge[1])
        elif function_name in library_functions["input"] and library_name == "Library function":
            # print(library_name, function_name)
            # if it is, check if there are call edges to this node
            for edge in plcg.in_edges(node):
                # add a back edge from the called node to current node
                modified_plcg.add_edge(node, edge[0])
                # and remove this edge in modified_plcg
                modified_plcg.remove_edge(edge[0], edge[1])
                # # also remove all call edges in pie_filter_graph
                # pipe_filter_graph.remove_edge(edge[0], edge[1])
                # and add a back edge in pipe_filter_graph
                pipe_filter_graph.add_edge(node, edge[0])

    return modified_plcg, pipe_filter_graph


def export_pipe_filter_dot(plcg: nx.DiGraph, pipe_filter_graph: nx.DiGraph, library_functions: dict, project_path: str):
    # write the dot file
    P = pydot.Dot(graph_type='digraph', rankdir="LR", splines="ortho")

    for node in pipe_filter_graph.nodes:
        # project_path = project_path.replace("/", "\\")
        all_path = ":".join(plcg.nodes[node]["label"].strip().strip('"').split(':')[:2])
        # all_path = all_path.replace("/","\\")
        # if all path is starts with project path
        if os.path.realpath(all_path).startswith(os.path.realpath(project_path)):
            relative_path = os.path.relpath(all_path, project_path).replace("\\", "/")
        else:
            relative_path = os.path.realpath(all_path).split('\\')[-1]
        function_name = plcg.nodes[node]["label"].strip().strip('"').split(':')[-1]
        print(all_path, project_path, relative_path)
        node_label = '"Filter: ' + relative_path + ':' + function_name + '"'
        P.add_node(pydot.Node(node, label=node_label, shape="box", style="filled", fillcolor="lightgreen"))

    for edge in pipe_filter_graph.edges:
        # add a label "Pipe" to the edge
        P.add_edge(pydot.Edge(edge[0], edge[1]))

    # finally add an edge from an input pool node to every node in the library_functions['input'] or main() function
    # this node is a cycle
    pump_node_count = 0
    for node in plcg.nodes:
        if plcg.nodes[node]["label"].split(":")[-1].strip().strip('"').strip() in library_functions["input"] or plcg.nodes[node]["label"].split(":")[-1].strip().strip('"').strip() == "main":
            # set pump node color to lightblue
            pump_node = pydot.Node("Pump_" + str(pump_node_count),
                                   label="Pump", style="filled", fillcolor="lightblue")
            P.add_node(pump_node)
            P.add_edge(pydot.Edge(pump_node, node))
            pump_node_count += 1

    # And add an edge from every node in the library_functions['output'] to an output pool node
    # this node is a cycle
    sink_node_count = 0
    for node in plcg.nodes:
        if plcg.nodes[node]["label"].split(":")[-1].strip().strip('"').strip() in library_functions["output"] or plcg.nodes[node]["label"].split(":")[-1].strip().strip('"').strip() == "main":
            # set sink node color to light yellow
            sink_node = pydot.Node("Sink_" + str(sink_node_count),
                                   label="Sink", style="filled", fillcolor="lightyellow")
            P.add_node(sink_node)
            P.add_edge(pydot.Edge(node, sink_node))
            sink_node_count += 1

    # write result to file
    print("writing svg file")
    # P.write("temp.dot", format='dot', prog=DOT_EXE_FILE_PATH)

    # 不再创建dot而是直接返回一个SVG
    return P.create_svg(prog=DOT_EXE_FILE_PATH)


def main(file_list, plcg: nx.DiGraph, project_path):
    # plcg_path = sys.argv[1]
    # project_path = sys.argv[2]
    # output_path = sys.argv[3]
    print("Pipe filter running...", project_path)
    pointer_parameters, no_parameters = pointer_parameters_info(file_list, project_path)
    # print(pointer_parameters, no_parameters)
    # plcg = nx.DiGraph(nx.nx_pydot.read_dot(plcg_path))

    library_functions = {'input': ['scanf', 'fread', 'sscanf', 'getchar', 'open'],
                         'output': ['printf', 'fwrite', 'system', 'fflush', 'open', 'asprintf']}
    modified_plcg, pipe_filter_graph = pipe_filter(
        plcg, library_functions, pointer_parameters, no_parameters)
    return pipe_filter_graph, export_pipe_filter_dot(modified_plcg, pipe_filter_graph, library_functions, project_path)

    # nx.nx_pydot.write_dot(pipe_filter_graph, "pipe_filter_graph.dot")


if __name__ == "__main__":
    # multiprocessing.freeze_support()
    main()
