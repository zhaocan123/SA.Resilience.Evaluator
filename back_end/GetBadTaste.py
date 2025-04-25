import time
import json
import Levenshtein
import itertools
import copy
from badsmell import BadSmell, add_bad_smell
import sys

from utils import get_file_encoding
sys.setrecursionlimit(3000)


def bad_smell_detection(data, projectinfo, threshold):  # 坏味信息，项目信息，阈值信息

    final_result = {"c_plus_info": None,
                    "c_info": None}
    bs = BadSmell()
    bs.project_name = projectinfo['projectInfo']['projectName']
    bs.threshold = str(json.dumps(threshold)).encode()
    if projectinfo['projectInfo']['projectType'] == 0:
        bs.cpp_dataClass = None
        bs.cpp_featureEnvy = None
        bs.cpp_funcCopy = None
        bs.cpp_largeClass = None
        bs.cpp_lazyClass = None
        bs.cpp_overCyclComplexityFunc = None
        bs.cpp_overDeepCall = None
        bs.cpp_overInOutDegreeFunc = None
        bs.cpp_overLongFunc = None
        bs.cpp_overLongParam = None
        bs.cpp_overCommentLineFunc = None
        bs.cpp_shotgunSurgery = None
        final_result['c_info'] = C_badSmell(data, projectinfo, threshold, bs)

    elif projectinfo['projectInfo']['projectType'] == 1:
        bs.c_funcCopy = None
        bs.c_overCommentLineFunc = None
        bs.c_overDeepCall = None
        bs.c_overInOutDegreeFunc = None
        bs.c_overLongFunc = None
        bs.c_overLongParam = None
        bs.c_overCyclComplexityFunc = None
        final_result['c_plus_info'] = CPP_badSmell(data, projectinfo, threshold, bs)

    else:
        final_result['c_info'] = C_badSmell(data, projectinfo, threshold, bs)
        final_result['c_plus_info'] = CPP_badSmell(data, projectinfo, threshold, bs)

    add_bad_smell(bs)
    return final_result


def C_badSmell(data, projectinfo, threshold, bs):
    start = time.perf_counter()
    ctyprlist = (".c", ".h")

    BadSmellResult = {}
    statisticTable = []
    fileBadvalue = []
    fileBadvaluedict = {}
    result = []
    Cstarttime = time.perf_counter()

    # 长函数代码坏味
    tempstart = time.perf_counter()
    detectionResults = []
    valuelist = []
    filenum = set()
    overLongFunc = {"name": "长函数代码坏味"}
    if 'overLongFunc' in threshold.keys():
        tempthreshold = threshold['overLongFunc']
        num = 0

        for i in data['overLongFunc']:
            tempfilename = ":".join(i['name'].split(":")[:2])

            if not tempfilename.endswith(ctyprlist):
                continue
            if float(i['val']) > int(tempthreshold):

                if tempfilename in fileBadvaluedict.keys():
                    fileBadvaluedict[tempfilename]['badSmellNum'] += 1
                    fileBadvaluedict[tempfilename]['badSmellKindNum'].add("overLongFunc")
                else:
                    fileBadvaluedict[tempfilename] = {}
                    fileBadvaluedict[tempfilename]['badSmellNum'] = 1
                    fileBadvaluedict[tempfilename]['badSmellKindNum'] = set()
                    fileBadvaluedict[tempfilename]['badSmellKindNum'].add("overLongFunc")

                num += 1
                filenum.add(tempfilename)
                detectionResults.append({
                    "fileName": i['name'].split("/")[-1].split(':')[0],
                    "funcName": i['name'].split(':')[-1],
                    "funcLength": str(i['val'])
                })
            valuelist.append(float(i['val']))
        overLongFunc['num'] = num
        statisticTable.append(overLongFunc)
        tempend = time.perf_counter()
        otherInfo = []
        otherInfo.append({
            "name": "坏味检测时间",
            "value": str(round((tempend - tempstart), 3)) + "秒"
        })
        otherInfo.append({
            "name": "含坏味文件数",
            "value": str(len(filenum)) + "个"
        })
        otherInfo.append({
            "name": "该坏味文件占比",
            "value": str(round(len(filenum) / int(projectinfo['projectInfo']['fileNumber']), 3))
        })
        otherInfo.append({
            "name": "最长函数长度",
            "value": str(0 if valuelist == [] else max(valuelist)) + "行"
        })

        bs.c_overLongFunc = str(json.dumps({
            "name": "长函数",
            "def": "函数长度过长",
            "key": "overLongFunc",
            "totalNum": len(detectionResults),
            "threshold": tempthreshold,
            "title": {
                "fileName": "文件名",
                "funcName": "函数名",
                "funcLength": "函数长度"
            },
            "detectionResults": detectionResults,
            "otherInfo": otherInfo
        })).encode()
        result.append({
            "name": "长函数",
            "def": "函数长度过长",
            "key": "overLongFunc",
            "totalNum": len(detectionResults),
            "threshold": tempthreshold,
            "title": {
                "fileName": "文件名",
                "funcName": "函数名",
                "funcLength": "函数长度"
            },
            "detectionResults": detectionResults[:20],
            "otherInfo": otherInfo
        })

    # 长参数代码坏味
    tempstart = time.perf_counter()
    detectionResults = []
    valuelist = []
    filenum = set()
    overLongParam = {"name": "长参数代码坏味"}
    if 'overLongParam' in threshold.keys():
        tempthreshold = threshold['overLongParam']
        num = 0
        for i in data['overLongParam']:
            tempfilename = ":".join(i['name'].split(":")[:2])

            if not tempfilename.endswith(ctyprlist):
                continue
            if float(i['val']) > int(tempthreshold):

                if tempfilename in fileBadvaluedict.keys():
                    fileBadvaluedict[tempfilename]['badSmellNum'] += 1
                    fileBadvaluedict[tempfilename]['badSmellKindNum'].add("overLongParam")
                else:
                    fileBadvaluedict[tempfilename] = {}
                    fileBadvaluedict[tempfilename]['badSmellNum'] = 1
                    fileBadvaluedict[tempfilename]['badSmellKindNum'] = set()
                    fileBadvaluedict[tempfilename]['badSmellKindNum'].add("overLongParam")
                num += 1
                filenum.add(tempfilename)
                detectionResults.append({
                    "fileName": i['name'].split("/")[-1].split(':')[0],
                    "funcName": i['name'].split(':')[-1],
                    "funcLength": str(i['val'])
                })
            valuelist.append(float(i['val']))
        overLongParam['num'] = num
        statisticTable.append(overLongParam)
        tempend = time.perf_counter()
        otherInfo = []
        otherInfo.append({
            "name": "坏味检测时间",
            "value": str(round((tempend - tempstart), 3)) + "秒"
        })
        otherInfo.append({
            "name": "含坏味文件数",
            "value": str(len(filenum)) + "个"
        })
        otherInfo.append({
            "name": "该坏味文件占比",
            "value": str(round(len(filenum) / int(projectinfo['projectInfo']['fileNumber']), 3))
        })
        otherInfo.append({
            "name": "最多参数数量",
            "value": str(0 if valuelist == [] else max(valuelist)) + "个"
        })

        bs.c_overLongParam = str(json.dumps({
            "name": "长参数",
            "def": "函数参数列表过长",
            "key": "overLongParam",
            "totalNum": len(detectionResults),
            "threshold": tempthreshold,
            "title": {
                "fileName": "文件名",
                "funcName": "函数名",
                "funcLength": "参数数量"
            },
            "detectionResults": detectionResults,
            "otherInfo": otherInfo
        })).encode()
        result.append({
            "name": "长参数",
            "def": "函数参数列表过长",
            "key": "overLongParam",
            "totalNum": len(detectionResults),
            "threshold": tempthreshold,
            "title": {
                "fileName": "文件名",
                "funcName": "函数名",
                "funcLength": "参数数量"
            },
            "detectionResults": detectionResults[:20],
            "otherInfo": otherInfo
        })
    # 注释代码坏味
    tempstart = time.perf_counter()
    detectionResults = []
    valuelist = []
    filenum = set()
    overCommentLineFile = {"name": "注释代码坏味"}
    if 'overCommentLineFile' in threshold.keys():

        tempthreshold = threshold['overCommentLineFile']
        num = 0
        for i in data['overCommentLineFunc']:
            tempfilename = ":".join(i['name'].split(":")[:2])

            if not tempfilename.endswith(ctyprlist):
                continue
            if float(i['val']) > int(tempthreshold):

                if tempfilename in fileBadvaluedict.keys():
                    fileBadvaluedict[tempfilename]['badSmellNum'] += 1
                    fileBadvaluedict[tempfilename]['badSmellKindNum'].add("overCommentLineFunc")
                else:
                    fileBadvaluedict[tempfilename] = {}
                    fileBadvaluedict[tempfilename]['badSmellNum'] = 1
                    fileBadvaluedict[tempfilename]['badSmellKindNum'] = set()
                    fileBadvaluedict[tempfilename]['badSmellKindNum'].add("overCommentLineFunc")
                num += 1
                filenum.add(tempfilename)
                detectionResults.append({
                    "fileName": i['name'].split("/")[-1].split(':')[0],
                    "funcName": i['name'].split(':')[-1],
                    "funcLength": str(i['val'])
                })
            valuelist.append(float(i['val']))
        overCommentLineFile['num'] = num
        statisticTable.append(overCommentLineFile)
        tempend = time.perf_counter()
        otherInfo = []
        otherInfo.append({
            "name": "坏味检测时间",
            "value": str(round((tempend - tempstart), 3)) + "秒"
        })
        otherInfo.append({
            "name": "含坏味文件数",
            "value": str(len(filenum)) + "个"
        })
        otherInfo.append({
            "name": "该坏味文件占比",
            "value": str(round(len(filenum) / int(projectinfo['projectInfo']['fileNumber']), 3))
        })
        otherInfo.append({
            "name": "最长注释行数",
            "value": str(0 if valuelist == [] else max(valuelist)) + "行"
        })

        bs.c_overCommentLineFunc = str(json.dumps({
            "name": "注释过多",
            "key": "overCommentLineFunc",
            "def": "代码文件注释内容过多",
            "totalNum": len(detectionResults),
            "threshold": tempthreshold,
            "title": {
                "fileName": "文件名",
                "funcName": "函数名",
                "funcLength": "注释行数"
            },
            "detectionResults": detectionResults,
            "otherInfo": otherInfo
        })).encode()
        result.append({
            "name": "注释过多",
            "key": "overCommentLineFunc",
            "def": "代码文件注释内容过多",
            "totalNum": len(detectionResults),
            "threshold": tempthreshold,
            "title": {
                "fileName": "文件名",
                "funcName": "函数名",
                "funcLength": "注释行数"
            },
            "detectionResults": detectionResults[:20],
            "otherInfo": otherInfo
        })
    # 过深函数调用代码坏味
    tempstart = time.perf_counter()
    detectionResults = []
    valuelist = []
    filenum = set()
    overDeepCall = {"name": "过深函数调用代码坏味"}
    if 'overDeepCall' in threshold.keys():
        tempthreshold = threshold["overDeepCall"]
        num = 0
        for i in data['overDeepCall']:
            tempfilename = ":".join(i[0].split(":")[:2])

            if not tempfilename.endswith(ctyprlist):
                continue
            if len(i) > int(tempthreshold):
                index = i[0].rfind(':')
                index = i[0][:index].rfind(":")
                tempfilename = i[0][:index]
                if tempfilename in fileBadvaluedict.keys():
                    fileBadvaluedict[tempfilename]['badSmellNum'] += 1
                    fileBadvaluedict[tempfilename]['badSmellKindNum'].add("overDeepCall")
                else:
                    fileBadvaluedict[tempfilename] = {}
                    fileBadvaluedict[tempfilename]['badSmellNum'] = 1
                    fileBadvaluedict[tempfilename]['badSmellKindNum'] = set()
                    fileBadvaluedict[tempfilename]['badSmellKindNum'].add("overDeepCall")
                num += 1
                filenum.add(tempfilename)
                detectionResults.append({
                    "fileName": i[0].split("/")[-1].split(':')[0],
                    "funcName": i[0].split(':')[-1],
                    "funcLength": str(len(i))
                })
            valuelist.append(len(i))
        overDeepCall['num'] = num
        statisticTable.append(overDeepCall)
        tempend = time.perf_counter()
        otherInfo = []
        otherInfo.append({
            "name": "坏味检测时间",
            "value": str(round((tempend - tempstart), 3)) + "秒"
        })
        otherInfo.append({
            "name": "含坏味文件数",
            "value": str(len(filenum)) + "个"
        })
        otherInfo.append({
            "name": "该坏味文件占比",
            "value": str(round(len(filenum) / int(projectinfo['projectInfo']['fileNumber']), 3))
        })
        otherInfo.append({
            "name": "调用深度",
            "value": str(0 if valuelist == [] else max(valuelist))
        })

        bs.c_overDeepCall = str(json.dumps({
            "name": "过深调用",
            "key": "overDeepCall",
            "totalNum": len(detectionResults),
            "def": "函数调用链长度过长，过长函数调用链容易导致空指针异常，并且在维护过程中需要同时修改多处地方",
            "threshold": tempthreshold,
            "title": {
                "fileName": "文件名",
                "funcName": "函数名",
                "funcLength": "调用深度"
            },
            "detectionResults": detectionResults,
            "otherInfo": otherInfo
        })).encode()
        result.append({
            "name": "过深调用",
            "key": "overDeepCall",
            "totalNum": len(detectionResults),
            "def": "函数调用链长度过长，过长函数调用链容易导致空指针异常，并且在维护过程中需要同时修改多处地方",
            "threshold": tempthreshold,
            "title": {
                "fileName": "文件名",
                "funcName": "函数名",
                "funcLength": "调用深度"
            },
            "detectionResults": detectionResults[:20],
            "otherInfo": otherInfo
        })

    # 扇入扇出代码坏味?
    tempstart = time.perf_counter()
    detectionResults = []
    valuelist = []
    filenum = set()
    overInOutDegreeFunc = {"name": "扇入扇出代码坏味"}
    if 'overInOutDegreeFunc' in threshold.keys():
        tempthreshold = threshold["overInOutDegreeFunc"]
        num = set()
        for i in data['overOutDegreeFunc']:
            tempfilename = ":".join(i['name'].split(":")[:2])

            if not tempfilename.endswith(ctyprlist):
                continue
            if float(i['val']) > int(tempthreshold):

                if tempfilename in fileBadvaluedict.keys():
                    fileBadvaluedict[tempfilename]['badSmellNum'] += 1
                    fileBadvaluedict[tempfilename]['badSmellKindNum'].add("overInOutDegreeFunc")
                else:
                    fileBadvaluedict[tempfilename] = {}
                    fileBadvaluedict[tempfilename]['badSmellNum'] = 1
                    fileBadvaluedict[tempfilename]['badSmellKindNum'] = set()
                    fileBadvaluedict[tempfilename]['badSmellKindNum'].add("overInOutDegreeFunc")
                num.add(i['name'])
                filenum.add(tempfilename)
                detectionResults.append({
                    "fileName": i['name'].split("/")[-1].split(':')[0],
                    "funcName": i['name'].split(':')[-1],
                    "funcLength": str(i['val'])
                })
            valuelist.append(float(i['val']))
        for i in data['overInDegreeFunc']:
            tempfilename = ":".join(i['name'].split(":")[:2])

            if not tempfilename.endswith(ctyprlist):
                continue
            if float(i['val']) > int(tempthreshold):

                if tempfilename in fileBadvaluedict.keys():
                    fileBadvaluedict[tempfilename]['badSmellNum'] += 1
                    fileBadvaluedict[tempfilename]['badSmellKindNum'].add("overInOutDegreeFunc")
                else:
                    fileBadvaluedict[tempfilename] = {}
                    fileBadvaluedict[tempfilename]['badSmellNum'] = 1
                    fileBadvaluedict[tempfilename]['badSmellKindNum'] = set()
                    fileBadvaluedict[tempfilename]['badSmellKindNum'].add("overInOutDegreeFunc")
                num.add(i['name'])
                filenum.add(tempfilename)
                detectionResults.append({
                    "fileName": i['name'].split("/")[-1].split(':')[0],
                    "funcName": i['name'].split(':')[-1],
                    "funcLength": str(i['val'])
                })
            valuelist.append(float(i['val']))
        overInOutDegreeFunc['num'] = len(num)
        statisticTable.append(overInOutDegreeFunc)
        tempend = time.perf_counter()
        otherInfo = []
        otherInfo.append({
            "name": "坏味检测时间",
            "value": str(round((tempend - tempstart), 3)) + "秒"
        })
        otherInfo.append({
            "name": "含坏味文件数",
            "value": str(len(filenum)) + "个"
        })
        otherInfo.append({
            "name": "该坏味文件占比",
            "value": str(round(len(filenum) / int(projectinfo['projectInfo']['fileNumber']), 3))
        })
        otherInfo.append({
            "name": "最长函数长度",
            "value": str(0 if valuelist == [] else max(valuelist)) + "行"
        })

        bs.c_overInOutDegreeFunc = str(json.dumps({
            "name": "扇入扇出",
            "key": "overInOutDegreeFunc",
            "totalNum": len(detectionResults),
            "def": "函数扇出或扇入过大。",
            "threshold": tempthreshold,
            "title": {
                "fileName": "文件名",
                "funcName": "函数名",
                "funcLength": "扇入扇出"
            },
            "detectionResults": detectionResults,
            "otherInfo": otherInfo
        })).encode()
        result.append({
            "name": "扇入扇出",
            "key": "overInOutDegreeFunc",
            "totalNum": len(detectionResults),
            "def": "函数扇出或扇入过大。",
            "threshold": tempthreshold,
            "title": {
                "fileName": "文件名",
                "funcName": "函数名",
                "funcLength": "扇入扇出"
            },
            "detectionResults": detectionResults[:20],
            "otherInfo": otherInfo
        })

    # 代码克隆代码坏味
    tempstart = time.perf_counter()
    detectionResults = []
    valuelist = []
    filenum = set()

    textCopy = {"name": "代码克隆代码坏味"}
    if 'textCopy' in threshold.keys():
        tempthreshold = float(threshold['textCopy'])
        num = 0

        funclist = list(projectinfo['funcInfo'].keys())
        functtuple = list(itertools.combinations(funclist, 2))
        for i in functtuple:
            tempfilename1 = ":".join(i[0].split(":")[:2])
            tempfilename2 = ":".join(i[1].split(":")[:2])
            if not tempfilename1.endswith(ctyprlist):
                continue
            func1 = i[0]
            func2 = i[1]
            str1 = ''
            for j in projectinfo['funcInfo'][func1]['codeText']:
                str1 += j
            str2 = ''
            for j in projectinfo['funcInfo'][func2]['codeText']:
                str2 += j
            sim = Levenshtein_sim(str1, str2)
            if sim > float(threshold['textCopy']):
                # index = func1.rfind(':')
                # index = func1[:index].rfind(":")
                # tempfilename1 = func1[:index]
                # tempfilename1 = func1.split(":")[0]
                # tempfilename2 = func2.split(":")[1]
                # index = func2.rfind(':')
                # index = func2[:index].rfind(":")
                # tempfilename2 = func2[:index]
                if tempfilename1 in fileBadvaluedict.keys():
                    fileBadvaluedict[tempfilename1]['badSmellNum'] += 1
                    fileBadvaluedict[tempfilename1]['badSmellKindNum'].add("textCopy")
                else:
                    fileBadvaluedict[tempfilename1] = {}
                    fileBadvaluedict[tempfilename1]['badSmellNum'] = 1
                    fileBadvaluedict[tempfilename1]['badSmellKindNum'] = set()
                    fileBadvaluedict[tempfilename1]['badSmellKindNum'].add("textCopy")
                if tempfilename2.endswith(ctyprlist):
                    if tempfilename2 in fileBadvaluedict.keys():
                        fileBadvaluedict[tempfilename2]['badSmellNum'] += 1
                        fileBadvaluedict[tempfilename2]['badSmellKindNum'].add("textCopy")
                    else:
                        fileBadvaluedict[tempfilename2] = {}
                        fileBadvaluedict[tempfilename2]['badSmellNum'] = 1
                        fileBadvaluedict[tempfilename2]['badSmellKindNum'] = set()
                        fileBadvaluedict[tempfilename2]['badSmellKindNum'].add("textCopy")

                num += 1
                filenum.add(tempfilename1)
                if tempfilename2.endswith(ctyprlist):
                    filenum.add(tempfilename2)
                detectionResults.append({
                    "fileNameA": func1.split("/")[-1].split(':')[0],
                    "funcNameA": func1.split(':')[-1],
                    "fileNameB": func2.split("/")[-1].split(':')[0],
                    "funcNameB": func2.split(':')[-1],
                    "similarity": str(round(sim, 4))
                })
            valuelist.append(round(float(sim), 4))

        for i in data['funcCopy']['cfg_copy']:
            tempfilename1 = ":".join(i[0].split(":")[:2])
            tempfilename2 = ":".join(i[1].split(":")[:2])
            if not tempfilename1.endswith(ctyprlist):
                continue
            func1 = i[0]
            func2 = i[1]
            # tempfilename1 = ":".join(i[0].split(":")[:2])
            # tempfilename1 = func1.split(":")[0]
            # tempfilename2 = func2.split(":")[1]

            if tempfilename1 in fileBadvaluedict.keys():
                fileBadvaluedict[tempfilename1]['badSmellNum'] += 1
                fileBadvaluedict[tempfilename1]['badSmellKindNum'].add("textCopy")
            else:
                fileBadvaluedict[tempfilename1] = {}
                fileBadvaluedict[tempfilename1]['badSmellNum'] = 1
                fileBadvaluedict[tempfilename1]['badSmellKindNum'] = set()
                fileBadvaluedict[tempfilename1]['badSmellKindNum'].add("textCopy")
            if tempfilename2.endswith(ctyprlist):
                if tempfilename2 in fileBadvaluedict.keys():
                    fileBadvaluedict[tempfilename2]['badSmellNum'] += 1
                    fileBadvaluedict[tempfilename2]['badSmellKindNum'].add("textCopy")
                else:
                    fileBadvaluedict[tempfilename2] = {}
                    fileBadvaluedict[tempfilename2]['badSmellNum'] = 1
                    fileBadvaluedict[tempfilename2]['badSmellKindNum'] = set()
                    fileBadvaluedict[tempfilename2]['badSmellKindNum'].add("textCopy")

            num += 1
            filenum.add(tempfilename1)
            if tempfilename2.endswith(ctyprlist):
                filenum.add(tempfilename2)
            detectionResults.append({
                "fileNameA": func1.split("/")[-1].split(':')[0],
                "funcNameA": func1.split(':')[-1],
                "fileNameB": func2.split("/")[-1].split(':')[0],
                "funcNameB": func2.split(':')[-1],
                "similarity": 'cfgCopy'
            })

        textCopy['num'] = num
        statisticTable.append(textCopy)
        tempend = time.perf_counter()
        otherInfo = []
        otherInfo.append({
            "name": "坏味检测时间",
            "value": str(round((tempend - tempstart), 3)) + "秒"
        })
        otherInfo.append({
            "name": "含坏味文件数",
            "value": str(len(filenum)) + "个"
        })
        otherInfo.append({
            "name": "该坏味文件占比",
            "value": str(round(len(filenum) / int(projectinfo['projectInfo']['fileNumber']), 3))
        })
        otherInfo.append({
            "name": "最大代码相似度",
            "value": str(round(max(valuelist), 4))
        })
        bs.c_funcCopy = str(json.dumps({
            "name": "代码克隆",
            "key": "funcCopy",
            "totalNum": len(detectionResults),
            "def": "函数之间内容相似，进而可以删除其中一个函数",
            "threshold": tempthreshold,
            "title": {
                "fileNameA": '相似文件A',
                "funcNameA": '相似函数A',
                "fileNameB": '相似文件B',
                "funcNameB": '相似函数B',
                "similarity": '代码相似度'
            },
            "detectionResults": detectionResults,
            "otherInfo": otherInfo
        })).encode()
        result.append({
            "name": "代码克隆",
            "key": "funcCopy",
            "totalNum": len(detectionResults),
            "def": "函数之间内容相似，进而可以删除其中一个函数",
            "threshold": tempthreshold,
            "title": {
                "fileNameA": '相似文件A',
                "funcNameA": '相似函数A',
                "fileNameB": '相似文件B',
                "funcNameB": '相似函数B',
                "similarity": '代码相似度'
            },
            "detectionResults": detectionResults[:20],
            "otherInfo": otherInfo
        })

    # 圈复杂度代码坏味
    tempstart = time.perf_counter()
    detectionResults = []
    valuelist = []
    filenum = set()

    overCyclComplexityFunc = {"name": "圈复杂度代码坏味"}
    if 'overCyclComplexityFunc' in threshold.keys():
        tempthreshold = threshold['overCyclComplexityFunc']
        num = 0
        for i in data['overCyclComplexityFunc']:
            tempfilename = ":".join(i['name'].split(":")[:2])
            if not tempfilename.endswith(ctyprlist):
                continue
            if float(i['val']) > int(tempthreshold):

                if tempfilename in fileBadvaluedict.keys():
                    fileBadvaluedict[tempfilename]['badSmellNum'] += 1
                    fileBadvaluedict[tempfilename]['badSmellKindNum'].add("overCyclComplexityFunc")
                else:
                    fileBadvaluedict[tempfilename] = {}
                    fileBadvaluedict[tempfilename]['badSmellNum'] = 1
                    fileBadvaluedict[tempfilename]['badSmellKindNum'] = set()
                    fileBadvaluedict[tempfilename]['badSmellKindNum'].add("overCyclComplexityFunc")
                num += 1
                filenum.add(tempfilename)
                detectionResults.append({
                    "fileName": i['name'].split("/")[-1].split(':')[0],
                    "funcName": i['name'].split(':')[-1],
                    "funcLength": str(i['val'])
                })
            valuelist.append(float(i['val']))
        overCyclComplexityFunc['num'] = num
        statisticTable.append(overCyclComplexityFunc)
        tempend = time.perf_counter()
        otherInfo = []
        otherInfo.append({
            "name": "坏味检测时间",
            "value": str(round((tempend - tempstart), 3)) + "秒"
        })
        otherInfo.append({
            "name": "含坏味文件数",
            "value": str(len(filenum)) + "个"
        })
        otherInfo.append({
            "name": "该坏味文件占比",
            "value": str(round(len(filenum) / int(projectinfo['projectInfo']['fileNumber']), 3))
        })
        otherInfo.append({
            "name": "最大圈复杂度",
            "value": str(0 if valuelist == [] else max(valuelist))
        })
        bs.c_overCyclComplexityFunc = str(json.dumps({
            "name": "圈复杂度",
            "def": "函数圈复杂度过高",
            "key": "overCyclComplexityFunc",
            "totalNum": len(detectionResults),
            "threshold": tempthreshold,
            "title": {
                "fileName": "文件名",
                "funcName": "函数名",
                "funcLength": "圈复杂度"
            },
            "detectionResults": detectionResults,
            "otherInfo": otherInfo
        })).encode()
        result.append({
            "name": "圈复杂度",
            "def": "函数圈复杂度过高",
            "key": "overCyclComplexityFunc",
            "totalNum": len(detectionResults),
            "threshold": tempthreshold,
            "title": {
                "fileName": "文件名",
                "funcName": "函数名",
                "funcLength": "圈复杂度"
            },
            "detectionResults": detectionResults[:20],
            "otherInfo": otherInfo
        })
    Cendtime = time.perf_counter()
    Ctime = Cendtime - Cstarttime
    fileBadvalue = get_filebadvalue(fileBadvaluedict)
    BadSmellResult['fileBadvalue'] = fileBadvalue

    # statisticTable
    BadSmellResult['statisticTable'] = statisticTable

    # result
    BadSmellResult['result'] = result

    # C
    # NPF
    BadSmellResult['NPF'] = int(projectinfo['projectInfo']['fileNumber'])

    # NCFBS
    numC = 0
    numCPP = 0
    clist = projectinfo['projectInfo']['fileTypes']['c']
    cpplist = projectinfo['projectInfo']['fileTypes']['cpp']
    cheaderlist = (".h")
    cppheaderlist = (".H", ".hh", ".hpp", ".hxx")
    for i in fileBadvaluedict:
        if i.endswith(cheaderlist):
            numC += 1
        elif i.endswith(cppheaderlist):
            numCPP += 1
        if i in clist:
            numC += 1
        elif i in cpplist:
            numCPP += 1
    BadSmellResult['NCFBS'] = numC

    # NCF
    BadSmellResult['NCF'] = len(projectinfo['projectInfo']['fileTypes']['c'])

    # RNCF
    BadSmellResult['RNCF'] = round((100 * BadSmellResult['NCF'] / BadSmellResult['NPF']), 2)

    # RNCFBS
    BadSmellResult['RNCFBS'] = round((100 * BadSmellResult['NCFBS'] / BadSmellResult['NPF']), 2)

    end = time.perf_counter()
    BadSmellResult['DT'] = round((end - start), 5)

    return BadSmellResult


def CPP_badSmell(data, projectinfo, threshold, bs):
    start = time.perf_counter()
    ctyprlist = (".c", ".h")
    BadSmellResult = {}
    statisticTable = []
    fileBadvalue = []
    fileBadvaluedict = {}
    result = []

    CPPstarttime = time.perf_counter()
    # 长函数代码坏味
    tempstart = time.perf_counter()
    detectionResults = []
    valuelist = []
    filenum = set()
    overLongFunc = {"name": "长函数代码坏味"}
    if 'overLongFunc' in threshold.keys():
        tempthreshold = threshold['overLongFunc']
        num = 0

        for i in data['overLongFunc']:
            tempfilename = ":".join(i['name'].split(":")[:2])

            if tempfilename.endswith(ctyprlist):
                continue
            if float(i['val']) > int(tempthreshold):

                if tempfilename in fileBadvaluedict.keys():
                    fileBadvaluedict[tempfilename]['badSmellNum'] += 1
                    fileBadvaluedict[tempfilename]['badSmellKindNum'].add("overLongFunc")
                else:
                    fileBadvaluedict[tempfilename] = {}
                    fileBadvaluedict[tempfilename]['badSmellNum'] = 1
                    fileBadvaluedict[tempfilename]['badSmellKindNum'] = set()
                    fileBadvaluedict[tempfilename]['badSmellKindNum'].add("overLongFunc")

                num += 1
                filenum.add(tempfilename)
                detectionResults.append({
                    "fileName": i['name'].split("/")[-1].split(':')[0],
                    "funcName": i['name'].split(':')[-1],
                    "funcLength": str(i['val'])
                })
            valuelist.append(float(i['val']))
        overLongFunc['num'] = num
        statisticTable.append(overLongFunc)
        tempend = time.perf_counter()
        otherInfo = []
        otherInfo.append({
            "name": "坏味检测时间",
            "value": str(round((tempend - tempstart), 3)) + "秒"
        })
        otherInfo.append({
            "name": "含坏味文件数",
            "value": str(len(filenum)) + "个"
        })
        otherInfo.append({
            "name": "该坏味文件占比",
            "value": str(round(len(filenum) / int(projectinfo['projectInfo']['fileNumber']), 3))
        })
        otherInfo.append({
            "name": "最长函数长度",
            "value": str(0 if valuelist == [] else max(valuelist)) + "行"
        })
        bs.cpp_overLongFunc = str(json.dumps({
            "name": "长函数",
            "key": "overLongFunc",
            "def": "函数长度过长",
            "totalNum": len(detectionResults),
            "threshold": tempthreshold,
            "title": {
                "fileName": "文件名",
                "funcName": "函数名",
                "funcLength": "函数长度"
            },
            "detectionResults": detectionResults,
            "otherInfo": otherInfo
        })).encode()
        result.append({
            "name": "长函数",
            "key": "overLongFunc",
            "def": "函数长度过长",
            "totalNum": len(detectionResults),
            "threshold": tempthreshold,
            "title": {
                "fileName": "文件名",
                "funcName": "函数名",
                "funcLength": "函数长度"
            },
            "detectionResults": detectionResults[:20],
            "otherInfo": otherInfo
        })

    # 长参数代码坏味
    tempstart = time.perf_counter()
    detectionResults = []
    valuelist = []
    filenum = set()
    overLongParam = {"name": "长参数代码坏味"}
    if 'overLongParam' in threshold.keys():
        tempthreshold = threshold['overLongParam']
        num = 0
        for i in data['overLongParam']:
            tempfilename = ":".join(i['name'].split(":")[:2])

            if tempfilename.endswith(ctyprlist):
                continue
            if float(i['val']) > int(tempthreshold):

                if tempfilename in fileBadvaluedict.keys():
                    fileBadvaluedict[tempfilename]['badSmellNum'] += 1
                    fileBadvaluedict[tempfilename]['badSmellKindNum'].add("overLongParam")
                else:
                    fileBadvaluedict[tempfilename] = {}
                    fileBadvaluedict[tempfilename]['badSmellNum'] = 1
                    fileBadvaluedict[tempfilename]['badSmellKindNum'] = set()
                    fileBadvaluedict[tempfilename]['badSmellKindNum'].add("overLongParam")
                num += 1
                filenum.add(tempfilename)
                detectionResults.append({
                    "fileName": i['name'].split("/")[-1].split(':')[0],
                    "funcName": i['name'].split(':')[-1],
                    "funcLength": str(i['val'])
                })
            valuelist.append(float(i['val']))
        overLongParam['num'] = num
        statisticTable.append(overLongParam)
        tempend = time.perf_counter()
        otherInfo = []
        otherInfo.append({
            "name": "坏味检测时间",
            "value": str(round((tempend - tempstart), 3)) + "秒"
        })
        otherInfo.append({
            "name": "含坏味文件数",
            "value": str(len(filenum)) + "个"
        })
        otherInfo.append({
            "name": "该坏味文件占比",
            "value": str(round(len(filenum) / int(projectinfo['projectInfo']['fileNumber']), 3))
        })
        otherInfo.append({
            "name": "最多参数数量",
            "value": str(0 if valuelist == [] else max(valuelist)) + "个"
        })
        bs.cpp_overLongParam = str(json.dumps({
            "name": "长参数",
            "key": "overLongParam",
            "def": "函数参数列表过长",
            "totalNum": len(detectionResults),
            "threshold": tempthreshold,
            "title": {
                "fileName": "文件名",
                "funcName": "函数名",
                "funcLength": "参数数量"
            },
            "detectionResults": detectionResults,
            "otherInfo": otherInfo
        })).encode()
        result.append({
            "name": "长参数",
            "key": "overLongParam",
            "def": "函数参数列表过长",
            "totalNum": len(detectionResults),
            "threshold": tempthreshold,
            "title": {
                "fileName": "文件名",
                "funcName": "函数名",
                "funcLength": "参数数量"
            },
            "detectionResults": detectionResults[:20],
            "otherInfo": otherInfo
        })
    # 注释代码坏味
    tempstart = time.perf_counter()
    detectionResults = []
    valuelist = []
    filenum = set()
    overCommentLineFile = {"name": "注释代码坏味"}
    if 'overCommentLineFile' in threshold.keys():

        tempthreshold = threshold['overCommentLineFile']
        num = 0
        for i in data['overCommentLineFunc']:
            tempfilename = ":".join(i['name'].split(":")[:2])

            if tempfilename.endswith(ctyprlist):
                continue
            if float(i['val']) > int(tempthreshold):

                if tempfilename in fileBadvaluedict.keys():
                    fileBadvaluedict[tempfilename]['badSmellNum'] += 1
                    fileBadvaluedict[tempfilename]['badSmellKindNum'].add("overCommentLineFunc")
                else:
                    fileBadvaluedict[tempfilename] = {}
                    fileBadvaluedict[tempfilename]['badSmellNum'] = 1
                    fileBadvaluedict[tempfilename]['badSmellKindNum'] = set()
                    fileBadvaluedict[tempfilename]['badSmellKindNum'].add("overCommentLineFunc")
                num += 1
                filenum.add(tempfilename)
                detectionResults.append({
                    "fileName": i['name'].split("/")[-1].split(':')[0],
                    "funcName": i['name'].split(':')[-1],
                    "funcLength": str(i['val'])
                })
            valuelist.append(float(i['val']))
        overCommentLineFile['num'] = num
        statisticTable.append(overCommentLineFile)
        tempend = time.perf_counter()
        otherInfo = []
        otherInfo.append({
            "name": "坏味检测时间",
            "value": str(round((tempend - tempstart), 3)) + "秒"
        })
        otherInfo.append({
            "name": "含坏味文件数",
            "value": str(len(filenum)) + "个"
        })
        otherInfo.append({
            "name": "该坏味文件占比",
            "value": str(round(len(filenum) / int(projectinfo['projectInfo']['fileNumber']), 3))
        })
        otherInfo.append({
            "name": "最长注释行数",
            "value": str(0 if valuelist == [] else max(valuelist)) + "行"
        })
        bs.cpp_overCommentLineFile = str(json.dumps({
            "name": "注释过多",
            "def": "代码文件注释内容过多",
            "key": "overCommentLineFunc",
            "totalNum": len(detectionResults),
            "threshold": tempthreshold,
            "title": {
                "fileName": "文件名",
                "funcName": "函数名",
                "funcLength": "注释行数"
            },
            "detectionResults": detectionResults,
            "otherInfo": otherInfo
        })).encode()
        result.append({
            "name": "注释过多",
            "def": "代码文件注释内容过多",
            "key": "overCommentLineFunc",
            "totalNum": len(detectionResults),
            "threshold": tempthreshold,
            "title": {
                "fileName": "文件名",
                "funcName": "函数名",
                "funcLength": "注释行数"
            },
            "detectionResults": detectionResults[:20],
            "otherInfo": otherInfo
        })
    # 过深函数调用代码坏味
    tempstart = time.perf_counter()
    detectionResults = []
    valuelist = []
    filenum = set()
    overDeepCall = {"name": "过深函数调用代码坏味"}
    if 'overDeepCall' in threshold.keys():
        tempthreshold = threshold["overDeepCall"]
        num = 0
        for i in data['overDeepCall']:
            tempfilename = ":".join(i[0].split(":")[:2])

            if tempfilename.endswith(ctyprlist):
                continue
            if len(i) > int(tempthreshold):
                index = i[0].rfind(':')
                index = i[0][:index].rfind(":")
                tempfilename = i[0][:index]
                if tempfilename in fileBadvaluedict.keys():
                    fileBadvaluedict[tempfilename]['badSmellNum'] += 1
                    fileBadvaluedict[tempfilename]['badSmellKindNum'].add("overDeepCall")
                else:
                    fileBadvaluedict[tempfilename] = {}
                    fileBadvaluedict[tempfilename]['badSmellNum'] = 1
                    fileBadvaluedict[tempfilename]['badSmellKindNum'] = set()
                    fileBadvaluedict[tempfilename]['badSmellKindNum'].add("overDeepCall")
                num += 1
                filenum.add(tempfilename)
                detectionResults.append({
                    "fileName": i[0].split("/")[-1].split(':')[0],
                    "funcName": i[0].split(':')[-1],
                    "funcLength": str(len(i))
                })
            valuelist.append(len(i))
        overDeepCall['num'] = num
        statisticTable.append(overDeepCall)
        tempend = time.perf_counter()
        otherInfo = []
        otherInfo.append({
            "name": "坏味检测时间",
            "value": str(round((tempend - tempstart), 3)) + "秒"
        })
        otherInfo.append({
            "name": "含坏味文件数",
            "value": str(len(filenum)) + "个"
        })
        otherInfo.append({
            "name": "该坏味文件占比",
            "value": str(round(len(filenum) / int(projectinfo['projectInfo']['fileNumber']), 3))
        })
        otherInfo.append({
            "name": "调用深度",
            "value": str(0 if valuelist == [] else max(valuelist))
        })
        bs.cpp_overDeepCall = str(json.dumps({
            "name": "过深调用",
            "def": "函数调用链长度过长，过长函数调用链容易导致空指针异常，并且在维护过程中需要同时修改多处地方",
            "key": "overDeepCall",
            "totalNum": len(detectionResults),
            "threshold": tempthreshold,
            "title": {
                "fileName": "文件名",
                "funcName": "函数名",
                "funcLength": "调用深度"
            },
            "detectionResults": detectionResults,
            "otherInfo": otherInfo
        })).encode()
        result.append({
            "name": "过深调用",
            "def": "函数调用链长度过长，过长函数调用链容易导致空指针异常，并且在维护过程中需要同时修改多处地方",
            "key": "overDeepCall",
            "totalNum": len(detectionResults),
            "threshold": tempthreshold,
            "title": {
                "fileName": "文件名",
                "funcName": "函数名",
                "funcLength": "调用深度"
            },
            "detectionResults": detectionResults[:20],
            "otherInfo": otherInfo
        })

    # 扇入扇出代码坏味?
    tempstart = time.perf_counter()
    detectionResults = []
    valuelist = []
    filenum = set()
    overInOutDegreeFunc = {"name": "扇入扇出代码坏味"}
    if 'overInOutDegreeFunc' in threshold.keys():
        tempthreshold = threshold["overInOutDegreeFunc"]
        num = set()
        for i in data['overOutDegreeFunc']:
            tempfilename = ":".join(i['name'].split(":")[:2])

            if tempfilename.endswith(ctyprlist):
                continue
            if float(i['val']) > int(tempthreshold):

                if tempfilename in fileBadvaluedict.keys():
                    fileBadvaluedict[tempfilename]['badSmellNum'] += 1
                    fileBadvaluedict[tempfilename]['badSmellKindNum'].add("overInOutDegreeFunc")
                else:
                    fileBadvaluedict[tempfilename] = {}
                    fileBadvaluedict[tempfilename]['badSmellNum'] = 1
                    fileBadvaluedict[tempfilename]['badSmellKindNum'] = set()
                    fileBadvaluedict[tempfilename]['badSmellKindNum'].add("overInOutDegreeFunc")
                num.add(i['name'])
                filenum.add(tempfilename)
                detectionResults.append({
                    "fileName": i['name'].split("/")[-1].split(':')[0],
                    "funcName": i['name'].split(':')[-1],
                    "funcLength": str(i['val'])
                })
            valuelist.append(float(i['val']))
        for i in data['overInDegreeFunc']:
            tempfilename = ":".join(i['name'].split(":")[:2])

            if tempfilename.endswith(ctyprlist):
                continue
            if float(i['val']) > int(tempthreshold):

                if tempfilename in fileBadvaluedict.keys():
                    fileBadvaluedict[tempfilename]['badSmellNum'] += 1
                    fileBadvaluedict[tempfilename]['badSmellKindNum'].add("overInOutDegreeFunc")
                else:
                    fileBadvaluedict[tempfilename] = {}
                    fileBadvaluedict[tempfilename]['badSmellNum'] = 1
                    fileBadvaluedict[tempfilename]['badSmellKindNum'] = set()
                    fileBadvaluedict[tempfilename]['badSmellKindNum'].add("overInOutDegreeFunc")
                num.add(i['name'])
                filenum.add(tempfilename)
                detectionResults.append({
                    "fileName": i['name'].split("/")[-1].split(':')[0],
                    "funcName": i['name'].split(':')[-1],
                    "funcLength": str(i['val'])
                })
            valuelist.append(float(i['val']))
        overInOutDegreeFunc['num'] = len(num)
        statisticTable.append(overInOutDegreeFunc)
        tempend = time.perf_counter()
        otherInfo = []
        otherInfo.append({
            "name": "坏味检测时间",
            "value": str(round((tempend - tempstart), 3)) + "秒"
        })
        otherInfo.append({
            "name": "含坏味文件数",
            "value": str(len(filenum)) + "个"
        })
        otherInfo.append({
            "name": "该坏味文件占比",
            "value": str(round(len(filenum) / int(projectinfo['projectInfo']['fileNumber']), 3))
        })
        otherInfo.append({
            "name": "最长函数长度",
            "value": str(0 if valuelist == [] else max(valuelist)) + "行"
        })
        bs.cpp_overInOutDegreeFunc = str(json.dumps({
            "name": "扇入扇出",
            "def": "函数扇出或扇入过大。",
            "key": "overInOutDegreeFunc",
            "totalNum": len(detectionResults),
            "threshold": tempthreshold,
            "title": {
                "fileName": "文件名",
                "funcName": "函数名",
                "funcLength": "扇入扇出"
            },
            "detectionResults": detectionResults,
            "otherInfo": otherInfo
        })).encode()
        result.append({
            "name": "扇入扇出",
            "def": "函数扇出或扇入过大。",
            "key": "overInOutDegreeFunc",
            "totalNum": len(detectionResults),
            "threshold": tempthreshold,
            "title": {
                "fileName": "文件名",
                "funcName": "函数名",
                "funcLength": "扇入扇出"
            },
            "detectionResults": detectionResults[:20],
            "otherInfo": otherInfo
        })

    # 代码克隆代码坏味
    tempstart = time.perf_counter()
    detectionResults = []
    valuelist = []
    filenum = set()

    textCopy = {"name": "代码克隆代码坏味"}
    if 'textCopy' in threshold.keys():
        tempthreshold = float(threshold['textCopy'])
        num = 0

        funclist = list(projectinfo['funcInfo'].keys())
        functtuple = list(itertools.combinations(funclist, 2))
        for i in functtuple:
            tempfilename1 = ":".join(i[0].split(":")[:2])
            tempfilename2 = ":".join(i[1].split(":")[:2])
            if tempfilename1.endswith(ctyprlist):
                continue
            func1 = i[0]
            func2 = i[1]
            str1 = ''
            for j in projectinfo['funcInfo'][func1]['codeText']:
                str1 += j
            str2 = ''
            for j in projectinfo['funcInfo'][func2]['codeText']:
                str2 += j
            sim = Levenshtein_sim(str1, str2)
            if sim > float(threshold['textCopy']):
                # index = func1.rfind(':')
                # index = func1[:index].rfind(":")
                # tempfilename1 = func1[:index]
                # tempfilename1 = func1.split(":")[0]
                # tempfilename2 = func2.split(":")[1]
                # index = func2.rfind(':')
                # index = func2[:index].rfind(":")
                # tempfilename2 = func2[:index]
                if tempfilename1 in fileBadvaluedict.keys():
                    fileBadvaluedict[tempfilename1]['badSmellNum'] += 1
                    fileBadvaluedict[tempfilename1]['badSmellKindNum'].add("textCopy")
                else:
                    fileBadvaluedict[tempfilename1] = {}
                    fileBadvaluedict[tempfilename1]['badSmellNum'] = 1
                    fileBadvaluedict[tempfilename1]['badSmellKindNum'] = set()
                    fileBadvaluedict[tempfilename1]['badSmellKindNum'].add("textCopy")
                if not tempfilename2.endswith(ctyprlist):
                    if tempfilename2 in fileBadvaluedict.keys():
                        fileBadvaluedict[tempfilename2]['badSmellNum'] += 1
                        fileBadvaluedict[tempfilename2]['badSmellKindNum'].add("textCopy")
                    else:
                        fileBadvaluedict[tempfilename2] = {}
                        fileBadvaluedict[tempfilename2]['badSmellNum'] = 1
                        fileBadvaluedict[tempfilename2]['badSmellKindNum'] = set()
                        fileBadvaluedict[tempfilename2]['badSmellKindNum'].add("textCopy")

                num += 1
                filenum.add(tempfilename1)
                if not tempfilename2.endswith(ctyprlist):
                    filenum.add(tempfilename2)
                detectionResults.append({
                    "fileNameA": func1.split("/")[-1].split(':')[0],
                    "funcNameA": func1.split(':')[-1],
                    "fileNameB": func2.split("/")[-1].split(':')[0],
                    "funcNameB": func2.split(':')[-1],
                    "similarity": str(round(sim, 4))
                })
            valuelist.append(round(float(sim), 4))

        for i in data['funcCopy']['cfg_copy']:
            tempfilename1 = ":".join(i[0].split(":")[:2])
            tempfilename2 = ":".join(i[1].split(":")[:2])
            if tempfilename1.endswith(ctyprlist):
                continue
            func1 = i[0]
            func2 = i[1]
            # tempfilename1 = ":".join(i[0].split(":")[:2])
            # tempfilename1 = func1.split(":")[0]
            # tempfilename2 = func2.split(":")[1]
            # tempfilename2 = ":".join(i[1].split(":")[:2])
            if tempfilename1 in fileBadvaluedict.keys():
                fileBadvaluedict[tempfilename1]['badSmellNum'] += 1
                fileBadvaluedict[tempfilename1]['badSmellKindNum'].add("textCopy")
            else:
                fileBadvaluedict[tempfilename1] = {}
                fileBadvaluedict[tempfilename1]['badSmellNum'] = 1
                fileBadvaluedict[tempfilename1]['badSmellKindNum'] = set()
                fileBadvaluedict[tempfilename1]['badSmellKindNum'].add("textCopy")
            if not tempfilename2.endswith(ctyprlist):
                if tempfilename2 in fileBadvaluedict.keys():
                    fileBadvaluedict[tempfilename2]['badSmellNum'] += 1
                    fileBadvaluedict[tempfilename2]['badSmellKindNum'].add("textCopy")
                else:
                    fileBadvaluedict[tempfilename2] = {}
                    fileBadvaluedict[tempfilename2]['badSmellNum'] = 1
                    fileBadvaluedict[tempfilename2]['badSmellKindNum'] = set()
                    fileBadvaluedict[tempfilename2]['badSmellKindNum'].add("textCopy")

            num += 1
            filenum.add(tempfilename1)
            if not tempfilename2.endswith(ctyprlist):
                filenum.add(tempfilename2)
            detectionResults.append({
                "fileNameA": func1.split("/")[-1].split(':')[0],
                "funcNameA": func1.split(':')[-1],
                "fileNameB": func2.split("/")[-1].split(':')[0],
                "funcNameB": func2.split(':')[-1],
                "similarity": 'cfgCopy'
            })

        textCopy['num'] = num
        statisticTable.append(textCopy)
        tempend = time.perf_counter()
        otherInfo = []
        otherInfo.append({
            "name": "坏味检测时间",
            "value": str(round((tempend - tempstart), 3)) + "秒"
        })
        otherInfo.append({
            "name": "含坏味文件数",
            "value": str(len(filenum)) + "个"
        })
        otherInfo.append({
            "name": "该坏味文件占比",
            "value": str(round(len(filenum) / int(projectinfo['projectInfo']['fileNumber']), 3))
        })
        otherInfo.append({
            "name": "最大代码相似度",
            "value": str(round(max(valuelist), 4))
        })
        bs.cpp_funcCopy = str(json.dumps({
            "name": "代码克隆",
            "def": "函数之间内容相似，进而可以删除其中一个函数",
            "key": "funcCopy",
            "totalNum": len(detectionResults),
            "threshold": tempthreshold,
            "title": {
                "fileNameA": '相似文件A',
                "funcNameA": '相似函数A',
                "fileNameB": '相似文件B',
                "funcNameB": '相似函数B',
                "similarity": '代码相似度'
            },
            "detectionResults": detectionResults,
            "otherInfo": otherInfo
        })).encode()
        result.append({
            "name": "代码克隆",
            "def": "函数之间内容相似，进而可以删除其中一个函数",
            "key": "funcCopy",
            "totalNum": len(detectionResults),
            "threshold": tempthreshold,
            "title": {
                "fileNameA": '相似文件A',
                "funcNameA": '相似函数A',
                "fileNameB": '相似文件B',
                "funcNameB": '相似函数B',
                "similarity": '代码相似度'
            },
            "detectionResults": detectionResults[:20],
            "otherInfo": otherInfo
        })

    # 圈复杂度代码坏味
    tempstart = time.perf_counter()
    detectionResults = []
    valuelist = []
    filenum = set()

    overCyclComplexityFunc = {"name": "圈复杂度代码坏味"}
    if 'overCyclComplexityFunc' in threshold.keys():
        tempthreshold = threshold['overCyclComplexityFunc']
        num = 0
        for i in data['overCyclComplexityFunc']:
            tempfilename = ":".join(i['name'].split(":")[:2])

            if tempfilename.endswith(ctyprlist):
                continue
            if float(i['val']) > int(tempthreshold):

                if tempfilename in fileBadvaluedict.keys():
                    fileBadvaluedict[tempfilename]['badSmellNum'] += 1
                    fileBadvaluedict[tempfilename]['badSmellKindNum'].add("overCyclComplexityFunc")
                else:
                    fileBadvaluedict[tempfilename] = {}
                    fileBadvaluedict[tempfilename]['badSmellNum'] = 1
                    fileBadvaluedict[tempfilename]['badSmellKindNum'] = set()
                    fileBadvaluedict[tempfilename]['badSmellKindNum'].add("overCyclComplexityFunc")
                num += 1
                filenum.add(tempfilename)
                detectionResults.append({
                    "fileName": i['name'].split("/")[-1].split(':')[0],
                    "funcName": i['name'].split(':')[-1],
                    "funcLength": str(i['val'])
                })
            valuelist.append(float(i['val']))
        overCyclComplexityFunc['num'] = num
        statisticTable.append(overCyclComplexityFunc)
        tempend = time.perf_counter()
        otherInfo = []
        otherInfo.append({
            "name": "坏味检测时间",
            "value": str(round((tempend - tempstart), 3)) + "秒"
        })
        otherInfo.append({
            "name": "含坏味文件数",
            "value": str(len(filenum)) + "个"
        })
        otherInfo.append({
            "name": "该坏味文件占比",
            "value": str(round(len(filenum) / int(projectinfo['projectInfo']['fileNumber']), 3))
        })
        otherInfo.append({
            "name": "最大圈复杂度",
            "value": str(0 if valuelist == [] else max(valuelist))
        })
        bs.cpp_overCyclComplexityFunc = str(json.dumps({
            "name": "圈复杂度",
            "def": "函数圈复杂度过高",
            "key": "overCyclComplexityFunc",
            "totalNum": len(detectionResults),
            "threshold": tempthreshold,
            "title": {
                "fileName": "文件名",
                "funcName": "函数名",
                "funcLength": "圈复杂度"
            },
            "detectionResults": detectionResults,
            "otherInfo": otherInfo
        })).encode()
        result.append({
            "name": "圈复杂度",
            "def": "函数圈复杂度过高",
            "key": "overCyclComplexityFunc",
            "totalNum": len(detectionResults),
            "threshold": tempthreshold,
            "title": {
                "fileName": "文件名",
                "funcName": "函数名",
                "funcLength": "圈复杂度"
            },
            "detectionResults": detectionResults[:20],
            "otherInfo": otherInfo
        })
    # 冗赘类代码坏味
    tempstart = time.perf_counter()
    detectionResults = []
    valuelist = []
    filenum = set()
    lazyClass = {"name": "冗赘类代码坏味"}
    if 'lazyClass' in threshold.keys():
        tempthreshold = threshold['lazyClass']
        num = 0
        for i in data['LargeClass']:
            tempfilename = ":".join(i['name'].split(":")[:2])

            if tempfilename.endswith(ctyprlist):
                continue
            if float(i['val']) > int(tempthreshold):

                if tempfilename in fileBadvaluedict.keys():
                    fileBadvaluedict[tempfilename]['badSmellNum'] += 1
                    fileBadvaluedict[tempfilename]['badSmellKindNum'].add("lazyClass")
                else:
                    fileBadvaluedict[tempfilename] = {}
                    fileBadvaluedict[tempfilename]['badSmellNum'] = 1
                    fileBadvaluedict[tempfilename]['badSmellKindNum'] = set()
                    fileBadvaluedict[tempfilename]['badSmellKindNum'].add("lazyClass")
                num += 1
                filenum.add(tempfilename)
                detectionResults.append({
                    "fileName": i['name'].split("/")[-1].split(':')[0],
                    "funcName": i['name'].split(':')[-1],
                    "funcLength": str(i['val'])
                })
            valuelist.append(float(i['val']))
        lazyClass['num'] = num
        statisticTable.append(lazyClass)
        tempend = time.perf_counter()
        otherInfo = []
        otherInfo.append({
            "name": "坏味检测时间",
            "value": str(round((tempend - tempstart), 3)) + "秒"
        })
        otherInfo.append({
            "name": "含坏味文件数",
            "value": str(len(filenum)) + "个"
        })
        otherInfo.append({
            "name": "该坏味文件占比",
            "value": str(round(len(filenum) / int(projectinfo['projectInfo']['fileNumber']), 3))
        })
        otherInfo.append({
            "name": "最大冗赘类指标值",
            "value": str(0 if valuelist == [] else max(valuelist))
        })
        bs.cpp_lazyClass = str(json.dumps({
            "name": "冗赘类",
            "def": "做的事情太少的类",
            "key": "lazyClass",
            "totalNum": len(detectionResults),
            "threshold": tempthreshold,
            "title": {
                "fileName": "文件名",
                "funcName": "类名",
                "funcLength": "冗赘类指标值(未被引用的成员变量数量+未被引用的成员方法数量)/(总成员变量数量+总成员方法数量)"
            },
            "detectionResults": detectionResults,
            "otherInfo": otherInfo
        })).encode()
        result.append({
            "name": "冗赘类",
            "def": "做的事情太少的类",
            "key": "lazyClass",
            "totalNum": len(detectionResults),
            "threshold": tempthreshold,
            "title": {
                "fileName": "文件名",
                "funcName": "类名",
                "funcLength": "冗赘类指标值(未被引用的成员变量数量+未被引用的成员方法数量)/(总成员变量数量+总成员方法数量)"
            },
            "detectionResults": detectionResults[:20],
            "otherInfo": otherInfo
        })

    # 过大的类代码坏味
    tempstart = time.perf_counter()
    detectionResults = []
    valuelist = []
    filenum = set()
    LargeClass = {"name": "过大的类代码坏味"}
    if 'LargeClass' in threshold.keys():
        tempthreshold = threshold['LargeClass']
        num = 0
        for i in data['LargeClass']:
            tempfilename = ":".join(i['name'].split(":")[:2])

            if tempfilename.endswith(ctyprlist):
                continue
            if float(i['val']) > int(tempthreshold):

                if tempfilename in fileBadvaluedict.keys():
                    fileBadvaluedict[tempfilename]['badSmellNum'] += 1
                    fileBadvaluedict[tempfilename]['badSmellKindNum'].add("LargeClass")
                else:
                    fileBadvaluedict[tempfilename] = {}
                    fileBadvaluedict[tempfilename]['badSmellNum'] = 1
                    fileBadvaluedict[tempfilename]['badSmellKindNum'] = set()
                    fileBadvaluedict[tempfilename]['badSmellKindNum'].add("LargeClass")
                num += 1
                filenum.add(tempfilename)
                detectionResults.append({
                    "fileName": i['name'].split("/")[-1].split(':')[0],
                    "funcName": i['name'].split(':')[-1],
                    "funcLength": str(i['val'])
                })
            valuelist.append(float(i['val']))
        LargeClass['num'] = num
        statisticTable.append(LargeClass)
        tempend = time.perf_counter()
        otherInfo = []
        otherInfo.append({
            "name": "坏味检测时间",
            "value": str(round((tempend - tempstart), 3)) + "秒"
        })
        otherInfo.append({
            "name": "含坏味文件数",
            "value": str(len(filenum)) + "个"
        })
        otherInfo.append({
            "name": "该坏味文件占比",
            "value": str(round(len(filenum) / int(projectinfo['projectInfo']['fileNumber']), 3))
        })
        otherInfo.append({
            "name": "最长类行数",
            "value": str(0 if valuelist == [] else max(valuelist)) + "行"
        })
        bs.cpp_largeClass = str(json.dumps({
            "name": "过大的类",
            "def": "类中出现过多实例变量",
            "key": "largeClass",
            "totalNum": len(detectionResults),
            "threshold": tempthreshold,
            "title": {
                "fileName": "文件名",
                "funcName": "类名",
                "funcLength": "类行数"
            },
            "detectionResults": detectionResults,
            "otherInfo": otherInfo
        })).encode()
        result.append({
            "name": "过大的类",
            "def": "类中出现过多实例变量",
            "key": "largeClass",
            "totalNum": len(detectionResults),
            "threshold": tempthreshold,
            "title": {
                "fileName": "文件名",
                "funcName": "类名",
                "funcLength": "类行数"
            },
            "detectionResults": detectionResults[:20],
            "otherInfo": otherInfo
        })

    # 散弹式修改代码坏味
    tempstart = time.perf_counter()
    detectionResults = []
    valuelist = []
    filenum = set()
    ShotgunSurgery = {"name": "散弹式修改代码坏味"}
    if 'ShotgunSurgery' in threshold.keys():
        tempthreshold = threshold['ShotgunSurgery']
        num = 0
        for i in data['ShotgunSurgery']:
            tempfilename = ":".join(i['name'].split(":")[:2])

            if tempfilename.endswith(ctyprlist):
                continue
            if float(i['val']) > int(tempthreshold):

                if tempfilename in fileBadvaluedict.keys():
                    fileBadvaluedict[tempfilename]['badSmellNum'] += 1
                    fileBadvaluedict[tempfilename]['badSmellKindNum'].add("ShotgunSurgery")
                else:
                    fileBadvaluedict[tempfilename] = {}
                    fileBadvaluedict[tempfilename]['badSmellNum'] = 1
                    fileBadvaluedict[tempfilename]['badSmellKindNum'] = set()
                    fileBadvaluedict[tempfilename]['badSmellKindNum'].add("ShotgunSurgery")
                num += 1
                filenum.add(tempfilename)
                detectionResults.append({
                    "fileName": i['name'].split("/")[-1].split(':')[0],
                    "funcName": i['name'].split(':')[-1],
                    "funcLength": str(i['val'])
                })
            valuelist.append(float(i['val']))
        ShotgunSurgery['num'] = num
        statisticTable.append(ShotgunSurgery)
        tempend = time.perf_counter()
        otherInfo = []
        otherInfo.append({
            "name": "坏味检测时间",
            "value": str(round((tempend - tempstart), 3)) + "秒"
        })
        otherInfo.append({
            "name": "含坏味文件数",
            "value": str(len(filenum)) + "个"
        })
        otherInfo.append({
            "name": "该坏味文件占比",
            "value": str(round(len(filenum) / int(projectinfo['projectInfo']['fileNumber']), 3))
        })
        otherInfo.append({
            "name": "最大散弹式修改指标值",
            "value": str(0 if valuelist == [] else max(valuelist))
        })
        bs.cpp_shotgunSurgery = str(json.dumps({
            "name": "散弹式修改",
            "def": "在修改代码时，需要在多个不同的地方做出许多小的修改",
            "key": "shotgunSurgery",
            "totalNum": len(detectionResults),
            "threshold": tempthreshold,
            "title": {
                "fileName": "文件名",
                "funcName": "类名",
                "funcLength": "散弹式修改指标值(所有成员变量被引用的次数+所有成员方法被引用的次数)"
            },
            "detectionResults": detectionResults,
            "otherInfo": otherInfo
        })).encode()
        result.append({
            "name": "散弹式修改",
            "def": "在修改代码时，需要在多个不同的地方做出许多小的修改",
            "key": "shotgunSurgery",
            "totalNum": len(detectionResults),
            "threshold": tempthreshold,
            "title": {
                "fileName": "文件名",
                "funcName": "类名",
                "funcLength": "散弹式修改指标值(所有成员变量被引用的次数+所有成员方法被引用的次数)"
            },
            "detectionResults": detectionResults[:20],
            "otherInfo": otherInfo
        })
    # 依恋情节代码坏味
    tempstart = time.perf_counter()
    detectionResults = []
    valuelistself = []
    valuelistother = []
    filenum = set()
    FeatureEnvy = {"name": "依恋情节代码坏味"}
    if 'FeatureEnvy' in threshold.keys():
        tempthreshold = int(threshold["FeatureEnvy"])
        num = 0
        for i in data['FeatureEnvy']:
            tempfilename = ":".join(i['name'].split(":")[:2])

            if tempfilename.endswith(ctyprlist):
                continue
            if float(i['maxSelf']) > tempthreshold or float(i['maxOther']) > tempthreshold:

                if tempfilename in fileBadvaluedict.keys():
                    fileBadvaluedict[tempfilename]['badSmellNum'] += 1
                    fileBadvaluedict[tempfilename]['badSmellKindNum'].add("FeatureEnvy")
                else:
                    fileBadvaluedict[tempfilename] = {}
                    fileBadvaluedict[tempfilename]['badSmellNum'] = 1
                    fileBadvaluedict[tempfilename]['badSmellKindNum'] = set()
                    fileBadvaluedict[tempfilename]['badSmellKindNum'].add("FeatureEnvy")
                num += 1
                filenum.add(tempfilename)
                detectionResults.append({
                    "fileName": i['name'].split("/")[-1].split(':')[0],
                    "funcName": i['name'].split(':')[-1],
                    "funcLength1": str(i['maxSelf']),
                    "funcLength1": str(i['maxOther'])
                })
            valuelistself.append(float(i['maxSelf']))
            valuelistother.append(float(i['maxOther']))
        FeatureEnvy['num'] = num
        statisticTable.append(FeatureEnvy)
        tempend = time.perf_counter()
        otherInfo = []
        if valuelistself == []:
            max_valuelistself = 0
        else:
            max_valuelistself = max(valuelistself)
        if valuelistother == []:
            max_valuelistother = 0
        else:
            max_valuelistother = max(valuelistother)
        otherInfo.append({
            "name": "坏味检测时间",
            "value": str(round((tempend - tempstart), 3)) + "秒"
        })
        otherInfo.append({
            "name": "含坏味文件数",
            "value": str(len(filenum)) + "个"
        })
        otherInfo.append({
            "name": "该坏味文件占比",
            "value": str(round(len(filenum) / int(projectinfo['projectInfo']['fileNumber']), 3))
        })
        otherInfo.append({
            "name": "最大对自身变量的最大变量引用值",
            "value": str(max_valuelistself)
        })
        otherInfo.append({
            "name": "最大对Other中最大的变量引用值",
            "value": str(max_valuelistother)
        })
        bs.cpp_featureEnvy = str(json.dumps({
            "name": "依恋情节",
            "def": "一个类的方法过多地使用了另一个类地方法",
            "key": "featureEnvy",
            "totalNum": len(detectionResults),
            "threshold": tempthreshold,
            "title": {
                "fileName": "文件名",
                "funcName": "类名",
                "funcLength1": "对自身变量的最大变量引用值",
                "funcLength2": "对Other中最大的变量引用值"
            },
            "detectionResults": detectionResults,
            "otherInfo": otherInfo
        })).encode()
        result.append({
            "name": "依恋情节",
            "def": "一个类的方法过多地使用了另一个类地方法",
            "key": "featureEnvy",
            "totalNum": len(detectionResults),
            "threshold": tempthreshold,
            "title": {
                "fileName": "文件名",
                "funcName": "类名",
                "funcLength1": "对自身变量的最大变量引用值",
                "funcLength2": "对Other中最大的变量引用值"
            },
            "detectionResults": detectionResults[:20],
            "otherInfo": otherInfo
        })

    # 纯数据类代码坏味
    tempstart = time.perf_counter()
    detectionResults = []
    valuelist = []
    filenum = set()
    DataClass = {"name": "纯数据类代码坏味",
                 "num": len(data['DataClass'])
                 }
    for i in data['DataClass']:
        tempfilename = ":".join(i.split(":")[:2])
        if tempfilename.endswith(ctyprlist):
            continue
        if tempfilename in fileBadvaluedict.keys():
            fileBadvaluedict[tempfilename]['badSmellNum'] += 1
            fileBadvaluedict[tempfilename]['badSmellKindNum'].add("DataClass")
        else:
            fileBadvaluedict[tempfilename] = {}
            fileBadvaluedict[tempfilename]['badSmellNum'] = 1
            fileBadvaluedict[tempfilename]['badSmellKindNum'] = set()
            fileBadvaluedict[tempfilename]['badSmellKindNum'].add("DataClass")
        filenum.add(tempfilename)
        detectionResults.append({
            "fileName": i.split("/")[-1].split(':')[0],
            "funcName": i.split(':')[-1],
        })
    statisticTable.append(DataClass)
    tempend = time.perf_counter()
    otherInfo = []
    otherInfo.append({
        "name": "坏味检测时间",
        "value": str(round((tempend - tempstart), 3)) + "秒"
    })
    otherInfo.append({
        "name": "含坏味文件数",
        "value": str(len(filenum)) + "个"
    })
    otherInfo.append({
        "name": "该坏味文件占比",
        "value": str(round(len(filenum) / int(projectinfo['projectInfo']['fileNumber']), 3))
    })
    bs.cpp_dataClass = str(json.dumps({
        "name": "纯数据类",
        "def": "仅用于存储数据的类，没有任何行为或逻辑的特殊类",
        "key": "dataClass",
        "totalNum": len(detectionResults),
        "threshold": tempthreshold,
        "title": {
            "fileName": "文件名",
            "funcName": "类名",
        },
        "detectionResults": detectionResults,
        "otherInfo": otherInfo
    })).encode()
    result.append({
        "name": "纯数据类",
        "def": "仅用于存储数据的类，没有任何行为或逻辑的特殊类",
        "key": "dataClass",
        "totalNum": len(detectionResults),
        "threshold": tempthreshold,
        "title": {
            "fileName": "文件名",
            "funcName": "类名",
        },
        "detectionResults": detectionResults[:20],
        "otherInfo": otherInfo
    })
    CPPendtime = time.perf_counter()
    CPPtime = CPPendtime - CPPstarttime
    fileBadvalue = get_filebadvalue(fileBadvaluedict)
    BadSmellResult['fileBadvalue'] = fileBadvalue

    # statisticTable
    BadSmellResult['statisticTable'] = statisticTable

    # result
    BadSmellResult['result'] = result
    # C++
    # NPF
    BadSmellResult['NPF'] = int(projectinfo['projectInfo']['fileNumber'])

    # NCFBS
    numC = 0
    numCPP = 0
    clist = projectinfo['projectInfo']['fileTypes']['c']
    cpplist = projectinfo['projectInfo']['fileTypes']['cpp']
    cheaderlist = (".h")
    cppheaderlist = (".H", ".hh", ".hpp", ".hxx")
    for i in fileBadvaluedict:
        if i.endswith(cheaderlist):
            numC += 1
        elif i.endswith(cppheaderlist):
            numCPP += 1
    # for i in fileBadvaluedict:

        if i in clist:
            numC += 1
        elif i in cpplist:
            numCPP += 1
    BadSmellResult['NCFBS'] = numCPP

    # NCF
    BadSmellResult['NCF'] = len(projectinfo['projectInfo']['fileTypes']['cpp'])

    # RNCF
    BadSmellResult['RNCF'] = round(100 * BadSmellResult['NCF'] / BadSmellResult['NPF'], 2)

    # RNCFBS
    BadSmellResult['RNCFBS'] = round(100 * BadSmellResult['NCFBS'] / BadSmellResult['NPF'], 2)

    # DT
    end = time.perf_counter()
    BadSmellResult['DT'] = round((end - start), 5)
    return BadSmellResult


def get_filebadvalue(valuedict):
    filebadvalue = []
    for key in valuedict.keys():
        filebadvalue.append({
            "filename": key,
            "badSmellNum": valuedict[key]["badSmellNum"],
            "badSmellKindNum": len(valuedict[key]["badSmellKindNum"])
        })
    return filebadvalue


def Levenshtein_sim(str1, str2):
    levD = float(Levenshtein.distance(str1, str2))
    return 1 - 2 * levD / (len(str1 + str2))


def get_deep_call(Info, tmp_call=[]):
    funcInfo = Info['funcInfo']
    funcname = tmp_call[-1]
    if not funcInfo[funcname]['fanOut']:
        return [tmp_call]
    res = []
    for func in funcInfo[funcname]['fanOut']:
        if func in tmp_call:
            res.append(tmp_call)
        else:
            call = copy.deepcopy(tmp_call)
            call.append(func)
            res.extend(get_deep_call(Info, call))
    return res


def Bad_smell_from_function(Info):
    bad_smell = {}
    funcInfo = Info['funcInfo']
    # overLongFunc
    bad_smell['overLongFunc'] = []
    # overLongParam
    bad_smell['overLongParam'] = []
    # overCommentLineFunc
    bad_smell['overCommentLineFunc'] = []
    # overCyclComplexityFunc
    bad_smell['overCyclComplexityFunc'] = []
    # overOutDegreeFunc
    bad_smell['overOutDegreeFunc'] = []
    # overInDegreeFunc
    bad_smell['overInDegreeFunc'] = []
    bad_smell['funcCopy'] = {}
    # overDeepCall
    bad_smell['overDeepCall'] = []

    for func in funcInfo.keys():
        bad_smell['overLongFunc'].append(
            {
                'name': func,
                'val': funcInfo[func]['codeInfo']['codeLine']
            }
        )
        bad_smell['overLongParam'].append(
            {
                'name': func,
                'val': len(funcInfo[func]['paramList'])
            }
        )
        bad_smell['overCommentLineFunc'].append(
            {
                'name': func,
                'val': funcInfo[func]['codeInfo']['commentLine']
            }
        )
        bad_smell['overCyclComplexityFunc'].append(
            {
                'name': func,
                'val': funcInfo[func]['cyclComplexity']
            }
        )
        bad_smell['overOutDegreeFunc'].append(
            {
                'name': func,
                'val': len(funcInfo[func]['fanOut'])
            }
        )
        bad_smell['overInDegreeFunc'].append(
            {
                'name': func,
                'val': len(funcInfo[func]['fanIn'])
            }
        )
        if funcInfo[func]['fanOut']:
            deepcall = get_deep_call(Info, [func, ])
            bad_smell['overDeepCall'].extend(deepcall)

    return bad_smell


def class_to_badsmell(Info, badsmell):
    classInfo = Info['classInfo']
    funcInfo = Info['funcInfo']

    badsmell['lazyClass'] = None
    badsmell['LargeClass'] = None
    badsmell['ShotgunSurgery'] = None
    badsmell['FeatureEnvy'] = None
    badsmell['DataClass'] = None

    lazyClass = []
    LargeClass = []
    ShotgunSurgery = []
    FeatureEnvy = []
    DataClass = []

    quote_dict = {}
    for classname in classInfo.keys():
        quote_dict[classname] = {}
    for classname in classInfo.keys():
        variable_list = classInfo[classname]['variable_list']
        for variable in variable_list:
            decl_class = variable['decl_class']
            if decl_class != ':':
                if variable['name'] in quote_dict[decl_class]:
                    quote_dict[decl_class][variable['name']] += 1
                else:
                    quote_dict[decl_class][variable['name']] = 1

    for classname in classInfo.keys():
        # 冗余类
        mem_varnum = 0
        mem_varlist = []
        mem_methodnum = 0
        quote_varset = set()
        quote_varnum = 0
        quote_methodset = set()
        quote_methodnum = 0

        mem_varnum = len(classInfo[classname]['mem_var'])
        # quote_varnum = len(quote_dict[classname])
        mem_methodnum = len(classInfo[classname]['mem_method'])

        for var_name in classInfo[classname]['mem_var']:
            mem_varlist.append(var_name['this_name'])

        # for tmp_var in classInfo[classname]['variable_list']:
        #     var_name = tmp_var['name']
        #     var_decl = tmp_var['decl_class']
        #     if var_decl == classname :
        #         quote_varnum += 1
        #         quote_varset.add(var_name)

        check = True
        data = {}
        for tmp_method in classInfo[classname]['mem_method']:
            method_name = tmp_method['this_loc'] + tmp_method['name']
            quote_methodnum += tmp_method["fanIn_num"]
            if tmp_method["fanIn_num"] == 0:
                quote_methodset.add(method_name)
            # method_name = tmp_method['this_loc'] + tmp_method['name']
            # if method_name in funcInfo.keys():
            #     fanIn = len(funcInfo[method_name]['fanIn'])
            #     if fanIn > 0:
            #         quote_methodset.add(method_name)

            if check:
                tmp_dict = {}
                for tmp_var in tmp_method['variable_list']:
                    decl_class = tmp_var['decl_class']
                    if decl_class != ":":
                        if decl_class not in tmp_dict.keys():
                            tmp_dict[decl_class] = 1
                        else:
                            tmp_dict[decl_class] += 1

                if classname in tmp_dict.keys():
                    maxself = tmp_dict[classname]
                else:
                    maxself = 0
                for key in tmp_dict.keys():
                    if tmp_dict[key] > maxself:
                        data['name'] = classname
                        data['maxSelf'] = maxself
                        data['maxOther'] = tmp_dict[key]
                        data['Other'] = key
                        check = False
                        break

        val = (mem_varnum - len(quote_dict[classname]) + len(quote_methodset)) / (mem_varnum+mem_methodnum) if (mem_varnum+mem_methodnum) else 0
        lazyClass.append({"name": classname,
                          "val": val})

        # 过大的类
        start_line = int(classInfo[classname]['start_line'])
        end_line = int(classInfo[classname]['end_line'])
        LargeClass.append({"name": classname,
                           "val": end_line - start_line + 1})

        # 霰弹式修改
        ShotgunSurgery.append({"name": classname,
                               "val": sum(quote_dict[classname].values()) + quote_methodnum})

        # 依恋情节
        if data:
            FeatureEnvy.append(data)

        # 数据类
        if len(classInfo[classname]['mem_method']) == 0:
            DataClass.append(classname)

    badsmell['lazyClass'] = lazyClass
    badsmell['LargeClass'] = LargeClass
    badsmell['ShotgunSurgery'] = ShotgunSurgery
    badsmell['FeatureEnvy'] = FeatureEnvy
    badsmell['DataClass'] = DataClass


if __name__ == '__main__':
    # num = 0
    # threshold = {
    #     'overLongFunc': num,
    #     'overLongParam': num,
    #     'overCommentLineFile': num,
    #     'overCyclComplexityFunc': num,
    #     'overInOutDegreeFunc': num,
    #     'overDeepCall': num,
    #     'lazyClass': num,
    #     'LargeClass': num,
    #     'ShotgunSurgery': num,
    #     'FeatureEnvy': num,
    #     'textCopy': num,
    #
    # }
    # encoding = get_file_encoding('main.json')
    # f = open('main.json', 'r', encoding=encoding)
    # content = f.read()
    # a = json.loads(content)
    # olddata = a
    # f.close()
    # encoding = get_file_encoding('badsmell.json')
    # f = open('badsmell.json', 'r', encoding=encoding)
    # content = f.read()
    # a = json.loads(content)
    # newdata = a
    # f.close()
    # badsmell = bad_smell_detection(newdata, olddata, threshold)
    # print(badsmell)
    # data = json.dumps(badsmell, indent=4, ensure_ascii=False)
    # with open('code/pre/badsmell.json', 'w', newline='\n') as f:
    #     f.write(data)
    badsmell = {}
    f = open('E:\program\wechat\WeChat Files\wxid_jb48j4gq3pde22\FileStorage\File/2023-09/classInfo(1).json', 'r', encoding='utf-8')
    content = f.read()
    a = json.loads(content)
    f = open('E:\program\wechat\WeChat Files\wxid_jb48j4gq3pde22\FileStorage\File/2023-09/funcInfo(1).json', 'r', encoding='utf-8')
    content = f.read()
    b = json.loads(content)
    Info = {"classInfo": a,
            "funcInfo": b}
    class_to_badsmell(Info, badsmell)
    print(badsmell)
