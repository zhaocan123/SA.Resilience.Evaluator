import networkx as nx
import re
import pydot
import os
import json

pwd = os.getcwd()
pwd = pwd.replace("\\", "/")
with open(pwd + "/config.json", "r", encoding="utf-8") as f:
    content = json.load(f)
DOT_EXE_FILE_PATH = content["DOT_EXE_FILE_PATH"]


def parameters_info(file_list, project_path: str) -> dict:
    # construct a list to store all functions whose parameters are not none
    # the elements are the '[file name]: [function name]'
    parameters_functions = {}
    not_parameter_functions = []
    # iterative all files in the project
    for file in os.listdir(project_path):
        tmp = os.path.join(project_path, file).replace("\\", "/").replace("//", "/")
        if (file.endswith(".c") or file.endswith(".h")) and tmp in file_list:
            # run the "GET_FUNCTION_INFO" command to get the function information (already finished in pre-process part)
            # and store the information in a file
            # if the file is not exist, then create it
            if not os.path.exists(os.path.join(project_path, file) + '.parameter'):
                err_msg = "[Pre-process Error] The file " + os.path.join(project_path, file) + '.parameter' + " is not exist"
                print(err_msg)
                raise Exception(err_msg)
            # open the file
            # print(project_path, file)
            with open(os.path.join(project_path, file) + '.parameter', "r") as f:
                functions = f.readlines()
                for function in functions:
                    if len(function.strip()) > 1:
                        temp = function.strip()[:-1].split(";")
                        name = temp[0]
                        parameters = temp[5:]
                        # print(name, parameters)
                        file = os.path.abspath(os.path.join(project_path, file)).replace("\\", "/")
                        if len(parameters) <= 4:
                            not_parameter_functions.append(file + ":" + temp[1] + ":" + name)
                        else:
                            for _ in parameters:
                                try:
                                    parameters_functions[file + ":" + temp[1] + ":" + name] += 0.5
                                except KeyError:
                                    parameters_functions[file + ":" + temp[1] + ":" + name] = 0.5

        # elif this is a folder, then recursive call this function
        elif os.path.isdir(os.path.join(project_path, file)):
            ppf, npf = parameters_info(file_list, os.path.join(project_path, file))
            # add result into current parameter infos
            parameters_functions.update(ppf)
            not_parameter_functions = not_parameter_functions + npf

    return parameters_functions, not_parameter_functions


def construct_func_level_sdg(plcg: nx.DiGraph, pointer_parameters_functions: dict):
    if "\\n" in plcg.nodes:
        plcg.remove_node('\\n')
    # no longer remove unconnected nodes
    # for node in list(plcg.nodes):
    #     # if this node has not in edge and no out edge, just remove it from pipe filter graph
    #     if len(list(plcg.predecessors(node))) == 0 and len(list(plcg.successors(node))) == 0:
    #         plcg.remove_node(node)
    pipe_filter_graph = nx.MultiDiGraph(plcg.copy())
    modified_plcg = plcg.copy()

    for edge in list(pipe_filter_graph.edges):
        pipe_filter_graph.edges[edge]['count'] = 1

    # add paremeter-out edges
    for node in list(pipe_filter_graph.nodes):
        if pipe_filter_graph.nodes[node]["file"].strip().strip('"').strip() != "Library function":
            call_infos = pipe_filter_graph.nodes[node]["call_code"].strip().strip('"').strip()
            function_calls = call_infos.split("|||")
            for function_call in function_calls:
                if function_call.strip().strip('"') != "":
                    function_name = function_call.strip().strip('"').split(":")[0]

                    calls = function_call[function_call.find(':')+1:].split("@@@")

                    # find the corresponding node of the function_name in pipe_filter_graph

                    # check all call in calls to see if there is a return value
                    # use regex to match if this is a simple function call with out return value
                    # a simple function call is like function1(para1, para2, ...);
                    # and it must have ");" at the end
                    # and shall start with a letter or "_", and can only contain letters, numbers, and "_" as the function name
                    # then a "(" shall follow
                    # between the "(" and ")" there can be any a string of any length and any character
                    return_call = False
                    # remove empty strings in calls
                    calls = [call.strip() for call in calls if call.strip() != "" and call.strip() != '"' and call.strip('"') != '']
                    for call in calls:
                        re_expression = r"^[a-zA-Z_][a-zA-Z0-9_]*\((.*)\);$"

                        # try to mathc the re_expression
                        match = re.match(re_expression, call.strip().strip('"'))
                        # print(match)
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

                    # if there is a return value, add parameter-out edges
                    if return_call:
                        for called_node in list(pipe_filter_graph.nodes):
                            label = pipe_filter_graph.nodes[called_node]["label"]
                            called_node_name = label.split(":")[-1].strip().strip('"').strip()
                            if called_node_name == function_name:
                                if (called_node, node) not in pipe_filter_graph.edges(called_node, node):
                                    pipe_filter_graph.add_edge(called_node, node, style="dotted", count=1)

                    for c_edge in pipe_filter_graph.out_edges(node):
                        called_node = c_edge[1]
                        label = pipe_filter_graph.nodes[called_node]["label"]
                        called_node_name = label.split(":")[-1].strip().strip('"').strip()
                        if called_node_name == function_name:
                            # set our edge's count to len(calls)
                            # print(pipe_filter_graph.edges[c_edge[0], c_edge[1],0])
                            pipe_filter_graph.edges[c_edge[0], c_edge[1], 0]['count'] = len(calls)
        else:
            pipe_filter_graph.remove_node(node)

    # add paremeter-in edges
    for node in plcg.nodes:
        # get the function name
        label = plcg.nodes[node]["label"]
        library_name = plcg.nodes[node]["file"].strip().strip('"').strip()
        function_name = label.split(":")[-1].strip().strip('"').strip()
        # check if this is a library function
        if library_name != "Library function":
            # print(label.strip().strip('"').strip())
            # check if this node has parameter, if there are parametes, add parameter-in edges
            if label.strip().strip('"').strip() in pointer_parameters_functions.keys():
                # print("function has parameter", label.strip().strip('"').strip())
                # if it is, check if there are call edges to this node
                for edge in plcg.in_edges(node):
                    # and add a back edge in pipe_filter_graph
                    pipe_filter_graph.add_edge(edge[0], node, style='dotted', count=int(pointer_parameters_functions[label.strip().strip('"').strip()]))

    # remove all call_code in pipe_filter_graph
    for node in pipe_filter_graph.nodes:
        # remove the key "call_code" in the node
        try:
            pipe_filter_graph.nodes[node]["code_file_path"] = pipe_filter_graph.nodes[node]["file"]
            del pipe_filter_graph.nodes[node]["file"]
            del pipe_filter_graph.nodes[node]["call_code"]
            del pipe_filter_graph.nodes[node]["Lib"]
        except KeyError:
            pass

    return modified_plcg, pipe_filter_graph


def export_pipe_filter_dot(plcg: nx.DiGraph, pipe_filter_graph: nx.MultiDiGraph, project_path: str):
    P = pydot.Dot(graph_type='digraph', rankdir="TD")  # , splines="line")

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
        # print(all_path, project_path, relative_path)
        node_label = '"Function: ' + relative_path + ':' + function_name + '"'
        P.add_node(pydot.Node(node, label=node_label, shape="box"))

    for edge in pipe_filter_graph.edges:
        # add an edge for each kind of edge in sdg
        # if data depend
        if 'style' in pipe_filter_graph.edges[edge].keys() and pipe_filter_graph.edges[edge]['style'] == "dotted":
            P.add_edge(pydot.Edge(edge[0], edge[1], style='dotted', color='blue'))
        else:
            P.add_edge(pydot.Edge(edge[0], edge[1], color='red'))

    # write result to file
    print("writing svg file for sdg")
    # P.write("temp.dot", format='dot', prog=DOT_EXE_FILE_PATH)
    sdg_svg = P.create_svg(prog=DOT_EXE_FILE_PATH)
    # with open("sdg.svg", "wb") as f:
    #     f.write(sdg_svg)
    # 不再创建dot而是直接返回一个SVG
    return sdg_svg


def main(file_list, plcg: nx.DiGraph, project_path):
    print("SDG running...", project_path)
    pointer_parameters, no_parameters = parameters_info(file_list, project_path)

    modified_plcg, pipe_filter_graph = construct_func_level_sdg(plcg, pointer_parameters)
    # save pipe_filter_graph to dot file
    nx.nx_pydot.write_dot(pipe_filter_graph, "temp/temp.dot")
    return export_pipe_filter_dot(modified_plcg, pipe_filter_graph, project_path), pipe_filter_graph

    # nx.nx_pydot.write_dot(pipe_filter_graph, "pipe_filter_graph.dot")


if __name__ == "__main__":
    main()
