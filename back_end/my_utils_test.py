import codecs
import json
import os
import re
import chardet
import shutil


def filter_directory(file_list, file_header, file_source, expect_file_list):
    file_set = set(file_list)
    header_set = set(file_header)
    source_set = set(file_source)
    file_list_temp = [i for i in file_set if i not in expect_file_list]
    file_header_temp = [i for i in header_set if i not in expect_file_list]
    file_source_temp = [i for i in source_set if i not in expect_file_list]

    return file_list_temp, file_header_temp, file_source_temp


def get_max_depth(file_list):
    max_depth = 0
    max_file = ""
    for file_path in file_list:
        depth = file_path.count("/")
        if depth > max_depth:
            max_depth = depth
            max_file = file_path
    return max_file, max_file.split("/")[-1]


def get_abs_header_path(source_path, header_path):
    if header_path.startswith("./"):
        header_path = header_path[2:]
        source_floder = "/".join(source_path.split("/")[:-1])
        return source_floder + "/" + header_path
    elif header_path.startswith("../"):
        header_floder_level = header_path.count("../")
        tmp_list = source_path.split("/")[:-1]
        if header_floder_level > len(tmp_list):
            raise "include " + header_path + "error!"
        else:
            header_floder = "/".join(tmp_list[:-header_floder_level])
            header_path = header_path.replace("../", "")
            return header_floder + "/" + header_path


def get_info_from_file_dict(file_dict):
    floder_set = set()
    file_list = set()
    other_file_list = []
    for key, value in file_dict.items():
        for file_path in value:
            floder_set.add("/".join(file_path.split("/")[:-1]))
            file_list.add(file_path)
    dir_num = len(floder_set)
    for floder in floder_set:
        for item in os.scandir(floder):
            if item.is_file():
                new_path = item.path.replace("\\", "/")
                if new_path not in file_list:
                    other_file_list.append(new_path)
    return file_dict["source"], file_dict["header"], other_file_list, dir_num


def copy_code_file(code_path, project_path):
    for item in os.scandir(code_path):
        if item.is_dir():
            if not os.path.exists(os.path.join(project_path, item.name)):
                os.makedirs(os.path.join(project_path, item.name))
            copy_code_file(item.path, os.path.join(project_path, item.name))
        elif item.is_file():
            if item.name.endswith(".c") or item.name.endswith(".h"):
                shutil.copy(item.path, os.path.join(project_path, item.name))


def walk_floder(root_path, replace_path):
    floder_list = []
    for item in os.scandir(root_path):
        if item.is_dir():
            floder_dict = {}
            floder_dict["path"] = item.path.replace("\\", "/").replace(replace_path, ".")
            floder_dict["label"] = item.name
            floder_dict["type"] = "folder"
            floder_dict["id"] = item.path.replace("\\", "/").replace(replace_path, ".")
            floder_dict["children"] = walk_floder(item.path, replace_path)
            floder_list.append(floder_dict)
        elif item.is_file():
            if item.name.endswith(".c") or item.name.endswith(".h"):
                floder_dict = {}
                floder_dict["path"] = item.path.replace("\\", "/").replace(replace_path, ".")
                floder_dict["label"] = item.name
                floder_dict["type"] = "file"
                floder_dict["id"] = item.path.replace("\\", "/").replace(replace_path, ".")
                floder_list.append(floder_dict)
    return floder_list


def find_code_file(root_path, begin_flag, replace_path, code_dict, includes_list):
    for item in os.scandir(root_path):
        if item.is_dir():
            begin_flag += 1
            find_code_file(item.path, begin_flag, replace_path, code_dict, includes_list)
        if item.is_file():
            if item.name.endswith(".c") or item.name.endswith(".h"):
                file_rpath = item.path.replace("\\", "/").replace(replace_path, ".")
                floder_path = "/".join(file_rpath.split("/")[:-1])
                if item.name not in code_dict:
                    if floder_path not in includes_list:
                        code_dict[item.name] = [(file_rpath, begin_flag, 1)]
                    else:
                        code_dict[item.name] = [(file_rpath, begin_flag, 0)]  # 优先选择在包含目录里的
                else:
                    if floder_path not in includes_list:
                        code_dict[item.name].append((file_rpath, begin_flag, 1))
                    else:
                        code_dict[item.name].append((file_rpath, begin_flag, 0))
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


# 这样添加宏没有考虑到条件引用，不能使用content[key]["fan_out_self"] == []进行判断
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
            if key.endswith(".h"):
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
            if file_i.endswith(".c") or file_i.endswith(".h"):
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
                with codecs.open(file_path, "rb", encoding=file_encoding, errors="ignore") as f:
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
                            if "/" in include_path:
                                new_file_lines.append(line)
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


if __name__ == "__main__":
    # line = "#if !definded(  STM32F405xx ) && !defdined   (STM32F415xx ) && !defdined (__STM32F407xx) &&"
    # pattern = re.compile(r'.defined[\s]*\([\s]*(\w*)[\s]*\)')
    # tmp = pattern.findall(line)
    # for i in tmp:
    #     if i is not None:
    #         print(i)
    import zipfile
    zip_file_path = r"D:\Code\test_project\test_imu_re\test_xg.zip"
    code_path = r'D:\Code\test_project\test_imu_re\code'
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        # 解压后如果是文件直接在code目录，如果是文件夹则在code目录下一个文件夹展开
        zip_ref.extractall(code_path)
    includes_list = []
    if os.path.exists(code_path+"/excluded_path.txt"):
        replace_dir = []
        for item in os.scandir(code_path):
            if item.is_dir():
                replace_dir.append(item.name)
        if len(replace_dir) > 1:
            raise Exception("压缩包中存在多个项目文件夹，不符合要求！")
        with open(code_path+"/excluded_path.txt", "r") as f:
            while True:
                line = f.readline()
                if not line:
                    break
                line = line.strip().strip("\n")
                if line != "":
                    if len(replace_dir) == 1:
                        line = line.replace("\\", "/")
                        line = line.replace(".", "./" + replace_dir[0])
                    else:
                        line = line.replace("\\", "/")
                    if line[-1] == "/":
                        line = line[:-1]
                    includes_list.append(line)
    rewrite_file(code_path, 'D:/Code/test_project/test_imu_re', includes_list)
    add_micro_define(code_path, 'D:/Code/test_project/test_imu_re')
    # if os.path.exists(code_path + "/micro_define.txt"):
    #     print("yes")
