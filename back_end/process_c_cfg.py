import networkx as nx
import sys
import re
import os
import json

pwd = os.getcwd()
pwd = pwd.replace("\\", "/")
print("process_c_cfg.py: pwd = ", pwd)
with open(pwd + "/config.json", "r", encoding="utf-8") as f:
    content = json.load(f)
DOT_EXE_FILE_PATH = content["DOT_EXE_FILE_PATH"]

replace_table = {
    "((void *)0)": "NULL",
    "(__acrt_iob_func(2))": "stderr",
    "(__iob_func(2))": "stderr",
    "(__acrt_iob_func(1))": "stdout",
    "(__iob_func(1))": "stdout",
    "(__acrt_iob_func(0))": "stdin",
    "(__iob_func(0))": "stdin",
    "__acrt_iob_func(2)": "stderr",
    "__iob_func(2)": "stderr",
    "__acrt_iob_func(1)": "stdout",
    "__iob_func(1)": "stdout",
    "__acrt_iob_func(0)": "stdin",
    "__iob_func(0)": "stdin",
    "_Bool ": "bool ",
}


def process_cfg(G: nx.DiGraph):
    nodes_results = dict()
    two_succ_edges_info = dict()
    block_to_id_dict = dict()
    labels = dict()
    for id in G.nodes:
        if 'Node' in id:
            label = G.nodes[id]['label']
            # print(label)
            if len(label) > 2:
                processed_label = label.strip('"').strip('{ ').strip('}')[
                    :-2].replace('\l', '\l ', 1).replace("(Unreachable)","")
                re_exp = r'\\[l][\s]*\w+:|\\[l][\s]*case[\s]+.*?:'
                # re_exp = r'\\[l][\s]*[0-9]+:|\\[l][\s]*T:|\\[l][\s]*default:|\\[l][\s]*case[\s]+.*?:|\\[l][\s]*fail:|\\[l][\s]*cleanup:|\\[l][\s]*out:|\\[l][\s]*nomem:'
                pred_re_exp = r'Preds \([0-9]+\):[ B[0-9]+]*'
                succ_re_exp = r'Succs \([0-9]+\):[ B[0-9]+]*'
                pred_matches = re.findall(pred_re_exp, processed_label)
                succ_matches = re.findall(succ_re_exp, processed_label)
                for pm in pred_matches:
                    processed_label = processed_label.replace(pm, "").strip()
                for sm in succ_matches:
                    processed_label = processed_label.replace(sm, "").strip()
                line_heads = re.findall(re_exp, processed_label)
                line_conts = re.split(re_exp, processed_label)
                lines = [line_conts[0].replace('\\l', '')] + [
                    line_heads[i].replace('\\l', '').strip() + line_conts[i + 1].replace('\\l', '') for i in range(len(line_heads))]
                result_dict = dict()
                header = None

                def replace_stmt(str):
                    flag = False
                    location = -1
                    if "(ImplicitCastExpr" in str:
                        str = str[:str.find("(ImplicitCastExpr")]
                    if "(CStyleCastExpr" in str:
                        str = str[:str.find("(CStyleCastExpr")]
                    if '[' + header in str:
                        flag = True
                        while flag:
                            flag = False
                            for rkey in result_dict.keys():
                                if '[' + rkey + ']' in str:
                                    str = str.replace(
                                        '[' + rkey + ']', result_dict[rkey][0])
                                    if result_dict[rkey][2] != -1:
                                        location = result_dict[rkey][2]
                                    result_dict[rkey][1] = 1
                            for rkey in result_dict.keys():
                                if '[' + rkey + ']' in str:
                                    flag = True
                                    break
                        return str.strip(), location
                    else:
                        return str.strip(), location

                for line in lines:
                    line = line.strip()
                    if ':' in line:
                        idx = line.find(':')
                        line_label = line[:idx]
                        line_cont = line[idx + 1:]
                        temp_index = line_cont.find('\\|\\|')
                        source_loc = -1
                        if temp_index != -1 and line_label != "T":
                            # print(line_label, line_cont.split(':'))
                            source_loc = int(line_cont.split(':')[2])
                            line_cont = line_cont[temp_index+len('\\|\\|'):]
                        if len(line_cont.strip()) < 1:
                            cont, location = replace_stmt(line_label.strip())
                            if source_loc == -1 and location != -1:
                                source_loc = location
                            result_dict['condition'] = [cont, 1, source_loc]
                        else:
                            cont, location = replace_stmt(line_cont.strip())
                            if source_loc == -1 and location != -1:
                                source_loc = location
                            result_dict[header + '.' +
                                        line_label.strip()] = [cont, 0, source_loc]
                            labels['[' + header + '.' +line_label.strip() + ']'] = cont

                    elif len(line) > 1:
                        header_text = line.strip()
                        if '(' in header_text and ')' in header_text and "ENTRY" not in header_text and "EXIT" not in header_text:
                            start_index = header_text.find('(')
                            end_index = header_text.find(')')
                            header_text = header_text[:start_index].strip(
                            ) + header_text[end_index:+1].strip()
                        header = header_text.strip(',').strip('[').strip(']')
                        result_dict["BLOCK"] = [header, 1, -1]
                nodes_results[id] = result_dict
                re_header_id = r'B[0-9]+'
                header_id = re.findall(re_header_id, header)[0]
                block_to_id_dict[header_id] = id
                if len(succ_matches) == 1:
                    sm = succ_matches[0]
                    re_su_count = r'\([0-9]+\):'
                    su_count = re.findall(re_su_count, sm)[0]
                    su_count = int(su_count.strip(":").strip("(").strip(")"))
                    if su_count == 2:
                        re_su_id = r' B[0-9]+'
                        succs = re.findall(re_su_id, sm)
                        if len(succs) == 2:
                            two_succ_edges_info[id] = {"true":succs[0].strip(), "false":succs[1].strip()}
    for key in two_succ_edges_info:
        try:
            G.edges[key, block_to_id_dict[two_succ_edges_info[key]["true"]]]['label'] = '\"' + ' ' + "true" + '\"'
        except KeyError:
            print(f"unreachable true edge {key}!")
        try:
            G.edges[key, block_to_id_dict[two_succ_edges_info[key]["false"]]]['label'] = '\"' + ' ' + "false" + '\"'
        except KeyError:
            print(f"unreachable false edge {key}!")

    for id in list(G.nodes).copy():
        if 'Node' in id:
            result_dict = nodes_results[id]
            header = result_dict["BLOCK"][0]
            sub_blocks = list()
            result = '"{' + header + '\l'
            source_location = -1
            for key, value in result_dict.items():
                if value[2] != -1:
                    source_location = value[2]
                if value[1] == 0 and (
                        ' ' in value[0] or '(' in value[0] or ')' in value[0] or '+' in value[0] or '-' in value[
                            0] or '*' in value[0] or '/' in value[0] or '%' in value[0]):
                    try:
                        if value[0] in result_dict[header + '.' + str(int(key[key.find('.') + 1:]) + 1)][0]:
                            bug_flag = 1
                        else:
                            bug_flag = 0
                    except:
                        bug_flag = 0

                    if bug_flag == 0:
                        value_str = value[0]
                        for k, v in labels.items():
                            if k in value_str:
                                value_str = value_str.replace(k, v)
                                for node_k, node_v in nodes_results.items():
                                    try:
                                        node_v[k.strip("[").strip("]")][1] = 1
                                    except KeyError:
                                        pass
                        if 'T' not in key:
                            if value_str.strip()[-1] != ";":
                                value_str = value_str + ";"
                            for replace_key, replace_value in replace_table.items():
                                if replace_key in value_str:
                                    value_str = value_str.replace(
                                        replace_key, replace_value)
                            if value_str.startswith("_wassert("):
                                value_str = "assert()"
                            if value_str.startswith("... , 0"):
                                continue
                            if value_str.startswith("(void)((!!") and value_str.endswith("\|\| (... , 0));"):
                                continue
                            if value_str.startswith("... ,"):
                                value_str = value_str.replace("... ,", "")
                            result += value_str + '\l'
                            sub_blocks.append((value_str, value[2]))
                        else:
                            if value_str.endswith("&& ...") or value_str.endswith("|| ...") or value_str.endswith(
                                    "\|\| ..."):
                                value_str = "if" + value_str
                            value_str = value_str.replace("&& ...", "").replace("|| ...", "").replace("\|\| ...",
                                                                                                      "").replace("?",
                                                                                                                  "").replace(
                                ":", "").replace("...", "").replace(";", "")
                            condition_ops = [
                                "if", "while", "do  while", "switch"]
                            op_count = 0
                            for op in condition_ops:
                                if value_str.find(op) != -1:
                                    value_str = op + \
                                        "(" + \
                                        value_str[value_str.find(
                                            op) + len(op):] + ")"
                                    break
                                op_count += 1
                            if op_count == 4 and "for" not in value_str:
                                value_str = "(" + value_str + ")"
                            for replace_key, replace_value in replace_table.items():
                                if replace_key in value_str:
                                    value_str = value_str.replace(
                                        replace_key, replace_value)
                            result += value_str + '\l'
                            sub_blocks.append((value_str, value[2]))
                            for edge in list(G.edges).copy():
                                if edge[0] == id:
                                    try:
                                        condition = nodes_results[edge[1]]['condition'][0]
                                    except KeyError:
                                        if 'switch ' in value_str:
                                            condition = "default"
                                        else:
                                            try:
                                                condition = G.edges[edge[0], edge[1]]['label'].replace('"','').strip()
                                            except KeyError:
                                                condition = ""
                                    edge_label = '\"' + ' ' + str(condition) + '\"'
                                    G.edges[edge[0], edge[1]]['label'] = edge_label
                elif value[1] == 1 and '.' in key and ".T" not in key:
                    count = int(key.split('.')[1])
                    flag = True
                    for ck in result_dict.keys():
                        if ".T" in ck:
                            flag = False
                            break
                        if '.' in ck and ".T" not in ck:
                            if int(ck.split('.')[1]) > count:
                                flag = False
                                break
                    if value[0].startswith("... , 0"):
                        flag = False
                    if flag:
                        result += value[0] + '\l'
            result += '}"'
            if len(sub_blocks) <= 1:
                G.nodes[id]['label'] = result
                G.nodes[id]['sourceLoc'] = source_location
            else:
                for index, (block, sourceLoc) in enumerate(sub_blocks):
                    new_node = f"{header}-{index}"
                    G.add_node(
                        new_node, label='"{' + new_node + '\l' + block + '}"', shape="record", sourceLoc = sourceLoc)
                    if index > 0:
                        G.add_edge(f"{header}-{index - 1}", new_node)
                for edge in list(G.edges).copy():
                    if edge[1] == id:
                        G.add_edge(edge[0], f"{header}-{0}")
                        try:
                            G.edges[edge[0],f"{header}-{0}"]['label'] = G.edges[edge[0], edge[1]]['label']
                        except KeyError:
                            pass
                        G.remove_edge(edge[0], edge[1])
                    if edge[0] == id:
                        G.add_edge(f"{header}-{len(sub_blocks) - 1}", edge[1])
                        try:
                            G.edges[f"{header}-{len(sub_blocks) - 1}", edge[1]]['label'] = G.edges[edge[0], edge[1]]['label']
                        except KeyError:
                            pass
                        G.remove_edge(edge[0], edge[1])
                G.remove_node(id)

    if "\\n" in G.nodes:
        G.remove_node("\\n")
    return G

if __name__ == "__main__":
    # file_path = sys.argv[1]
    ucfg = nx.DiGraph(nx.nx_pydot.read_dot("C:/Users/user/AppData/Local/Temp/CFG-931bd6.dot"))
    process_cfg(ucfg)
