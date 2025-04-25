"""
代码信息提取
作者：刘梓轩
时间：2023.8.2
"""
import subprocess
import os
import sys
import json
import traceback
import chardet
import copy
from utils import *
from merge_funcInfo import *
import networkx as nx
import call_back
import sdg_new
import Component_recovery
import Class_Diagram
import BuildCG

pwd = os.getcwd()
with open(pwd + "/config.json", "r", encoding="utf-8") as f:
    content = json.load(f)
DOT_EXE_FILE_PATH = content["DOT_EXE_FILE_PATH"]


# 存储C/C++数据输入函数
input_func = ['cin', 'scanf', 'getchar', 'gets', 'fgetc', 'fgets', 'getc', 'getchar_unlocked', 'getch', 'getche', 'getwchar', 'getwc', 'fgetwc', 'fgetws', 'fgetws_unlocked',
              'fgetc_unlocked', 'fread', 'fread_unlocked', 'read', 'readlink', 'pread', 'pread64', 'getdelim', 'getline', 'get_current_dir_name', 'getwd', 'getc', 'get']


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


class varInfo:
    # 变量信息类
    def __init__(self, key):
        self.key = key  # 变量唯一标识，即变量名
        self.name = ''  # 变量名
        self.type = ''  # 变量类型
        self.usingLoc = ''  # 变量使用位置
        self.declLoc = ''  # 变量声明位置
        self.declClass = ''  # 变量声明类
        self.authority = []  # 变量权限


class codeFileInfo:
    # 代码文件信息类
    def __init__(self, key):
        self.key = key  # 文件唯一标识，即文件路径
        self.name = ''  # 文件名
        self.type = ''  # 文件类型，后缀名
        self.codePath = ''  # 文件路径
        self.size = 0  # 文件大小
        self.functionNumber = 0  # 函数数量
        self.globalVariable = 0  # 全局变量数量
        self.functionList = []  # 函数列表
        self.classList = []  # 类列表
        self.globalVariableList = []  # 全局变量列表
        self.fanIn = []  # 被调用函数列表
        self.fanOut = []  # 调用函数列表
        self.codeInfo = {}  # 代码信息
        self.codeInfo['codeLine'] = 0
        self.codeInfo['codeLineExp'] = 0
        self.codeInfo['commentLine'] = 0
        self.codeInfo['commentLineExp'] = 0
        self.codeInfo['fileLine'] = 0


class funcInfo:
    # 函数信息类
    def __init__(self, key):
        self.key = key
        self.name = ''  # 函数名
        self.locateFile = ''  # 所在文件
        self.headerFile = ''  # 头文件
        self.sourceFile = ''  # 源文件
        self.ifbody = 0  # 是否有函数体
        self.startLine = 0  # 起始行
        self.endLine = 0  # 结束行
        self.codeText = []  # 函数代码
        self.variableList = []  # 变量列表
        self.type = ''  # 函数类型, Method or Function
        self.locateClass = ''  # 所在类
        self.paramList = []  # 参数列表
        self.returnType = ''  # 返回值类型
        self.modify = []  # 修饰符列表
        self.fanIn = []  # 被调用函数列表
        self.fanOut = []  # 调用函数列表
        self.cyclComplexity = 0  # 圈复杂度
        self.variableList = []  # 变量列表
        self.codeInfo = {}  # 代码信息
        self.codeInfo['codeLine'] = 0
        self.codeInfo['codeLineExp'] = 0
        self.codeInfo['commentLine'] = 0
        self.codeInfo['commentLineExp'] = 0
        self.codeInfo['funcLine'] = 0


class lib_funcInfo:
    # 库函数信息类
    def __init__(self, key):
        self.key = key
        self.name = ''
        self.locateFile = ''


class classInfo:
    # 类信息类
    def __init__(self, key):
        self.key = key
        self.name = ''  # 类名
        self.locateFile = ''  # 所在文件
        self.headerFile = ''  # 头文件
        self.sourceFile = ''  # 源文件
        self.type = ''  # 类型 Class or Struct or Union
        self.locateLine = 0  # 定位行
        self.start_Line = 0  # 起始行
        self.end_Line = 0  # 结束行
        self.mem_var = []  # 成员变量列表
        self.mem_method = []  # 成员函数列表
        self.varialbeList = []  # 变量列表
        self.baseClass = []  # 基类列表

# headertypelist = (".h", ".H", ".hh", ".hpp", ".hxx")


def getfilelist(path):
    # Convert relative path to absolute path
    # path = os.path.abspath(path)
    path = "/".join(path.split('/')[:-1])
    # Get all files in the path
    filelist = []
    fileTypes = {
        "c": [],
        "cpp": [],
        "header": [],
        "other": []
    }
    ctypelist = (".c")
    cpptypelist = (".C", ".cc", ".CC", ".cp", ".c++", ".C++", ".cxx", ".cpp", ".CPP", ".CXX")
    sourcetypelist = (".c", ".C", ".cc", ".CC", ".cp", ".c++", ".C++", ".cxx", ".cpp", ".CPP", ".CXX")
    headertypelist = (".h", ".H", ".hh", ".hpp", ".hxx")
    with open(path + "/analyze_files.json", 'r', encoding="utf-8") as f:
        file_select = json.load(f)
    filelist += file_select['header']
    filelist += file_select['source']
    for file_path in file_select['source']:
        if file_path.endswith(ctypelist):
            fileTypes['c'].append(file_path)
        else:
            fileTypes["cpp"].append(file_path)
    fileTypes['header'] = file_select['header']
    # for root, dirs, files in os.walk(path):
    #     for file in files:
    #         # if os.path.splitext(file)[1] == '.c' or os.path.splitext(file)[1] == '.h' or os.path.splitext(file)[1] == '.l' or os.path.splitext(file)[1] == '.C' or os.path.splitext(file)[1] == '.H' or os.path.splitext(file)[1] == '.cpp' or os.path.splitext(file)[1] == '.hpp' or os.path.splitext(file)[1] == '.CPP' or os.path.splitext(file)[1] == '.HPP':
    #         if file.endswith(sourcetypelist) or file.endswith(headertypelist):
    #             filelist.append(os.path.join(root, file).replace('\\', '/'))
    #         if file.endswith(ctypelist):
    #             fileTypes['c'].append(os.path.join(root, file).replace('\\', '/'))
    #         elif file.endswith(cpptypelist):
    #             fileTypes['cpp'].append(os.path.join(root, file).replace('\\', '/'))
    #         elif file.endswith(headertypelist):
    #             fileTypes['header'].append(os.path.join(root, file).replace('\\', '/'))
    #         else:
    #             fileTypes['other'].append(os.path.join(root, file).replace('\\', '/'))
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
    return filelist, fileTypes


def runParsing(file_list, project_path):
    # 运行parsing程序
    ctypelist = (".c")
    cpptypelist = (".C", ".cc", ".CC", ".cp", ".c++", ".C++", ".cxx", ".cpp", ".CPP", ".CXX")
    sourcetypelist = (".c", ".C", ".cc", ".CC", ".cp", ".c++", ".C++", ".cxx", ".cpp", ".CPP", ".CXX")
    headertypelist = (".h", ".H", ".hh", ".hpp", ".hxx")
    fanIn, fanOut = projectInclude(file_list, project_path)
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
            run_cmd('./CPP_Parsing/build/CPP_Parsing ' + new_file)
            call_txt = new_file+".call"
            with open(call_txt, 'r') as f:
                with open(file+".call", 'w') as f1:
                    for line in f.readlines():
                        f1.write(line.replace(new_file, file))
            parameter_txt = new_file+".parameter"
            with open(parameter_txt, 'r') as f:
                with open(file+".parameter", 'w') as f1:
                    for line in f.readlines():
                        f1.write(line.replace(new_file, file))
            class_txt = new_file+".class"
            with open(class_txt, 'r') as f:
                with open(file+".class", 'w') as f1:
                    for line in f.readlines():
                        f1.write(line.replace(new_file, file))
            class_var_txt = new_file+".class_var"
            with open(class_var_txt, 'r') as f:
                with open(file+".class_var", 'w') as f1:
                    for line in f.readlines():
                        f1.write(line.replace(new_file, file))
            gvar_txt = new_file+".gvar"
            with open(gvar_txt, 'r') as f:
                with open(file+".gvar", 'w') as f1:
                    for line in f.readlines():
                        f1.write(line.replace(new_file, file))
            if_txt = new_file+".if"
            with open(if_txt, 'r') as f:
                with open(file+".if", 'w') as f1:
                    for line in f.readlines():
                        f1.write(line.replace(new_file, file))
            param_txt = new_file+".param"
            with open(param_txt, 'r') as f:
                with open(file+".param", 'w') as f1:
                    for line in f.readlines():
                        f1.write(line.replace(new_file, file))
            parameter_txt = new_file+".parameter"
            with open(parameter_txt, 'r') as f:
                with open(file+".parameter", 'w') as f1:
                    for line in f.readlines():
                        f1.write(line.replace(new_file, file))
            pf_txt = new_file+".pf"
            with open(pf_txt, 'r') as f:
                with open(file+".pf", 'w') as f1:
                    for line in f.readlines():
                        f1.write(line.replace(new_file, file))
            txt = new_file+".txt"
            with open(txt, 'r') as f:
                with open(file+".txt", 'w') as f1:
                    for line in f.readlines():
                        f1.write(line.replace(new_file, file))
            var_txt = new_file+".var"
            with open(var_txt, 'r') as f:
                with open(file+".var", 'w') as f1:
                    for line in f.readlines():
                        f1.write(line.replace(new_file, file))
            # 删除新建的.hpp文件
            os.remove(new_file)
        else:
            run_cmd('./CPP_Parsing/build/CPP_Parsing ' + file)


def deal_path(path):
    # 处理路径，删掉../和./等
    if path == '<invalid loc>':
        return '<invalid loc>'
    fun_file = os.path.abspath(path).replace('\\', '/')
    return fun_file
# 获取函数注释


class Function:
    def __init__(self, name, param_list, file, start, end, return_type):
        self.name = name
        self.param_list = param_list
        self.file = ""
        self.file = file
        self.start = start
        self.end = end
        self.anno = ""
        self.return_type = return_type


def get_func_anno(FILE, funcInfo_dict, codefileInfo_dict):
    file_list, _ = getfilelist(FILE)  # (os.path.join(FILE,"code"))

    function_list = []

    for file in file_list:
        call_txt = file+".call"
        parameter_txt = file+".parameter"
        temp_func_list = []

        start_list = []
        end_list = []
        # 按行读取call_txt和parameter_txt，去掉空行
        call_list = []
        parameter_list = []
        encoding = get_file_encoding(call_txt)
        with open(call_txt, 'r', encoding=encoding) as f:
            for line in f.readlines():
                if line.strip() != '':
                    call_list.append(line.strip())
        encoding = get_file_encoding(parameter_txt)
        with open(parameter_txt, 'r', encoding=encoding) as f:
            for line in f.readlines():
                if line.strip() != '':
                    parameter_list.append(line.strip())

        for i in range(len(call_list)):
            func_info = call_list[i].split('],')[0][2:]
            func_param = parameter_list[i]
            return_type = func_param.split(';')[3].split('$$')[-1]
            func_name = func_info.split(' ;; ')[2]
            start = func_param.split(';')[1]
            start_list.append(int(start))
            end = func_param.split(';')[2]
            end_list.append(int(end))
            param_list = []
            if len(func_param.split(';')) > 6:
                # 从第四个分号开始，每两个分号为一组，分别为参数类型和参数名
                for j in range(5, len(func_param.split(';')), 2):
                    if func_param.split(';')[j] != "" and func_param.split(';')[j+1] != "":
                        param_list.append((func_param.split(';')[j].split('$$')[-1], func_param.split(';')[j+1]))

            new_func = Function(func_name, param_list, file, start, end, return_type)
            function_list.append(new_func)
            temp_func_list.append(new_func)

        # start_list从小到大排序
        start_list.sort()
        end_list.sort

        # 获取函数注释
        # 按行读取file，不去掉空行
        code = []
        encoding = get_file_encoding(file)
        with open(file, 'r', encoding=encoding) as f:
            for line in f.readlines():
                code.append(line)
        for func in temp_func_list:
            # if func.name == 'CU_set_output_filename':
            #     print(1)
            # 获取函数注释
            start_line = int(func.start)
            last_end_line = 0
            for line in end_list:
                if line < start_line:
                    last_end_line = line
            # if func.name == 'CU_set_suite_cleanup_failure_handler':
            #     print(last_end_line)
            anno = []
            # 遍历函数之前行，找到注释，注释结束行为函数开始行的前一行 如果开头为//，则为单行注释，如果开头为/*，则为多行注释
            for i in range(start_line-1, -1, -1):
                # 如果前一行为空行，则不含注释
                if code[i].strip() == '' or i+1 == last_end_line:
                    break
                # 如果前一行为单行注释，则将注释加入anno
                if code[i].strip().startswith('//'):
                    anno.append(code[i].replace('"', '').replace('\'', ''))
                # 如果前一行结尾为*/，则将注释加入anno，往前遍历，每一行都加入anno，直到遇到/*，则停止遍历
                elif code[i].strip().endswith('*/'):
                    anno.append(code[i].replace('"', '').replace('\'', ''))
                    for j in range(i, -1, -1):
                        if j != i:
                            anno.append(code[j].replace('"', '').replace('\'', ''))
                        if code[j].strip().startswith('/*'):
                            # 修改i，使得i为多行注释的第一行
                            i = j
                            break
            # 将注释倒序
            anno.reverse()
            # 遍历函数之后行，找到注释，注释开始行为函数结束行的后一行 如果开头为//，则为单行注释，如果开头为/*，则为多行注释
            end_line = int(func.end)
            next_start_line = 0
            for line in start_list:
                if line > end_line:
                    next_start_line = line
                    break
            # 如果函数结束行为文件最后一行，则不含注释
            if start_line == end_line:
                for i in range(end_line, len(code)):
                    # 如果后一行为空行，则不含注释
                    if code[i].strip() == '' or i+1 == next_start_line:
                        break
                    # 如果后一行为单行注释，则将注释加入anno
                    if code[i].strip().startswith('//'):
                        anno.append(code[i].replace('"', '').replace('\'', ''))
                    # 如果后一行开头为/*，则将注释加入anno，往后遍历，每一行都加入anno，直到遇到*/，则停止遍历
                    elif code[i].strip().startswith('/*'):
                        anno.append(code[i].replace('"', '').replace('\'', ''))
                        for j in range(i, len(code)):
                            if j != i:
                                anno.append(code[j].replace('"', '').replace('\'', ''))
                            if code[j].strip().endswith('*/'):
                                # 修改i，使得i为多行注释的最后一行
                                i = j
                                break
            func.anno = anno
        fileinfo = codefileInfo_dict[file]
        for func1 in temp_func_list:
            key = func1.return_type + ' '+func1.name+'('
            if len(func1.param_list) == 0:
                key += ")"
            else:
                for p in func1.param_list:
                    key += p[0]+' '+p[1]+', '
                key = key[:-2]+')'
            for func2 in fileinfo['functionList']:
                if key == func2[0]:
                    funcInfo_dict[func2[-2]]['anno'] += func1.anno

    return funcInfo_dict

# 获取类注释


class Class:
    def __init__(self, name, start, end):
        self.name = name
        self.start = start
        self.end = end
        self.anno = []


def get_class_anno(FILE, classInfo_dict, codefileInfo_dict):
    file_list, _ = getfilelist(FILE)  # (os.path.join(FILE,"code"))
    for file in file_list:
        temp_class_list = []

        start_list = []
        end_list = []
        class_txt = file+'.class'
        class_list = []
        encoding = get_file_encoding(class_txt)
        with open(class_txt, 'r', encoding=encoding) as f:
            for line in f.readlines():
                if line.strip() != '':
                    class_list.append(line.strip())

        for i in range(len(class_list)):
            name = class_list[i].split(" ## ")[0].replace('{', '')

            start = int(class_list[i].split(" ## ")[1])
            start_list.append(start)
            end = int(class_list[i].split(" ## ")[2])
            end_list.append(end)
            new_class = Class(name, start, end)
            temp_class_list.append(new_class)

        # start_list从小到大排序
        start_list.sort()
        end_list.sort

        # 获取函数注释
        # 按行读取file，不去掉空行
        code = []
        encoding = get_file_encoding(file)
        with open(file, 'r', encoding=encoding) as f:
            for line in f.readlines():
                code.append(line)
        for c in temp_class_list:
            # 获取函数注释
            start_line = int(c.start)
            last_end_line = 0
            for line in end_list:
                if line < start_line:
                    last_end_line = line
            # if func.name == 'CU_set_suite_cleanup_failure_handler':
            #     print(last_end_line)
            anno = []
            # 遍历函数之前行，找到注释，注释结束行为函数开始行的前一行 如果开头为//，则为单行注释，如果开头为/*，则为多行注释
            for i in range(start_line-1, -1, -1):
                # 如果前一行为空行，则不含注释
                if code[i].strip() == '' or i+1 == last_end_line:
                    break
                # 如果前一行为单行注释，则将注释加入anno
                if code[i].strip().startswith('//'):
                    anno.append(code[i].replace('"', '').replace('\'', ''))
                # 如果前一行结尾为*/，则将注释加入anno，往前遍历，每一行都加入anno，直到遇到/*，则停止遍历
                elif code[i].strip().endswith('*/'):
                    anno.append(code[i].replace('"', '').replace('\'', ''))
                    for j in range(i, -1, -1):
                        if j != i:
                            anno.append(code[j].replace('"', '').replace('\'', ''))
                        if code[j].strip().startswith('/*'):
                            # 修改i，使得i为多行注释的第一行
                            i = j
                            break
            # 将注释倒序
            anno.reverse()
            # 遍历函数之后行，找到注释，注释开始行为函数结束行的后一行 如果开头为//，则为单行注释，如果开头为/*，则为多行注释
            end_line = int(c.end)
            next_start_line = 0
            for line in start_list:
                if line > end_line:
                    next_start_line = line
                    break
            # 如果函数结束行为文件最后一行，则不含注释
            if start_line == end_line:
                for i in range(end_line, len(code)):
                    # 如果后一行为空行，则不含注释
                    if code[i].strip() == '' or i+1 == next_start_line:
                        break
                    # 如果后一行为单行注释，则将注释加入anno
                    if code[i].strip().startswith('//'):
                        anno.append(code[i].replace('"', '').replace('\'', ''))
                    # 如果后一行开头为/*，则将注释加入anno，往后遍历，每一行都加入anno，直到遇到*/，则停止遍历
                    elif code[i].strip().startswith('/*'):
                        anno.append(code[i].replace('"', '').replace('\'', ''))
                        for j in range(i, len(code)):
                            if j != i:
                                anno.append(code[j].replace('"', '').replace('\'', ''))
                            if code[j].strip().endswith('*/'):
                                # 修改i，使得i为多行注释的最后一行
                                i = j
                                break
            c.anno = anno

        fileinfo = codefileInfo_dict[file]
        for c1 in temp_class_list:
            for c2 in fileinfo['classList']:
                if c2.split(':')[-1] == c1.name:
                    classInfo_dict[c2]['anno'] += c1.anno

    return classInfo_dict


def get_define_macro(macro_loc):
    tmp = macro_loc.split(":")
    if os.path.exists(tmp[0]+':'+tmp[1]):
        with open(tmp[0]+':'+tmp[1], "r", encoding="utf-8") as f:
            lines = f.readlines()
        line_num = int(tmp[-2])
        col_num = int(tmp[-1])
        line = lines[line_num-1]
        txt = line[:col_num-1]
        txt = txt.replace("#define", "")
        txt = txt.replace(" ", "")
        txt = txt.replace("\t", "")
        return txt
    else:
        return ""


def get_code_from_line(line):
    code_txt = ""
    result = get1stSymPos(line, 0)
    if result[0] == -1:
        # 没有找到符号，可以返回处理纯代码
        code_txt += line
    else:
        if result[1] == '//' or result[1] == '/*':  # 单行注释
            code_txt += line[:result[0]]
        else:
            code_txt += line
    code_txt = code_txt.strip()
    return code_txt


def get_define_macro1(macro_loc):
    tmp = macro_loc.split(":")
    if os.path.exists(tmp[0]+':'+tmp[1]):
        with open(tmp[0]+':'+tmp[1], "r", encoding="utf-8") as f:
            lines = f.readlines()
        line_num = int(tmp[-2])
        col_num = int(tmp[-1])
        line = lines[line_num-1]
        txt = line[col_num-1:]
        txt = get_code_from_line(txt)
        return txt
    else:
        return ""


def GetInfo(file_list, project_path):
    global_var_list = []  # 全局变量列表
    codeFileInfo_dict = {}  # 代码文件信息字典
    funcInfo_dict = {}  # 函数信息字典
    classInfo_dict = {}  # 类信息字典
    input_locate = []  # 输入函数位置
    if_locate = []  # if语句位置
    matched_func_key = {}
    lib_func_list = []
    for codefile in file_list:
        print("GetInfo: ", codefile)
        # if "TestRun.h" in codefile:
        #     print()
        # 新建代码文件信息
        new_codeFileInfo = codeFileInfo(codefile)
        new_codeFileInfo.name = os.path.basename(codefile)
        new_codeFileInfo.type = os.path.splitext(codefile)[1]
        new_codeFileInfo.codePath = codefile
        new_codeFileInfo.size = os.path.getsize(codefile)
        codeFileInfo_dict[codefile] = new_codeFileInfo
        # 按行读取代码文件
        codeText = []  # 代码文件内容列表
        f = open(codefile, 'rb')
        data = f.read()
        encoding = chardet.detect(data)['encoding']
        f.close()
        with open(codefile, 'r', encoding=encoding) as f:
            for line in f.readlines():
                codeText.append(line)

        # 获取函数基本信息
        funcInfo_txt = codefile + '.call'

        # 判断是否存在call文件
        if not os.path.exists(funcInfo_txt):
            continue

        funcInfo_list = []  # 函数信息列表
        # 按行读取函数信息
        encoding = get_file_encoding(funcInfo_txt)
        with open(funcInfo_txt, 'r', encoding=encoding) as f:
            for line in f.readlines():
                line = line.strip('\n')
                funcInfo_list.append(line)

        for funcInfo_str in funcInfo_list:
            # 去除首尾花括号
            funcInfo_str = funcInfo_str.strip('{')
            funcInfo_str = funcInfo_str.strip('}')
            # 按], 分割
            funcInfo_str_list = funcInfo_str.split('],')
            if funcInfo_str_list[0] == '':
                continue
            first_func_key = ""
            for i in range(len(funcInfo_str_list)):
                # 第一个为自定义函数信息，其余为被调用函数信息
                if i == 0:
                    fun_info = funcInfo_str_list[i]
                    fun_info = fun_info.strip('[')
                    fun_info = fun_info.strip(']')
                    infos = fun_info.split(' ;; ')
                    locateFile = infos[0]
                    funcName = infos[2]
                    if locateFile.find(' <') != -1:
                        # fun_file = fun_file[:fun_file.find(' <')]
                        temp_file = locateFile[locateFile.find(' <'):].replace('Spelling=', '').replace('>', '').replace(' <', '')
                        define_name = get_define_macro1(temp_file)
                        pattern = re.compile(r'[\w]*'+funcName+r'[\w]*')
                        if pattern.findall(define_name) != []:
                            locateFile = deal_path(temp_file)
                        else:
                            locateFile = deal_path(locateFile[:locateFile.find(' <')])
                    # 去掉最后一个冒号之后的字符串
                    if locateFile[1] == ':':
                        locateFile = locateFile.split(':')[0]+':'+locateFile.split(':')[1]+':'+locateFile.split(':')[2]
                    else:
                        locateFile = locateFile.split(':')[0]+':'+locateFile.split(':')[1]
                    if locateFile[1] == ':':
                        locateFile_path = locateFile.split(':')[0]+':'+locateFile.split(':')[1]
                    else:
                        locateFile_path = locateFile.split(':')[0]
                    if locateFile_path[1] != ':':
                        # if '/' in locateFile_path:
                        #     print(locateFile_path)
                        for file in file_list:
                            if locateFile_path in file:
                                locateFile_path = file
                                locateFile = file + ':' + locateFile.split(':')[1]
                                break
                    isbody = infos[1]
                    funcName = infos[2]
                    funcClass = infos[3]
                    funcType = "Function"
                    if funcClass != '':
                        funcType = "Method"

                    if_static = infos[5]
                    authority = infos[6]
                    start = int(infos[7])
                    end = int(infos[8])
                    # func_code_text = codeText[start-1:end]
                    first_func_key = locateFile + ":" + funcName
                    # 在同一个文件中，函数名相同，且参数列表相同的函数，认为是同一个函数
                    # for func, value in funcInfo_dict.items():
                    #     if value.name == funcName and locateFile_path in value.locateFile:
                    #         matched_func_key[first_func_key] = func
                    #         first_func_key = func
                    #         locateFile = value.locateFile
                    #         break
                    new_funcInfo = funcInfo(locateFile + ":" + funcName)
                    new_funcInfo.name = funcName
                    new_funcInfo.locateFile = locateFile
                    new_funcInfo.ifbody = isbody
                    new_funcInfo.type = funcType
                    new_funcInfo.locateClass = funcClass
                    new_funcInfo.startLine = start
                    new_funcInfo.endLine = end
                    if if_static == "1":
                        new_funcInfo.modify.append("static")
                    new_funcInfo.modify.append(authority)
                    funcInfo_dict[first_func_key] = new_funcInfo
                    if locateFile_path not in codeFileInfo_dict.keys():
                        break
                    if first_func_key not in codeFileInfo_dict[locateFile_path].functionList:
                        codeFileInfo_dict[locateFile_path].functionList.append(first_func_key)
                else:
                    fun_info = funcInfo_str_list[i]
                    fun_info = fun_info.replace(' [', '').replace(']', '')
                    infos = fun_info.split(' ;; ')
                    if infos[0] == ' ':
                        continue
                    locateFile = infos[0]
                    funcName = infos[2]
                    # 去掉最后一个冒号之后的字符串
                    if locateFile != '<invalid loc>':
                        if locateFile.find(' <') != -1:
                            temp_file = locateFile[locateFile.find(' <'):].replace('Spelling=', '').replace('>', '').replace(' <', '')
                            define_name = get_define_macro1(temp_file)
                            pattern = re.compile(r'[\w]*'+funcName+r'[\w]*')
                            if pattern.findall(define_name) != []:
                                locateFile = deal_path(temp_file)
                            else:
                                locateFile = deal_path(locateFile[:locateFile.find(' <')])
                        locateFile = locateFile.split(':')
                    funcName = infos[2]

                    call_loc = infos[1]
                    if call_loc.find(' <') != -1:
                        call_loc = call_loc[:call_loc.find(' <')]
                    call_loc = call_loc.split(':')[0]+':'+call_loc.split(':')[1] # +':'+call_loc.split(':')[2]
                    if call_loc[1] != ':':
                        for file in file_list:
                            if call_loc.split(':')[0] in file:
                                call_loc = file + ':' + call_loc.split(':')[1]
                                break
                    if funcName in input_func and call_loc not in input_locate:
                        input_locate.append(call_loc)

                    call_line = int(call_loc.split(':')[-1])
                    if locateFile != '<invalid loc>' and locateFile[0] != '':

                        file = locateFile[0] # + ':' + locateFile[1]
                        file = deal_path(file)

                        locateFile = file  + ':' + locateFile[1]
                        func_key = locateFile + ":" + funcName

                        if_lib_func = 0
                        if file not in file_list:
                            # 为库函数
                            new_lib_funcInfo = lib_funcInfo(func_key)
                            new_lib_funcInfo.name = funcName
                            new_lib_funcInfo.locateFile = locateFile
                            lib_func_list.append(new_lib_funcInfo)
                            if_lib_func = 1

                        # if if_lib_func == 0:
                        #     if func_key not in funcInfo_dict.keys():
                        #         func_key = matched_func_key[func_key]
                        if funcInfo_dict[first_func_key].startLine <= call_line and funcInfo_dict[first_func_key].endLine >= call_line:
                            funcInfo_dict[first_func_key].fanOut.append([func_key, call_loc, if_lib_func])
                        else:
                            func_key_list = []
                            for key, value in funcInfo_dict.items():
                                if value.startLine <= call_line and value.endLine >= call_line:
                                    func_key_list.append(key)
                            
                            funcInfo_dict[func_key_list[-1]].fanOut.append([func_key, call_loc, if_lib_func])
                    else:
                        func_key = "Unrecognized File: "+funcName
                        new_funcInfo = funcInfo(func_key)
                        new_funcInfo.name = funcName
                        new_funcInfo.locateFile = "Unrecognized File"
                        funcInfo_dict[func_key] = new_funcInfo
                        if funcInfo_dict[first_func_key].startLine <= call_line and funcInfo_dict[first_func_key].endLine >= call_line:
                            funcInfo_dict[first_func_key].fanOut.append([func_key, call_loc, if_lib_func])
                        else:
                            func_key_list = []
                            for key, value in funcInfo_dict.items():
                                if value.startLine <= call_line and value.endLine >= call_line:
                                    func_key_list.append(key)
                            
                            funcInfo_dict[func_key_list[-1]].fanOut.append([func_key, call_loc, if_lib_func])

        # for func, value in funcInfo_dict.items():
        #     for fanout_func in value.fanOut:
        #         if func not in funcInfo_dict[fanout_func].fanIn:
        #             funcInfo_dict[fanout_func].fanIn.append(func)

        # 获取函数参数信息
        funcParam_txt = codefile + '.param'
        funcParam_list = []  # 函数参数信息列表
        # 按行读取函数参数信息
        encoding = get_file_encoding(funcParam_txt)
        with open(funcParam_txt, 'r', encoding=encoding) as f:
            for line in f.readlines():
                line = line.strip('\n')
                funcParam_list.append(line)
        for funcParam_str in funcParam_list:
            # 按分号分割
            param_info = funcParam_str.split(';')
            func_name = param_info[0].replace('[', '')
            start_line = int(param_info[1].split(' <Spelling')[0])
            end_line = int(param_info[2].split(' <Spelling')[0])
            func_code_text = [c.replace('\"', '@@').replace('\'', "@@") for c in codeText[start_line-1:end_line]]
            total_code_line, vaild_code_line, total_comment_line, vaild_comment_line = code_comment_line(codeText[start_line-1:end_line])
            codeInfo = {}
            codeInfo['codeLine'] = total_code_line
            codeInfo['codeLineExp'] = vaild_code_line
            codeInfo['commentLine'] = total_comment_line
            codeInfo['commentLineExp'] = vaild_comment_line
            codeInfo['funcLine'] = len(func_code_text)
            # codeFileInfo_dict[codefile].codeInfo = codeInfo
            return_type = param_info[3]
            locateFile = param_info[4]
            if locateFile.find(' <') != -1:
                # fun_file = fun_file[:fun_file.find(' <')]
                temp_file = locateFile[locateFile.find(' <'):].replace('Spelling=', '').replace('>', '').replace(' <', '')
                define_name = get_define_macro1(temp_file)
                pattern = re.compile(r'[\w]*'+func_name+r'[\w]*')
                if pattern.findall(define_name) != []:
                    locateFile = deal_path(temp_file)
                else:
                    locateFile = deal_path(locateFile[:locateFile.find(' <')])
            if locateFile[1] == ':':
                locateFile = locateFile.split(':')[0]+':'+locateFile.split(':')[1]+':'+locateFile.split(':')[2]
            else:
                locateFile = locateFile.split(':')[0]+':'+locateFile.split(':')[1]
            if locateFile[1] != ':':
                for file in file_list:
                    if locateFile.split(':')[0] in file:
                        locateFile = file + ':' + locateFile.split(':')[1]
                        break
            func_key = locateFile + ":" + func_name
            # if func_key not in funcInfo_dict.keys():
            #     func_key = matched_func_key[func_key]
            funcInfo_dict[func_key].startLine = start_line
            funcInfo_dict[func_key].endLine = end_line
            funcInfo_dict[func_key].returnType = return_type
            funcInfo_dict[func_key].codeText = func_code_text
            funcInfo_dict[func_key].codeInfo = codeInfo
            params = param_info[5:]
            for param in params:
                if param == '':
                    continue
                param.strip('[')
                param_name = param.split('@@')[0].split('[')[1]
                param_type = param.split('@@')[1].replace(']', '')
                funcInfo_dict[func_key].paramList.append([param_name, param_type])

        # 获取函数变量使用信息
        funcVariable_txt = codefile + '.var'
        funcVariable_list = []  # 函数变量使用信息列表
        # 按行读取函数变量使用信息
        encoding = get_file_encoding(funcVariable_txt)
        with open(funcVariable_txt, 'r', encoding=encoding) as f:
            for line in f.readlines():
                line = line.strip('\n')
                funcVariable_list.append(line)
        for funcVariable_str in funcVariable_list:
            # 按;;分割
            funcVariable_str = funcVariable_str.replace('[', '').replace(']', '')
            funcVariable_str_list = funcVariable_str.split(';;')
            func_name = funcVariable_str_list[0]
            locateFile = funcVariable_str_list[1]
            if locateFile.find(' <') != -1:
                # fun_file = fun_file[:fun_file.find(' <')]
                temp_file = locateFile[locateFile.find(' <'):].replace('Spelling=', '').replace('>', '').replace(' <', '')
                define_name = get_define_macro1(temp_file)
                pattern = re.compile(r'[\w]*'+func_name+r'[\w]*')
                if pattern.findall(define_name) != []:
                    locateFile = deal_path(temp_file)
                else:
                    locateFile = deal_path(locateFile[:locateFile.find(' <')])
            if locateFile[1] == ':':
                locateFile = locateFile.split(':')[0]+':'+locateFile.split(':')[1]+':'+locateFile.split(':')[2]
            else:
                locateFile = locateFile.split(':')[0]+':'+locateFile.split(':')[1]
            if locateFile[1] != ':':
                for file in file_list:
                    if locateFile.split(':')[0] in file:
                        locateFile = file + ':' + locateFile.split(':')[1]
                        break
            func_key = locateFile + ":" + func_name
            # if func_key not in funcInfo_dict.keys():
            #     func_key = matched_func_key[func_key]
            for k in range(2, len(funcVariable_str_list)):
                var = funcVariable_str_list[k]
                if var == '':
                    continue
                var.strip('[')
                if len(var.split('@@')) == 2:
                    continue
                var_name = var.split('@@')[0]
                var_type = var.split('@@')[1]
                var_using_loc = var.split('@@')[2]
                var_decl_loc = var.split('@@')[3]
                var_decl_class = var.split('@@')[4]
                new_varInfo = varInfo(var_name)
                new_varInfo.name = var_name
                new_varInfo.type = var_type
                new_varInfo.usingLoc = var_using_loc
                new_varInfo.declLoc = var_decl_loc
                new_varInfo.declClass = var_decl_class

                find = 0
                for temp_var in funcInfo_dict[func_key].variableList:
                    if temp_var.name == new_varInfo.name and temp_var.declLoc == new_varInfo.declLoc:
                        find = 1
                        break
                if find == 0:
                    funcInfo_dict[func_key].variableList.append(new_varInfo)

        # 获取全局变量信息
        globalVariable_txt = codefile + '.gvar'
        globalVariable_list = []  # 全局变量信息列表
        # 按行读取全局变量信息
        encoding = get_file_encoding(globalVariable_txt)
        with open(globalVariable_txt, 'r', encoding=encoding) as f:
            for line in f.readlines():
                line = line.strip('\n')
                globalVariable_list.append(line)
        for globalVariable_str in globalVariable_list:
            # 按;;分割
            globalVariable_str_list = globalVariable_str.split(';;')
            var_name = globalVariable_str_list[0]
            var_type = globalVariable_str_list[1]
            var_decl_loc = globalVariable_str_list[2]
            new_varInfo = varInfo(var_name)
            new_varInfo.name = var_name
            new_varInfo.type = var_type
            new_varInfo.declLoc = var_decl_loc
            global_var_list.append(new_varInfo)
            codeFileInfo_dict[codefile].globalVariableList.append(new_varInfo)

        # 获取类信息
        classInfo_txt = codefile + '.class'
        classInfo_list = []  # 类信息列表
        # 按行读取类信息
        encoding = get_file_encoding(classInfo_txt)
        with open(classInfo_txt, 'r', encoding=encoding) as f:
            for line in f.readlines():
                line = line.strip('\n')
                classInfo_list.append(line)
        for classInfo_str in classInfo_list:
            # 按 ## 分割
            classInfo_str_list = classInfo_str.split(' ## ')
            class_name = classInfo_str_list[0].replace('{', '')
            start_line = classInfo_str_list[1].split(' <Spelling')[0]
            end_line = classInfo_str_list[2].split(' <Spelling')[0]
            class_type = classInfo_str_list[3]
            locateFile = classInfo_str_list[4].split(':')[0]+':'+classInfo_str_list[4].split(':')[1]
            locateFile = locateFile.replace('\\', '/')
            if locateFile.find(' <') != -1:
                # fun_file = fun_file[:fun_file.find(' <')]
                temp_file = locateFile[locateFile.find(' <'):].replace('Spelling=', '').replace('>', '').replace(' <', '')
                define_name = get_define_macro1(temp_file)
                pattern = re.compile(r'[\w]*'+class_name+r'[\w]*')
                if pattern.findall(define_name) != []:
                    locateFile = deal_path(temp_file)
                else:
                    locateFile = deal_path(locateFile[:locateFile.find(' <')])
            locateLine = start_line
            class_key = locateFile + ":" + class_name

            # 基类
            base_list = []
            baseClasses = classInfo_str_list[5].split('][')
            for base in baseClasses:
                base = base.replace('[', '').replace(']', '')
                # 按@@分割
                base = base.split('@@')
                if base[0] == '':
                    continue
                base_class_name = base[0]
                base_file = base[1].split(':')[0]+':'+base[1].split(':')[1]
                base_class_key = base_file + ":" + base_class_name
                isvirtual = base[2]
                base_list.append([base_class_key, isvirtual])
            # 成员变量
            mem_var_list = []
            # 按] ;; 分割
            mem_vars = classInfo_str_list[6].split('] ;; ')
            for mem_var in mem_vars:
                mem_var = mem_var.replace('[', '').replace(']', '').replace('{', '').replace('}', '')
                if mem_var == '':
                    continue
                # 按 ;; 分割
                mem_var = mem_var.split(' ;; ')
                mem_var_name = mem_var[0]
                mem_var_decl_loc = mem_var[1]
                mem_var_class = mem_var[2]
                mem_var_type = mem_var[3]
                mem_var_authority = mem_var[4]
                new_varInfo = varInfo(mem_var_name)
                new_varInfo.name = mem_var_name
                new_varInfo.type = mem_var_type
                new_varInfo.declLoc = mem_var_decl_loc
                new_varInfo.declClass = mem_var_class
                new_varInfo.authority.append(mem_var_authority)
                mem_var_list.append(new_varInfo)
            # 成员函数
            mem_method_list = []
            # 按] ;; 分割
            mem_methods = classInfo_str_list[7].split('] ;; ')
            for mem_method in mem_methods:

                mem_method = mem_method.replace('[', '').replace(']', '').replace('{', '').replace('}', '')
                if mem_method == '':
                    continue
                # 按 ;; 分割
                mem_method = mem_method.split(' ;; ')
                mem_method_name = mem_method[0]
                mem_method_decl_loc = mem_method[1].split(':')[0]+':'+mem_method[1].split(':')[1]+':'+mem_method[1].split(':')[2]
                func_key = mem_method_decl_loc + ":" + mem_method_name
                # if func_key not in funcInfo_dict.keys():
                #     func_key = matched_func_key[func_key]
                mem_method_list.append(func_key)
                isstatic = mem_method[3]
                isvirtual = mem_method[4]
                if isstatic == "1":
                    funcInfo_dict[func_key].modify.append("static")
                if isvirtual == "1":
                    funcInfo_dict[func_key].modify.append("virtual")
            new_classInfo = classInfo(class_key)
            new_classInfo.name = class_name
            new_classInfo.type = class_type
            new_classInfo.start_Line = start_line
            new_classInfo.end_Line = end_line
            new_classInfo.locateFile = locateFile
            new_classInfo.locateLine = locateLine
            new_classInfo.baseClass = base_list
            new_classInfo.mem_var = mem_var_list
            new_classInfo.mem_method = mem_method_list
            classInfo_dict[class_key] = new_classInfo
            codeFileInfo_dict[locateFile].classList.append(class_key)

        # 获取类变量使用信息
        classVariable_txt = codefile + '.class_var'
        classVariable_list = []  # 类变量使用信息列表
        # 按行读取类变量使用信息
        encoding = get_file_encoding(classVariable_txt)
        with open(classVariable_txt, 'r', encoding=encoding) as f:
            for line in f.readlines():
                line = line.strip('\n')
                classVariable_list.append(line)
        for classVariable_str in classVariable_list:
            # 按;;分割
            classVariable_str = classVariable_str.replace('[', '').replace(']', '')
            classVariable_str_list = classVariable_str.split(';;')
            class_name = classVariable_str_list[0]
            locateFile = classVariable_str_list[1].split(':')[0]+':'+classVariable_str_list[1].split(':')[1]
            if locateFile.find(' <') != -1:
                # fun_file = fun_file[:fun_file.find(' <')]
                temp_file = locateFile[locateFile.find(' <'):].replace('Spelling=', '').replace('>', '').replace(' <', '')
                define_name = get_define_macro1(temp_file)
                pattern = re.compile(r'[\w]*'+class_name+r'[\w]*')
                if pattern.findall(define_name) != []:
                    locateFile = deal_path(temp_file)
                else:
                    locateFile = deal_path(locateFile[:locateFile.find(' <')])
            class_key = locateFile + ":" + class_name
            for k in range(2, len(classVariable_str_list)):
                vars = classVariable_str_list[k].split('];;')
                for var in vars:
                    if var == '':
                        continue
                    var.strip('[')
                    var_name = var.split('@@')[0]
                    var_type = var.split('@@')[1]
                    var_using_loc = var.split('@@')[2]
                    var_decl_loc = var.split('@@')[3]
                    var_decl_class = var.split('@@')[4]
                    new_varInfo = varInfo(var_name)
                    new_varInfo.name = var_name
                    new_varInfo.type = var_type
                    new_varInfo.usingLoc = var_using_loc
                    new_varInfo.declLoc = var_decl_loc
                    new_varInfo.declClass = var_decl_class
                    find = 0
                    for temp_var in classInfo_dict[class_key].varialbeList:
                        if temp_var.name == new_varInfo.name and temp_var.declLoc == new_varInfo.declLoc:
                            find = 1
                            break
                    if find == 0:
                        classInfo_dict[class_key].varialbeList.append(new_varInfo)

        # 获取文件代码信息
        total_code_line, vaild_code_line, total_comment_line, vaild_comment_line = code_comment_line(codeText)
        codeInfo = {}
        codeInfo['codeLine'] = total_code_line
        codeInfo['codeLineExp'] = vaild_code_line
        codeInfo['commentLine'] = total_comment_line
        codeInfo['commentLineExp'] = vaild_comment_line
        codeInfo['fileLine'] = len(codeText)
        codeFileInfo_dict[codefile].codeInfo = codeInfo

        # 获取if语句信息
        if_file = codefile + '.if'
        # 按行读取if语句信息
        encoding = get_file_encoding(if_file)
        with open(if_file, 'r', encoding=encoding) as f:
            for line in f.readlines():
                line = line.strip('\n')
                line = ":".join(line.split(':')[:-1])
                if line not in if_locate:
                    if_locate.append(line)
        print("GetInfo: ", codefile, " finished!")
    # 获取文件的其他信息
    fanIn, fanOut = projectInclude(file_list, project_path)
    for key, value in fanIn.items():
        if key in codeFileInfo_dict.keys():
            codeFileInfo_dict[key].fanIn = value

    for key, value in fanOut.items():
        if key in codeFileInfo_dict.keys():
            codeFileInfo_dict[key].fanOut = value

    return codeFileInfo_dict, funcInfo_dict, classInfo_dict, global_var_list, input_locate, if_locate, matched_func_key


def saveasdict(codeFileInfo_dict, funcInfo_dict, classInfo_dict, global_var_list):
    new_codeFileInfo_dict = {}
    new_funcInfo_dict = {}
    new_classInfo_dict = {}

    for key, value in codeFileInfo_dict.items():
        new_codeFileInfo_dict[key] = {}
        new_codeFileInfo_dict[key]['name'] = value.name
        new_codeFileInfo_dict[key]['type'] = value.type
        new_codeFileInfo_dict[key]['codePath'] = value.codePath
        new_codeFileInfo_dict[key]['size'] = value.size
        new_codeFileInfo_dict[key]['functionNumber'] = len(value.functionList)
        new_codeFileInfo_dict[key]['globalVariable'] = len(value.globalVariableList)
        new_codeFileInfo_dict[key]['fanIn'] = value.fanIn
        new_codeFileInfo_dict[key]['fanOut'] = value.fanOut
        new_codeFileInfo_dict[key]['codeInfo'] = value.codeInfo
        new_codeFileInfo_dict[key]['functionList'] = []
        for func in value.functionList:
            func_temp = []
            func_head = ""
            func_info = funcInfo_dict[func]
            func_head += func_info.returnType.split('$$')[1] + " "
            func_head += func_info.name + "("
            for param in func_info.paramList:
                func_head += param[1].split('$$')[1] + " " + param[0] + ", "
            if len(func_info.paramList) > 0:
                func_head = func_head[:-2]
            func_head += ")"

            temp_key = func_info.name
            for param in func_info.paramList:
                temp_key += param[0]

            func_class = func_info.locateClass
            func_line = str(func_info.startLine)
            func_temp.append(func_head)
            func_temp.append(func_class)
            func_temp.append(func_line)
            func_temp.append(func_info.key)
            func_temp.append(temp_key)
            new_codeFileInfo_dict[key]['functionList'].append(func_temp)
        new_codeFileInfo_dict[key]['classList'] = value.classList

    for key, value in funcInfo_dict.items():
        new_funcInfo_dict[key] = {}
        new_funcInfo_dict[key]['name'] = value.name
        new_funcInfo_dict[key]['locateFile'] = ":".join(value.key.split(":")[:-1])
        new_funcInfo_dict[key]['codeText'] = value.codeText
        new_funcInfo_dict[key]['ifbody'] = value.ifbody
        new_funcInfo_dict[key]['variableNum'] = len(value.variableList)
        new_funcInfo_dict[key]['type'] = value.type
        new_funcInfo_dict[key]['locateClass'] = value.locateClass
        new_funcInfo_dict[key]['anno'] = []
        new_funcInfo_dict[key]['modify'] = list(set(value.modify))

        fanOut = []
        # print(value.name)
        # print("value.fanOut", value.fanOut)
        for fan in value.fanOut:
            if fan[2] == 0 and fan[0] in funcInfo_dict.keys() and fan[0] not in fanOut:
                fanOut.append(fan[0])
        # print(funcInfo_dict.keys())
        new_funcInfo_dict[key]['fanOut'] = fanOut
        new_funcInfo_dict[key]['fanIn'] = []
        new_funcInfo_dict[key]['codeInfo'] = value.codeInfo
        new_funcInfo_dict[key]['paramList'] = []
        for param in value.paramList:
            param_temp = {}
            param_temp['name'] = param[0]
            param_temp['type'] = param[1].split('$$')[1]
            new_funcInfo_dict[key]['paramList'].append(param_temp)
        void = {}
        void['name'] = ""
        void['type'] = 'void'
        if new_funcInfo_dict[key]['paramList'] == []:
            new_funcInfo_dict[key]['paramList'].append(void)
        if '$$' in value.returnType:
            new_funcInfo_dict[key]['returnType'] = value.returnType.split('$$')[1]
        else:
            new_funcInfo_dict[key]['returnType'] = ''

    for key, value in classInfo_dict.items():
        new_classInfo_dict[key] = {}
        new_classInfo_dict[key]['name'] = value.name
        new_classInfo_dict[key]['locateFile'] = value.locateFile
        new_classInfo_dict[key]['start_line'] = value.start_Line
        new_classInfo_dict[key]['end_line'] = value.end_Line
        new_classInfo_dict[key]['type'] = value.type
        new_classInfo_dict[key]['locateLine'] = value.locateLine
        new_classInfo_dict[key]['fanIn'] = []
        new_classInfo_dict[key]['fanOut'] = []
        new_classInfo_dict[key]['anno'] = []
        new_classInfo_dict[key]['mem_var'] = []
        for var in value.mem_var:
            mem_var_temp = {}
            if var.type.split('$$')[1][-1] == '*' or var.type.split('$$')[1][-1] == '&':
                mem_var_temp['call_name'] = ''.join(var.type.split('$$')[1].split(' ')[-2:])

            mem_var_temp['call_loc'] = var.type.split('$$')[0]
            # 去掉最后一个空格之后的字符串
            if var.type.split('$$')[1][-1] == '*' or var.type.split('$$')[1][-1] == '&':
                call_type = var.type.split('$$')[-1]
            else:
                call_type = var.type.split('$$')[-1]
            if call_type == "":
                call_type = "var"
            mem_var_temp['call_type'] = call_type
            f_file = value.locateFile.split(':')[0] + ':' + value.locateFile.split(':')[1]
            for include in codeFileInfo_dict[f_file].fanOut + [value.locateFile]:
                if include in codeFileInfo_dict.keys():
                    include_info = codeFileInfo_dict[include]
                    for cc in include_info.classList:
                        if cc.split(':')[-1] in call_type:
                            # mem_var_temp['call_type'] = cc.split(':')[-1]
                            mem_var_temp['call_loc'] = cc
                            break
            mem_var_temp['this_name'] = var.name
            mem_var_temp['this_loc'] = var.declLoc.split(':')[2]
            mem_var_temp['authority'] = var.authority
            if "static" in call_type:
                mem_var_temp['authority'].append("static")
            if "const" in call_type:
                mem_var_temp['authority'].append("const")
            if "virtual" in call_type:
                mem_var_temp['authority'].append("virtual")
            new_classInfo_dict[key]['mem_var'].append(mem_var_temp)
        new_classInfo_dict[key]['mem_method'] = []
        for method in value.mem_method:
            method_info = funcInfo_dict[method]
            mem_method_temp = {}
            mem_method_temp['name'] = method_info.name
            mem_method_temp['return_type'] = method_info.returnType.split('$$')[1]
            mem_method_temp['return_type_loc'] = method_info.returnType.split('$$')[0]
            mem_method_temp['fanIn_num'] = 0
            f_file = value.locateFile.split(':')[0] + ':' + value.locateFile.split(':')[1]
            for include in codeFileInfo_dict[f_file].fanOut + [value.locateFile]:
                if include in codeFileInfo_dict.keys():
                    include_info = codeFileInfo_dict[include]
                    for cc in include_info.classList:
                        if cc.split(':')[-1] in mem_method_temp['return_type']:
                            # mem_method_temp['return_type'] = cc.split(':')[-1]
                            mem_method_temp['return_type_loc'] = cc
                            break
            method_line = method_info.locateFile.split(':')[-1]
            if int(method_line) <= int(value.start_Line) or int(method_line) >= int(value.end_Line):
                # 从new_funcInfo_dict中删除
                func_key = method_info.locateFile + ":" + method_info.name
                if func_key in new_funcInfo_dict.keys():
                    del new_funcInfo_dict[func_key]
                for func, funcvalue in new_funcInfo_dict.items():
                    if func_key in funcvalue['fanOut']:
                        funcvalue['fanOut'].remove(func_key)
                # 从new_codeFileInfo_dict中删除
                file = method_info.locateFile.split(':')[0] + ':' + method_info.locateFile.split(':')[1]
                if file in new_codeFileInfo_dict.keys():
                    for func in new_codeFileInfo_dict[file]['functionList']:
                        if func[3] == func_key:
                            new_codeFileInfo_dict[file]['functionList'].remove(func)
                            break
                continue
            mem_method_temp['param_list'] = []
            mem_method_temp['this_loc'] = method_info.locateFile
            for param in method_info.paramList:
                param_temp = {}
                if param[1].split('$$')[1][-1] == '*' or param[1].split('$$')[1][-1] == '&':
                    param_temp['call_name'] = ''.join(param[1].split('$$')[1].split(' ')[-2:])
                param_temp['call_loc'] = param[1].split('$$')[0]
                # 去掉最后一个空格之后的字符串
                if param[1].split('$$')[1][-1] == '*' or param[1].split('$$')[1][-1] == '&':
                    call_type = param[1].split('$$')[-1]
                else:
                    call_type = param[1].split('$$')[-1]
                if call_type == "":
                    call_type = "var"
                param_temp['call_type'] = call_type
                f_file = value.locateFile.split(':')[0] + ':' + value.locateFile.split(':')[1]
                for include in codeFileInfo_dict[f_file].fanOut + [value.locateFile]:
                    if include in codeFileInfo_dict.keys():
                        include_info = codeFileInfo_dict[include]
                        for cc in include_info.classList:
                            if cc.split(':')[-1] in call_type:
                                # param_temp['call_type'] = cc.split(':')[-1]
                                param_temp['call_loc'] = cc
                                break
                param_temp['this_name'] = param[0]
                mem_method_temp['param_list'].append(param_temp)
            mem_method_temp['authority'] = method_info.modify
            mem_method_temp['variable_list'] = []
            for var in method_info.variableList:
                var_temp = {}
                var_temp['name'] = var.name
                var_temp['type'] = var.type.split('$$')[1]
                var_temp['type_loc'] = var.type.split('$$')[0]
                f_file = value.locateFile.split(':')[0] + ':' + value.locateFile.split(':')[1]
                for include in codeFileInfo_dict[f_file].fanOut + [value.locateFile]:
                    if include in codeFileInfo_dict.keys():
                        include_info = codeFileInfo_dict[include]
                        for cc in include_info.classList:
                            if cc.split(':')[-1] in var_temp['type']:
                                # var_temp['type'] = cc.split(':')[-1]
                                var_temp['type_loc'] = cc
                                break
                var_temp['this_loc'] = ":".join(var.usingLoc.split(':')[:-1])
                var_temp['decl_loc'] = ":".join(var.declLoc.split(':')[:-1])
                var_temp['decl_class'] = ':'.join(var.declClass.split('$$')[0].split(':')[:-2]) + ':' + var.declClass.split('$$')[1].split(' ')[-1]
                for include in codeFileInfo_dict[f_file].fanOut + [value.locateFile]:
                    if include in codeFileInfo_dict.keys():
                        include_info = codeFileInfo_dict[include]
                        for cc in include_info.classList:
                            if cc.split(':')[-1] in var.declClass.split('$$')[1]:
                                # var_temp['decl_class'] = cc.split(':')[-1]
                                var_temp['decl_class'] = cc
                                break
                var_temp['is_global'] = False
                for g_var in global_var_list:
                    if g_var.declLoc == var.declLoc:
                        var_temp['is_global'] = True
                        break
                var_temp['is_record'] = False
                if 'class' in var_temp['type'] or 'struct' in var_temp['type'] or 'union' in var_temp['type']:
                    var_temp['is_record'] = True
                mem_method_temp['variable_list'].append(var_temp)
            new_classInfo_dict[key]['mem_method'].append(mem_method_temp)
        new_classInfo_dict[key]['baseClass'] = []
        for base in value.baseClass:
            base_temp = {}
            base_temp['class_loc'] = base[0]
            if base[1] == "1":
                base_temp['is_abstract'] = True
            else:
                base_temp['is_abstract'] = False
            new_classInfo_dict[key]['baseClass'].append(base_temp)
        new_classInfo_dict[key]['variable_list'] = []
        for var in value.varialbeList:
            var_temp = {}
            var_temp['name'] = var.name
            var_temp['type'] = var.type.split('$$')[1]
            var_temp['type_loc'] = var.type.split('$$')[0]

            f_file = value.locateFile.split(':')[0] + ':' + value.locateFile.split(':')[1]
            for include in codeFileInfo_dict[f_file].fanOut + [value.locateFile]:
                if include in codeFileInfo_dict.keys():
                    include_info = codeFileInfo_dict[include]
                    for cc in include_info.classList:
                        if cc.split(':')[-1] in var_temp['type']:
                            # var_temp['type'] = cc.split(':')[-1]
                            var_temp['type_loc'] = cc
                            break
            var_temp['this_loc'] = ":".join(var.usingLoc.split(':')[:-1])
            using_loc = var.usingLoc.split(':')[-2]
            if int(using_loc) <= int(value.start_Line) or int(using_loc) >= int(value.end_Line):
                continue
            var_temp['decl_loc'] = ":".join(var.declLoc.split(':')[:-1])
            var_temp['decl_class'] = ':'.join(var.declClass.split('$$')[0].split(':')[:-2]) + ':' + var.declClass.split('$$')[1].split(' ')[-1]
            for include in codeFileInfo_dict[f_file].fanOut + [value.locateFile]:
                if include in codeFileInfo_dict.keys():
                    include_info = codeFileInfo_dict[include]
                    for cc in include_info.classList:
                        if cc.split(':')[-1] in var.declClass.split('$$')[1]:
                            # var_temp['decl_class'] = cc.split(':')[-1]
                            var_temp['decl_class'] = cc
                            break
            var_temp['is_global'] = False
            for g_var in global_var_list:
                if g_var.declLoc == var.declLoc:
                    var_temp['is_global'] = True
                    break
            var_temp['is_record'] = False
            if 'class' in var_temp['type'] or 'struct' in var_temp['type'] or 'union' in var_temp['type']:
                var_temp['is_record'] = True
            new_classInfo_dict[key]['variable_list'].append(var_temp)

    return new_codeFileInfo_dict, new_funcInfo_dict, new_classInfo_dict


def file2project(projectname, new_codeFileInfo_dict, project_path, fileTypes):
    print("_ _________")
    projectInfo_dict = {"projectName": projectname,
                        "fileNumber": len(new_codeFileInfo_dict.keys())}
    functionNumber = 0
    codeInfo = {
        "codeLine": 0,
        "codeLineExp": 0,
        "commentLine": 0,
        "commentLineExp": 0,
        "projectLine": 0
    }

    functionNumber = set()
    for filename in new_codeFileInfo_dict.keys():
        # functionNumber += len(new_codeFileInfo_dict[filename]['functionList'])
        functionNumber.update([i[3] for i in new_codeFileInfo_dict[filename]['functionList']])
        codeInfo['codeLine'] += new_codeFileInfo_dict[filename]['codeInfo']['codeLine']
        codeInfo['codeLineExp'] += new_codeFileInfo_dict[filename]['codeInfo']['codeLineExp']
        codeInfo['commentLine'] += new_codeFileInfo_dict[filename]['codeInfo']['commentLine']
        codeInfo['commentLineExp'] += new_codeFileInfo_dict[filename]['codeInfo']['commentLineExp']
        codeInfo['projectLine'] += new_codeFileInfo_dict[filename]['codeInfo']['fileLine']

        # if new_codeFileInfo_dict[filename]["type"] in ctypelist:
        #     fileTypes['c'].append(filename)
        # elif new_codeFileInfo_dict[filename]['type'] in cpptypelist:
        #     fileTypes['cpp'].append(filename)
        # elif new_codeFileInfo_dict[filename]['type'] in headertypelist:
        #     fileTypes['header'].append(filename)
        # else:
        #     fileTypes['other'].append(filename)

    if fileTypes['c']:
        if fileTypes['cpp']:
            projectInfo_dict['projectType'] = 2
        else:
            projectInfo_dict['projectType'] = 0
    else:
        projectInfo_dict['projectType'] = 1

    projectInfo_dict['functionNumber'] = len(functionNumber)
    projectInfo_dict['codeInfo'] = copy.deepcopy(codeInfo)
    projectInfo_dict['fileTypes'] = copy.deepcopy(fileTypes)

    return projectInfo_dict


def get_Buffer_overflow(input_locate, if_locate):
    print("huanchongqu")
    input_lins = {}
    for input in input_locate:
        file = ":".join(input.split(":")[:-1])
        line = int(input.split(':')[-1])
        if file not in input_lins.keys():
            input_lins[file] = []
        input_lins[file].append(line)
    if_lines = {}
    for if_line in if_locate:
        file = ":".join(if_line.split(":")[:-1])
        line = int(if_line.split(':')[-1])
        if file not in if_lines.keys():
            if_lines[file] = []
        if_lines[file].append(line)
    print("huanchongqu2")
    buffer_overflow = {}
    for file in input_lins.keys():
        count = 0
        for line in input_lins[file]:
            line1 = line + 1
            line2 = line + 2
            if file in if_lines.keys():
                if line1 in if_lines[file] or line2 in if_lines[file]:
                    count += 1
        buffer_overflow[file] = [count, len(input_lins[file])]  # count有多少个判断溢出，len(input_lins[file])有多少个输入
    return buffer_overflow


def print2json(project_path, new_codeFileInfo_dict, new_funcInfo_dict, new_classInfo_dict, projectInfo_dict):
    # 保存为json文件
    with open(project_path + '//codeFileInfo.json', 'w', encoding='utf-8') as f:
        json.dump(new_codeFileInfo_dict, f, ensure_ascii=False, indent=4)
    with open(project_path + '//funcInfo.json', 'w', encoding='utf-8') as f:
        json.dump(new_funcInfo_dict, f, ensure_ascii=False, indent=4)
    with open(project_path + '//classInfo.json', 'w', encoding='utf-8') as f:
        json.dump(new_classInfo_dict, f, ensure_ascii=False, indent=4)
    with open(project_path + '//projectInfo.json', 'w', encoding='utf-8') as f:
        json.dump(projectInfo_dict, f, ensure_ascii=False, indent=4)


def build_plcg_dot(new_funcInfo_dict, project_path, funcInfo_dict):
    # 生成plcg.dot文件
    id_label_match = {}
    count = 1
    PLCG_nx = nx.DiGraph()
    try:
        for key, value in new_funcInfo_dict.items():
            # if key == "Unrecognized File: traceISR_EXIT":
            #     print("Unrecognized File: traceISR_EXIT")
            find = 0
            for node in PLCG_nx.nodes:
                node_label = PLCG_nx.nodes[node]['label']
                if '"' + key + '"' == node_label:
                    find = 1
                    break
            if find == 0:
                file = '"'+":".join(key.split(":")[:-2]) + '"'
                id = "node" + str(count)
                label = '"' + key+'"'
                # print(label)
                id_label_match[key] = id
                PLCG_nx.add_node(id, label=label, Lib="", file=file, call_code="")
                count += 1

            call_code_dict = {}
            source_key = key
            if 'source_key' in value.keys():
                source_key = value['source_key']
            for fan in funcInfo_dict[source_key].fanOut:
                fan_key = fan[0]
                find = 0
                called_id = ""
                lib_file = ""
                for node in PLCG_nx.nodes:
                    node_label = PLCG_nx.nodes[node]['label']
                    if fan_key in node_label:
                        find = 1
                        called_id = node
                        break
                if find == 0:
                    file = '"'+":".join(fan_key.split(":")[:-2]) + '"'
                    if fan[2] == 1:
                        lib_file = '"' + fan_key.split(":")[1].split("/")[-1] + '"'
                        file = "Library function"
                        id = "node" + str(count)
                        called_id = id
                        label = '"' + fan_key+'"'
                        # print(label)
                        id_label_match[fan_key] = id
                        PLCG_nx.add_node(id, label=label, Lib=lib_file, file=file)
                        count += 1
                if fan[2] == 1:
                    PLCG_nx.add_edge(id_label_match[key], called_id)
                call_loc = fan[1]
                loc = call_loc.split(":")[-1]
                start_line = funcInfo_dict[source_key].startLine
                func_code = funcInfo_dict[source_key].codeText
                func_name = fan_key.split(":")[-1]
                if func_name not in call_code_dict.keys():
                    call_code_dict[func_name] = []
                call_code_dict[func_name].append(func_code[int(loc) - start_line].replace("\n", "").replace('\t', ''))
                # call_code += func_code[int(loc) - start_line].replace("\n","") + "@@@"

            # 为key的node添加call_code属性
            call_code = ""
            for called_func_name, value in call_code_dict.items():
                call_code += called_func_name + ": "
                for line in value:
                    call_code += line + "@@@"
                call_code += "|||"
            PLCG_nx.nodes[id_label_match[key]]['call_code'] = '"'+call_code+'"'
    except Exception as e:
        traceback.print_exc()
    for key, value in new_funcInfo_dict.items():
        for fan in value['fanOut']:
            fan_key = fan
            PLCG_nx.add_edge(id_label_match[key], id_label_match[fan_key])

    # 输出到dot
    dot_file = project_path.replace('\\', '/') + '/PLCG' + '.dot'
    png_file = project_path.replace('\\', '/') + '/PLCG' + '.png'
    nx.drawing.nx_pydot.write_dot(PLCG_nx, dot_file)
    run_cmd(f'{DOT_EXE_FILE_PATH} -Tpng ' + dot_file + ' -o ' + png_file)

    return PLCG_nx


def get_info_from_func(func_data):
    # 获取所有入度为0的函数和所有函数的头文件和源文件
    in_degree_0 = []
    func_header_source = {}
    for key, value in func_data.items():
        if len(value['fanIn']) == 0:
            in_degree_0.append(key)
        func_header_source[key] = [value['source'], value['header']]

    return in_degree_0, func_header_source


def main(file_list, fileTypes, project_path):
    # 获取代码文件列表
    # file_list, fileTypes = getfilelist(project_path)
    # 运行解析程序
    runParsing(file_list, project_path)
    # 获取信息
    codeFileInfo_dict, funcInfo_dict, classInfo_dict, global_var_list, input_locate, if_locate, matched_func_key = GetInfo(file_list, project_path)

    # 保存为字典
    new_codeFileInfo_dict, new_funcInfo_dict, new_classInfo_dict = saveasdict(codeFileInfo_dict, funcInfo_dict, classInfo_dict, global_var_list)
    # 合并函数信息
    new_codeFileInfo_dict, new_funcInfo_dict = merge_funcInfo(new_codeFileInfo_dict, new_funcInfo_dict, matched_func_key)

    new_funcInfo_dict = get_func_anno(project_path, new_funcInfo_dict, new_codeFileInfo_dict)
    new_classInfo_dict = get_class_anno(project_path, new_classInfo_dict, new_codeFileInfo_dict)

    # 项目级信息
    projectname = "project"
    projectInfo_dict = file2project(projectname, new_codeFileInfo_dict, project_path, fileTypes)
    # 保存为json文件
    print2json(project_path, new_codeFileInfo_dict, new_funcInfo_dict, new_classInfo_dict, projectInfo_dict)

    # 将plcg存到nx中
    PLCG_nx = build_plcg_dot(new_funcInfo_dict, project_path, funcInfo_dict)

    # 获取所有入度为0的函数和所有函数的头文件和源文件
    in_degree_0, func_header_source = get_info_from_func(new_funcInfo_dict)

    # 构造CG
    try:
        func_data, bad_smell, graph_json, CG, file_data, Component_redundancy, Standalone_components = BuildCG.BUILDCG_main(file_list, project_path, 'rt', PLCG_nx, in_degree_0, func_header_source, {})
    except Exception as e:
        print("BUILDCG ERROR", e)
        traceback.print_exc()

    sdg_svg, sdg_nx = sdg_new.main(file_list, PLCG_nx, project_path)
    dot_file = project_path.replace('\\', '/') + '/sdg' + '.dot'
    png_file = project_path.replace('\\', '/') + '/sdg' + '.png'
    nx.drawing.nx_pydot.write_dot(sdg_nx, dot_file)
    run_cmd(f'{DOT_EXE_FILE_PATH} -Tpng ' + dot_file + ' -o ' + png_file)
    comp_js = Component_recovery.deal_sdg(nx.MultiDiGraph(PLCG_nx), sdg_nx, func_header_source)
    # call_back.main(project_path, PLCG_nx, func_header_source, init_method="add", random_seed=42, use_tfidf=False, project_floder_name="")
    # 合并类信息 （戴政再添加）

    # 项目级信息
    projectname = "project"
    projectInfo_dict = file2project(projectname, new_codeFileInfo_dict, project_path, fileTypes)

    # 获取缓冲区溢出信息
    buffer_overflow = get_Buffer_overflow(input_locate, if_locate)

    # 类图
    new_classInfo_dict, class_js_data = Class_Diagram.CLASS_main(new_classInfo_dict, new_funcInfo_dict)

    # 保存为json文件
    print2json(project_path, new_codeFileInfo_dict, new_funcInfo_dict, new_classInfo_dict, projectInfo_dict)

    # # # 构造掉返回风格 架构图 # 测试用
    import pipe_filter
    pipe_filter_svg = pipe_filter.main(PLCG_nx, project_path)
    with open("static/pipe_filter.svg", 'wb') as f:
        f.write(pipe_filter_svg)
    # comp_data_csv_path = call_back.main(project_path, PLCG_nx, func_header_source)
    # call_back_json = call_back.comp2json(PLCG_nx, comp_data_csv_path)
    # # save to static folder
    # with open("static/callback.js", 'w') as f:
    #     f.write("var comp=")
    #     f.write(call_back_json)
    # # graph_json['call_back'] = call_back_json
    # # 构造层次图
    # layer_graph_json = layer_graph.main(comp_data_csv_path, PLCG_nx)
    # with open("static/layer.js", 'w') as f: # 测试用
    #     f.write("var layer_graph=")
    #     f.write(layer_graph_json)
    # # graph_json['layer_graph'] = layer_graph_json

    return buffer_overflow, PLCG_nx  # , call_back_json, layer_graph_json


if __name__ == "__main__":
    project_path = r"/temp_grad/back_end_app/upload/sudo/code"
    file_list, fileTypes = getfilelist(project_path)
    main(file_list, fileTypes, project_path)
