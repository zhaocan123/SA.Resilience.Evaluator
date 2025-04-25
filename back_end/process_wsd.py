COMP_PERFORMANCE = 0.2
INTER_PERFORMANCE = 0.2

import re as re

def process_activity(text):

    result_text = ""
    link_format = "\nlink: {} -> {}\n"
    node_format = "\nnode: {}\ntype: {}\nobject: {}\ncomp: {}\nend node\n"

    # re to match nodes
    action_node_pattern = ":[^:><;]+?;"
    send_node_pattern = ":[^:><;]+?>"
    receive_node_pattern = ":[^:><;]+?<"
    start_node_pattern = "start[\s]*\n?"
    stop_node_pattern = "stop[\s]*?"
    node_patterns = "|".join([action_node_pattern,send_node_pattern,receive_node_pattern,start_node_pattern,stop_node_pattern])

    # For if statement
    if_pattern = "if [\s\S]+?\n"
    endif_pattern = "endif[\s]*?\n"
    else_pattern = "elseif[\s\S]+?\n|else[\s\S]*?\n"
    kill_pattern = "kill[\s]*?\n"
    detach_paattern = "detach[\s]*?\n"
    if_statement_patterns = "|".join([if_pattern,endif_pattern,else_pattern,kill_pattern,detach_paattern])

    # For split statement
    split_pattern = "split[\s]*?\n"
    splitagain_pattern = "split again[\s]*?\n"
    endsplit_pattern = "end split[\s]*?\n"
    split_statement_patterns = "|".join([splitagain_pattern,split_pattern,endsplit_pattern])

    # For fork statement
    fork_pattern = "fork[\s]*?\n"
    forkagain_pattern = "fork again[\s]*?\n"
    endfork_pattern = "end fork[\s]*?\n|end merge[\s]*?\n"
    fork_statement_patterns = "|".join([fork_pattern,forkagain_pattern,endfork_pattern])

    # For while statement
    while_pattern = "while[\s\S]+?\n"
    endwhile_pattern = "endwhile[\s\S]*?\n"
    while_statement_patterns = "|".join([while_pattern,endwhile_pattern])

    # For repeat statement
    repeat_pattern = "repeat[\s]*?\n"
    endrepeat_repeat = "repeat while[\s\S]+?\n"
    repeat_statement_patterns = "|".join([repeat_pattern,endrepeat_repeat])

    # join them together
    statements_heads_pattern = "^" + "|^".join([repeat_pattern,while_pattern,fork_pattern,split_pattern,if_pattern])
    plantUML_pattern = "|".join([node_patterns,if_statement_patterns,split_statement_patterns,fork_statement_patterns,while_statement_patterns,repeat_statement_patterns])
    # statement_patterns = "|".join([if_statement_patterns,split_statement_patterns,fork_statement_patterns,while_statement_patterns,repeat_statement_patterns])

    uml_text = re.findall("@startuml[\s\S]+?@enduml",text)
    if len(uml_text) != 1:
        raise ValueError("Invalid plantUML text!")
    else:
        uml_text = "\n".join([line for line in uml_text[0].split("\n")[1:-1] if line.find("title") == -1 and len(re.findall("\|[\s\S]+?\|",line)) == 0]) # 去掉泳道标识，去掉title， 去掉@标记的开始和结束行
        
        links = []
        nodes = re.findall(plantUML_pattern,uml_text)
        def construct_statement(index):
            in_nodes = set([index])
            out_nodes = set([])
            j = index + 1
            haveElse = False
            while j < len(nodes):
                if len(re.findall(statements_heads_pattern,nodes[j])) != 0:# 处理嵌套
                    j = construct_statement(j)
                # if statement
                elif len(re.findall(endif_pattern,nodes[j])) != 0: 
                    if haveElse == False:
                        links.append((index, j))
                    out_nodes.add(j-1)
                    for node in in_nodes:
                        links.append((index-1,node))
                    for node in out_nodes:
                        links.append((node,j))
                    return j
                elif len(re.findall(else_pattern,nodes[j])) != 0: 
                    haveElse = True   
                    in_nodes.add(j)
                    out_nodes.add(j-1)
                # repeat statement
                elif len(re.findall(endrepeat_repeat,nodes[j])) != 0:
                    links.append((index-1,index))
                    links.append((j-1,j))
                    links.append((j,index))
                    return j
                # while statement
                elif len(re.findall(endwhile_pattern,nodes[j])) != 0:
                    links.append((index-1,index))
                    links.append((j-1,j))
                    links.append((j,index))
                    return j
                # split statement # 其实这split和fork可以合并到if语句的处理当中，因为很类似，但是为了好理解我还是分开了
                elif len(re.findall(splitagain_pattern,nodes[j])) != 0:
                    in_nodes.add(j)
                    out_nodes.add(j-1)
                elif len(re.findall(endsplit_pattern,nodes[j])) != 0:
                    out_nodes.add(j-1)
                    for node in in_nodes:
                        links.append((index-1,node))
                    for node in out_nodes:
                        links.append((node,j))
                    return j
                # fork statement 
                elif len(re.findall(forkagain_pattern,nodes[j])) != 0:
                    in_nodes.add(j)
                    out_nodes.add(j-1)
                elif len(re.findall(endfork_pattern,nodes[j])) != 0:
                    out_nodes.add(j-1)
                    for node in in_nodes:
                        links.append((index-1,node))
                    for node in out_nodes:
                        links.append((node,j))
                    return j
                # if node[j] is just a node
                elif len(re.findall(node_patterns,nodes[j])) != 0:
                    links.append((j-1,j))
                j += 1

        index = 0
        while index < len(nodes) - 1:
            old_index = index
            # check if there is a statement
            if len(re.findall(statements_heads_pattern,nodes[index])) != 0: 
                index = construct_statement(index)
            # if next node is a normal node, add a link
            if len(re.findall(node_patterns,nodes[index+1])) != 0:
                # special for while statement!
                if len(re.findall(while_pattern,nodes[old_index])) != 0: 
                    links.append((old_index, index+1))
                else: 
                    links.append((index, index+1))
            index += 1

        # print("links:",links)

    count = 1
    nodenames = []
    for node in nodes:
        if len(re.findall(action_node_pattern,node)) != 0:
            result_text += node_format.format(node[1:-1],"action_node","TODO","TODO")
            nodenames.append(node[1:-1])
        elif len(re.findall(send_node_pattern,node)) != 0:
            result_text += node_format.format(node[1:-1],"send_node","TODO","TODO")
            nodenames.append(node[1:-1])
        elif len(re.findall(receive_node_pattern,node)) != 0:
            result_text += node_format.format(node[1:-1],"receive_node","TODO","TODO")
            nodenames.append(node[1:-1])
        elif len(re.findall(start_node_pattern,node)) != 0:
            result_text += node_format.format(node[0:-1],"start_node","TODO","TODO")
            nodenames.append(node[0:-1])
        elif len(re.findall(stop_node_pattern,node)) != 0:
            result_text += node_format.format(node,"end_node","TODO","TODO")
            nodenames.append(node)
        else:
            result_text += node_format.format(f"statement{count}","statement_node","TODO","TODO")
            nodenames.append(f"statement{count}",)
            count += 1

    for link in links:
        result_text += link_format.format(nodenames[link[0]],nodenames[link[1]])

    return result_text

def process_component(text):
    result_text = ""
    node_format = "\nnode: {}\ntype: {}\nresilience: {}\nperformance: {}\nend node\n"
    link_format = "\nlink: {}\ntype: {}\nnode1: {}\nnode2: {}\nend link\n"

    comp_pattern = "\[[\s\S]+?]\n|component [\s\S]+?\n|\[[\s\S]+?] as [\s\S]+?\n|component \[[\s\S]+?] as [\s\S]+?\n"
    link_pattern = "[^\n]+? --\( [^\n]+?\n|[^\n]+? -- [^\n]+?\n|[^\n]+? \.\.> [^\n]+?\n|[^\n]+? \.\. [^\n]+?\n|[^\n]+? - [^\n]+?\n|[^\n]+? --> [^\n]+?\n"

    nodes = []
    links = []

    uml_text = re.findall("@startuml[\s\S]+?@enduml",text)
    
    if len(uml_text) != 1:
        raise ValueError("Invalid plantUML text!")
    else:
        uml_text = "\n".join([line for line in uml_text[0].split("\n")[1:-1] if line.find("title") == -1 and line != ""]) + "\n"
        comps = re.findall(comp_pattern,uml_text)
        for comp in comps:
            if comp.find("component ") != -1:
                name = comp.split()
                nodes.append([name[1][:-1],"None"])
            elif comp.find(" as ") != -1:
                names = comp.split(" as ")
                nodes.append([names[1][:-1],names[0]])
            else:
                name = comp
                nodes.append([name,"None"])

        for node in nodes:
            result_text += node_format.format(node[0],"component","TODO","TODO")

        comp_nodes_num = len(nodes)

        lines = re.findall(link_pattern,uml_text)
        for line in lines:
            line = line.strip()
            if line.find(' -- ') != -1:
                temp_nodes = line.split(' -- ')
                temp_nodes[0], temp_nodes[1] = temp_nodes[0].strip(), temp_nodes[1].strip()
                is_interface = True
                for node in temp_nodes:
                    is_interface = True
                    for other_node in nodes:
                        if node == other_node[0] or node == other_node[1]:
                            is_interface = False
                    if is_interface:
                        nodes.append([node,"None"])
                links.append(["provide",temp_nodes[0],temp_nodes[1]])
            elif line.find(' - ') != -1:
                temp_nodes = line.split(' - ')
                for node in temp_nodes:
                    is_interface = True
                    for other_node in nodes:
                        if node == other_node[0] or node == other_node[1]:
                            is_interface = False
                    if is_interface:
                        nodes.append([node,"None"])
                links.append(["provide",temp_nodes[0],temp_nodes[1]])
            elif line.find(' ..> ') != -1:
                temp_nodes = line.split(' ..> ')
                for node in temp_nodes:
                    is_interface = True
                    for other_node in nodes:
                        if node == other_node[0] or node == other_node[1]:
                            is_interface = False
                    if is_interface:
                        nodes.append([node,"None"])
                links.append(["depend",temp_nodes[0],temp_nodes[1]])
            elif line.find(' .. ') != -1:
                temp_nodes = line.split(' .. ')
                for node in temp_nodes:
                    is_interface = True
                    for other_node in nodes:
                        if node == other_node[0] or node == other_node[1]:
                            is_interface = False
                    if is_interface:
                        nodes.append([node,"None"])
                links.append(["provide",temp_nodes[0],temp_nodes[1]])
            elif line.find(' --> ') != -1:
                temp_nodes = line.split(' --> ')
                for node in temp_nodes:
                    is_interface = True
                    for other_node in nodes:
                        if node == other_node[0] or node == other_node[1]:
                            is_interface = False
                    if is_interface:
                        nodes.append([node,"None"])
                links.append(["depend",temp_nodes[0],temp_nodes[1]])
            elif line.find(' --( ') != -1:
                temp_nodes = line.split(' --( ')
                for node in temp_nodes:
                    is_interface = True
                    for other_node in nodes:
                        if node == other_node[0] or node == other_node[1]:
                            is_interface = False
                    if is_interface:
                        nodes.append([node,"None"])
                links.append(["depend",temp_nodes[0],temp_nodes[1]])
            else:
                raise TypeError("Invalid link type in UML !")

        for index,node in enumerate(nodes):
            if index >= comp_nodes_num:
                result_text += node_format.format(node[0],"interface","TODO",str(INTER_PERFORMANCE))

        for link in links:
            result_text += link_format.format("",link[0],link[1],link[2])
        return result_text

if __name__ == "__main__":

    # with open("performance_testcases/online_shopping/object/activity.wsd","r") as f:
    #     text = f.read()
    #     result = process_activity(text)
    # with open("performance_testcases/online_shopping/object/activity.txt","w") as f:
    #     f.write(result)

    # with open("performance_testcases/online_shopping/object/comp.wsd","r") as f:
    #     text = f.read()
    #     result = process_component(text)
    # with open("performance_testcases/online_shopping/object/comp.txt","w") as f:
    #     f.write(result)

    # print("Process finished!")

    import os
    # 递归处理指定路径下所有wsd文件
    comp_folder_path = "testcases2"

    def re_process(path):
        print("Processing files in: "+path)
        for file in os.listdir(path):
            if not os.path.isdir(path+"/"+file) and file == "comp.wsd":
                with open(path+"/"+file,'r') as f:
                    text = f.read()
                    result = process_component(text)
                with open(path+"/"+file[:-4]+".txt",'w') as f:
                    f.write(result)
            elif not os.path.isdir(path+"/"+file) and file == "activity.wsd":
                with open(path+"/"+file,'r') as f:
                    text = f.read()
                    result = process_activity(text)
                with open(path+"/"+file[:-4]+".txt",'w') as f:
                    f.write(result)
            elif os.path.isdir(path+"/"+file):
                re_process(path+"/"+file)

    #re_process(comp_folder_path)
    filename = "testcases2/online_shopping_v4/comp.wsd"
    with open(filename,'r') as f:
        text = f.read()
        result = process_component(text)
    with open(filename[:-4]+".txt",'w') as f:
        f.write(result)

