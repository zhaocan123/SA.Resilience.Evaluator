import copy
import sys


MAX_INT = sys.maxsize


def CodeAnalysis_C(Info):
    result = {}
    projectInfo = Info['projectInfo']
    filelist_C = projectInfo['fileTypes']['c']
    filelist_h = projectInfo['fileTypes']['header']
    result['cFileProp'] = round(len(projectInfo['fileTypes']['c']) / int(projectInfo['fileNumber']), 2)
    result['funcTotal'] = int(projectInfo['functionNumber'])
    filepath2all = {}
    # 函数行数
    funcInfo = Info['funcInfo']
    totallength = 0
    maxlength = 0
    maxfunc = None
    maxfuncpath = None
    minlength = MAX_INT - 1
    minfunc = None
    minfuncpath = None
    for key in funcInfo.keys():
        codeline = int(funcInfo[key]['codeInfo']['codeLine'])
        totallength += codeline
        if codeline > maxlength:
            maxlength = codeline
            maxfunc = funcInfo[key]['name']
            maxfuncpath = funcInfo[key]['locateFile']
        elif codeline < minlength:
            minlength = codeline
            minfunc = funcInfo[key]['name']
            minfuncpath = funcInfo[key]['locateFile']

    avglength = totallength / len(funcInfo.keys())
    if not minfunc:
        minlength = 0
    datalist = [maxfunc, maxfuncpath, maxlength,
                minfunc, minfuncpath, minlength, avglength]
    result['functionLine'] = get_Funcdict(datalist)

    # 文件行数
    fileInfo = Info['codeFileInfo']
    totallength = 0
    maxlength = 0
    minlength = MAX_INT - 1
    maxfile = maxfilepath = minfile = minfilepath = None
    for key in fileInfo.keys():
        if key not in filelist_C and key not in filelist_h:
            continue
        filepath2all[fileInfo[key]['codePath']] = key
        codeline = int(fileInfo[key]['codeInfo']['codeLine'])
        totallength += codeline
        if codeline > maxlength:
            maxlength = codeline
            maxfile = fileInfo[key]['name']
            maxfilepath = fileInfo[key]['codePath']
        elif codeline < minlength:
            minlength = codeline
            minfile = fileInfo[key]['name']
            minfilepath = fileInfo[key]['codePath']

    avglength = totallength / len(fileInfo.keys())
    if not minfile:
        minlength = 0
    datalist = [maxfile, maxfilepath, maxlength,
                minfile, minfilepath, minlength, avglength]
    result['fileLine'] = get_Filedict(datalist)

    # 文件包含函数
    # fileinfo = Info['codeFileInfo']
    totallength = 0
    maxlength = 0
    minlength = MAX_INT - 1
    maxfile = maxfilepath = minfile = minfilepath = None
    for key in fileInfo.keys():
        if key not in filelist_C and key not in filelist_h:
            continue

        codeline = len(fileInfo[key]['functionList'])
        totallength += codeline
        if codeline > maxlength:
            maxlength = codeline
            maxfile = fileInfo[key]['name']
            maxfilepath = fileInfo[key]['codePath']
        elif codeline < minlength:
            minlength = codeline
            minfile = fileInfo[key]['name']
            minfilepath = fileInfo[key]['codePath']

    avglength = totallength / len(fileInfo.keys())
    if not minfile:
        minlength = 0
    datalist = [maxfile, maxfilepath, maxlength,
                minfile, minfilepath, minlength, avglength]
    result['defineFuncFile'] = get_FuncFiledict(datalist)

    result['filePathList'] = list(filepath2all.keys())

    return result


def get_Funcdict(datalist):
    res = {}
    res['maxLineFunc'] = datalist[0]
    res['maxLineFuncPath'] = datalist[1]
    res['maxLine'] = datalist[2]
    res['minLineFunc'] = datalist[3]
    res['minLineFuncPath'] = datalist[4]
    res['minLine'] = datalist[5]
    res['avgLine'] = datalist[6]
    return res


def get_Filedict(datalist):
    res = {}
    res['maxLineFile'] = datalist[0]
    res['maxLineFilePath'] = datalist[1]
    res['maxLine'] = datalist[2]
    res['minLineFile'] = datalist[3]
    res['minLineFilePath'] = datalist[4]
    res['minLine'] = datalist[5]
    res['avgLine'] = datalist[6]
    return res


def get_FuncFiledict(datalist):
    res = {}
    res['maxFuncFile'] = datalist[0]
    res['maxFuncFilePath'] = datalist[1]
    res['maxFunc'] = datalist[2]
    res['minFuncFile'] = datalist[3]
    res['minFuncFilePath'] = datalist[4]
    res['minFunc'] = datalist[5]
    res['avgFunc'] = datalist[6]
    return res


def get_func_info(filepath, Info):
    result = []
    fileInfo = Info['codeFileInfo']
    funcInfo = Info['funcInfo']

    for key in funcInfo.keys():
        if filepath in key:
            temp = {}
            temp['funcName'] = funcInfo[key]['name']
            temp['returnVal'] = funcInfo[key]['returnType']
            temp['params'] = len(funcInfo[key]['paramList'])
            temp['inDegree'] = len(funcInfo[key]['fanIn'])
            temp['outDegree'] = len(funcInfo[key]['fanOut'])
            temp['filePath'] = key
            result.append(copy.deepcopy(temp))
    # print('funcresult', result)
    return result


def get_class_info(filepath, Info):
    result = []
    fileInfo = Info['codeFileInfo']
    classInfo = Info['classInfo']
    # totalpath = filepath2all[filepath]

    for key in classInfo.keys():
        if filepath in key:
            temp = {}
            temp['className'] = classInfo[key]['name']
            temp['memberVariable'] = len(classInfo[key]['mem_var'])
            temp['memberFunc'] = len(classInfo[key]['mem_method'])
            temp['superClass'] = len(classInfo[key]['baseClass'])
            temp['inDegree'] = len(classInfo[key]['fanIn'])
            temp['outDegree'] = len(classInfo[key]['fanOut'])
            temp['filePath'] = key
            result.append(copy.deepcopy(temp))
    return result


def CodeAnalysis_CPP(Info):
    result = {}
    projectInfo = Info['projectInfo']
    filelist_CPP = projectInfo['fileTypes']['cpp']
    filenamelist = []
    for filename in filelist_CPP:
        filenamelist.append(filename.split('/')[-1])
    filelist_h = projectInfo['fileTypes']['header']

    result['cppFileProp'] = round(len(projectInfo['fileTypes']['cpp']) / int(projectInfo['fileNumber']), 2)
    classInfo = Info['classInfo']
    result['classTotal'] = len(classInfo.keys())
    filepath2all = {}
    filepath2class = {}
    # 类成员数

    totallength = 0
    maxlength = 0
    maxfunc = None
    maxfuncpath = None
    minlength = MAX_INT - 1
    minfunc = None
    minfuncpath = None
    for key in classInfo.keys():
        if classInfo[key]['locateFile'].split('/')[-1] not in filenamelist:
            continue
        if classInfo[key]['locateFile'] not in filepath2class.keys():
            filepath2class[classInfo[key]['locateFile']] = [classInfo[key]['name']]
        else:
            filepath2class[classInfo[key]['locateFile']].append(classInfo[key]['name'])
        codeline = len(classInfo[key]['mem_var']) + len(classInfo[key]['mem_method'])
        totallength += codeline
        if codeline > maxlength:
            maxlength = codeline
            maxfunc = classInfo[key]['name']
            maxfuncpath = classInfo[key]['locateFile']
        elif codeline < minlength:
            minlength = codeline
            minfunc = classInfo[key]['name']
            minfuncpath = classInfo[key]['locateFile']

    avglength = 0 if not len(classInfo.keys()) else totallength / len(classInfo.keys())
    if not minfunc:
        minlength = 0
    datalist = [maxfunc, maxfuncpath, maxlength,
                minfunc, minfuncpath, minlength, avglength]
    result['classMember'] = get_Memberdict(datalist)

    # 文件行数?
    fileInfo = Info['codeFileInfo']
    totallength = 0
    maxlength = 0
    minlength = MAX_INT - 1
    maxfile = maxfilepath = minfile = minfilepath = None
    for key in fileInfo.keys():
        if key not in filelist_CPP and key not in filelist_h:
            continue
        # filepath2all[fileInfo[key]['codePath']] = key
        codeline = int(fileInfo[key]['codeInfo']['codeLine'])
        totallength += codeline
        if codeline > maxlength:
            maxlength = codeline
            maxfile = fileInfo[key]['name']
            maxfilepath = fileInfo[key]['codePath']
        elif codeline < minlength:
            minlength = codeline
            minfile = fileInfo[key]['name']
            minfilepath = fileInfo[key]['codePath']

    avglength = totallength / len(fileInfo.keys())
    if not minfile:
        minlength = 0
    datalist = [maxfile, maxfilepath, maxlength,
                minfile, minfilepath, minlength, avglength]
    result['fileLine'] = get_Filedict(datalist)

    # 文件包含文件中定义类数量
    # fileinfo = Info['codeFileInfo']
    totallength = 0
    maxlength = 0
    minlength = MAX_INT - 1
    maxfile = maxfilepath = minfile = minfilepath = None

    for key in filepath2class.keys():
        if key not in filelist_CPP and key not in filelist_h:
            continue
        codeline = len(filepath2class[key])
        totallength += codeline
        if codeline > maxlength:
            maxlength = codeline
            maxfile = key.split('/')[-1]
            maxfilepath = key
        elif codeline < minlength:
            minlength = codeline
            minfile = key.split('/')[-1]
            minfilepath = key

    avglength = 0 if not len(classInfo.keys()) else totallength / len(classInfo.keys())
    if not minfile:
        minlength = 0
    datalist = [maxfile, maxfilepath, maxlength,
                minfile, minfilepath, minlength, avglength]
    result['defineClassFile'] = get_ClassFiledict(datalist)

    result['filePathList'] = list(filepath2class.keys())

    return result


def get_Memberdict(datalist):
    res = {}
    res['maxMemberClass'] = datalist[0]
    res['maxMemberClassPath'] = datalist[1]
    res['maxMember'] = datalist[2]
    res['minMemberClass'] = datalist[3]
    res['minMemberClassPath'] = datalist[4]
    res['minMember'] = datalist[5]
    res['avgMember'] = datalist[6]
    return res


def get_ClassFiledict(datalist):
    res = {}
    res['maxClassFile'] = datalist[0]
    res['maxClassFilePath'] = datalist[1]
    res['maxClass'] = datalist[2]
    res['minClassFile'] = datalist[3]
    res['minClassFilePath'] = datalist[4]
    res['minClass'] = datalist[5]
    res['avgClass'] = datalist[6]
    return res

# if __name__ == '__main__':
#     # print(getmd5("main.c") == getmd5("main1.c"))
#     from CPP_support.back_end.project import query2
#
#     a, b, c, d, e, f, g = query2("sl1")
#     Info = {}
#     Info["projectInfo"] = a
#     Info["codeFileInfo"] = g
#     Info["funcInfo"] = c
#     Info["classInfo"] = d
#
#     import json
#     # f = open('code/data/main.json', 'r')
#     # content = f.read()
#     # a = json.loads(content)
#     # olddata = a
#     # f.close()
#     # f = open('code/data/main1.json', 'r')
#     # content = f.read()
#     # a = json.loads(content)
#     # newdata = a
#     # f.close()
#     #
#     # f = open('code/data/mainclass.json', 'r')
#     # content = f.read()
#     # a = json.loads(content)
#     # olddata['classInfo'] = a['classInfo']
#     # f.close()
#     # f = open('code/data/mainclass1.json', 'r')
#     # content = f.read()
#     # a = json.loads(content)
#     # newdata['classInfo'] = a['classInfo']
#     # f.close()
#     olddata = Info
#     result = CodeAnalysis_C(olddata)
#     # print(result)
#     data = json.dumps(result,indent=4,ensure_ascii=False)
#     with open('codeanalysec.json','w',newline='\n') as f:
#         f.write(data)
#
#     for i in result['filePathList']:
#         print(i)
#         print(get_func_info(i,Info),'\n')
#     # result = CodeAnalysis_CPP(newdata)
#     # print(result)
#     # data = json.dumps(result,indent=4,ensure_ascii=False)
#     # with open('code/pre/codeanalysecpp.json','w',newline='\n') as f:
#     #     f.write(data)
