import xml.dom.minidom
import codecs
import json
import os
import re
import chardet
TYPELIST = (".c", ".C", ".cc", ".CC", ".cp", ".c++", ".C++", ".cxx", ".cpp", ".CPP", ".CXX", ".h", ".H", ".hh", ".hpp", ".hxx")
HEARDERTYPE = (".h", ".H", ".hh", ".hpp", ".hxx")


def walk_floder(root_path, replace_path, uvprojx_path):
    floder_list = []
    for item in os.scandir(root_path):
        if item.is_dir():
            floder_dict = {}
            floder_dict["path"] = item.path.replace("\\", "/").replace(replace_path, ".")
            floder_dict["label"] = item.name
            floder_dict["type"] = "folder"
            floder_dict["id"] = item.path.replace("\\", "/").replace(replace_path, ".")
            floder_dict["children"] = walk_floder(item.path, replace_path, uvprojx_path)
            floder_list.append(floder_dict)
        elif item.is_file():
            if item.name.endswith(TYPELIST):
                floder_dict = {}
                floder_dict["path"] = item.path.replace("\\", "/").replace(replace_path, ".")
                floder_dict["label"] = item.name
                floder_dict["type"] = "file"
                floder_dict["id"] = item.path.replace("\\", "/").replace(replace_path, ".")
                floder_list.append(floder_dict)
            elif item.name.endswith(".uvprojx"):
                uvprojx_path.append(item.path.replace("\\", "/"))
    return floder_list


def find_code_file(root_path, begin_flag, replace_path, code_dict, includes_list):
    for item in os.scandir(root_path):
        if item.is_dir():
            begin_flag += 1
            find_code_file(item.path, begin_flag, replace_path, code_dict, includes_list)
        if item.is_file():
            if item.name.endswith(TYPELIST):
                file_rpath = item.path.replace("\\", "/").replace(replace_path, ".")
                floder_path = "/".join(file_rpath.split("/")[:-1])
                if item.name not in code_dict:
                    if floder_path not in includes_list:
                        code_dict[item.name] = [(file_rpath, begin_flag, 0)]  # 0表示不在exclude_list中，优先使用
                    else:
                        code_dict[item.name] = [(file_rpath, begin_flag, 1)]
                else:
                    if floder_path not in includes_list:
                        code_dict[item.name].append((file_rpath, begin_flag, 0))
                    else:
                        code_dict[item.name].append((file_rpath, begin_flag, 1))
    return None


def get_new_include(s_file_path, t_file_path):
    """
    获取新的include
    :param s_file_path: 当前文件路径
    :param t_file_path: 查找到的include文件路径
    :return: 新的include路径
    """
    s_path_list = s_file_path.split("/")
    t_path_list = t_file_path.split("/")
    i = 0
    while i < len(s_path_list) - 1 and i < len(t_path_list) - 1:
        if s_path_list[i] == t_path_list[i]:
            i += 1
        else:
            break
    if i == len(s_path_list) - 1:
        new_include = "./"
        new_path = t_path_list[i:]
        new_include += "/".join(new_path)
        return new_include
    else:
        new_include = "../" * (len(s_path_list) - i - 1)
        new_path = t_path_list[i:]
        new_include += "/".join(new_path)
        return new_include


def add_micro_define(project_path, project_data_path):
    micro_list = []
    if os.path.exists(project_path + "/macro_define.txt"):
        with open(project_path + "/macro_define.txt", "r") as f:
            line_list = f.readlines()
        for line in line_list:
            line = line.strip()
            if line != "":
                micro_list.append(line)
        with open(project_data_path + "/fan_dict.json", "r", encoding="utf-8") as f:
            content = dict(json.load(f))
        for key in content.keys():
            if key.endswith(HEARDERTYPE):
                # 顶层头文件
                if not os.path.exists(key):
                    continue
                add_line = []
                for micro in micro_list:
                    if micro in content[key]["macro_used"]:
                        add_line.append("#ifndef " + micro + "\n")
                        add_line.append("#define " + micro + "\n")
                        add_line.append("#endif \n")
                if len(add_line) > 0:
                    with open(key, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                    with open(key, "w", encoding="utf-8") as f:
                        for line in add_line:
                            f.write(line)
                        f.writelines(lines)
                    print("add macro define in " + key)


def deal_macro_include(line):
    # HEARDERTYPE = (".h", ".H", ".hh", ".hpp", ".hxx")
    tmp = re.search(r'#define\s+\w+\s+\"\w+.(h|hh|H|hpp|hxx)\"', line)
    if tmp:
        # 如果本身就是相对路径，就不用改了
        txt = tmp.group(0)
        begin = txt.find("\"")
        end = txt.rfind("\"")
        include_txt = txt[begin + 1:end].replace("\\", "/")
        if "/" in include_txt:
            return include_txt, 0
        else:
            return include_txt, 1
    else:
        return line, -1


def rewrite_file(project_path, project_data_path, includes_list):
    code_dict = {}
    project_path = project_path.replace("\\", "/")
    if project_path.endswith("/"):
        project_path = project_path[:-1]
    find_code_file(project_path, 0, project_path, code_dict, includes_list)
    fan_dict = {}
    pattern = re.compile(r'.defined[\s]*\([\s]*(\w*)[\s]*\)')
    ifn_pattern = re.compile(r'.ifndef[\s]*(\w*)[\s]*')
    ifdef_pattern = re.compile(r'.ifdef[\s]*(\w*)[\s]*')
    for root, dirs, files in os.walk(project_path):
        for file_i in files:
            if file_i.endswith(TYPELIST):
                file_path = os.path.join(root, file_i).replace("\\", "/").replace("//", "/")
                file_encoding = chardet.detect(open(file_path, "rb").read())["encoding"]
                if file_encoding == "GB2312":
                    file_encoding = "GBK"
                print(file_path, file_encoding)
                # if file_path.endswith("main.c"):
                #     print("yes")
                lines = None
                if file_path not in fan_dict:
                    fan_dict[file_path] = {"fan_in_self": [], "fan_out_self": [], "fan_in_lib": [], "fan_out_lib": [], "macro_used": []}  # fan_in: 该文件被哪些文件包含，fan_out: 该文件包含哪些文件
                with codecs.open(file_path, "r", encoding=file_encoding, errors="ignore") as f:
                    lines = f.readlines()
                new_file_lines = []
                for line in lines:
                    # #ifdef判断
                    tmp = ifdef_pattern.findall(line.replace("\t", " "))
                    fan_dict[file_path]["macro_used"].extend(tmp)
                    # ifndef判断
                    tmp = ifn_pattern.findall(line.replace("\t", " "))
                    fan_dict[file_path]["macro_used"].extend(tmp)
                    # #if判断
                    tmp = pattern.findall(line.replace("\t", " "))
                    fan_dict[file_path]["macro_used"].extend(tmp)
                    # include判断
                    if line.strip().startswith("#include"):
                        tmp = re.search(r'(<|").*("|>)', line)
                        if tmp:
                            # 如果本身就是相对路径，就不用改了
                            include_path = tmp.group(0)[1:-1]
                            include_path = include_path.replace("\\", "/")
                            include_file = include_path.split("/")[-1]
                            # if include_file == "game.h":
                            #     print("yes")
                            if "/" in include_path and os.path.exists(os.path.join(root, include_path)):
                                # 判断自带的引用路径是否正确
                                # 如果是相对路径，判断引用符号是引号还是尖括号
                                if tmp.group(0)[0] == "<":
                                    # 尖括号替换为引号
                                    new_file_lines.append(line.replace("<", '"').replace(">", '"'))
                                else:
                                    new_file_lines.append(line)
                                # new_file_lines.append(line)
                                if include_file in code_dict:
                                    real_path = os.path.abspath(os.path.join(root, include_path)).replace("\\", "/").replace("//", "/")
                                    fan_dict[file_path]["fan_out_self"].append(real_path)
                                    if real_path not in fan_dict:
                                        fan_dict[real_path] = {"fan_in_self": [file_path], "fan_out_self": [], "fan_in_lib": [], "fan_out_lib": [], "macro_used": []}
                                    else:
                                        fan_dict[real_path]["fan_in_self"].append(file_path)
                                else:
                                    fan_dict[file_path]["fan_out_lib"].append(include_path)
                                continue
                            else:
                                if include_file in code_dict:
                                    s_floder_flag = 0
                                    tmp_source_file = code_dict[file_i]
                                    now_code = file_path.replace(project_path, ".")
                                    # 取出当前文件的文件夹索引
                                    for file_s in tmp_source_file:
                                        if file_s[0] == now_code:
                                            s_floder_flag = file_s[1]
                                            break
                                    tmp_target_file = code_dict[include_file]
                                    # 排序，优先找x[2]为1的，即在include_list中的
                                    # 在include_list中的，优先找目录近的
                                    tmp_space_list = [(i[0], abs(i[1] - s_floder_flag), i[2]) for i in tmp_target_file]
                                    stored_list = sorted(tmp_space_list, key=lambda x: (x[2], x[1]))
                                    now_include = stored_list[0][0]
                                    # now_include = tmp_target_file[tmp_space_list.index(min(tmp_space_list))][0]
                                    new_include = get_new_include(now_code, now_include)
                                    new_line = line.replace(include_path, new_include)
                                    # 如果引用是尖括号，替换为引号
                                    if tmp.group(0)[0] == "<":
                                        new_line = new_line.replace("<", '"').replace(">", '"')
                                        new_file_lines.append(new_line)
                                    else:
                                        new_file_lines.append(new_line)
                                    new_real_include = os.path.abspath(os.path.join(root, new_include)).replace("\\", "/").replace("//", "/")
                                    fan_dict[file_path]["fan_out_self"].append(new_real_include)
                                    if new_real_include not in fan_dict:
                                        fan_dict[new_real_include] = {"fan_in_self": [file_path], "fan_out_self": [], "fan_in_lib": [], "fan_out_lib": [], "macro_used": []}
                                    else:
                                        fan_dict[new_real_include]["fan_in_self"].append(file_path)
                                else:
                                    new_file_lines.append(line)
                                    fan_dict[file_path]["fan_out_lib"].append(include_path)
                        else:
                            new_file_lines.append(line)
                    elif line.strip().startswith("#define"):
                        txt, deal_flag = deal_macro_include(line.strip())
                        if deal_flag == -1:
                            new_file_lines.append(line)
                        elif deal_flag == 0:
                            file_name = txt.split("/")[-1]
                            if file_name in code_dict:
                                tmp_path = code_dict[file_name][0][0].replace("./", project_path + "/")
                                line = line.replace(txt, tmp_path)
                                new_file_lines.append(line)
                            else:
                                new_file_lines.append(line)
                        else:
                            if txt in code_dict:
                                tmp_path = code_dict[txt][0][0].replace("./", project_path + "/")
                                line = line.replace(txt, tmp_path)
                                new_file_lines.append(line)
                            else:
                                new_file_lines.append(line)
                    else:
                        new_file_lines.append(line)
                with codecs.open(file_path, "w", encoding="utf-8") as f:
                    f.writelines(new_file_lines)
    for key in fan_dict.keys():
        fan_dict[key]["fan_in_self"] = list(set(fan_dict[key]["fan_in_self"]))
        fan_dict[key]["fan_out_self"] = list(set(fan_dict[key]["fan_out_self"]))
        fan_dict[key]["fan_in_lib"] = list(set(fan_dict[key]["fan_in_lib"]))
        fan_dict[key]["fan_out_lib"] = list(set(fan_dict[key]["fan_out_lib"]))
        fan_dict[key]["macro_used"] = list(set(fan_dict[key]["macro_used"]))
    with open(project_data_path + "/fan_dict.json", "w") as f:
        json.dump(fan_dict, f, indent=4, ensure_ascii=False)
    return code_dict


def get_pro_files(projx_path, replace_path, code_dict):
    tmp_list = []
    floder_path = "/".join(os.path.abspath(projx_path).replace("\\", "/").split("/")[:-1])
    dom = xml.dom.minidom.parse(projx_path)
    Group_list = dom.getElementsByTagName('Group')
    for group in Group_list:
        file_list = group.getElementsByTagName('FilePath')
        for file in file_list:
            filePath = file.childNodes[0].data
            if filePath.endswith(TYPELIST):
                tmp_path = os.path.abspath(os.path.join(floder_path, filePath))
                if os.path.exists(tmp_path):
                    tmp_list.append(tmp_path.replace("\\", "/").replace(replace_path, "."))
                else:
                    file_name = filePath.replace("\\", "/").split("/")[-1]
                    if file_name in code_dict:
                        tmp_list.append(code_dict[file_name][0][0])
    return tmp_list


# def rewrite_file(project_path):
#     code_dict = {}
#     project_path = project_path.replace("\\", "/")
#     if project_path.endswith("/"):
#         project_path = project_path[:-1]
#     find_code_file(project_path, 0, project_path, code_dict)
#     for root, dirs, files in os.walk(project_path):
#         for file_i in files:
#             if file_i.endswith(TYPELIST):
#                 file_path = os.path.join(root, file_i).replace("\\", "/")
#                 file_encoding = chardet.detect(open(file_path, "rb").read())["encoding"]
#                 if file_encoding == "GB2312":
#                     file_encoding = "GBK"
#                 print(file_path, file_encoding)
#                 lines = None
#                 with codecs.open(file_path, "rb", encoding=file_encoding) as f:
#                     lines = f.readlines()
#                 new_file_lines = []
#                 for line in lines:
#                     if line.strip().startswith("#include"):
#                         tmp = re.search(r'(<|").*("|>)', line)
#                         if tmp:
#                             # 如果本身就是相对路径，就不用改了
#                             if "/" in tmp.group(0)[1:-1]:
#                                 new_file_lines.append(line)
#                                 continue
#                             include_path = tmp.group(0)[1:-1]
#                             include_file = include_path.split("/")[-1]
#                             if include_file in code_dict:
#                                 s_floder_flag = 0
#                                 tmp_source_file = code_dict[file_i]
#                                 now_code = file_path.replace(project_path, ".")
#                                 for file_s in tmp_source_file:
#                                     if file_s[0] == now_code:
#                                         s_floder_flag = file_s[1]
#                                         break
#                                 tmp_target_file = code_dict[include_file]
#                                 tmp_space_list = [abs(i[1] - s_floder_flag) for i in tmp_target_file]
#                                 now_include = tmp_target_file[tmp_space_list.index(min(tmp_space_list))][0]
#                                 new_include = get_new_include(now_code, now_include)
#                                 new_line = line.replace(include_path, new_include)
#                                 new_file_lines.append(new_line)
#                             else:
#                                 new_file_lines.append(line)
#                         else:
#                             new_file_lines.append(line)
#                     else:
#                         new_file_lines.append(line)
#                 os.chmod(file_path, 0o777)
#                 with codecs.open(file_path, "w", encoding="utf-8") as f:
#                     f.writelines(new_file_lines)


if __name__ == "__main__":
    # tmp = walk_floder(r'D:\Code\test_project\CUnit_all', 0, 'D:/Code/test_project/CUnit_all')
    # print(tmp)

    # code_dict = {}
    # find_code_file(r'D:\Code\test_project\CUnit_all', 0, 'D:/Code/test_project/CUnit_all', code_dict)
    # print(code_dict)

    # print(get_new_include('./Sources/Test1/Console/Console.c', './Sources/Test1/Console/Test2/test_cunit.h'))
    # print(get_new_include('./Sources/Test1/Console/Console.c', './Sources/Test/test_cunit.h'))
    rewrite_file(r'D:\Code\test_project\xg_test')
