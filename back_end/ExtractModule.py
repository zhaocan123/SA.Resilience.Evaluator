import pickle

import InfoExtract
import CodeAnalysis
import GetFileInfo
import GetProjectInfo
import GetFuncInfo
import GetClassInfo
import GetBadTaste
from Advice import Advice
from FaultRateCal import FaultRateCal
from project import *
from app import redis
'''
Info = {
    "projectInfo":projectInfo-json,
    "codeFileInfo":codeFileInfo-json,
    "funcInfo":funcInfo-json,
    "classInfo":classInfo-json,
}

'''


# 项目信息提取
def ProjectInfoExtract(projectname):
    data = redis.get("projectInfo:"+projectname)
    if data is not None:
        res = pickle.loads(data)
        return res
    else:
        a, b, c, d, e, f, g, h = query2(projectname)
        Info = {}
        Info["projectInfo"] = a
        Info["codeFileInfo"] = g
        Info["funcInfo"] = c
        Info["classInfo"] = d
        res = InfoExtract.InfoExtract(Info)
        bytes_info = pickle.dumps(res)
        redis.set("projectInfo:"+projectname, bytes_info)
    return res

# 代码解析及信息提取


def CodeAnalyseExtract(projectname):
    a, b, c, d, e, f, g, h = query2(projectname)
    Info = {}
    Info["projectInfo"] = a
    Info["codeFileInfo"] = g
    Info["funcInfo"] = c
    Info["classInfo"] = d
    result = {'c_info': None, 'c_plus_info': None}
    print('a', a['projectType'])
    if a['projectType'] == 0 or a['projectType'] == 2:
        result['c_info'] = CodeAnalysis.CodeAnalysis_C(Info)
    if a['projectType'] == 1 or a['projectType'] == 2:
        result['c_plus_info'] = CodeAnalysis.CodeAnalysis_CPP(Info)
    return result


def FileAnalyseExtract(projectname, selectfile, type):
    a, b, c, d, e, f, g, h = query2(projectname)
    Info = {}
    Info["projectInfo"] = a
    Info["codeFileInfo"] = g
    Info["funcInfo"] = c
    Info["classInfo"] = d
    result = None
    if type == 'c_info':
        result = CodeAnalysis.get_func_info(selectfile, Info)
    elif type == 'c_plus_info':
        result = CodeAnalysis.get_class_info(selectfile, Info)

    return result

# 坏味检测


def BadSmellDetection(projectname, threshold):
    '''

    :param Badsmell:  Badsmell-json
    :param Info:
    :param threshold:
    :return:
    '''
    a, b, c, d, e, f, g, h = query2(projectname)
    Info = {}
    Info["projectInfo"] = a
    Info["codeFileInfo"] = g
    Info["funcInfo"] = c
    Info["classInfo"] = d
    Badsmell = b
    GetBadTaste.class_to_badsmell(Info, Badsmell)
    rst = GetBadTaste.bad_smell_detection(Badsmell, Info, threshold)
    return rst


# 变更信息检测模块
def ChangeInfoDetection(oldprojectname, newprojectname):
    '''

    :param oldInfo:
    :param newInfo:
    :param oldindex: {"25010": 25010-json, "design_metrics": design_metrics-json}
    :param newindex: {"25010": 25010-json, "design_metrics": design_metrics-json}
    :return:
    '''
    a, b, c, d, e, f, g, h = query2(oldprojectname)
    oldInfo = {}
    oldInfo["projectInfo"] = a
    oldInfo["codeFileInfo"] = g
    oldInfo["funcInfo"] = c
    oldInfo["classInfo"] = d
    oldindex = {}
    oldindex["25010"] = f
    oldindex["design_metrics"] = h

    a, b, c, d, e, f, g, h = query2(newprojectname)
    newInfo = {}
    newInfo["projectInfo"] = a
    newInfo["codeFileInfo"] = g
    newInfo["funcInfo"] = c
    newInfo["classInfo"] = d
    newindex = {}
    newindex["25010"] = f
    newindex["design_metrics"] = h

    result = {}
    if (oldInfo['projectInfo']['projectType'] == 0 or oldInfo['projectInfo']['projectType'] == 2) and (newInfo['projectInfo']['projectType'] == 0 or newInfo['projectInfo']['projectType'] == 2):
        result['c_info'] = {}
        result['c_info']['systemLevel'] = GetProjectInfo.getproject(oldInfo, newInfo, oldindex, newindex)
        result['c_info']['fileLevel'] = GetFileInfo.getfile(oldInfo, newInfo)
        # print(result['c_info']['fileLevel'])
        result['c_info']['functionLevel'] = GetFuncInfo.getfunc(oldInfo, newInfo)
    if (oldInfo['projectInfo']['projectType'] == 1 or oldInfo['projectInfo']['projectType'] == 2) and (newInfo['projectInfo']['projectType'] == 1 or newInfo['projectInfo']['projectType'] == 2):
        result['c_plus_info'] = {}
        result['c_plus_info']['systemLevel'] = GetProjectInfo.getprojectCPP(oldInfo, newInfo, oldindex, newindex)
        result['c_plus_info']['fileLevel'] = GetFileInfo.getfileCPP(oldInfo, newInfo)
        result['c_plus_info']['classLevel'] = GetClassInfo.getclass(oldInfo, newInfo)

    return result


# 缺陷率计算模块
"""
rps_path:rps文件路径
weight:权重，三元组(强制类权重，建议类权重，可选类权重)
"""


def FaultCal(rps_path):
    '''

    :param rps_path: :rps文件路径
    :param weight: 三元组(强制类权重，建议类权重，可选类权重)
    :return: 缺陷率字典
    '''
    return FaultRateCal(rps_path).out


# 重构建议模块
"""

"""


def getAdvice(projectname, threshold):
    '''

    :param threshold: 阈值，例如
    threshold = {
    "par":[20,10],
    "var":[30,10],
    "cir":[10,20],
    "out":[10,10],
    "in":[10,10]
    }
    :param funcInfo: 函数信息字典
    :return: 重构建议字典
    '''
    a, b, c, d, e, f, g, h = query2(projectname)
    return Advice(threshold, c).getAdvice()


# with open("project.json", "r", encoding="utf-8") as f:
#     pj = json.load(f)
# a = Project(name = "CUnit")
# a.function_info_json = str(pj["funcInfo"]).encode()
# add_project(a)
# print(getAdvice(threshold={
#     "par": [20, 10],
#     "var": [30, 10],
#     "cir": [10, 20],
#     "out": [10, 10],
#     "in": [10, 10]
# }, name="CUnit"))
