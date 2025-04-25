def getclass(oldproject, newproject):
    oldinfo = oldproject['classInfo']
    olddata = dict()
    newinfo = newproject['classInfo']
    newdata = dict()
    for key in oldinfo.keys():
        tmpname = key.split('/')[-1]
        funcname = tmpname.split(':')[0] + tmpname.split(':')[-1]
        olddata[funcname] = oldinfo[key]

    for key in newinfo.keys():
        tmpname = key.split('/')[-1]
        funcname = tmpname.split(':')[0] + tmpname.split(':')[-1]
        newdata[funcname] = newinfo[key]

    oldfunclist = list(olddata.keys())
    newfunclist = list(newdata.keys())
    commonlist = []
    for func in oldfunclist:
        if func in newfunclist:
            commonlist.append(func)

    # print(checkparameter(olddata,newdata,commonlist))
    # print(checkvar(olddata,newdata,commonlist))
    # print(checkcyclComplexity(olddata, newdata, commonlist))
    # print(checkcodeLine(olddata, newdata, commonlist))
    # print(checkfanin(olddata, newdata, commonlist))
    # print(checkfanout(olddata, newdata, commonlist))
    functionlevel = {}
    # 成员方法
    paramNum = checkfunc(olddata, newdata, commonlist)
    functionlevel['memberFunctionNum'] = {}
    add_functiondata(functionlevel['memberFunctionNum'], paramNum)
    # 成员变量
    functionlevel['memberVariableNum'] = {}
    varNum = checkvar(olddata, newdata, commonlist)
    add_functiondata(functionlevel['memberVariableNum'], varNum)
    # 基类个数
    functionlevel['classNum'] = {}
    baseClassNum = checkbaseClass(olddata, newdata, commonlist)
    add_functiondata(functionlevel['classNum'], baseClassNum)
    # functionlevel['codeNum'] = {}
    # codeNum = checkcodeLine(olddata, newdata, commonlist)
    # add_functiondata(functionlevel['codeNum'], codeNum)
    functionlevel['outDegree'] = {}
    outNum = checkfanout(olddata, newdata, commonlist)
    add_functiondata(functionlevel['outDegree'], outNum)
    functionlevel['inDegree'] = {}
    inNum = checkfanin(olddata, newdata, commonlist)
    add_functiondata(functionlevel['inDegree'], inNum)

    # print('********************************')
    # print(functionlevel)
    return functionlevel


def add_functiondata(data, param):
    data['totalNum'] = param[0]
    data['totalProp'] = str(param[1] * 100) + '%'
    data['increaseNum'] = param[2]
    data['increaseProp'] = str(param[3] * 100) + '%'
    data['decreaseNum'] = param[4]
    data['decreaseProp'] = str(param[5] * 100) + '%'
    data['changeinfoList'] = param[6]


def checkfunc(olddata, newdata, commonlist):
    '''
    成员方法个数
    :param olddata:
    :param newdata:
    :param commonlist:
    :return:
    '''
    total_num = len(commonlist)
    changelist = []
    riselist = []
    droplist = []
    for i in commonlist:
        old_param_num = len(olddata[i]['mem_method'])
        new_param_num = len(newdata[i]['mem_method'])
        if old_param_num < new_param_num:
            funcpath = olddata[i]['locateFile'] + "/" + olddata[i]['name']
            changelist.append({"classPath": funcpath,
                               "selectedValue": old_param_num,
                               "latestValue": new_param_num})
            riselist.append(funcpath)
        elif old_param_num > new_param_num:
            funcpath = olddata[i]['locateFile'] + "/" + olddata[i]['name']
            changelist.append({"classPath": funcpath,
                               "selectedValue": old_param_num,
                               "latestValue": new_param_num})
            droplist.append(funcpath)
    change_num = len(changelist)
    rate = change_num / total_num if total_num else 0 if total_num else 0
    if change_num:
        rise_num = len(riselist)
        riserate = rise_num / change_num
        drop_num = len(droplist)
        droprate = drop_num / change_num
    else:
        rise_num = 0
        riserate = 0
        drop_num = 0
        droprate = 0

    return change_num, rate, rise_num, riserate, drop_num, droprate, changelist


def checkvar(olddata, newdata, commonlist):
    '''
    成员变量个数
    :param olddata:
    :param newdata:
    :param commonlist:
    :return:
    '''
    total_num = len(commonlist)
    changelist = []
    riselist = []
    droplist = []
    for i in commonlist:
        old_param_num = len(olddata[i]['mem_var'])
        new_param_num = len(newdata[i]['mem_var'])
        if old_param_num < new_param_num:
            funcpath = olddata[i]['locateFile'] + "/" + olddata[i]['name']
            changelist.append({"functionPath": funcpath,
                               "selectedValue": old_param_num,
                               "latestValue": new_param_num})
            riselist.append(funcpath)
        elif old_param_num > new_param_num:
            funcpath = olddata[i]['locateFile'] + "/" + olddata[i]['name']
            changelist.append({"functionPath": funcpath,
                               "selectedValue": old_param_num,
                               "latestValue": new_param_num})
            droplist.append(funcpath)
    change_num = len(changelist)
    rate = change_num / total_num if total_num else 0
    if change_num:
        rise_num = len(riselist)
        riserate = rise_num / change_num
        drop_num = len(droplist)
        droprate = drop_num / change_num
    else:
        rise_num = 0
        riserate = 0
        drop_num = 0
        droprate = 0

    return change_num, rate, rise_num, riserate, drop_num, droprate, changelist


def checkbaseClass(olddata, newdata, commonlist):
    '''
    基类
    :param olddata:
    :param newdata:
    :param commonlist:
    :return:
    '''
    total_num = len(commonlist)
    changelist = []
    riselist = []
    droplist = []
    for i in commonlist:
        old_param_num = len(olddata[i]['baseClass'])
        new_param_num = len(newdata[i]['baseClass'])
        if old_param_num < new_param_num:
            funcpath = olddata[i]['locateFile'] + "/" + olddata[i]['name']
            changelist.append({"functionPath": funcpath,
                               "selectedValue": old_param_num,
                               "latestValue": new_param_num})
            riselist.append(funcpath)
        elif old_param_num > new_param_num:
            funcpath = olddata[i]['locateFile'] + "/" + olddata[i]['name']
            changelist.append({"functionPath": funcpath,
                               "selectedValue": old_param_num,
                               "latestValue": new_param_num})
            droplist.append(funcpath)
    change_num = len(changelist)
    rate = change_num / total_num if total_num else 0
    if change_num:
        rise_num = len(riselist)
        riserate = rise_num / change_num
        drop_num = len(droplist)
        droprate = drop_num / change_num
    else:
        rise_num = 0
        riserate = 0
        drop_num = 0
        droprate = 0

    return change_num, rate, rise_num, riserate, drop_num, droprate, changelist


# def checkcodeLine(olddata, newdata, commonlist):
#     '''
#     代码行
#     :param olddata:
#     :param newdata:
#     :param commonlist:
#     :return:
#     '''
#     total_num = len(commonlist)
#     changelist = []
#     riselist = []
#     droplist = []
#     for i in commonlist:
#         old_param_num = float(olddata[i]['codeInfo']['codeLine'])
#         new_param_num = float(newdata[i]['codeInfo']['codeLine'])
#         if old_param_num < new_param_num:
#             funcpath = olddata[i]['locateFile'] + "/" + olddata[i]['name']
#             changelist.append({"functionPath": funcpath,
#                                "selectedValue": old_param_num,
#                                "latestValue": new_param_num})
#             riselist.append(funcpath)
#         elif old_param_num > new_param_num:
#             funcpath = olddata[i]['locateFile'] + "/" + olddata[i]['name']
#             changelist.append({"functionPath": funcpath,
#                                "selectedValue": old_param_num,
#                                "latestValue": new_param_num})
#             droplist.append(funcpath)
#     change_num = len(changelist)
#     rate = change_num / total_num if total_num else 0
#     if change_num:
#         rise_num = len(riselist)
#         riserate = rise_num / change_num
#         drop_num = len(droplist)
#         droprate = drop_num / change_num
#     else:
#         rise_num = 0
#         riserate = 0
#         drop_num = 0
#         droprate = 0
#
#     return change_num, rate, rise_num, riserate, drop_num, droprate, changelist

def checkfanin(olddata, newdata, commonlist):
    '''
    入度
    :param olddata:
    :param newdata:
    :param commonlist:
    :return:
    '''
    total_num = len(commonlist)
    changelist = []
    riselist = []
    droplist = []
    for i in commonlist:
        old_param_num = len(olddata[i]['fanIn'])
        new_param_num = len(newdata[i]['fanIn'])
        if old_param_num < new_param_num:
            funcpath = olddata[i]['locateFile'] + "/" + olddata[i]['name']
            changelist.append({"functionPath": funcpath,
                               "selectedValue": old_param_num,
                               "latestValue": new_param_num})
            riselist.append(funcpath)
        elif old_param_num > new_param_num:
            funcpath = olddata[i]['locateFile'] + "/" + olddata[i]['name']
            changelist.append({"functionPath": funcpath,
                               "selectedValue": old_param_num,
                               "latestValue": new_param_num})
            droplist.append(funcpath)
    change_num = len(changelist)
    rate = change_num / total_num if total_num else 0
    if change_num:
        rise_num = len(riselist)
        riserate = rise_num / change_num
        drop_num = len(droplist)
        droprate = drop_num / change_num
    else:
        rise_num = 0
        riserate = 0
        drop_num = 0
        droprate = 0

    return change_num, rate, rise_num, riserate, drop_num, droprate, changelist


def checkfanout(olddata, newdata, commonlist):
    '''
    出度
    :param olddata:
    :param newdata:
    :param commonlist:
    :return:
    '''
    total_num = len(commonlist)
    changelist = []
    riselist = []
    droplist = []
    for i in commonlist:
        old_param_num = len(olddata[i]['fanOut'])
        new_param_num = len(newdata[i]['fanOut'])
        if old_param_num < new_param_num:
            funcpath = olddata[i]['locateFile'] + "/" + olddata[i]['name']
            changelist.append({"functionPath": funcpath,
                               "selectedValue": old_param_num,
                               "latestValue": new_param_num})
            riselist.append(funcpath)
        elif old_param_num > new_param_num:
            funcpath = olddata[i]['locateFile'] + "/" + olddata[i]['name']
            changelist.append({"functionPath": funcpath,
                               "selectedValue": old_param_num,
                               "latestValue": new_param_num})
            droplist.append(funcpath)
    change_num = len(changelist)
    rate = change_num / total_num if total_num else 0
    if change_num:
        rise_num = len(riselist)
        riserate = rise_num / change_num
        drop_num = len(droplist)
        droprate = drop_num / change_num
    else:
        rise_num = 0
        riserate = 0
        drop_num = 0
        droprate = 0

    return change_num, rate, rise_num, riserate, drop_num, droprate, changelist


if __name__ == '__main__':
    # print(getmd5("main.c") == getmd5("main1.c"))
    import json

    f = open('code/data/classInfo.json', 'r')
    content = f.read()
    a = json.loads(content)
    olddata = {"classInfo": a}
    f.close()
    f = open('code/data/classInfo.json', 'r')
    content = f.read()
    a = json.loads(content)
    newdata = {"classInfo": a}
    f.close()
    result = getclass(olddata, newdata)
    print(result)
    data = json.dumps(result, indent=4, ensure_ascii=False)
    with open('code/pre/classinfo.json', 'w', newline='\n') as f:
        f.write(data)
