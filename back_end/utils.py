# import pymongo
import json
import sys
import codecs
import re
import os
import chardet


g_DictSymbols = {'"': '"', '/*': '*/', '//': '\n'}
# 判断dictSymbols的key中，最先出现的符号是哪个，并返回其所在位置以及该符号


def get1stSymPos(s, fromPos=0):
    listPos = []  # 位置,符号
    for b in g_DictSymbols:
        pos = s.find(b, fromPos)
        listPos.append((pos, b))  # 插入位置以及结束符号
    minIndex = -1  # 最小位置在listPos中的索引
    index = 0  # 索引
    while index < len(listPos):
        pos = listPos[index][0]  # 位置
        if minIndex < 0 and pos >= 0:  # 第一个非负位置
            minIndex = index
        if 0 <= pos < listPos[minIndex][0]:  # 后面出现的更靠前的位置
            minIndex = index
        index = index+1
    if minIndex == -1:  # 没找到
        return (-1, None)
    else:
        return (listPos[minIndex])


def code_comment_line(code_text: list):
    code_flag_list = [[text, 0] for text in code_text]
    comment_text = []
    code_text = []
    for i in range(len(code_flag_list)):
        if i == 0 or code_flag_list[i-1][1] == 0:
            fromPos = 0
            s = code_flag_list[i][0]
            while (fromPos < len(s)):
                result = get1stSymPos(s, fromPos)
                # logging.info(result)
                if result[0] == -1:  # 没有符号了
                    code_text.append((s, i))
                    s = s.replace(s, '', 1)
                else:
                    endPos = s.find(g_DictSymbols[result[1]], result[0]+len(result[1]))
                    if result[1] == '//':  # 单行注释
                        if endPos == -1:  # 没有换行符也可以
                            endPos = len(s)
                            code_flag_list[i][1] = 0
                        comment_text.append((s[result[0]:endPos], i))
                        s = s.replace(s[result[0]:endPos], '', 1)
                        fromPos = result[0]
                    elif result[1] == '/*':  # 区块注释
                        if endPos == -1:  # 区块注释没有结束
                            code_flag_list[i][1] = 1
                            fromPos = len(s)
                            comment_text.append((s[result[0]:], i))
                            s = s.replace(s[result[0]:], '', 1)
                        else:
                            comment_text.append((s[result[0]:endPos+2], i))
                            s = s.replace(s[result[0]:endPos+2], '', 1)
                            fromPos = result[0]
                    else:  # 字符串
                        if endPos == -1:  # 字符串没有结束
                            code_flag_list[i][1] = 2
                            fromPos = len(s)
                        else:
                            fromPos = endPos + len(g_DictSymbols[result[1]])
            if s != '':
                code_text.append((s, i))
        elif code_flag_list[i-1][1] == 1:  # 找块注释结束
            s = code_flag_list[i][0]
            fromPos = 0
            endPos = s.find('*/', fromPos)
            if endPos == -1:  # 没有结束符就报错
                code_flag_list[i][1] = 1
                fromPos = len(s)
                comment_text.append((s, i))
                s = s.replace(s, '', 1)
            else:
                comment_text.append((s[fromPos:endPos+2], i))
                s = s.replace(s[fromPos:endPos+2], '', 1)
                fromPos = 0
                code_flag_list[i][1] = 0
                while (fromPos < len(s)):
                    result = get1stSymPos(s, fromPos)
                    # logging.info(result)
                    if result[0] == -1:  # 没有符号了
                        code_text.append((s, i))
                        s = s.replace(s, '', 1)
                    else:
                        endPos = s.find(g_DictSymbols[result[1]], result[0]+len(result[1]))
                        if result[1] == '//':  # 单行注释
                            if endPos == -1:  # 没有换行符也可以
                                endPos = len(s)
                                code_flag_list[i][1] = 0
                            comment_text.append((s[result[0]:endPos], i))
                            s = s.replace(s[result[0]:endPos], '', 1)
                            fromPos = result[0]
                        elif result[1] == '/*':  # 区块注释
                            if endPos == -1:  # 区块注释没有结束
                                code_flag_list[i][1] = 1
                                fromPos = len(s)
                                comment_text.append((s[result[0]:], i))
                                s = s.replace(s[result[0]:], '', 1)
                            else:
                                comment_text.append((s[result[0]:endPos+2], i))
                                s = s.replace(s[result[0]:endPos+2], '', 1)
                                fromPos = result[0]
                        else:  # 字符串
                            if endPos == -1:  # 字符串没有结束
                                code_flag_list[i][1] = 2
                                fromPos = len(s)
                            else:
                                fromPos = endPos + len(g_DictSymbols[result[1]])
                if s != '':
                    code_text.append((s, i))
        elif code_flag_list[i-1][1] == 2:  # 找字符串结束
            s = code_flag_list[i][0]
            fromPos = 0
            endPos = s.find('"', fromPos)
            if endPos == -1:  # 字符没有结束
                code_flag_list[i][1] = 2
                fromPos = len(s)
                code_text.append((s, i))
            else:
                code_text.append((s[fromPos:endPos+1], i))
                s = s.replace(s[fromPos:endPos+1], '', 1)
                fromPos = 0
                code_flag_list[i][1] = 0
                while (fromPos < len(s)):
                    result = get1stSymPos(s, fromPos)
                    # logging.info(result)
                    if result[0] == -1:  # 没有符号了
                        code_text.append((s, i))
                        s = s.replace(s, '', 1)
                    else:
                        endPos = s.find(g_DictSymbols[result[1]], result[0]+len(result[1]))
                        if result[1] == '//':  # 单行注释
                            if endPos == -1:  # 没有换行符也可以
                                endPos = len(s)
                                code_flag_list[i][1] = 0
                            comment_text.append((s[result[0]:endPos], i))
                            s = s.replace(s[result[0]:endPos], '', 1)
                            fromPos = result[0]
                        elif result[1] == '/*':  # 区块注释
                            if endPos == -1:  # 区块注释没有结束
                                code_flag_list[i][1] = 1
                                fromPos = len(s)
                                comment_text.append((s[result[0]:], i))
                                s = s.replace(s[result[0]:], '', 1)
                            else:
                                comment_text.append((s[result[0]:endPos+2], i))
                                s = s.replace(s[result[0]:endPos+2], '', 1)
                                fromPos = result[0]
                        else:  # 字符串
                            if endPos == -1:  # 字符串没有结束
                                code_flag_list[i][1] = 2
                                fromPos = len(s)
                            else:
                                fromPos = endPos + len(g_DictSymbols[result[1]])
                if s != '':
                    code_text.append((s, i))
    comment_lines = set([j for (i, j) in comment_text])
    code_rst = []
    blank_code = []
    for code, line in code_text:
        if line in comment_lines and code.replace(' ', '') == '\n':
            continue
        else:
            code_rst.append((code, line))
            if code.replace(' ', '') == '\n':
                blank_code.append((code, line))
    # with open(r'D:\Code\VScode\C_Quality_Evaluator\C_Quality_Evaluator\app\CUnit\Sources\Automated\Automated.comment.c', 'w', encoding='utf-8') as f:
    #     for i in range(len(comment_text)):
    #         f.write(comment_text[i][0])
    # with open(r'D:\Code\VScode\C_Quality_Evaluator\C_Quality_Evaluator\app\CUnit\Sources\Automated\Automated.code.c', 'w', encoding='utf-8') as f:
    #     for i in range(len(code_rst)):
    #         f.write(code_rst[i][0])
    total_code_line = len(set([j for (i, j) in code_rst]))
    blank_line = len(set([j for (i, j) in blank_code]))
    vaild_code_line = total_code_line - blank_line
    total_comment_line = len(comment_lines)
    blank_comment = []
    for comment, line in comment_text:
        new = re.sub(r'[\*\-\+\^ ]', '', comment)
        if new == '\n':
            blank_comment.append((comment, line))
    blank_comment_line = len(set([j for (i, j) in blank_comment]))
    vaild_comment_line = total_comment_line - blank_comment_line
    return total_code_line, vaild_code_line, total_comment_line, vaild_comment_line


# f = open(r'D:\Code\VScode\C_Quality_Evaluator\C_Quality_Evaluator\app\CUnit\Sources\Automated\Automated.c', 'r', encoding='utf-8')
# file = f.readlines()
# r4 = code_comment_line(file)
# f.close()
# print(r4)


# 获取文件中的include
def getInclude(filePath):
    f = open(filePath, 'rb')
    data = f.read()
    encoding = chardet.detect(data)['encoding']
    f = open(filePath, 'r', encoding=encoding)
    file = f.readlines()
    f.close()
    include = []
    for line in file:
        if line.strip().startswith('#include'):
            tmp = re.search(r'(<|").*("|>)', line)
            if tmp:
                include.append(tmp.group())
    return include


# print(getInclude(r'D:\Code\VScode\C_Quality_Evaluator\C_Quality_Evaluator\app\CUnit\Sources\Automated\Automated.c'))

# 获取文件路径


def getFilePath(fileName, projectPath):
    for root, dirs, files in os.walk(projectPath):
        for file in files:
            if file == fileName:
                return os.path.join(root, file).replace('\\', '/')
    return None

# 获取项目中文件的fanIn和fanOut


def projectInclude(codeFileList, projectPath):  # 传入源文件列表和项目文件夹路径
    fanIn = {}  # key: file, value: include by which file
    fanOut = {}  # key: file, value: include which file
    projectPath = projectPath.replace('\\', '/').replace('//', '/')
    tmp = "/".join(projectPath.split("/")[:-1])
    with open(tmp + "/fan_dict.json", "r", encoding="utf-8") as f:
        analyze_data = json.load(f)
    for file in codeFileList:
        fanIn[file] = []
        fanIn[file] += analyze_data[file]["fan_in_self"]
        fanIn[file] += analyze_data[file]["fan_in_lib"]
        fanOut[file] = []
        fanOut[file] += analyze_data[file]["fan_out_self"]
        fanOut[file] += analyze_data[file]["fan_out_lib"]
    # for file in codeFileList:
    #     file = file.replace('\\', '/')
    #     include = getInclude(file)
    #     for i in range(len(include)):
    #         tmp_flag = include[i][0]
    #         include[i] = include[i].replace('"', '').replace('<', '').replace('>', '')
    #         if include[i].startswith('..') or include[i].startswith('.'):
    #             tmp = include[i].replace('\\', '/').split('/')[-1]
    #             tmp_path = getFilePath(tmp, projectPath)
    #             if tmp_path:
    #                 if tmp_path not in fanIn:
    #                     fanIn[tmp_path] = set()
    #                 fanIn[tmp_path].add(tmp_path)
    #                 if file not in fanOut:
    #                     fanOut[file] = set()
    #                 fanOut[file].add(tmp_path)
    #             else:
    #                 if file not in fanOut:
    #                     fanOut[file] = set()
    #                 fanOut[file].add(include[i])
    #                 if include[i] not in fanIn:
    #                     fanIn[include[i]] = set()
    #                 fanIn[include[i]].add(file)
    #         else:
    #             if tmp_flag == '"':
    #                 tmp = getFilePath(include[i], projectPath)
    #                 if tmp:
    #                     if tmp not in fanIn:
    #                         fanIn[tmp] = set()
    #                     fanIn[tmp].add(file)
    #                     if file not in fanOut:
    #                         fanOut[file] = set()
    #                     fanOut[file].add(tmp)
    #                 else:
    #                     if file not in fanOut:
    #                         fanOut[file] = set()
    #                     fanOut[file].add(include[i])
    #                     if include[i] not in fanIn:
    #                         fanIn[include[i]] = set()
    #                     fanIn[include[i]].add(file)
    #             else:
    #                 if file not in fanOut:
    #                     fanOut[file] = set()
    #                 fanOut[file].add(include[i])
    #                 if include[i] not in fanIn:
    #                     fanIn[include[i]] = set()
    #                 fanIn[include[i]].add(file)
    # for key in fanIn:
    #     fanIn[key] = list(fanIn[key])
    # for key in fanOut:
    #     fanOut[key] = list(fanOut[key])
    return fanIn, fanOut


def ReadFile(filePath):
    file = open(filePath, 'rb')
    # 根据二进制信息判断编码{'encoding': 'ascii', 'confidence': 1.0, 'language': ''}
    encoding_message = chardet.detect(file.read())
    print(filePath, encoding_message['encoding'])
    file.close()
    if encoding_message["encoding"] is None:
        return None
    if encoding_message['encoding'] == "GB2312":
        encoding_message['encoding'] = "GBK"
    with codecs.open(filePath, "rb", encoding=encoding_message['encoding']) as f:
        return f.read()


def SaveAsUTF8(filePath):
    for root, dirs, files in os.walk(filePath):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                content = ReadFile(path)
                if content is not None:
                    with codecs.open(path, "w", encoding="utf-8") as f:
                        f.write(content)


def get_param_list(func_code_list, llvm_param_list):
    """
    返回函数的参数类型列表
    :param func_code_list: 函数代码列表
    :param llvm_param_list: LLVM解析得到的参数列表
    """
    param_list = []
    code_text = "".join(func_code_list)
    code_text = code_text.replace("\n", "")
    code_text = code_text.replace("\t", "")
    index = code_text.find("(")
    if index == -1:
        return []
    code_text = code_text[index+1:]
    flag = 1
    tmp = ""
    for i in range(len(code_text)):
        if code_text[i] == "(":
            flag += 1
        elif code_text[i] == ")":
            flag -= 1
            if flag == 0:
                tmp = code_text[:i]
                break
    split_list = tmp.split(",")
    i = 0
    while i < len(split_list):
        left = split_list[i].count("(")
        right = split_list[i].count(")")
        if left == right:
            param_list.append(split_list[i].strip())
            i += 1
        else:
            start = i
            end = i
            while left != right:
                end += 1
                left += split_list[end].count("(")
                right += split_list[end].count(")")
            param_list.append(",".join(split_list[start:end+1]).strip())
            i = end+1
    param_type_list = []
    flag = 0
    if len(param_list) != len(llvm_param_list):
        flag = 1
    for i in range(len(param_list)):
        if flag == 0 and llvm_param_list[i]['name'] == "" and param_list[i] != "":
            param_type_list.append(param_list[i].replace(" ", ""))
            continue
        tmp = param_list[i].split(" ")
        if len(tmp) < 2:
            if tmp[0].strip() == "":
                param_type_list.append('void')
            else:
                param_type_list.append(tmp[0])
        else:
            t = deal_with_brace(tmp, 1)
            t[-1] = re.sub("[0-9]|[a-zA-Z]|\s+|\_", "", t[-1])
            param_type_list.append("".join(t).replace(" ", ""))
    return param_type_list


def deal_with_brace(space_code_list, director):
    """
    处理以空格分割的代码列表，将()中的代码合并
    :param space_code_list: 以空格分割的代码列表
    :param director: 方向，0为从左到右，1为从右到左
    """
    space_code_list = [i for i in space_code_list]
    if director == 1:
        space_code_list.reverse()
    return_list = []
    i = 0
    while i < len(space_code_list):
        left = space_code_list[i].count("(")
        right = space_code_list[i].count(")")
        if left == right:
            return_list.append(space_code_list[i])
            i += 1
        else:
            start = i
            end = i
            while left != right:
                end += 1
                left += space_code_list[end].count("(")
                right += space_code_list[end].count(")")
            return_list.append(",".join(space_code_list[start:end+1]).strip())
            i = end+1
    if director == 1:
        return_list.reverse()
    return return_list


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


if __name__ == "__main__":

    def getfilelist(path):
        # Convert relative path to absolute path
        path = os.path.abspath(path)
        # Get all files in the path
        filelist = []
        fileTypes = {
            "c": [],
            "cpp": [],
            "header": [],
            # "other": []

        }
        ctypelist = (".c")
        cpptypelist = (".C", ".cc", ".CC", ".cp", ".c++", ".C++", ".cxx", ".cpp", ".CPP", ".CXX")
        sourcetypelist = (".c", ".C", ".cc", ".CC", ".cp", ".c++", ".C++", ".cxx", ".cpp", ".CPP", ".CXX")
        headertypelist = (".h", ".H", ".hh", ".hpp", ".hxx")
        for root, dirs, files in os.walk(path):
            for file in files:
                # if os.path.splitext(file)[1] == '.c' or os.path.splitext(file)[1] == '.h' or os.path.splitext(file)[1] == '.l' or os.path.splitext(file)[1] == '.C' or os.path.splitext(file)[1] == '.H' or os.path.splitext(file)[1] == '.cpp' or os.path.splitext(file)[1] == '.hpp' or os.path.splitext(file)[1] == '.CPP' or os.path.splitext(file)[1] == '.HPP':
                if file.endswith(sourcetypelist) or file.endswith(headertypelist):
                    filelist.append(os.path.join(root, file).replace('\\', '/'))
                if file.endswith(ctypelist):
                    fileTypes['c'].append(os.path.join(root, file).replace('\\', '/'))
                elif file.endswith(cpptypelist):
                    fileTypes['cpp'].append(os.path.join(root, file).replace('\\', '/'))
                elif file.endswith(headertypelist):
                    fileTypes['header'].append(os.path.join(root, file).replace('\\', '/'))
                else:
                    fileTypes['other'].append(os.path.join(root, file).replace('\\', '/'))
        new_filelist = []
        for file in filelist:
            # 先存储头文件
            # if (file.find('.h') != -1 or file.find('.H') != -1 or file.find('.hpp') != -1 or file.find('.HPP') != -1) and file.find('ncurses') == -1 and file.find('ncursesw') == -1:
            if file.endswith(headertypelist) and file.find('ncurses') == -1 and file.find('ncursesw') == -1:
                new_filelist.append(file)
        for file in filelist:
            # 再存储源文件
            # if (file.find('.c') != -1 or file.find('.C') != -1 or file.find('.cpp') != -1 or file.find('.CPP') != -1 or os.path.splitext(file)[1] == '.l') and file.find('ncurses') == -1 and file.find('ncursesw') == -1:
            if file.endswith(sourcetypelist) and file.find('ncurses') == -1 and file.find('ncursesw') == -1:
                new_filelist.append(file)
        return new_filelist, fileTypes

    projectPath = r"D:\Code\test_project\CUnit"
    codeFileList, _ = getfilelist(projectPath)
    print(codeFileList)
    fanIn, fanOut = projectInclude(codeFileList, projectPath)
    # print(fanIn)

    print(fanOut)
# t = get_file_encoding(r"D:\Code\VScode\CPP_Support\CPP_support\uploads\saolei3\code\saolei\badSmell_fromfunc.json")
# print(t)
# with open(r"D:\Code\VScode\CPP_Support\CPP_support\uploads\ccc\code\CUnit\funcInfo.json") as f:
#     funcInfo_data = json.load(f)
# print(str(len(funcInfo_data))+"**************")
# file_dict = {}
# func_list = {}
# same_func = []
# for func in funcInfo_data:
#     locate = "".join(funcInfo_data[func]["locateFile"].split(":")[:-1])
#     if locate not in file_dict:
#         file_dict[locate] = []
#     if funcInfo_data[func]["name"] not in func_list:
#         func_list[funcInfo_data[func]["name"]] = locate
#     else:
#         same_func.append([locate, func_list[funcInfo_data[func]["name"]], funcInfo_data[func]["name"], get_param_list(funcInfo_data[func]["codeText"])])
#     file_dict[locate].append([funcInfo_data[func]["name"], get_param_list(funcInfo_data[func]["codeText"])])
    # print(funcInfo_data[func]["name"], get_param_list(funcInfo_data[func]["codeText"]))
# for key in file_dict:
#     print("------------------"+key+"===="+str(len(file_dict[key])))
#     for func in file_dict[key]:
#         print(func)
# for k in same_func:
#     print(k)
