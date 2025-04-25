import ReqFunc
import Extract2_14 as ex
import ReqFunc as rq
import UserMannelFunc as um
import match2
import match2 as mt
import InterfaceDesignFunc
import UserMannelFunc
from Extract2_14 import *
import os

# global TestSpecFile
# global TestReportFile
# global RequirementFile
# global UserMannelFile
# global InterfaceDesignFile
# global MaintainFile
# global SystemDesignFile


def pin2g(UserTree, testcases, r2c):
    B_dict = {
        "id": "B",
        "type": "用户手册",
        "source": UserMannelFile + "/访问软件/软件的首次用户/安装和设置",
        "des": "为使用方便,用户尝试自定义安装规程的数量",
        "val": None
    }
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/系统安装的灵活性",
        "des": "用户成功自定义安装规程的数量",
        "val": None
    }
    B = len(UserMannelFunc.func_75(UserTree))

    if B:
        B_dict = {
            "id": "B",
            "type": "用户手册",
            "source": UserMannelFile + "/访问软件/软件的首次用户/安装和设置",
            "des": "为使用方便,用户尝试自定义安装规程的数量",
            "val": B
        }
    else:
        B_dict = {
            "id": "B",
            "type": "用户手册",
            "source": UserMannelFile + "/访问软件/软件的首次用户/安装和设置",
            "des": "为使用方便,用户尝试自定义安装规程的数量",
            "val": None
        }

    A = match2.getTestCases("系统安装的灵活性", testcases, r2c)
    num = 0

    if A:
        for key in A.keys():
            if A[key] == "通过":
                num += 1
        A_dict = {
            "id": "A",
            "type": "测试文档",
            "source": TestReportFile + "/系统安装的灵活性",
            "des": "用户成功自定义安装规程的数量",
            "val": num
        }
    else:
        A_dict = {
            "id": "A",
            "type": "测试文档",
            "source": TestReportFile + "/系统安装的灵活性",
            "des": "用户成功自定义安装规程的数量",
            "val": None
        }

    if A and B:
        res = num / B
        res_dict = {
            "val": res,
            "sub": [A_dict, B_dict]
        }
    else:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }

    return res_dict


def pin1g(UserTree, testcases, r2c):
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/系统安装时间",
        "des": "第i次安装所消耗的总工作时间",
        "val": None
    }
    B_dict = {
        "id": "B",
        "type": "测试文档",
        "source": TestReportFile + "/系统安装时间",
        "des": "第i次安装的预期时间",
        "val": None
    }
    try:
        res = match2.getTestCases("系统安装时间", testcases, r2c)
        N = len(res.keys())
        reskeys = list(res.keys())
        sublist = []
        val = 0
        for i in range(N):
            A_id = "A" + str(i)
            A_dict = {
                "id": A_id,
                "type": "测试文档",
                "source": TestReportFile + "/系统安装时间",
                "des": "第i次安装所消耗的总工作时间",
                "val": res[reskeys[i]]["res"]
            }

            B_id = "B" + str(i)
            B_dict = {
                "id": B_id,
                "type": "测试文档",
                "source": TestReportFile + "/系统安装时间",
                "des": "第i次安装的预期时间",
                "val": res[reskeys[i]]["pre"]
            }
            sublist.append(A_dict)
            sublist.append(B_dict)
            val += res[reskeys[i]]["res"] / res[reskeys[i]]["pre"]
        res_dict = {
            "val": val/N,
            "sub": sublist
        }
        return res_dict
    except:
        A_dict = {
            "id": "A",
            "type": "测试文档",
            "source": TestReportFile + "/系统安装时间",
            "des": "第i次安装所消耗的总工作时间",
            "val": None
        }
        B_dict = {
            "id": "B",
            "type": "测试文档",
            "source": TestReportFile + "/系统安装时间",
            "des": "第i次安装的预期时间",
            "val": None
        }
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }
        return res_dict


def pad3s(testcases, r2c):

    try:
        test = match2.getTestCases("运营环境的适应性", testcases, r2c)
        B = len(test.keys())
        B_dict = {
            "id": "B",
            "type": "测试文档",
            "source": TestReportFile + "/运营环境的适应性",
            "des": "在不同运营环境中测试的功能数量",
            "val": B
        }
        A = 0
        for val in test.values():
            if val == "通过":
                A += 1
        A_dict = {
            "id": "A",
            "type": "测试文档",
            "source": TestReportFile + "/运营环境的适应性",
            "des": "在带有用户环境的运营测试中,测试期间没有完成或结果没有达到要求的功能数量",
            "val": B - A
        }
        res_dict = {
            "val": A/B,
            "sub": [A_dict, B_dict]
        }
        return res_dict
    except:
        A_dict = {
            "id": "A",
            "type": "测试文档",
            "source": TestReportFile+"/运营环境的适应性",
            "des": "在带有用户环境的运营测试中,测试期间没有完成或结果没有达到要求的功能数量",
            "val": None
        }
        B_dict = {
            "id": "B",
            "type": "测试文档",
            "source": TestReportFile+"/运营环境的适应性",
            "des": "在不同运营环境中测试的功能数量",
            "val": None
        }
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }
        return res_dict


def pad2g(testcases, r2c):

    try:
        test = match2.getTestCases("软件环境的适应性", testcases, r2c)
        B = len(test.keys())
        B_dict = {
            "id": "B",
            "type": "测试文档",
            "source": TestReportFile+"/软件环境的适应性",
            "des": "不同系统软件环境下需要测试的功能数量",
            "val": B
        }
        A = 0
        for val in test.values():
            if val == "通过":
                A += 1
            A_dict = {
                "id": "A",
                "type": "测试文档",
                "source": TestReportFile+"/软件环境的适应性",
                "des": "测试期间未完成或结果没有达到要求的功能数量",
                "val": B - A
            }
            res_dict = {
                "val": A / B,
                "sub": [A_dict, B_dict]
            }
            return res_dict
    except:
        A_dict = {
            "id": "A",
            "type": "测试文档",
            "source": TestReportFile+"/软件环境的适应性",
            "des": "测试期间未完成或结果没有达到要求的功能数量",
            "val": None
        }
        B_dict = {
            "id": "B",
            "type": "测试文档",
            "source": TestReportFile+"/软件环境的适应性",
            "des": "不同系统软件环境下需要测试的功能数量",
            "val": None
        }
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }
        return res_dict


def pad1g(testcases, r2c):

    try:
        test = match2.getTestCases("硬件环境的适应性", testcases, r2c)
        B = len(test.keys())
        B_dict = {
            "id": "B",
            "type": "测试文档",
            "source": TestReportFile+"/硬件环境的适应性",
            "des": "不同硬件环境中需要测试的功能数量",
            "val": B
        }
        A = 0
        for val in test.values():
            if val == "通过":
                A += 1
            A_dict = {
                "id": "A",
                "type": "测试文档",
                "source": TestReportFile+"/硬件环境的适应性",
                "des": "测试期间未完成或结果没有达到要求的功能数量",
                "val": B - A
            }
            res_dict = {
                "val": A / B,
                "sub": [A_dict, B_dict]
            }
            return res_dict
    except:
        A_dict = {
            "id": "A",
            "type": "测试文档",
            "source": TestReportFile+"/硬件环境的适应性",
            "des": "测试期间未完成或结果没有达到要求的功能数量",
            "val": None
        }
        B_dict = {
            "id": "B",
            "type": "测试文档",
            "source": TestReportFile+"/硬件环境的适应性",
            "des": "不同硬件环境中需要测试的功能数量",
            "val": None
        }
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }
        return res_dict


def mte3s(TestReportTree):
    try:
        ans = match2.func69(TestReportTree)
        A_dict = {
            "id": "A",
            "type": "测试文档",
            "source": TestReportFile+"/测试结果概述/测试的重启动性",
            "des": "在逐步检测的期望点,维护方能够暂停并重启执行中的测试运行的事例数",
            "val": ans["A"]
        }
        B_dict = {
            "id": "B",
            "type": "测试文档",
            "source": TestReportFile+"/测试结果概述/测试的重启动性",
            "des": "执行中的测试运行能被暂停的事例数",
            "val": ans["B"]
        }
        res = ans["A"] / ans["B"]
        res_dict = {
            "val": res,
            "sub": [A_dict, B_dict]
        }
        return res_dict
    except:
        A_dict = {
            "id": "A",
            "type": "测试文档",
            "source": TestReportFile+"/测试结果概述/测试的重启动性",
            "des": "在逐步检测的期望点,维护方能够暂停并重启执行中的测试运行的事例数",
            "val": None
        }
        B_dict = {
            "id": "B",
            "type": "测试文档",
            "source": TestReportFile+"/测试结果概述/测试的重启动性",
            "des": "执行中的测试运行能被暂停的事例数",
            "val": None
        }
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }
        return res_dict


def mte2s(TestReportTree):
    try:
        ans = match2.func68(TestReportTree)
        A_dict = {
            "id": "A",
            "type": "测试文档",
            "source": TestReportFile+"/测试结果概述/测试的独立性",
            "des": "在依赖其他系统测试时,能被桩模拟的测试数量",
            "val": ans["A"]
        }
        B_dict = {
            "id": "B",
            "type": "测试文档",
            "source": TestReportFile+"/测试结果概述/测试的独立性",
            "des": "依赖其他系统的测试数量",
            "val": ans["B"]
        }
        res = ans["A"] / ans["B"]
        res_dict = {
            "val": res,
            "sub": [A_dict, B_dict]
        }
        return res_dict
    except:
        A_dict = {
            "id": "A",
            "type": "测试文档",
            "source": TestReportFile+"/测试结果概述/测试的独立性",
            "des": "在依赖其他系统测试时,能被桩模拟的测试数量",
            "val": None
        }
        B_dict = {
            "id": "B",
            "type": "测试文档",
            "source": TestReportFile+"/测试结果概述/测试的独立性",
            "des": "依赖其他系统的测试数量",
            "val": None
        }
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }
        return res_dict


def mte1g():
    '''
    源码
    :return:
    '''
    pass


def man3s(UserTree, testcases, r2c):
    try:
        list_b = UserMannelFunc.func_67(UserTree)
        B = len(list_b)
        B_dict = {
            "id": "B",
            "type": "用户手册",
            "source": UserMannelFile+"/~/消息/诊断消息/表格",
            "des": "需要实现的诊断功能数量",
            "val": B
        }
    except:
        B_dict = {
            "id": "B",
            "type": "用户手册",
            "source": UserMannelFile+"/~/消息/诊断消息/表格",
            "des": "需要实现的诊断功能数量",
            "val": None
        }
    try:
        test = match2.getTestCases("诊断消息的充分性", testcases, r2c)
        A = 0
        for val in test.values():
            if val == "通过":
                A += 1
        A_dict = {
            "id": "A",
            "type": "测试文档",

            "source": TestReportFile+"/诊断消息的充分性",
            "des": "已实现的诊断功能数量",
            "val": A
        }
    except:
        A_dict = {
            "id": "A",
            "type": "测试文档",

            "source": TestReportFile+"/诊断消息的充分性",
            "des": "已实现的诊断功能数量",
            "val": None
        }

    if A_dict["val"] is not None and B_dict["val"] is not None:
        res_dict = {
            "val": A_dict["val"]/B_dict["val"],
            "sub": [A_dict, B_dict]
        }

    else:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }
    return res_dict


def man2s(UserTree, testcases, r2c):
    try:
        test = match2.getTestCases("诊断消息的充分性", testcases, r2c)
        B = 0
        for val in test.values():
            if val == "通过":
                B += 1
        if B:
            B_dict = {
                "id": "B",
                "type": "测试文档",

                "source": TestReportFile+"/诊断消息的充分性",
                "des": "已实现的诊断功能数量",
                "val": B
            }
        else:
            B_dict = {
                "id": "B",
                "type": "测试文档",

                "source": TestReportFile+"/诊断消息的充分性",
                "des": "已实现的诊断功能数量",
                "val": None
            }
    except:
        B_dict = {
            "id": "B",
            "type": "测试文档",

            "source": TestReportFile+"/诊断消息的充分性",
            "des": "已实现的诊断功能数量",
            "val": None
        }

    try:
        test = match2.getTestCases("诊断消息的有效性", testcases, r2c)
        A = 0
        for val in test.values():
            if val == "通过":
                A += 1

        A_dict = {
            "id": "A",
            "type": "测试文档",

            "source": TestReportFile+"/诊断消息的有效性",
            "des": "对原因分析有效的诊断功能数量",
            "val": A
        }
    except:
        A_dict = {
            "id": "A",
            "type": "测试文档",
            "source": TestReportFile+"/诊断消息的有效性",
            "des": "对原因分析有效的诊断功能数量",
            "val": None
        }

    if A_dict["val"] is not None and B_dict["val"] is not None:
        res_dict = {
            "val": A_dict["val"]/B_dict["val"],
            "sub": [A_dict, B_dict]
        }

    else:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }
    return res_dict


def man1g(ReqTree, testcases, r2c):
    B = ReqFunc.func_66(ReqTree)
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile+"/操作日志的完整性",
        "des": "实际记录在系统中的日志条数",
        "val": None
    }
    B_dict = {
        "id": "B",
        "type": "测试文档",
        "source": TestReportFile + "/操作日志的完整性",
        "des": "操作期问审计跟踪所需的日志条数",
        "val": None
    }
    if not B:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }
        return res_dict
    test = match2.getTestCases("操作日志的完整性", testcases, r2c)
    A = 0
    B = 0
    for key in test.keys():
        B += test[key]["pre"]
        A += test[key]["res"]

    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile+"/操作日志的完整性",
        "des": "实际记录在系统中的日志条数",
        "val": A
    }
    if B:
        B_dict = {
            "id": "B",
            "type": "测试文档",
            "source": TestReportFile+"/操作日志的完整性",
            "des": "操作期问审计跟踪所需的日志条数",
            "val": B
        }
    else:
        B_dict = {
            "id": "B",
            "type": "测试文档",
            "source": TestReportFile+"/操作日志的完整性",
            "des": "操作期问审计跟踪所需的日志条数",
            "val": None
        }
    if A_dict["val"] is not None and B_dict["val"] is not None:
        res_dict = {
            "val": A_dict["val"] / B_dict["val"],
            "sub": [A_dict, B_dict]
        }

    else:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }
    return res_dict


def mre2s(ReqTree, testcases, r2c):
    B_dict = {
        "id": "B",
        "type": "测试文档",
        "source": TestReportFile + "/编码规则",
        "des": "已实现的软件模功数量",
        "val": None
    }
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/编码规则",
        "des": "符合特定系统编码规则的软件模块数量",
        "val": None
    }
    check = ReqFunc.func_65(ReqTree)
    if check:
        test = match2.getTestCases("编码规则", testcases, r2c)
        A = 0
        B = len(test)
        if B:
            B_dict = {
                "id": "B",
                "type": "测试文档",
                "source": TestReportFile+"/编码规则",
                "des": "已实现的软件模功数量",
                "val": B
            }
        else:
            B_dict = {
                "id": "B",
                "type": "测试文档",
                "source": TestReportFile+"/编码规则",
                "des": "已实现的软件模功数量",
                "val": None
            }
        for val in test.values():
            if val == "通过":
                A += 1
        A_dict = {
            "id": "A",
            "type": "测试文档",
            "source": TestReportFile+"/编码规则",
            "des": "符合特定系统编码规则的软件模块数量",
            "val": A
        }

        if A_dict["val"] is not None and B_dict["val"] is not None:
            res_dict = {
                "val": A_dict["val"] / B_dict["val"],
                "sub": [A_dict, B_dict]
            }

        else:
            res_dict = {
                "val": None,
                "sub": [A_dict, B_dict]
            }
        return res_dict
    else:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }
        return res_dict


def sau2s(InterfaceTree, testcases, r2c):
    B_dict = {
        "id": "B",
        "type": "测试文档",
        "source": TestReportFile + "/接口的鉴别规则",
        "des": "规定的鉴别规则的数量",
        "val": None
    }
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/接口的鉴别规则",
        "des": "已实现的鉴别规则的数量",
        "val": None
    }
    check = InterfaceDesignFunc.func_ck2(InterfaceTree)
    if check:
        test = match2.getTestCases("接口的鉴别规则", testcases, r2c)
        A = 0
        B = len(check)
        if B:
            B_dict = {
                "id": "B",
                "type": "测试文档",
                "source": TestReportFile+"/接口的鉴别规则",
                "des": "规定的鉴别规则的数量",
                "val": B
            }
        else:
            B_dict = {
                "id": "B",
                "type": "测试文档",
                "source": TestReportFile+"/接口的鉴别规则",
                "des": "规定的鉴别规则的数量",
                "val": None
            }
        for val in test.values():
            if val == "通过":
                A += 1
        A_dict = {
            "id": "A",
            "type": "测试文档",
            "source": TestReportFile+"/接口的鉴别规则",
            "des": "已实现的鉴别规则的数量",
            "val": A
        }

        if A_dict["val"] is not None and B_dict["val"] is not None:
            res_dict = {
                "val": A_dict["val"] / B_dict["val"],
                "sub": [A_dict, B_dict]
            }

        else:
            res_dict = {
                "val": None,
                "sub": [A_dict, B_dict]
            }
        return res_dict
    else:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }
        return res_dict


def sau1g(InterfaceTree, testcases, r2c):
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/接口的鉴别机制",
        "des": "提供鉴别机制的数量",
        "val": None
    }
    B_dict = {
        "id": "B",
        "type": "测试文档",
        "source": TestReportFile + "/接口的鉴别机制",
        "des": "规定的鉴别机制数量",
        "val": None
    }
    check = InterfaceDesignFunc.func_ck1(InterfaceTree)
    if check:
        test = match2.getTestCases("接口的鉴别机制", testcases, r2c)
        A = 0
        B = len(check)
        if B:
            B_dict = {
                "id": "B",
                "type": "测试文档",
                "source": TestReportFile+"/接口的鉴别机制",
                "des": "规定的鉴别机制数量",
                "val": B
            }
        else:
            B_dict = {
                "id": "B",
                "type": "测试文档",
                "source": TestReportFile+"/接口的鉴别机制",
                "des": "规定的鉴别机制数量",
                "val": None
            }
        for val in test.values():
            if val == "通过":
                A += 1
        A_dict = {
            "id": "A",
            "type": "测试文档",
            "source": TestReportFile+"/接口的鉴别机制",
            "des": "提供鉴别机制的数量",
            "val": A
        }

        if A_dict["val"] is not None and B_dict["val"] is not None:
            res_dict = {
                "val": A_dict["val"] / B_dict["val"],
                "sub": [A_dict, B_dict]
            }

        else:
            res_dict = {
                "val": None,
                "sub": [A_dict, B_dict]
            }
        return res_dict
    else:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }
        return res_dict


def sac2s(ReqTree, testcases, r2c):

    try:
        num, _ = ReqFunc.func_64(ReqTree)
        if _ == "天":
            B = float(num) / 30
        B_dict = {
            "id": "B",
            "type": "需求文档",
            "source": RequirementFile+"/具体需求(运行模式组织1)/软件系统属性/可审查性/系统日志保留时长",
            "des": "要求系统日志存储在稳定存储器中的时间",
            "val": B
        }
    except:
        B_dict = {
            "id": "B",
            "type": "需求文档",
            "source": RequirementFile+"/具体需求(运行模式组织1)/软件系统属性/可审查性/系统日志保留时长",
            "des": "要求系统日志存储在稳定存储器中的时间",
            "val": None
        }
    try:

        A = match2.getTestCases("操作日志保留的时长", testcases, r2c)
        N = len(A.keys())
        if N:
            A_dict = {
                "id": "A",
                "type": "测试文档",
                "source": TestReportFile+"/操作日志保留的时长",
                "des": "要求系统日志存储在稳定存储器中的时间",
                "val": sum(list(A.values())) / N
            }
        else:
            A_dict = {
                "id": "A",
                "type": "测试文档",
                "source": TestReportFile+"/操作日志保留的时长",
                "des": "要求系统日志存储在稳定存储器中的时间",
                "val": None
            }
    except:
        A_dict = {
            "id": "A",
            "type": "测试文档",
            "source": TestReportFile+"/操作日志保留的时长",
            "des": "要求系统日志存储在稳定存储器中的时间",
            "val": None
        }
    if A_dict["val"] is not None and B_dict["val"] is not None:
        res_dict = {
            "val": A_dict["val"] / B_dict["val"],
            "sub": [A_dict, B_dict]
        }

    else:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }
    return res_dict


def sac1g(ReqTree, testcases, r2c):
    B_dict = {
        "id": "B",
        "type": "测试文档",
        "source": TestReportFile + "/操作日志的数量",
        "des": "对系统或数据的访问次数",
        "val": None
    }
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/操作日志的数量",
        "des": "所有日志中记录的访问次数",
        "val": None
    }
    check = ReqFunc.func_63(ReqTree)
    if check:
        test = match2.getTestCases("操作日志的数量", testcases, r2c)
        A = 0
        B = 0
        for key in test.keys():
            B += test[key]["pre"]
            A += test[key]["res"]
        if B:
            B_dict = {
                "id": "B",
                "type": "测试文档",
                "source": TestReportFile+"/操作日志的数量",
                "des": "对系统或数据的访问次数",
                "val": B
            }
        else:
            B_dict = {
                "id": "B",
                "type": "测试文档",
                "source": TestReportFile+"/操作日志的数量",
                "des": "对系统或数据的访问次数",
                "val": None
            }
        A_dict = {
            "id": "A",
            "type": "测试文档",
            "source": TestReportFile+"/操作日志的数量",
            "des": "所有日志中记录的访问次数",
            "val": A
        }

        if A_dict["val"] is not None and B_dict["val"] is not None:
            res_dict = {
                "val": A_dict["val"] / B_dict["val"],
                "sub": [A_dict, B_dict]
            }

        else:
            res_dict = {
                "val": None,
                "sub": [A_dict, B_dict]
            }
        return res_dict
    else:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }
        return res_dict


def sno1g(ReqTree, testcases, r2c):
    list_B = ReqFunc.func_62(ReqTree)
    B = len(list_B)
    if B:
        B_dict = {
            "id": "B",
            "type": "需求文档",
            "source": RequirementFile+"/具体需求(运行模式组织1)/数据库逻辑需求/访问能力/表格",
            "des": "使用数字签名要求抗抵赖性事务的数量",
            "val": B
        }
    else:
        B_dict = {
            "id": "B",
            "type": "需求文档",
            "source": RequirementFile+"/具体需求(运行模式组织1)/数据库逻辑需求/访问能力/表格",
            "des": "使用数字签名要求抗抵赖性事务的数量",
            "val": None
        }
    try:
        test = match2.getTestCases("事务是否具有数字签名", testcases, r2c)
        A = 0
        for val in test.values():
            if val == "通过":
                A += 1
        A_dict = {
            "id": "A",
            "type": "测试文档",
            "source": TestReportFile+"/事务是否具有数字签名",
            "des": "实际使用数字签名确保抗抵赖性事务的数量",
            "val": A
        }
    except:
        A_dict = {
            "id": "A",
            "type": "测试文档",
            "source": TestReportFile+"/事务是否具有数字签名",
            "des": "实际使用数字签名确保抗抵赖性事务的数量",
            "val": None
        }
    if A_dict["val"] is not None and B_dict["val"] is not None:
        res_dict = {
            "val": A_dict["val"] / B_dict["val"],
            "sub": [A_dict, B_dict]
        }

    else:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }
    return res_dict


def sin2g(ReqTree, testcases, r2c):
    list_B = ReqFunc.func_61(ReqTree)
    B = len(list_B)
    if B:
        B_dict = {
            "id": "B",
            "type": "需求文档",
            "source": RequirementFile+"/具体需求(运行模式组织1)/软件系统属性/安全保密性/保留某些特定数据组的历史或记录/表格",
            "des": "可用及推荐的用于数据抗讹误性方法的数量",
            "val": B
        }
    else:
        B_dict = {
            "id": "B",
            "type": "需求文档",
            "source": RequirementFile+"/具体需求(运行模式组织1)/软件系统属性/安全保密性/保留某些特定数据组的历史或记录/表格",
            "des": "可用及推荐的用于数据抗讹误性方法的数量",
            "val": None
        }
    try:
        test = match2.getTestCases("特定数据项的存储", testcases, r2c)
        A = 0
        for val in test.values():
            if val == "通过":
                A += 1

        A_dict = {
            "id": "A",
            "type": "测试文档",
            "source": TestReportFile+"/特定数据项的存储",
            "des": "实际用于数据抗讹误性方法的数量",
            "val": A
        }

    except:
        A_dict = {
            "id": "A",
            "type": "测试文档",
            "source": "测试报告/特定数据项的存储",
            "des": "实际用于数据抗讹误性方法的数量",
            "val": None
        }
    if A_dict["val"] is not None and B_dict["val"] is not None:
        res_dict = {
            "val": A_dict["val"] / B_dict["val"],
            "sub": [A_dict, B_dict]
        }

    else:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }
    return res_dict


def sin1g(ReqTree, testcases, r2c):
    list_B = ReqFunc.func_60(ReqTree)
    B = len(list_B)
    if B:
        B_dict = {
            "id": "B",
            "type": "需求文档",
            "source": RequirementFile+"/具体需求(运行模式组织1)/软件系统属性/安全保密性/对于关键变量检查数据的完整性/表格",
            "des": "需要避免数据破坏或复改的数据项数量",
            "val": B
        }
    else:
        B_dict = {
            "id": "B",
            "type": "需求文档",
            "source": RequirementFile+"/具体需求(运行模式组织1)/软件系统属性/安全保密性/对于关键变量检查数据的完整性/表格",
            "des": "需要避免数据破坏或复改的数据项数量",
            "val": None
        }
    try:
        test = match2.getTestCases("关键数据项的完整性", testcases, r2c)
        A = 0
        for val in test.values():
            if val == "通过":
                A += 1
        A_dict = {
            "id": "A",
            "type": "测试文档",
            "source": TestReportFile+"/关键数据项的完整性",
            "des": "因未经授权访问而破坏或篡改数据项的数量",
            "val": B-A
        }

    except:
        A_dict = {
            "id": "A",
            "type": "测试文档",
            "source": TestReportFile+"/关键数据项的完整性",
            "des": "因未经授权访问而破坏或篡改数据项的数量",
            "val": None
        }
    if A_dict["val"] is not None and B_dict["val"] is not None:
        res_dict = {
            "val": 1 - A_dict["val"] / B_dict["val"],
            "sub": [A_dict, B_dict]
        }

    else:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }
    return res_dict


def sco3s(ReqTree, testcases, r2c):
    list_B = ReqFunc.func_58(ReqTree)
    B = len(list_B)
    if B:
        B_dict = {
            "id": "B",
            "type": "需求文档",
            "source": RequirementFile+"/具体需求(运行模式组织1)/软件系统属性/安全保密性/使用的密码技术/表格",
            "des": "所使用的加密算法的数量",
            "val": B
        }
    else:
        B_dict = {
            "id": "B",
            "type": "需求文档",
            "source": RequirementFile+"/具体需求(运行模式组织1)/软件系统属性/安全保密性/使用的密码技术/表格",
            "des": "所使用的加密算法的数量",
            "val": None
        }
    try:
        test = match2.getTestCases("加密方法", testcases, r2c)
        A = 0
        for val in test.values():
            if val == "通过":
                A += 1
        A_dict = {
            "id": "A",
            "type": "测试文档",
            "source": TestReportFile+"/加密方法",
            "des": "使用时遭到破坏或存在不可接受风险的加密算法的数量",
            "val": B-A
        }

    except:
        A_dict = {
            "id": "A",
            "type": "测试文档",
            "source": TestReportFile+"/加密方法",
            "des": "使用时遭到破坏或存在不可接受风险的加密算法的数量",
            "val": None
        }
    if A_dict["val"] is not None and B_dict["val"] is not None:
        res_dict = {
            "val": 1 - A_dict["val"] / B_dict["val"],
            "sub": [A_dict, B_dict]
        }

    else:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }
    return res_dict


def sco2g(InterfaceTree, testcases, r2c):
    list_B = InterfaceDesignFunc.func_56(InterfaceTree)
    B = len(list_B)
    if B:
        B_dict = {
            "id": "B",
            "type": "设计文档",
            "source": InterfaceDesignFile+"/接口设计/数据元素集合体特性/保密性和私密性/表格",
            "des": "需要加密/解密的数据项数量",
            "val": B
        }
    else:
        B_dict = {
            "id": "B",
            "type": "设计文档",
            "source": InterfaceDesignFile+"/接口设计/数据元素集合体特性/保密性和私密性/表格",
            "des": "需要加密/解密的数据项数量",
            "val": None
        }
    try:
        test = match2.getTestCases("数据加密", testcases, r2c)
        A = 0
        for val in test.values():
            if val == "通过":
                A += 1
        A_dict = {
            "id": "A",
            "type": "测试文档",
            "source": TestReportFile+"/数据加密",
            "des": "正确加密/解密的数据项数量",
            "val": A
        }

    except:
        A_dict = {
            "id": "A",
            "type": "测试文档",
            "source": TestReportFile+"/数据加密",
            "des": "正确加密/解密的数据项数量",
            "val": None
        }
    if A_dict["val"] is not None and B_dict["val"] is not None:
        res_dict = {
            "val": A_dict["val"] / B_dict["val"],
            "sub": [A_dict, B_dict]
        }

    else:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }
    return res_dict


def sco1g(InterfaceTree, testcases, r2c):
    list_B = InterfaceDesignFunc.func_54(InterfaceTree)
    B = len(list_B)
    if B:
        B_dict = {
            "id": "B",
            "type": "设计文档",
            "source": InterfaceDesignFile+"/接口设计/数据元素集合体特性/保密性和私密性/表格",
            "des": "需要访问控制的保密数据项的数量",
            "val": B
        }
    else:
        B_dict = {
            "id": "B",
            "type": "设计文档",
            "source": InterfaceDesignFile+"/接口设计/数据元素集合体特性/保密性和私密性/表格",
            "des": "需要访问控制的保密数据项的数量",
            "val": None
        }
    try:
        test = match2.getTestCases("接口是否实现访问控制", testcases, r2c)
        A = 0
        for val in test.values():
            if val == "通过":
                A += 1
        A_dict = {
            "id": "A",
            "type": "测试文档",
            "source": TestReportFile+"/接口是否实现访问控制",
            "des": "未经授权可访问的保密数据项的数量",
            "val": B - A
        }

    except:
        A_dict = {
            "id": "A",
            "type": "测试文档",
            "source": TestReportFile+"/接口是否实现访问控制",
            "des": "未经授权可访问的保密数据项的数量",
            "val": None
        }
    if A_dict["val"] is not None and B_dict["val"] is not None:
        res_dict = {
            "val": 1 - A_dict["val"] / B_dict["val"],
            "sub": [A_dict, B_dict]
        }

    else:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }
    return res_dict


def rre2s(UserTree, testcases, r2c):
    try:
        list_b = UserMannelFunc.func_53(UserTree)
        B = len(list_b)
        if B:
            B_dict = {
                "id": "B",
                "type": "用户手册",
                "source": UserMannelFile+"/~/数据备份/",
                "des": "需要备份的数据项的数量",
                "val": B
            }
        else:
            B_dict = {
                "id": "B",
                "type": "用户手册",
                "source": UserMannelFile+"/~/数据备份/",
                "des": "需要备份的数据项的数量",
                "val": None
            }
    except:
        B_dict = {
            "id": "B",
            "type": "用户手册",
            "source": UserMannelFile+"/~/数据备份/",
            "des": "需要备份的数据项的数量",
            "val": None
        }
    try:
        test = match2.getTestCases("数据备份能力", testcases, r2c)
        A = 0
        for val in test.values():
            if val == "通过":
                A += 1
        A_dict = {
            "id": "A",
            "type": "测试文档",
            "source": TestReportFile+"/数据备份能力",
            "des": "实际定期备份数据项的数量",
            "val": A
        }
    except:
        A_dict = {
            "id": "A",
            "type": "测试文档",
            "source": TestReportFile+"/数据备份能力",
            "des": "实际定期备份数据项的数量",
            "val": None
        }
    if A_dict["val"] is not None and B_dict["val"] is not None:
        res_dict = {
            "val": 1 - A_dict["val"] / B_dict["val"],
            "sub": [A_dict, B_dict]
        }

    else:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }
    return res_dict


def rre1g(ReqTree, testcases, r2c):
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/系统平均恢复时间",
        "des": "由于第i次失效而重新启动,并恢复岩机的软件/系统所花费的总时间",
        "val": None
    }
    N_dict = {
        "id": "N",
        "type": "测试文档",
        "source": TestReportFile + "/系统平均恢复时间",
        "des": "发生失效的次数",
        "val": None
    }
    try:
        num, _ = ReqFunc.func_52(ReqTree)
        if num:
            A = match2.getTestCases("系统平均恢复时间", testcases, r2c)
            N = len(A.keys())
            Alist = list(A.values())
            sublist = []
            for i in range(N):
                A_dict = {
                    "id": "A"+str(i),
                    "type": "测试文档",
                    "source": TestReportFile+"/系统平均恢复时间",
                    "des": "由于第i次失效而重新启动,并恢复岩机的软件/系统所花费的总时间",
                    "val": Alist[i]
                }
                sublist.append(A_dict)
            N_dict = {
                "id": "N",
                "type": "测试文档",
                "source": TestReportFile+"/系统平均恢复时间",
                "des": "发生失效的次数",
                "val": N
            }
            sublist.append(N_dict)
            res = sum(list(A.values())) / N
            res_dict = {
                "val": res,
                "sub": sublist
            }
        else:
            res_dict = {
                "val": None,
                "sub": [A_dict, N_dict]
            }

    except:
        res_dict = {
            "val": None,
            "sub": [A_dict, N_dict]
        }

    return res_dict


def rft3s(ReqTree, testcases, r2c):
    A_dict = {
        "id": "A-B",
        "type": "测试文档",
        "source": TestReportFile + "/平均故障通告时间",
        "des": "故障通告时间",
        "val": None
    }
    N_dict = {
        "id": "N",
        "type": "测试文档",
        "source": TestReportFile + "/系统平均恢复时间",
        "des": "检测到的故障数",
        "val": None
    }
    try:
        num, _ = ReqFunc.func_51(ReqTree)
        if num:
            A = match2.getTestCases("平均故障通告时间", testcases, r2c)
            N = len(A.keys())
            Alist = list(A.values())
            sublist = []
            for i in range(N):
                A_dict = {
                    "id": "A" + str(i) + "-B" + str(i),
                    "type": "测试文档",
                    "source": TestReportFile+"/平均故障通告时间",
                    "des": "故障通告时间",
                    "val": Alist[i]
                }
                sublist.append(A_dict)
            N_dict = {
                "id": "N",
                "type": "测试文档",
                "source": TestReportFile+"/系统平均恢复时间",
                "des": "检测到的故障数",
                "val": N
            }
            sublist.append(N_dict)
            res = sum(list(A.values())) / N
            res_dict = {
                "val": res,
                "sub": sublist
            }
        else:
            res_dict = {
                "val": None,
                "sub": [A_dict, N_dict]
            }
    except:
        res_dict = {
            "val": None,
            "sub": [A_dict, N_dict]
        }

    return res_dict


def rft1g(ReqTree, testcases, r2c):
    B_dict = {
        "id": "B",
        "type": "需求文档",
        "source": RequirementFile + "/具体需求(运行模式组织1)/软件系统属性/可靠性/故障模式",
        "des": "测试中执行的故障模式(几乎导致失效)的测试用例数量",
        "val": None
    }
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/避免失效率",
        "des": "避免发生关键和严重失效的次数(以测试用例为单位计算的数量)",
        "val": None
    }
    try:
        list_b = ReqFunc.func_50(ReqTree)
        B = len(list_b)
        if B:
            B_dict = {
                "id": "B",
                "type": "需求文档",
                "source": RequirementFile+"/具体需求(运行模式组织1)/软件系统属性/可靠性/故障模式",
                "des": "测试中执行的故障模式(几乎导致失效)的测试用例数量",
                "val": B
            }
            test = match2.getTestCases("避免失效率", testcases, r2c)
            A = 0
            for val in test.values():
                if val == "通过":
                    A += 1
            A_dict = {
                "id": "A",
                "type": "测试文档",
                "source": TestReportFile+"/避免失效率",
                "des": "避免发生关键和严重失效的次数(以测试用例为单位计算的数量)",
                "val": A
            }
            res_dict = {
                "val": A/B,
                "sub": [A_dict, B_dict]
            }

        else:
            res_dict = {
                "val": None,
                "sub": [A_dict, B_dict]
            }
    except:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }

    return res_dict


def rav2g(ReqTree, testcases, r2c):
    B_dict = {
        "id": "B",
        "type": "测试文档",
        "source": TestReportFile + "/平均宕机时间",
        "des": "观察到的岩机数量",
        "val": None
    }
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/平均宕机时间",
        "des": "总的启机时间",
        "val": None
    }
    try:
        list_b = ReqFunc.func_49(ReqTree)
        B = len(list_b)
        if B:

            test = match2.getTestCases("平均宕机时间", testcases, r2c)
            B_dict = {
                "id": "B",
                "type": "测试文档",
                "source": TestReportFile+"/平均宕机时间",
                "des": "观察到的岩机数量",
                "val": len(test.keys())
            }
            A_dict = {
                "id": "A",
                "type": "测试文档",
                "source": TestReportFile+"/平均宕机时间",
                "des": "总的启机时间",
                "val": sum(list(test.values()))
            }

            res = sum(list(test.values())) / len(test.keys())
            res_dict = {
                "val": res,
                "sub": [A_dict, B_dict]
            }

        else:
            res_dict = {
                "val": None,
                "sub": [A_dict, B_dict]
            }
    except:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }

    return res_dict


def rav1g(ReqTree, testcases, r2c):
    B_dict = {
        "id": "B",
        "type": "需求文档",
        "source": RequirementFile + "/具体需求(运行模式组织1)/软件系统属性/可用性/系统运行时间",
        "des": "操作计划中规定的系统运行时间",
        "val": None
    }
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/测试系统运行时间",
        "des": "实际提供的系统运行时间",
        "val": None
    }
    try:
        num, _ = ReqFunc.func_47(ReqTree)
        if _ == "天":
            B = float(num) * 24
        if B:
            B_dict = {
                "id": "B",
                "type": "需求文档",
                "source": RequirementFile+"/具体需求(运行模式组织1)/软件系统属性/可用性/系统运行时间",
                "des": "操作计划中规定的系统运行时间",
                "val": B
            }
            try:
                test = match2.getTestCases("测试系统运行时间", testcases, r2c)
                A_dict = {
                    "id": "A",
                    "type": "测试文档",
                    "source": TestReportFile+"/测试系统运行时间",
                    "des": "实际提供的系统运行时间",
                    "val": sum(list(test.values())) / len(test.keys())
                }
                res = sum(list(test.values())) / B / len(test.keys())
                res_dict = {
                    "val": res,
                    "sub": [A_dict, B_dict]
                }
            except:
                A_dict = {
                    "id": "A",
                    "type": "测试文档",
                    "source": TestReportFile+"/测试系统运行时间",
                    "des": "实际提供的系统运行时间",
                    "val": None
                }
                res_dict = {
                    "val": None,
                    "sub": [A_dict, B_dict]
                }
        else:
            res_dict = {
                "val": None,
                "sub": [A_dict, B_dict]
            }
    except:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }

    return res_dict


def rma4s(testReportTree):
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/测试结果概述/对被测试软件的总体评估/表格",
        "des": "预期包含的功能数量",
        "val": None
    }
    B_dict = {
        "id": "B",
        "type": "测试文档",
        "source": TestReportFile + "/测试结果概述/对被测试软件的总体评估/表格",
        "des": "实际提供的系统运行时间",
        "val": None
    }
    try:
        test = match2.func46(testReportTree)[0]

        if test:
            A, B = test
            A = int(A)
            B = int(B)
            A_dict = {
                "id": "A",
                "type": "测试文档",
                "source": TestReportFile+"/测试结果概述/对被测试软件的总体评估/表格",
                "des": "预期包含的功能数量",
                "val": A
            }
            B_dict = {
                "id": "B",
                "type": "测试文档",
                "source": TestReportFile+"/测试结果概述/对被测试软件的总体评估/表格",
                "des": "实际提供的系统运行时间",
                "val": B
            }
            res_dict = {
                "val": A/B,
                "sub": [A_dict, B_dict]
            }
        else:
            res_dict = {
                "val": None,
                "sub": [A_dict, B_dict]
            }
    except:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }

    return res_dict


def rma3g(ReqTree, testcases, r2c):
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/周期失效率",
        "des": "在观察时间内检测到的失效数量",
        "val": None
    }
    B_dict = {
        "id": "B",
        "type": "测试文档",
        "source": TestReportFile + "/周期失效率",
        "des": "观察持续周期数",
        "val": None
    }
    try:
        time = ReqFunc.func_45(ReqTree)
        if time:
            test = match2.getTestCases("周期失效率", testcases, r2c)
            A_dict = {
                "id": "A",
                "type": "测试文档",
                "source": TestReportFile+"/周期失效率",
                "des": "在观察时间内检测到的失效数量",
                "val": sum(list(test.values()))
            }
            B_dict = {
                "id": "B",
                "type": "测试文档",
                "source": TestReportFile+"/周期失效率",
                "des": "观察持续周期数",
                "val": len(test.keys())
            }
            res = sum(list(test.values())) / len(test.keys())
            res_dict = {
                "val": res,
                "sub": [A_dict, B_dict]
            }
        else:
            res_dict = {
                "val": None,
                "sub": [A_dict, B_dict]
            }
    except:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }

    return res_dict


def rma2g(ReqTree, testcases, r2c):
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/平均失效间隔",
        "des": "运行时间",
        "val": None
    }
    B_dict = {
        "id": "B",
        "type": "测试文档",
        "source": TestReportFile + "/平均失效间隔",
        "des": "实际发生的系统/软件失效次数",
        "val": None
    }
    try:
        time = ReqFunc.func_44(ReqTree)
        if time:
            test = match2.getTestCases("平均失效间隔", testcases, r2c)
            A_dict = {
                "id": "A",
                "type": "测试文档",
                "source": TestReportFile+"/平均失效间隔",
                "des": "运行时间",
                "val": sum(list(test.values()))
            }
            B_dict = {
                "id": "B",
                "type": "测试文档",
                "source": TestReportFile+"/平均失效间隔",
                "des": "实际发生的系统/软件失效次数",
                "val": len(test.keys())
            }
            res = sum(list(test.values())) / len(test.keys())
            res_dict = {
                "val": res,
                "sub": [A_dict, B_dict]
            }
        else:
            res_dict = {
                "val": None,
                "sub": [A_dict, B_dict]
            }
    except:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }

    return res_dict


def rma1g(ReqTree, testcases, r2c):
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/故障修复率",
        "des": "设计/编码/测试阶段修复的与可靠性相关故障数",
        "val": None
    }
    B_dict = {
        "id": "B",
        "type": "测试文档",
        "source": TestReportFile + "/故障修复率",
        "des": "设计/编码/测试阶段检测到的与可靠性相关的故障数",
        "val": None
    }
    try:
        time = ReqFunc.func_43(ReqTree)
        if time:
            test = match2.getTestCases("故障修复率", testcases, r2c)
            # print("test",test)
            A = 0
            B = 0
            for key in test.keys():
                A += test[key]['res']
                B += test[key]['pre']

            A_dict = {
                "id": "A",
                "type": "测试文档",
                "source": TestReportFile+"/故障修复率",
                "des": "设计/编码/测试阶段修复的与可靠性相关故障数",
                "val": A
            }
            B_dict = {
                "id": "B",
                "type": "测试文档",
                "source": TestReportFile+"/故障修复率",
                "des": "设计/编码/测试阶段检测到的与可靠性相关的故障数",
                "val": B
            }
            res = A_dict['val'] / B_dict['val']
            res_dict = {
                "val": res,
                "sub": [A_dict, B_dict]
            }
        else:
            res_dict = {
                "val": None,
                "sub": [A_dict, B_dict]
            }
    except:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }

    return res_dict


def uac2s(UserTree, testcases, r2c):
    B_dict = {
        "id": "B",
        "type": "用户手册",
        "source": UserMannelFile + "/引言/系统概述/语言种类/表格",
        "des": "需要支持的语种数量",
        "val": None
    }
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/支持的语种充分性",
        "des": "实际支持的语种数量",
        "val": None
    }

    try:
        time = UserMannelFunc.func_42(UserTree)
        if time:
            B = len(time)
            B_dict = {
                "id": "B",
                "type": "用户手册",
                "source": UserMannelFile+"/引言/系统概述/语言种类/表格",
                "des": "需要支持的语种数量",
                "val": B
            }
            test = match2.getTestCases("支持的语种充分性", testcases, r2c)
            A = 0
            for i in test.values():
                if i == "通过":
                    A += 1
            A_dict = {
                "id": "A",
                "type": "测试文档",
                "source": TestReportFile+"/支持的语种充分性",
                "des": "实际支持的语种数量",
                "val": A
            }
            res = A / B
            res_dict = {
                "val": res,
                "sub": [A_dict, B_dict]
            }
        else:
            res_dict = {
                "val": None,
                "sub": [A_dict, B_dict]
            }
    except:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }

    return res_dict


def uac1g(UserTree, testcases, r2c):
    B_dict = {
        "id": "B",
        "type": "用户手册",
        "source": UserMannelFile + "/~/快速引用指南/特殊群体支持/表格",
        "des": "实现的功能数量",
        "val": None
    }
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/特殊群体的易访问性",
        "des": "特殊群体用户成功使用的功能数量",
        "val": None
    }
    try:
        time = UserMannelFunc.func_x1(UserTree)
        if time:
            B = len(time)
            B_dict = {
                "id": "B",
                "type": "用户手册",
                "source": UserMannelFile+"/~/快速引用指南/特殊群体支持/表格",
                "des": "实现的功能数量",
                "val": B
            }
            test = match2.getTestCases("特殊群体的易访问性", testcases, r2c)
            A = 0
            for i in test.values():
                if i == "通过":
                    A += 1
            A_dict = {
                "id": "A",
                "type": "测试文档",
                "source": TestReportFile+"/特殊群体的易访问性",
                "des": "特殊群体用户成功使用的功能数量",
                "val": A
            }
            res = A / B
            res_dict = {
                "val": res,
                "sub": [A_dict, B_dict]
            }
        else:
            res_dict = {
                "val": None,
                "sub": [A_dict, B_dict]
            }
    except:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }

    return res_dict


def uin1s(ReqTree, testcases, r2c):
    B_dict = {
        "id": "B",
        "type": "需求文档",
        "source": RequirementFile + "/总体描述/产品描述/用户界面/",
        "des": "显示界面数量",
        "val": None
    }
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/用户界面外观舒适性",
        "des": "在外观舒适性上令人愉悦的显示界面数量",
        "val": None
    }
    try:
        time = ReqFunc.func_41(ReqTree)
        if time:
            B = len(time)
            B_dict = {
                "id": "B",
                "type": "需求文档",
                "source": RequirementFile+"/总体描述/产品描述/用户界面/",
                "des": "显示界面数量",
                "val": B
            }
            test = match2.getTestCases("用户界面外观舒适性", testcases, r2c)
            A = 0
            for i in test.values():
                if i == "通过":
                    A += 1
            A_dict = {
                "id": "A",
                "type": "测试文档",
                "source": TestReportFile+"/用户界面外观舒适性",
                "des": "在外观舒适性上令人愉悦的显示界面数量",
                "val": A
            }
            res = A / B
            res_dict = {
                "val": res,
                "sub": [A_dict, B_dict]
            }
        else:
            res_dict = {
                "val": None,
                "sub": [A_dict, B_dict]
            }
    except:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }

    return res_dict


def uep3s(UserTree, testcases, r2c):
    B_dict = {
        "id": "B",
        "type": "用户手册",
        "source": UserMannelFile + "/~/错误,故障和紧急情况时的恢复/",
        "des": "操作过程中可能发生的用户差错数量",
        "val": None
    }
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/用户差错易恢复性",
        "des": "由系统恢复的用户差错数量,这些用户差错是经设计并测试的",
        "val": None
    }
    try:
        time = UserMannelFunc.func_u1(UserTree)
        if time:
            B = len(time)
            B_dict = {
                "id": "B",
                "type": "用户手册",
                "source": UserMannelFile+"/~/错误,故障和紧急情况时的恢复/",
                "des": "操作过程中可能发生的用户差错数量",
                "val": B
            }
            test = match2.getTestCases("用户差错易恢复性", testcases, r2c)
            A = 0
            for i in test.values():
                if i == "通过":
                    A += 1
            A_dict = {
                "id": "A",
                "type": "测试文档",
                "source": TestReportFile+"/用户差错易恢复性",
                "des": "由系统恢复的用户差错数量,这些用户差错是经设计并测试的",
                "val": A
            }
            res = A / B
            res_dict = {
                "val": res,
                "sub": [A_dict, B_dict]
            }
        else:
            res_dict = {
                "val": None,
                "sub": [A_dict, B_dict]
            }
    except:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }

    return res_dict


def uep2s(testcases, r2c):
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/用户输入差错纠正率",
        "des": "系统提供建议的修改值的输入差错数量",
        "val": None
    }
    B_dict = {
        "id": "B",
        "type": "测试文档",
        "source": TestReportFile + "/用户输入差错纠正率",
        "des": "检测到的输入差错数量",
        "val": None
    }
    try:
        test = match2.getTestCases("用户输入差错纠正率", testcases, r2c)
        B = len(test.keys())
        B_dict = {
            "id": "B",
            "type": "测试文档",
            "source": TestReportFile+"/用户输入差错纠正率",
            "des": "检测到的输入差错数量",
            "val": B
        }
        A = 0
        for i in test.values():
            if i == "通过":
                A += 1
        A_dict = {
            "id": "A",
            "type": "测试文档",
            "source": TestReportFile+"/用户输入差错纠正率",
            "des": "系统提供建议的修改值的输入差错数量",
            "val": A
        }
        res = A / B
        res_dict = {
            "val": res,
            "sub": [A_dict, B_dict]
        }

    except:

        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }

    return res_dict


def uep1g(ReqTree, testcases, r2c):
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/抵御误操作",
        "des": "可以防止导致系统故障的用户操作和输人的数量",
        "val": None
    }
    B_dict = {
        "id": "B",
        "type": "需求文档",
        "source": RequirementFile + "/总体描述/产品描述/操作/用户特定的操作/表格",
        "des": "实际操作中可以防止导致系统故障的用户操作和输入的数量",
        "val": None
    }
    try:
        time = ReqFunc.func_40(ReqTree)
        if time:
            B = len(time)
            B_dict = {
                "id": "B",
                "type": "需求文档",
                "source": RequirementFile+"/总体描述/产品描述/操作/用户特定的操作/表格",
                "des": "实际操作中可以防止导致系统故障的用户操作和输入的数量",
                "val": B
            }
            test = match2.getTestCases("抵御误操作", testcases, r2c)
            A = 0
            for i in test.values():
                if i == "通过":
                    A += 1
            A_dict = {
                "id": "A",
                "type": "测试文档",
                "source": TestReportFile+"/抵御误操作",
                "des": "可以防止导致系统故障的用户操作和输人的数量",
                "val": A
            }
            res = A / B
            res_dict = {
                "val": res,
                "sub": [A_dict, B_dict]
            }
        else:
            res_dict = {
                "val": None,
                "sub": [A_dict, B_dict]
            }
    except:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }

    return res_dict


def uop9s(UserTree, testcases, r2c):
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/输入设备的支持性",
        "des": "可由所有适当的输入方法启动任务的数量",
        "val": None
    }
    B_dict = {
        "id": "B",
        "type": "用户手册",
        "source": UserMannelFile + "/~/键盘、鼠标、语音",
        "des": "系统支持的任务数量",
        "val": None
    }
    try:
        time = UserMannelFunc.func_39(UserTree)
        if time:
            B = len(time)
            B_dict = {
                "id": "B",
                "type": "用户手册",
                "source": UserMannelFile+"/~/键盘、鼠标、语音",
                "des": "系统支持的任务数量",
                "val": B
            }
            test = match2.getTestCases("输入设备的支持性", testcases, r2c)
            A = 0
            for i in test.values():
                if i == "通过":
                    A += 1
            A_dict = {
                "id": "A",
                "type": "测试文档",
                "source": TestReportFile+"/输入设备的支持性",
                "des": "可由所有适当的输入方法启动任务的数量",
                "val": A
            }
            res = A / B
            res_dict = {
                "val": res,
                "sub": [A_dict, B_dict]
            }
        else:
            res_dict = {
                "val": None,
                "sub": [A_dict, B_dict]
            }
    except:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }

    return res_dict


def uop8s(ReqTree, testcases, r2c):
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/外观一致性",
        "des": "具有相似项但外观不同的用户界面的数量",
        "val": None
    }
    B_dict = {
        "id": "B",
        "type": "需求文档",
        "source": RequirementFile + "/其他需求/界面外观一致性/表格",
        "des": "只有相似项的用户界面的数量",
        "val": None
    }
    try:
        time = ReqFunc.func_38(ReqTree)
        if time:
            B = len(time)
            B_dict = {
                "id": "B",
                "type": "需求文档",
                "source": RequirementFile+"/其他需求/界面外观一致性/表格",
                "des": "只有相似项的用户界面的数量",
                "val": B
            }
            test = match2.getTestCases("外观一致性", testcases, r2c)
            A = 0
            for i in test.values():
                if i == "通过":
                    A += 1
            A_dict = {
                "id": "A",
                "type": "测试文档",
                "source": TestReportFile+"/外观一致性",
                "des": "具有相似项但外观不同的用户界面的数量",
                "val": A
            }
            res = A / B
            res_dict = {
                "val": res,
                "sub": [A_dict, B_dict]
            }
        else:
            res_dict = {
                "val": None,
                "sub": [A_dict, B_dict]
            }
    except:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }

    return res_dict


def uop7s(InterfaceTree, testcases, r2c):
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/信息分类的易理解性",
        "des": "对于预期用户来说,熟悉和方便的信息结构数量",
        "val": None
    }
    B_dict = {
        "id": "B",
        "type": "设计文档",
        "source": InterfaceDesignFile + "/接口设计/接口通信特性/消息格式化/表格",
        "des": "使用的信息结构数量",
        "val": None
    }
    try:
        time = InterfaceDesignFunc.func_33(InterfaceTree)
        if time:
            B = len(time)
            B_dict = {
                "id": "B",
                "type": "设计文档",
                "source": InterfaceDesignFile+"/接口设计/接口通信特性/消息格式化/表格",
                "des": "使用的信息结构数量",
                "val": B
            }
            test = match2.getTestCases("信息分类的易理解性", testcases, r2c)
            A = 0
            for i in test.values():
                if i == "通过":
                    A += 1
            A_dict = {
                "id": "A",
                "type": "测试文档",
                "source": TestReportFile+"/信息分类的易理解性",
                "des": "对于预期用户来说,熟悉和方便的信息结构数量",
                "val": A
            }
            res = A / B
            res_dict = {
                "val": res,
                "sub": [A_dict, B_dict]
            }
        else:
            res_dict = {
                "val": None,
                "sub": [A_dict, B_dict]
            }
    except:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }

    return res_dict


def uop6s(ReqTree, testcases, r2c):
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/撤销操作能力",
        "des": "提供撤销操作或重新确认的任务数量",
        "val": None
    }
    B_dict = {
        "id": "B",
        "type": "需求文档",
        "source": RequirementFile + "/具体需求(运行模式组织1)/ 功能需求/~/",
        "des": "用户能够从重新确认或撒销操作中获益的任务数量",
        "val": None
    }
    try:
        time = ReqFunc.func_37(ReqTree)
        if time:
            B = len(time)
            B_dict = {
                "id": "B",
                "type": "需求文档",
                "source": RequirementFile+"/具体需求(运行模式组织1)/ 功能需求/~/",
                "des": "用户能够从重新确认或撒销操作中获益的任务数量",
                "val": B
            }
            test = match2.getTestCases("撤销操作能力", testcases, r2c)
            A = 0
            for i in test.values():
                if i == "通过":
                    A += 1
            A_dict = {
                "id": "A",
                "type": "测试文档",
                "source": TestReportFile+"/撤销操作能力",
                "des": "提供撤销操作或重新确认的任务数量",
                "val": A
            }
            res = A / B
            res_dict = {
                "val": res,
                "sub": [A_dict, B_dict]
            }
        else:
            res_dict = {
                "val": None,
                "sub": [A_dict, B_dict]
            }
    except:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }

    return res_dict


def uop5s(ReqTree, testcases, r2c):
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/监视能力",
        "des": "具有状态监视能力的功能数量",
        "val": None
    }
    B_dict = {
        "id": "B",
        "type": "需求文档",
        "source": RequirementFile + "/具体需求(运行模式组织1)/ 功能需求/~/",
        "des": "期望受益于监视能力的功能数量",
        "val": None
    }
    try:
        time = ReqFunc.func_36(ReqTree)
        if time:
            B = len(time)
            B_dict = {
                "id": "B",
                "type": "需求文档",
                "source": RequirementFile+"/具体需求(运行模式组织1)/ 功能需求/~/",
                "des": "期望受益于监视能力的功能数量",
                "val": B
            }
            test = match2.getTestCases("监视能力", testcases, r2c)
            A = 0
            for i in test.values():
                if i == "通过":
                    A += 1
            A_dict = {
                "id": "A",
                "type": "测试文档",
                "source": TestReportFile+"/监视能力",
                "des": "具有状态监视能力的功能数量",
                "val": A
            }
            res = A / B
            res_dict = {
                "val": res,
                "sub": [A_dict, B_dict]
            }
        else:
            res_dict = {
                "val": None,
                "sub": [A_dict, B_dict]
            }
    except:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }

    return res_dict


def uop4s(ReqTree, testcases, r2c):
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/用户界面的易定制性",
        "des": "可以定制的用户界面元素数量",
        "val": None
    }
    B_dict = {
        "id": "B",
        "type": "需求文档",
        "source": RequirementFile + "/具体需求(运行模式组织1)/其他需求/支持用户定制界面/表格",
        "des": "期望能够受益于定制的用户界面元素数量",
        "val": None
    }
    try:
        time = ReqFunc.func_35(ReqTree)
        if time:
            B = len(time)
            B_dict = {
                "id": "B",
                "type": "需求文档",
                "source": RequirementFile+"/具体需求(运行模式组织1)/其他需求/支持用户定制界面/表格",
                "des": "期望能够受益于定制的用户界面元素数量",
                "val": B
            }
            test = match2.getTestCases("用户界面的易定制性", testcases, r2c)
            A = 0
            for i in test.values():
                if i == "通过":
                    A += 1
            A_dict = {
                "id": "A",
                "type": "测试文档",
                "source": TestReportFile+"/用户界面的易定制性",
                "des": "可以定制的用户界面元素数量",
                "val": A
            }
            res = A / B
            res_dict = {
                "val": res,
                "sub": [A_dict, B_dict]
            }
        else:
            res_dict = {
                "val": None,
                "sub": [A_dict, B_dict]
            }
    except:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }

    return res_dict


def uop3s(ReqTree, testcases, r2c):
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/功能的易定制性",
        "des": "为用户使用方便而提供的可被定制的功能和操作规程的数量",
        "val": None
    }
    B_dict = {
        "id": "B",
        "type": "需求文档",
        "source": RequirementFile + "/具体需求(运行模式组织1)/其他需求/支持用户定制功能/表格",
        "des": "用户能够受益于定制的功能和操作规程的数量",
        "val": None
    }
    try:
        time = ReqFunc.func_34(ReqTree)
        if time:
            B = len(time)
            B_dict = {
                "id": "B",
                "type": "需求文档",
                "source": RequirementFile+"/具体需求(运行模式组织1)/其他需求/支持用户定制功能/表格",
                "des": "用户能够受益于定制的功能和操作规程的数量",
                "val": B
            }
            test = match2.getTestCases("功能的易定制性", testcases, r2c)
            A = 0
            for i in test.values():
                if i == "通过":
                    A += 1
            A_dict = {
                "id": "A",
                "type": "测试文档",
                "source": TestReportFile+"/功能的易定制性",
                "des": "为用户使用方便而提供的可被定制的功能和操作规程的数量",
                "val": A
            }
            res = A / B
            res_dict = {
                "val": res,
                "sub": [A_dict, B_dict]
            }
        else:
            res_dict = {
                "val": None,
                "sub": [A_dict, B_dict]
            }
    except:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }

    return res_dict


def uop2g(InterfaceTree, testcases, r2c):
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/消息的明确性",
        "des": "传达给用户正确结果或指令的消息数量",
        "val": None
    }
    B_dict = {
        "id": "B",
        "type": "设计文档",
        "source": InterfaceDesignFile + "/接口设计/接口通信特性/消息格式化/表格",
        "des": "实现的消息数量",
        "val": None
    }
    try:
        time = InterfaceDesignFunc.func_333(InterfaceTree)
        if time:
            B = len(time)
            B_dict = {
                "id": "B",
                "type": "设计文档",
                "source": InterfaceDesignFile+"/接口设计/接口通信特性/消息格式化/表格",
                "des": "实现的消息数量",
                "val": B
            }
            test = match2.getTestCases("消息的明确性", testcases, r2c)
            A = 0
            for i in test.values():
                if i == "通过":
                    A += 1
            A_dict = {
                "id": "A",
                "type": "测试文档",
                "source": TestReportFile+"/消息的明确性",
                "des": "传达给用户正确结果或指令的消息数量",
                "val": A
            }
            res = A / B
            res_dict = {
                "val": res,
                "sub": [A_dict, B_dict]
            }
        else:
            res_dict = {
                "val": None,
                "sub": [A_dict, B_dict]
            }
    except:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }

    return res_dict


def uop1g(ReqTree, testcases, r2c):
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/操作一致性",
        "des": "不一致的特定交互式任务数量",
        "val": None
    }
    B_dict = {
        "id": "B",
        "type": "需求文档",
        "source": RequirementFile + "/总体描述/产品描述/操作/操作一致性任务/表格",
        "des": "需要一致的交互任务的数量",
        "val": None
    }
    try:
        time = ReqFunc.func_32(ReqTree)
        if time:
            B = len(time)
            B_dict = {
                "id": "B",
                "type": "需求文档",
                "source": RequirementFile+"/总体描述/产品描述/操作/操作一致性任务/表格",
                "des": "需要一致的交互任务的数量",
                "val": B
            }
            test = match2.getTestCases("操作一致性", testcases, r2c)
            A = 0
            for i in test.values():
                if i == "通过":
                    A += 1
            A_dict = {
                "id": "A",
                "type": "测试文档",
                "source": TestReportFile+"/操作一致性",
                "des": "不一致的特定交互式任务数量",
                "val": B-A
            }
            res = A / B
            res_dict = {
                "val": res,
                "sub": [A_dict, B_dict]
            }
        else:
            res_dict = {
                "val": None,
                "sub": [A_dict, B_dict]
            }
    except:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }

    return res_dict


def ule4s(UserTree, testcases, r2c):
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile+"/用户界面的自解释性",
        "des": "以用户可以理解的方式所呈现信息元素和步骤的数量",
        "val": None
    }
    B_dict = {
        "id": "B",
        "type": "用户手册",
        "source": UserMannelFile+"/~/处理过程/",
        "des": "对于新用户来说完成常规任务所需信息元素和步骤的数量",
        "val": None
    }
    try:
        time = UserMannelFunc.func_31(UserTree)
        if time:
            B = len(time)
            B_dict = {
                "id": "B",
                "type": "用户手册",
                "source": UserMannelFile+"/~/处理过程/",
                "des": "对于新用户来说完成常规任务所需信息元素和步骤的数量",
                "val": B
            }
            test = match2.getTestCases("用户界面的自解释性", testcases, r2c)
            A = 0
            for i in test.values():
                if i == "通过":
                    A += 1
            A_dict = {
                "id": "A",
                "type": "测试文档",
                "source": TestReportFile+"/用户界面的自解释性",
                "des": "以用户可以理解的方式所呈现信息元素和步骤的数量",
                "val": A
            }
            res = A / B
            res_dict = {
                "val": res,
                "sub": [A_dict, B_dict]
            }
        else:
            res_dict = {
                "val": None,
                "sub": [A_dict, B_dict]
            }
    except:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }
    return res_dict


def ule3s(testcases, r2c):
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/差错信息的易理解性",
        "des": "给出差错发生原因及可能解决方法的差错信息数量",
        "val": None
    }
    B_dict = {
        "id": "B",
        "type": "测试文档",
        "source": TestReportFile + "/差错信息的易理解性",
        "des": "差错信息的数量",
        "val": None
    }
    try:
        test = match2.getTestCases("差错信息的易理解性", testcases, r2c)
        B = len(test)
        if B:
            B_dict = {
                "id": "B",
                "type": "测试文档",
                "source": TestReportFile+"/差错信息的易理解性",
                "des": "差错信息的数量",
                "val": B
            }
            A = 0
            for i in test.values():
                if i == "通过":
                    A += 1
            A_dict = {
                "id": "A",
                "type": "测试文档",
                "source": TestReportFile+"/差错信息的易理解性",
                "des": "给出差错发生原因及可能解决方法的差错信息数量",
                "val": A
            }
            res = A / B
            res_dict = {
                "val": res,
                "sub": [A_dict, B_dict]
            }
        else:
            res_dict = {
                "val": None,
                "sub": [A_dict, B_dict]
            }
    except:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }
    return res_dict


def ule2s(InterfaceTree, testcases, r2c):
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/输入字段的默认值",
        "des": "运行过程中自动填充默认值的输人字段数量",
        "val": None
    }
    B_dict = {
        "id": "B",
        "type": "设计文档",
        "source": InterfaceDesignFile + "/差错信息的易理解性",
        "des": "具有默认值的输人字段的数量",
        "val": None
    }
    try:
        time = InterfaceDesignFunc.func_29(InterfaceTree)
        if time:
            B = len(time)
            B_dict = {
                "id": "B",
                "type": "设计文档",
                "source": InterfaceDesignFile+"/差错信息的易理解性",
                "des": "具有默认值的输人字段的数量",
                "val": B
            }
            test = match2.getTestCases("输入字段的默认值", testcases, r2c)
            A = 0
            for i in test.values():
                if i == "通过":
                    A += 1
            A_dict = {
                "id": "A",
                "type": "测试文档",
                "source": TestReportFile + "/输入字段的默认值",
                "des": "运行过程中自动填充默认值的输人字段数量",
                "val": A
            }
            res = A / B
            res_dict = {
                "val": res,
                "sub": [A_dict, B_dict]
            }
        else:
            res_dict = {
                "val": None,
                "sub": [A_dict, B_dict]
            }
    except:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }
    return res_dict


def ule1g(UserTree, ReqTree):
    A_dict = {
        "id": "A",
        "type": "用户手册",
        "source": UserMannelFile + "/~/处理过程/",
        "des": "在用户文档和/或帮助机制中按要求描述的功能数量",
        "val": None
    }
    B_dict = {
        "id": "B",
        "type": "需求文档",
        "source": RequirementFile + "/总体描述/产品功能/",
        "des": "要求实现的功能总数量",
        "val": None
    }
    try:
        time = UserMannelFunc.func_28(UserTree)
        if time:
            A = len(time)
            A_dict = {
                "id": "A",
                "type": "用户手册",
                "source": UserMannelFile+"/~/处理过程/",
                "des": "在用户文档和/或帮助机制中按要求描述的功能数量",
                "val": A
            }
            test = ReqFunc.func_24(ReqTree)
            B = len(test)
            B_dict = {
                "id": "B",
                "type": "需求文档",
                "source": RequirementFile+"/总体描述/产品功能/",
                "des": "要求实现的功能总数量",
                "val": B
            }

            res = A / B
            res_dict = {
                "val": res,
                "sub": [A_dict, B_dict]
            }
        else:
            res_dict = {
                "val": None,
                "sub": [A_dict, B_dict]
            }
    except:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }
    return res_dict


def uap3g(testcases, r2c):
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/入口点的自描述性",
        "des": "能说明网站目的的引导页数量",
        "val": None
    }
    B_dict = {
        "id": "B",
        "type": "测试文档",
        "source": TestReportFile + "/入口点的自描述性",
        "des": "网站中引导页的数量",
        "val": None
    }
    try:
        test = match2.getTestCases("入口点的自描述性", testcases, r2c)
        B = len(test)
        if B:
            B_dict = {
                "id": "B",
                "type": "测试文档",
                "source": TestReportFile+"/入口点的自描述性",
                "des": "网站中引导页的数量",
                "val": B
            }
            A = 0
            for i in test.values():
                if i == "通过":
                    A += 1
            A_dict = {
                "id": "A",
                "type": "测试文档",
                "source": TestReportFile + "/入口点的自描述性",
                "des": "能说明网站目的的引导页数量",
                "val": A
            }
            res = A / B
            res_dict = {
                "val": res,
                "sub": [A_dict, B_dict]
            }
        else:
            res_dict = {
                "val": None,
                "sub": [A_dict, B_dict]
            }
    except:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }
    return res_dict


def uap2g(ReqTree, testcases, r2c):
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/系统的演示功能",
        "des": "具有演示功能的任务的数量",
        "val": None
    }
    B_dict = {
        "id": "B",
        "type": "需求文档",
        "source": RequirementFile + "/总体描述/产品功能/功能演示",
        "des": "期望能从演示功能中获益的任务数量",
        "val": None
    }
    try:
        time = ReqFunc.func_25(ReqTree)
        if time:
            B = len(time)
            B_dict = {
                "id": "B",
                "type": "需求文档",
                "source": RequirementFile+"/总体描述/产品功能/功能演示",
                "des": "期望能从演示功能中获益的任务数量",
                "val": B
            }
            test = match2.getTestCases("系统的演示功能", testcases, r2c)
            A = 0
            for i in test.values():
                if i == "通过":
                    A += 1
            A_dict = {
                "id": "A",
                "type": "测试文档",
                "source": TestReportFile + "/系统的演示功能",
                "des": "具有演示功能的任务的数量",
                "val": A
            }
            res = A / B
            res_dict = {
                "val": res,
                "sub": [A_dict, B_dict]
            }
        else:
            res_dict = {
                "val": None,
                "sub": [A_dict, B_dict]
            }
    except:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }
    return res_dict


def uap1g(UserTree, ReqTree):
    A_dict = {
        "id": "A",
        "type": "用户手册",
        "source": UserMannelFile + "/~",
        "des": "在产品描述或用户文档中所描述的使用场景数量",
        "val": None
    }
    B_dict = {
        "id": "B",
        "type": "需求文档",
        "source": RequirementFile + "/总体描述/产品功能/",
        "des": "要求实现的功能总数量",
        "val": None
    }
    try:
        time = UserMannelFunc.func_23(UserTree)
        if time:
            A = len(time)
            A_dict = {
                "id": "A",
                "type": "用户手册",
                "source": UserMannelFile+"/~",
                "des": "在产品描述或用户文档中所描述的使用场景数量",
                "val": A
            }
            test = ReqFunc.func_24(ReqTree)
            B = len(test)
            B_dict = {
                "id": "B",
                "type": "需求文档",
                "source": RequirementFile+"/总体描述/产品功能/",
                "des": "要求实现的功能总数量",
                "val": B
            }

            res = A / B
            res_dict = {
                "val": res,
                "sub": [A_dict, B_dict]
            }
        else:
            res_dict = {
                "val": None,
                "sub": [A_dict, B_dict]
            }
    except:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }
    return res_dict


def mte1g(TestTree):
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/测试活动总结/测试功能实现/表格",
        "des": "按照规定已实现的测试功能数量",
        "val": None
    }
    B_dict = {
        "id": "B",
        "type": "测试文档",
        "source": TestReportFile + "/测试活动总结/测试功能实现/表格",
        "des": "需要的测试功能的数量",
        "val": None
    }
    res = -1
    A = 0
    B = 0
    root = TestTree[0]
    name_1 = "测试活动总结"
    if name_1 in root.son_text:
        idx = root.son_text.index(name_1)
        node_1 = TestTree[root.son_id[idx]]
        name_2 = "测试功能实现"
        if name_2 in node_1.son_text:
            idx_2 = node_1.son_text.index(name_2)
            node_2 = TestTree[node_1.son_id[idx_2]]
            try:
                table = TestTree[node_2.son_id[0]].table_info
                if table:
                    for val in list(table.values())[1:]:
                        B += int(val[1])
                        A += int(val[2])
                    A_dict = {
                        "id": "A",
                        "type": "测试文档",
                        "source": TestReportFile + "/测试活动总结/测试功能实现/表格",
                        "des": "按照规定已实现的测试功能数量",
                        "val": A
                    }
                    B_dict = {
                        "id": "B",
                        "type": "测试文档",
                        "source": TestReportFile + "/测试活动总结/测试功能实现/表格",
                        "des": "需要的测试功能的数量",
                        "val": B
                    }
                    res = A / B
                    res_dict = {
                        "val": res,
                        "sub": [A_dict, B_dict]
                    }
            except:
                print("找不到表格")
                res_dict = {
                    "val": None,
                    "sub": [A_dict, B_dict]
                }

    else:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }
    return res_dict


def mmd1g(MaintainTree):
    B_dict = {
        "id": "B",
        "type": "维护手册",
        "source": MaintainFile + "/预期维护过的模块和系统的成本/工作：/表格",
        "des": "对一个指定类型的修改i所消耗的预期时间",
        "val": None
    }
    res = -1
    A = []
    B = []
    sublist = []
    root = MaintainTree[0]
    name = "预期维护过的模块和系统的成本/工作："
    if name in root.son_text:
        idx = root.son_text.index(name)
        node_1 = MaintainTree[root.son_id[idx]]
        try:
            table = MaintainTree[node_1.son_id[0]].table_info
            if table:
                for val in list(table.values())[2:]:
                    B.append(int(val[-1]))
            for i in range(len(B)):
                B_dict = {
                    "id": "B" + str(i),
                    "type": "维护手册",
                    "source": MaintainFile + "/预期维护过的模块和系统的成本/工作：/表格",
                    "des": "对一个指定类型的修改i所消耗的预期时间",
                    "val": B[i]
                }
                sublist.append(B_dict)
        except:
            print("找不到表格")
            B_dict = {
                "id": "B",
                "type": "维护手册",
                "source": MaintainFile + "/预期维护过的模块和系统的成本/工作：/表格",
                "des": "对一个指定类型的修改i所消耗的预期时间",
                "val": None
            }
            sublist.append(B_dict)

    name2 = "所有维护的模块和系统的结果及工作量："
    if name2 in root.son_text:
        idx_2 = root.son_text.index(name2)
        node_2 = MaintainTree[root.son_id[idx_2]]
        try:
            table2 = MaintainTree[node_2.son_id[0]].table_info
            if table2:
                for val2 in list(table2.values())[1:]:
                    A.append(int(val2[-1]))
            for i in range(len(A)):
                A_dict = {
                    "id": "A" + str(i),
                    "type": "维护手册",
                    "source": MaintainFile + "/所有维护的模块和系统的结果及工作量：/表格",
                    "des": "对一个指定类型的修改i所消耗的总工作时间",
                    "val": A[i]
                }
                sublist.append(A_dict)
        except:
            print("找不到表格")
            A_dict = {
                "id": "A",
                "type": "维护手册",
                "source": MaintainFile + "/所有维护的模块和系统的结果及工作量：/表格",
                "des": "对一个指定类型的修改i所消耗的总工作时间",
                "val": None
            }
            sublist.append(A_dict)

    try:
        res = 0
        for i in range(len(B)):
            res += A[i]/B[i]
        res = res/len(B)
        N_dict = {
            "id": "N",
            "type": "维护手册",
            "source": MaintainFile + "/预期维护过的模块和系统的成本/工作：/表格",
            "des": "测量的修改数量",
            "val": len(B)
        }
        sublist.append(N_dict)
        res_dict = {
            "val": res,
            "sub": sublist
        }

    except:
        res_dict = {
            "val": None,
            "sub": sublist
        }

    return res_dict


def mmd2g(MaintainTree):
    res = -1
    A = 0
    B = 0
    root = MaintainTree[0]

    name2 = "所有维护的模块和系统的结果及工作量："
    if name2 in root.son_text:
        idx_2 = root.son_text.index(name2)
        node_2 = MaintainTree[root.son_id[idx_2]]
        try:
            table2 = MaintainTree[node_2.son_id[0]].table_info
            if table2:
                for val2 in list(table2.values())[1:]:
                    content = val2[1]
                    B += 1
                    check = "无失效"
                    if check in content:
                        A += 1
            A_dict = {
                "id": "A",
                "type": "维护手册",
                "source": MaintainFile + "/所有维护的模块和系统的结果及工作量：/表格",
                "des": "在实施后的规定时间内,导致事故或失效发生的修改数量",
                "val": B-A
            }
            B_dict = {
                "id": "B",
                "type": "维护手册",
                "source": MaintainFile + "/所有维护的模块和系统的结果及工作量：/表格",
                "des": "实施的修改数量",
                "val": B
            }
        except:
            print("找不到表格")
            A_dict = {
                "id": "A",
                "type": "维护手册",
                "source": MaintainFile + "/所有维护的模块和系统的结果及工作量：/表格",
                "des": "在实施后的规定时间内,导致事故或失效发生的修改数量",
                "val": None
            }
            B_dict = {
                "id": "B",
                "type": "维护手册",
                "source": MaintainFile + "/所有维护的模块和系统的结果及工作量：/表格",
                "des": "实施的修改数量",
                "val": None
            }
    if B:
        res = A / B
        res_dict = {
            "val": res,
            "sub": [A_dict, B_dict]
        }
    else:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }

    return res_dict


def check_time(pre, ral):
    pre_start = pre[0].split(".")
    pre_end = pre[1].split(".")
    ral_start = ral[0].split(".")
    ral_end = ral[1].split(".")
    res = 1
    for i in range(len(pre_start)):
        if int(pre_start[i]) < int(ral_start[i]):
            break
        elif int(pre_start[i]) > int(ral_start[i]):
            res = 0
            break
    if res == 0:
        return 0

    for i in range(len(pre_start)):
        if int(pre_end[i]) > int(ral_end[i]):
            break
        elif int(pre_end[i]) < int(ral_end[i]):
            res = 0
            break
    return res


def mmd3s(MaintainTree):
    A_dict = {
        "id": "A",
        "type": "维护手册",
        "source": MaintainFile + "/所有维护的模块和系统的结果及工作量：/表格",
        "des": "在指定的持续时间内实际做出修改的项目数",
        "val": None
    }
    B_dict = {
        "id": "B",
        "type": "维护手册",
        "source": MaintainFile + "/预期维护过的模块和系统的成本/工作：/表格",
        "des": "在指定的持续时间内要求修改的项目数",
        "val": None
    }
    res = -1
    A = 0
    B = 0
    dict = {}
    root = MaintainTree[0]
    name = "预期维护过的模块和系统的成本/工作："
    if name in root.son_text:
        idx = root.son_text.index(name)
        node_1 = MaintainTree[root.son_id[idx]]
        try:
            table = MaintainTree[node_1.son_id[0]].table_info
            if table:
                for val in list(table.values())[2:]:
                    dict[val[0]] = [val[4], val[5]]
        except:
            print("找不到预期表格")
    B = len(dict.keys())
    if B:
        B_dict = {
            "id": "B",
            "type": "维护手册",
            "source": MaintainFile + "/预期维护过的模块和系统的成本/工作：/表格",
            "des": "在指定的持续时间内要求修改的项目数",
            "val": B
        }
    name2 = "所有维护的模块和系统的结果及工作量："
    if name2 in root.son_text:
        idx_2 = root.son_text.index(name2)
        node_2 = MaintainTree[root.son_id[idx_2]]
        try:
            table2 = MaintainTree[node_2.son_id[0]].table_info
            if table2:
                for val2 in list(table2.values())[1:]:
                    id = val2[0]
                    pre = dict[id]
                    ral = [val2[2], val2[3]]
                    if check_time(pre, ral):
                        A += 1

            A_dict = {
                "id": "A",
                "type": "维护手册",
                "source": MaintainFile + "/所有维护的模块和系统的结果及工作量：/表格",
                "des": "在指定的持续时间内实际做出修改的项目数",
                "val": A
            }

        except:
            print("找不到结果表格")
    # print(A, B)
    if B:
        res = A / B
        res_dict = {
            "val": res,
            "sub": [A_dict, B_dict]
        }
    else:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }

    return res_dict


def fcr1g(TreeList1, TreeList2, TreeList3):
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/",
        "des": "功能不正确的数量",
        "val": None
    }
    B_dict = {
        "id": "B",
        "type": "需求文档",
        "source": RequirementFile + "/具体需求(运行模式组织1)/ 功能需求/~/",
        "des": "考虑的功能数量",
        "val": None
    }

    res_1 = rq.func_1(TreeList3)
    B = len(res_1)
    if B:
        B_dict = {
            "id": "B",
            "type": "需求文档",
            "source": RequirementFile + "/具体需求(运行模式组织1)/ 功能需求/~/",
            "des": "考虑的功能数量",
            "val": B
        }
    # print("fcr1g",B)
    A = 0
    r2c = mt.func4(TreeList1)
    testcases = mt.func3(TreeList2)
    for requirement in res_1:
        res = mt.getTestCases(requirement.text, testcases, r2c)
        for key in res.keys():
            if res[key] == "不通过":
                A += 1
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/",
        "des": "功能不正确的数量",
        "val": A
    }
    res = 1 - (A * 1.0) / B
    res_dict = {
        "val": res,
        "sub": [A_dict, B_dict]
    }
    return res_dict


def ptb1g(TreeList1, TreeList2):
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/平均响应时间",
        "des": "第i次测量时系统响应一个特定用户任务或系统任务花费的时间",
        "val": None
    }
    N_dict = {
        "id": "N",
        "type": "测试文档",
        "source": TestReportFile + "/平均响应时间",
        "des": "测得的响应次数",
        "val": None
    }
    sublist = []
    r2c = mt.func4(TreeList1)
    testcases = mt.func3(TreeList2)
    time = 0
    if "平均响应时间" in r2c.keys():
        res = mt.getTestCases("平均响应时间", testcases, r2c)
        n = len(res.keys())
        if n:
            N_dict = {
                "id": "N",
                "type": "测试文档",
                "source": TestReportFile + "/平均响应时间",
                "des": "测得的响应次数",
                "val": n
            }
        sublist.append(N_dict)
        index = 0
        for key in res.keys():
            time += res[key]
            A_dict = {
                "id": "A" + str(index),
                "type": "测试文档",
                "source": TestReportFile + "/平均响应时间",
                "des": "第i次测量时系统响应一个特定用户任务或系统任务花费的时间",
                "val": res[key]
            }
            sublist.append(A_dict)
            index += 1

        res = time / n
        res_dict = {
            "val": res,
            "sub": sublist
        }
        return res_dict
    else:
        res_dict = {
            "val": None,
            "sub": [A_dict, N_dict]
        }
        return res_dict


def ptb2g(TreeList3, PTb_1_G):
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/平均响应时间",
        "des": "PTb-1-G测度中所测量的平均响应时间",
        "val": None
    }
    B_dict = {
        "id": "B",
        "type": "需求文档",
        "source": RequirementFile + "/具体需求(运行模式组织1)/性能需求时间特性/平均响应时间",
        "des": "规定的任务响应时间",
        "val": None
    }
    if PTb_1_G:
        A_dict = {
            "id": "A",
            "type": "测试文档",
            "source": TestReportFile + "/平均响应时间",
            "des": "PTb-1-G测度中所测量的平均响应时间",
            "val": PTb_1_G
        }
    res_1 = rq.func_7(TreeList3)
    B = float(res_1[0])
    if res_1[1] == "s":
        B *= 1000

    if B:
        B_dict = {
            "id": "B",
            "type": "需求文档",
            "source": RequirementFile + "/具体需求(运行模式组织1)/性能需求时间特性/平均响应时间",
            "des": "规定的任务响应时间",
            "val": B
        }
    if A_dict['val'] is not None and B_dict['val'] is not None:
        res = PTb_1_G / B
        res_dict = {
            "val": res,
            "sub": [A_dict, B_dict]
        }
    else:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }

    return res_dict


def ptb3g(TreeList1, TreeList2):
    A_dict = {
        "id": "B-A",
        "type": "测试文档",
        "source": TestReportFile + "/平均周转时间",
        "des": "周转时间",
        "val": None
    }
    N_dict = {
        "id": "N",
        "type": "测试文档",
        "source": TestReportFile + "/平均周转时间",
        "des": "测量的次数",
        "val": None
    }
    sublist = []
    r2c = mt.func4(TreeList1)
    testcases = mt.func3(TreeList2)
    time = 0
    if "平均周转时间" in r2c.keys():
        res = mt.getTestCases("平均周转时间", testcases, r2c)
        n = len(res.keys())
        if n:
            N_dict = {
                "id": "N",
                "type": "测试文档",
                "source": TestReportFile + "/平均周转时间",
                "des": "测量的次数",
                "val": n
            }
        sublist.append(N_dict)
        index = 0
        for key in res.keys():
            time += res[key]
            A_dict = {
                "id": "B"+str(index)+"-A"+str(index),
                "type": "测试文档",
                "source": TestReportFile + "/平均周转时间",
                "des": "周转时间",
                "val": res[key]
            }
            index += 1
            sublist.append(A_dict)
        res = time / n
        res_dict = {
            "val": res,
            "sub": sublist
        }
        return res_dict
    else:
        res_dict = {
            "val": None,
            "sub": [A_dict, N_dict]
        }
        return res_dict


def ptb4g(TreeList3, PTb_3_G):

    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/平均周转时间",
        "des": "PTb-3-G测度中所测量的平均周转时间",
        "val": PTb_3_G
    }
    B_dict = {
        "id": "B",
        "type": "需求文档",
        "source": RequirementFile + "/具体需求(运行模式组织1)/性能需求/时间特性/平均周转时间",
        "des": "规定的作业或异步进程的周转时间",
        "val": None
    }
    res_1 = rq.func_8(TreeList3)
    B = float(res_1[0])
    if res_1[1] == "s":
        B *= 1000
    if B:
        B_dict = {
            "id": "B",
            "type": "需求文档",
            "source": RequirementFile + "/具体需求(运行模式组织1)/性能需求/时间特性/平均周转时间",
            "des": "规定的作业或异步进程的周转时间",
            "val": B
        }
        res = PTb_3_G / B
        res_dict = {
            "val": res,
            "sub": [A_dict, B_dict]
        }
    else:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }
    return res_dict


def ptb5g(TreeList1, TreeList2):
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/平均吞吐量",
        "des": "第i次观察时间内完成的作业数量",
        "val": None
    }
    B_dict = {
        "id": "B",
        "type": "测试文档",
        "source": TestReportFile + "/平均吞吐量",
        "des": "第i次观察时间的周期",
        "val": None
    }
    N_dict = {
        "id": "N",
        "type": "测试文档",
        "source": TestReportFile + "/平均吞吐量",
        "des": "观察的次数",
        "val": None
    }
    sublist = []
    r2c = mt.func4(TreeList1)
    testcases = mt.func3(TreeList2)
    time = 0
    if "平均吞吐量" in r2c.keys():
        res = mt.getTestCases("平均吞吐量", testcases, r2c)
        # print("res",res)
        n = len(res.keys())
        if n:
            N_dict = {
                "id": "N",
                "type": "测试文档",
                "source": TestReportFile + "/平均吞吐量",
                "des": "观察的次数",
                "val": n
            }
        sublist.append(N_dict)
        index = 0
        for key in res.keys():
            A = res[key]['A']
            A_dict = {
                "id": "A" + str(index),
                "type": "测试文档",
                "source": TestReportFile + "/平均吞吐量",
                "des": "第i次观察时间内完成的作业数量",
                "val": A
            }
            sublist.append(A_dict)
            B = res[key]['B']
            if B:
                B_dict = {
                    "id": "B" + str(index),
                    "type": "测试文档",
                    "source": TestReportFile + "/平均吞吐量",
                    "des": "第i次观察时间的周期",
                    "val": B
                }
                sublist.append(B_dict)
                time += A/B
            index += 1
        res_dict = {
            "val": time / n,
            "sub": sublist
        }
        return res_dict
    else:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict, N_dict]
        }
        return res_dict


def pru1g(TreeList1, TreeList2):
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/处理器平均占用率",
        "des": "第i次观察中,处理器执行一组给定任务所用的时间",
        "val": None
    }
    B_dict = {
        "id": "B",
        "type": "测试文档",
        "source": TestReportFile + "/处理器平均占用率",
        "des": "第i次观察中,执行任务的运行时间",
        "val": None
    }
    N_dict = {
        "id": "N",
        "type": "测试文档",
        "source": TestReportFile + "/处理器平均占用率",
        "des": "观察的次数",
        "val": None
    }
    sublist = []
    r2c = mt.func4(TreeList1)
    testcases = mt.func3(TreeList2)
    time = 0
    if "处理器平均占用率" in r2c.keys():
        res = mt.getTestCases("处理器平均占用率", testcases, r2c)
        n = len(res.keys())
        if n:
            N_dict = {
                "id": "N",
                "type": "测试文档",
                "source": TestReportFile + "/处理器平均占用率",
                "des": "观察的次数",
                "val": n
            }
        sublist.append(N_dict)
        index = 0
        for key in res.keys():
            A = res[key]['res']
            A_dict = {
                "id": "A" + str(index),
                "type": "测试文档",
                "source": TestReportFile + "/处理器平均占用率",
                "des": "第i次观察中,处理器执行一组给定任务所用的时间",
                "val": A
            }
            sublist.append(A_dict)
            B = res[key]["pre"]
            if B:
                B_dict = {
                    "id": "B" + str(index),
                    "type": "测试文档",
                    "source": TestReportFile + "/处理器平均占用率",
                    "des": "第i次观察中,执行任务的运行时间",
                    "val": B
                }
                sublist.append(B_dict)
                time += A/B
            index += 1
        res_dict = {
            "val": time / n,
            "sub": sublist
        }
        return res_dict
    else:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict, N_dict]
        }
        return res_dict


def pru2g(TreeList1, TreeList2):
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/内存平均占用率",
        "des": "第i次样本处理中执行一组给定任务所占用的实际内存大小",
        "val": None
    }
    B_dict = {
        "id": "B",
        "type": "测试文档",
        "source": TestReportFile + "/内存平均占用率",
        "des": "第i次样本处理期间可用于执行任务的内存大小",
        "val": None
    }
    N_dict = {
        "id": "N",
        "type": "测试文档",
        "source": TestReportFile + "/内存平均占用率",
        "des": "处理的样本数",
        "val": None
    }
    sublist = []
    r2c = mt.func4(TreeList1)
    testcases = mt.func3(TreeList2)
    time = 0
    if "内存平均占用率" in r2c.keys():
        res = mt.getTestCases("内存平均占用率", testcases, r2c)
        n = len(res.keys())
        if n:
            N_dict = {
                "id": "N",
                "type": "测试文档",
                "source": TestReportFile + "/内存平均占用率",
                "des": "处理的样本数",
                "val": n
            }
        sublist.append(N_dict)
        index = 0
        for key in res.keys():
            A = res[key]['res']
            A_dict = {
                "id": "A" + str(index),
                "type": "测试文档",
                "source": TestReportFile + "/内存平均占用率",
                "des": "第i次样本处理中执行一组给定任务所占用的实际内存大小",
                "val": A
            }
            sublist.append(A_dict)
            B = res[key]['pre']
            if B:
                B_dict = {
                    "id": "B"+str(index),
                    "type": "测试文档",
                    "source": TestReportFile + "/内存平均占用率",
                    "des": "第i次样本处理期间可用于执行任务的内存大小",
                    "val": B
                }
                sublist.append(B_dict)
                time += A/B
            index += 1
        res_dict = {
            "val": time / n,
            "sub": sublist
        }
        return res_dict
    else:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict, N_dict]
        }
        return res_dict


def pru3g(TreeList1, TreeList2):
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/I/O设备平均占用率",
        "des": "第i次观察中,执行一组给定任务所占用I/O设备的持续时间",
        "val": None
    }
    B_dict = {
        "id": "B",
        "type": "测试文档",
        "source": TestReportFile + "/I/O设备平均占用率",
        "des": "第i次观察中,执行任务所需I/O运行的持续时间",
        "val": None
    }
    N_dict = {
        "id": "N",
        "type": "测试文档",
        "source": TestReportFile + "/I/O设备平均占用率",
        "des": "观察次数",
        "val": None
    }
    sublist = []
    r2c = mt.func4(TreeList1)
    testcases = mt.func3(TreeList2)
    time = 0
    if "I/O设备平均占用率" in r2c.keys():
        res = mt.getTestCases("I/O设备平均占用率", testcases, r2c)
        n = len(res.keys())
        if n:
            N_dict = {
                "id": "N",
                "type": "测试文档",
                "source": TestReportFile + "/I/O设备平均占用率",
                "des": "观察次数",
                "val": n
            }
        sublist.append(N_dict)
        index = 0
        for key in res.keys():
            A = res[key]['res']
            A_dict = {
                "id": "A",
                "type": "测试文档",
                "source": TestReportFile + "/I/O设备平均占用率",
                "des": "第i次观察中,执行一组给定任务所占用I/O设备的持续时间",
                "val": A
            }
            sublist.append(A_dict)
            B = res[key]['pre']
            if B:
                B_dict = {
                    "id": "B",
                    "type": "测试文档",
                    "source": TestReportFile + "/I/O设备平均占用率",
                    "des": "第i次观察中,执行任务所需I/O运行的持续时间",
                    "val": B
                }
                sublist.append(B_dict)
                time += A/B
            index += 1
        res_dict = {
            "val": time / n,
            "sub": sublist
        }
        return res_dict
    else:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict, N_dict]
        }
        return res_dict


def pru4s(TreeList1, TreeList2):
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/带宽平均占用率",
        "des": "执行一组给定任务时测得的实际传输带宽",
        "val": None
    }
    B_dict = {
        "id": "B",
        "type": "测试文档",
        "source": TestReportFile + "/带宽平均占用率",
        "des": "执行一组任务时可用带宽容量",
        "val": None
    }
    sublist = []
    r2c = mt.func4(TreeList1)
    testcases = mt.func3(TreeList2)
    time = 0
    if "带宽平均占用率" in r2c.keys():
        res = mt.getTestCases("带宽平均占用率", testcases, r2c)
        n = len(res.keys())

        index = 0
        time = 0
        for key in res.keys():
            A = res[key]['res']
            B = res[key]['pre']
            A_dict = {
                "id": "A"+str(index),
                "type": "测试文档",
                "source": TestReportFile + "/带宽平均占用率",
                "des": "执行一组给定任务时测得的实际传输带宽",
                "val": A
            }
            sublist.append(A_dict)
            B_dict = {
                "id": "B"+str(index),
                "type": "测试文档",
                "source": TestReportFile + "/带宽平均占用率",
                "des": "执行一组任务时可用带宽容量",
                "val": B
            }
            sublist.append(B_dict)
            time += A/B
            index += 1

        res_dict = {
            "val": time/n,
            "sub": sublist
        }
        return res_dict
    else:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }
        return res_dict


def pca1g(TreeList1, TreeList2):
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/同时运行的用户数量",
        "des": "观察时间内完成事务的数量",
        "val": None
    }
    B_dict = {
        "id": "B",
        "type": "测试文档",
        "source": TestReportFile + "/同时运行的用户数量",
        "des": "观察时间",
        "val": None
    }
    sublist = []
    r2c = mt.func4(TreeList1)
    testcases = mt.func3(TreeList2)
    time = 0
    if "同时运行的用户数量" in r2c.keys():
        res = mt.getTestCases("同时运行的用户数量", testcases, r2c)
        n = len(res.keys())
        i = 0
        time = 0
        for key in res.keys():
            A = res[key]['A']
            A_dict = {
                "id": "A"+str(i),
                "type": "测试文档",
                "source": TestReportFile + "/同时运行的用户数量",
                "des": "观察时间内完成事务的数量",
                "val": A
            }
            B = res[key]['B']
            B_dict = {
                "id": "B"+str(i),
                "type": "测试文档",
                "source": TestReportFile + "/同时运行的用户数量",
                "des": "观察时间",
                "val": B
            }
            time += A/B
            sublist.append(A_dict)
            sublist.append(B_dict)
            i += 1
        res_dict = {
            "val": time / n,
            "sub": sublist
        }
        return res_dict
    else:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }
        return res_dict


def pca2g(TreeList1, TreeList2):
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/系统支持的用户访问量",
        "des": "第i次观察中,同时访问系统的最大用户数量",
        "val": None
    }
    N_dict = {
        "id": "N",
        "type": "测试文档",
        "source": TestReportFile + "/系统支持的用户访问量",
        "des": "观察次数",
        "val": None
    }
    sublist = []
    r2c = mt.func4(TreeList1)
    testcases = mt.func3(TreeList2)
    time = 0
    if "系统支持的用户访问量" in r2c.keys():
        res = mt.getTestCases("系统支持的用户访问量", testcases, r2c)
        n = len(res.keys())
        i = 0
        if n:
            N_dict = {
                "id": "N",
                "type": "测试文档",
                "source": TestReportFile + "/系统支持的用户访问量",
                "des": "观察次数",
                "val": n
            }
        sublist.append(N_dict)
        for key in res.keys():
            time += res[key]
            A_dict = {
                "id": "A" + str(i),
                "type": "测试文档",
                "source": TestReportFile + "/系统支持的用户访问量",
                "des": "第i次观察中,同时访问系统的最大用户数量",
                "val": res[key]
            }
            sublist.append(A_dict)
            i += 1
        res_dict = {
            "val": time / n,
            "sub": sublist
        }
        return res_dict
    else:
        res_dict = {
            "val": None,
            "sub": [A_dict, N_dict]
        }
        return res_dict


def pca3s(TreeList1, TreeList2):
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/用户访问增长充分性",
        "des": "观察时间内成功增加的用户数量",
        "val": None
    }
    B_dict = {
        "id": "B",
        "type": "测试文档",
        "source": TestReportFile + "/用户访问增长充分性",
        "des": "观察时间",
        "val": None
    }
    sublist = []
    r2c = mt.func4(TreeList1)
    testcases = mt.func3(TreeList2)
    time = 0
    if "用户访问增长充分性" in r2c.keys():
        res = mt.getTestCases("用户访问增长充分性", testcases, r2c)
        n = len(res.keys())
        i = 0
        for key in res.keys():
            A = res[key]["A"]
            B = res[key]['B']
            A_dict = {
                "id": "A" + str(i),
                "type": "测试文档",
                "source": TestReportFile + "/用户访问增长充分性",
                "des": "观察时间内成功增加的用户数量",
                "val": A
            }
            B_dict = {
                "id": "B" + str(i),
                "type": "测试文档",
                "source": TestReportFile + "/用户访问增长充分性",
                "des": "观察时间",
                "val": B
            }
            sublist.append(A_dict)
            sublist.append(B_dict)
            time += A/B
            i += 1
        res_dict = {
            "val": time / n,
            "sub": sublist
        }
        return res_dict
    else:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }
        return res_dict


def cco1g(TreeList1, TreeList2, TreeList3):
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/与其他软件的共存性",
        "des": "与该产品可共存的其他规定的软件产品数量",
        "val": None
    }
    B_dict = {
        "id": "B",
        "type": "需求文档",
        "source": RequirementFile + "/具体需求(运行模式组织1)/软件系统属性/ 兼容性/ 运行时允许共存的软件",
        "des": "在运行环境中,该产品需要与其他软件产品共存的数量",
        "val": None
    }
    r2c = mt.func4(TreeList1)
    testcases = mt.func3(TreeList2)
    res_1 = rq.func_19(TreeList3)
    B = len(res_1)
    if B:
        B_dict = {
            "id": "B",
            "type": "需求文档",
            "source": RequirementFile + "/具体需求(运行模式组织1)/软件系统属性/ 兼容性/ 运行时允许共存的软件/表格",
            "des": "在运行环境中,该产品需要与其他软件产品共存的数量",
            "val": B
        }
    time = 0
    if "与其他软件的共存性" in r2c.keys():
        res = mt.getTestCases("与其他软件的共存性", testcases, r2c)
        for key in res.keys():
            if res[key] == "通过":
                time += 1
        A_dict = {
            "id": "A",
            "type": "测试文档",
            "source": TestReportFile + "/与其他软件的共存性",
            "des": "与该产品可共存的其他规定的软件产品数量",
            "val": time
        }
        res_dict = {
            "val": time / B,
            "sub": [A_dict, B_dict]
        }
    else:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }
    return res_dict


def cin1g(TreeList1, TreeList2, TreeList3):
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/数据格式的可交换性",
        "des": "与其他软件或系统可交换数据格式的数量",
        "val": None
    }
    B_dict = {
        "id": "B",
        "type": "需求文档",
        "source": RequirementFile + "/总体描述/产品描述/软件接口/表格",
        "des": "需要交换的数据格式数量",
        "val": None
    }
    r2c = mt.func4(TreeList1)
    testcases = mt.func3(TreeList2)
    res_1 = rq.func_20(TreeList3)
    B = len(res_1)
    if B:
        B_dict = {
            "id": "B",
            "type": "需求文档",
            "source": RequirementFile + "/总体描述/产品描述/软件接口/表格",
            "des": "需要交换的数据格式数量",
            "val": B
        }
    time = 0
    if "数据格式的可交换性" in r2c.keys():
        res = mt.getTestCases("数据格式的可交换性", testcases, r2c)
        for key in res.keys():
            if res[key] == "通过":
                time += 1
        A_dict = {
            "id": "A",
            "type": "测试文档",
            "source": TestReportFile + "/数据格式的可交换性",
            "des": "与其他软件或系统可交换数据格式的数量",
            "val": time
        }
        res_dict = {
            "val": time / B,
            "sub": [A_dict, B_dict]
        }
    else:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }
    return res_dict


def cin2g(TreeList1, TreeList2, TreeList3):
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/数据交换协议",
        "des": "实际支持数据交换协议的数量",
        "val": None
    }
    B_dict = {
        "id": "B",
        "type": "需求文档",
        "source": RequirementFile + "/总体描述/产品描述/通信接口/表格",
        "des": "规定支持的数据交换协议数量",
        "val": None
    }
    r2c = mt.func4(TreeList1)
    testcases = mt.func3(TreeList2)
    res_1 = rq.func_21(TreeList3)
    B = len(res_1)
    if B:
        B_dict = {
            "id": "B",
            "type": "需求文档",
            "source": RequirementFile + "/总体描述/产品描述/通信接口/表格",
            "des": "规定支持的数据交换协议数量",
            "val": B
        }
    time = 0
    if "数据交换协议" in r2c.keys():
        res = mt.getTestCases("数据交换协议", testcases, r2c)
        for key in res.keys():
            if res[key] == "通过":
                time += 1
        A_dict = {
            "id": "A",
            "type": "测试文档",
            "source": TestReportFile + "/数据交换协议",
            "des": "实际支持数据交换协议的数量",
            "val": time
        }
        res_dict = {
            "val": time / B,
            "sub": [A_dict, B_dict]
        }
    else:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }
    return res_dict


def cin3s(TreeList1, TreeList2, TreeList3):
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/外部接口的有效性",
        "des": "有效的外部接口数量",
        "val": None
    }
    B_dict = {
        "id": "B",
        "type": "需求文档",
        "source": RequirementFile + "/具体需求(运行模式组织1)/外部接口需求/",
        "des": "规定的外部接口数量",
        "val": None
    }
    r2c = mt.func4(TreeList1)
    testcases = mt.func3(TreeList2)
    res_1 = rq.func_22(TreeList3)
    B = len(res_1)
    if B:
        B_dict = {
            "id": "B",
            "type": "需求文档",
            "source": RequirementFile + "/具体需求(运行模式组织1)/外部接口需求/",
            "des": "规定的外部接口数量",
            "val": B
        }
    time = 0
    if "外部接口的有效性" in r2c.keys():
        res = mt.getTestCases("外部接口的有效性", testcases, r2c)
        for key in res.keys():
            if res[key] == "通过":
                time += 1
        A_dict = {
            "id": "A",
            "type": "测试文档",
            "source": TestReportFile + "/外部接口的有效性",
            "des": "有效的外部接口数量",
            "val": time
        }
        res_dict = {
            "val": time / B,
            "sub": [A_dict, B_dict]
        }
    else:
        res_dict = {
            "val": None,
            "sub": [A_dict, B_dict]
        }
    return res_dict


# def uap1g(TreeList3, TreeList4):
#     res_1 = rq.func_24(TreeList3)
#     res_2 = um.func_23(TreeList4)
#     B = len(res_1)
#     A = len(res_2)
#     return A * 1.0 / B


def prc1g(TreeList4):
    A_dict = {
        "id": "A",
        "type": "用户手册",
        "source": UserMannelFile + "/软件应用/表格",
        "des": "替换原软件产品后,本软件产品在没有任何额外的学习或变通的情况下,能够执行的用户功能数量",
        "val": None
    }
    B_dict = {
        "id": "B",
        "type": "用户手册",
        "source": UserMannelFile + "/软件应用/表格",
        "des": "替换原软件产品后,本软件产品中用户功能的数量",
        "val": None
    }
    sublist = []
    res = {}
    for node in TreeList4:
        if node.text.strip() == "软件应用":
            for j in node.son_id:
                if len(TreeList4[j].table_info.keys()) > 0:
                    table_dict = TreeList4[j].table_info
                    temp = {}
                    snames = table_dict[0]
                    for i in range(3, len(snames)):
                        temp[snames[i]] = [0, 0]
                    for key in table_dict.keys():
                        if table_dict[key][0] == "功能特性":
                            if table_dict[key][2] == "支持":
                                for i in range(3, len(snames)):
                                    if table_dict[key][i] == "支持/相似":
                                        temp[snames[i]][0] += 1
                                        temp[snames[i]][1] += 1
                                    elif table_dict[key][i] == "支持/不相似":
                                        temp[snames[i]][1] += 1
                    i = 0
                    for key in temp.keys():
                        res[key] = temp[key][0] * 1.0 / temp[key][1]
                        A_dict = {
                            "id": "A"+str(i),
                            "type": "用户手册",
                            "source": UserMannelFile + "/软件应用/表格",
                            "des": "替换原软件产品后,本软件产品在没有任何额外的学习或变通的情况下,能够执行的用户功能数量",
                            "val": temp[key][0]
                        }
                        B_dict = {
                            "id": "B" + str(i),
                            "type": "用户手册",
                            "source": UserMannelFile + "/软件应用/表格",
                            "des": "替换原软件产品后,本软件产品中用户功能的数量",
                            "val": temp[key][1]
                        }
                        sublist.append(A_dict)
                        sublist.append(B_dict)
                        i += 1
    res_dict = {
        "val": sum(list(res.values()))/len(list(res.keys())),
        "sub": sublist
    }
    return res_dict


def pre2s(TreeList4):
    A_dict = {
        "id": "A",
        "type": "用户手册",
        "source": UserMannelFile + "/软件应用/表格",
        "des": "优于或等于被替换产品的新产品质量测度数量",
        "val": None
    }
    B_dict = {
        "id": "B",
        "type": "用户手册",
        "source": UserMannelFile + "/软件应用/表格",
        "des": "被替换软件产品中的质量测度数量",
        "val": None
    }
    sublist = []
    res = {}
    for node in TreeList4:
        if node.text.strip() == "软件应用":
            for j in node.son_id:
                if len(TreeList4[j].table_info.keys()) > 0:
                    table_dict = TreeList4[j].table_info
                    snames = table_dict[0]
                    temp = {}
                    for i in range(3, len(snames)):
                        temp[snames[i]] = [0, 0]
                    for key in table_dict.keys():
                        if table_dict[key][0] == "质量特性":
                            origin = float(table_dict[key][2])
                            for i in range(3, len(snames)):
                                if float(table_dict[key][i]) <= origin:
                                    temp[snames[i]][0] += 1
                                    temp[snames[i]][1] += 1
                                else:
                                    temp[snames[i]][1] += 1
                    i = 0
                    for key in temp.keys():
                        res[key] = temp[key][0] * 1.0 / temp[key][1]
                        A_dict = {
                            "id": "A"+str(i),
                            "type": "用户手册",
                            "source": UserMannelFile + "/软件应用/表格",
                            "des": "优于或等于被替换产品的新产品质量测度数量",
                            "val": temp[key][0]
                        }
                        B_dict = {
                            "id": "B"+str(i),
                            "type": "用户手册",
                            "source": UserMannelFile + "/软件应用/表格",
                            "des": "被替换软件产品中的质量测度数量",
                            "val": temp[key][1]
                        }
                        sublist.append(A_dict)
                        sublist.append(B_dict)
                        i += 1
    res_dict = {
        "val": sum(list(res.values()))/len(list(res.keys())),
        "sub": sublist
    }
    return res_dict


def pre3s(TreeList4):
    A_dict = {
        "id": "A",
        "type": "用户手册",
        "source": UserMannelFile + "/软件应用/表格",
        "des": "结果与被替换软件产品相似的产品功能数量",
        "val": None
    }
    B_dict = {
        "id": "B",
        "type": "用户手册",
        "source": UserMannelFile + "/软件应用/表格",
        "des": "被替换软件产品中需要使用的功能数量",
        "val": None
    }
    sublist = []
    res = {}
    for node in TreeList4:
        if node.text.strip() == "软件应用":
            for j in node.son_id:
                if len(TreeList4[j].table_info.keys()) > 0:
                    table_dict = TreeList4[j].table_info
                    temp = {}
                    snames = table_dict[0]
                    for i in range(3, len(snames)):
                        temp[snames[i]] = [0, 0]
                    for key in table_dict.keys():
                        if table_dict[key][0] == "功能特性":
                            if table_dict[key][2] == "支持":
                                for i in range(3, len(snames)):
                                    if table_dict[key][i] == "支持/相似" or table_dict[key][i] == "支持/不相似":
                                        temp[snames[i]][0] += 1
                                        temp[snames[i]][1] += 1
                            elif table_dict[key][2] == "不支持":
                                for i in range(3, len(snames)):
                                    if table_dict[key][i] == "支持/不相似":
                                        temp[snames[i]][1] += 1
                    i = 0
                    for key in temp.keys():
                        res[key] = temp[key][0] * 1.0 / temp[key][1]
                        A_dict = {
                            "id": "A"+str(i),
                            "type": "用户手册",
                            "source": UserMannelFile + "/软件应用/表格",
                            "des": "结果与被替换软件产品相似的产品功能数量",
                            "val": temp[key][0]
                        }
                        B_dict = {
                            "id": "B"+str(i),
                            "type": "用户手册",
                            "source": UserMannelFile + "/软件应用/表格",
                            "des": "被替换软件产品中需要使用的功能数量",
                            "val": temp[key][1]
                        }
                        sublist.append(A_dict)
                        sublist.append(B_dict)
                        i += 1
    res_dict = {
        "val": sum(list(res.values()))/len(list(res.keys())),
        "sub": sublist
    }
    return res_dict


def pre4s(TreeList4):
    A_dict = {
        "id": "A",
        "type": "用户手册",
        "source": UserMannelFile + "/软件应用/表格",
        "des": "能像被替换软件产品一样继续使用的数据数量",
        "val": None
    }
    B_dict = {
        "id": "B",
        "type": "用户手册",
        "source": UserMannelFile + "/软件应用/表格",
        "des": "被替换软件产品中需要维续使用的数据数量",
        "val": None
    }
    sublist = []
    res = {}
    for node in TreeList4:
        if node.text.strip() == "软件应用":
            for j in node.son_id:
                if len(TreeList4[j].table_info.keys()) > 0:
                    table_dict = TreeList4[j].table_info
                    temp = {}
                    snames = table_dict[0]
                    for i in range(3, len(snames)):
                        temp[snames[i]] = [0, 0]
                    for key in table_dict.keys():
                        if table_dict[key][1] == "数据导入":
                            data_in = table_dict[key][2].split(",")
                            for i in range(3, len(snames)):
                                data_in_i = table_dict[key][i].split(",")
                                for d in data_in_i:
                                    if d in data_in:
                                        temp[snames[i]][0] += 1
                                        temp[snames[i]][1] += 1
                                    else:
                                        temp[snames[i]][1] += 1
                        if table_dict[key][1] == "数据导出":
                            data_out = table_dict[key][2].split(",")
                            for i in range(3, len(snames)):
                                data_out_i = table_dict[key][i].split(",")
                                for d in data_out_i:
                                    if d in data_out:
                                        temp[snames[i]][0] += 1
                                        temp[snames[i]][1] += 1
                                    else:
                                        temp[snames[i]][1] += 1
                    i = 0
                    for key in temp.keys():
                        res[key] = temp[key][0] * 1.0 / temp[key][1]
                        A_dict = {
                            "id": "A"+str(i),
                            "type": "用户手册",
                            "source": UserMannelFile + "/软件应用/表格",
                            "des": "能像被替换软件产品一样继续使用的数据数量",
                            "val": temp[key][0]
                        }
                        B_dict = {
                            "id": "B"+str(i),
                            "type": "用户手册",
                            "source": UserMannelFile + "/软件应用/表格",
                            "des": "被替换软件产品中需要维续使用的数据数量",
                            "val": temp[key][1]
                        }
                        sublist.append(A_dict)
                        sublist.append(B_dict)
                        i += 1
    res_dict = {
        "val": sum(list(res.values()))/len(list(res.keys())),
        "sub": sublist
    }
    return res_dict


def rft2s(A, B):
    '''
    :param A: 冗余安装系统组件的数量
    :param B:系统组件数量
    :return:组件的冗余度RFt-2-S
    '''
    A_dict = {
        "id": "A",
        "source": "源码",
        "des": "冗余安装系统组件的数量",
        "val": A
    }
    B_dict = {
        "id": "B",
        "source": "源码",
        "des": "系统组件数量",
        "val": B
    }
    res_dict = {
        "val": A*B,
        "sub": [A_dict, B_dict]
    }
    return res_dict


def mmo2s(TreeList3):
    '''
    :param A:圈复杂度的得分超过规定阈值的软件模块数量
    :param B:已实现的软件模块数量
    :return:圈复杂度的充分性MMo-2-S
    '''
    threshold = ReqFunc.func_xx2(TreeList3)
    A_dict = {
        "id": "A",
        "source": "源码",
        "des": "圈复杂度的得分超过规定阈值的软件模块数量",
        "val": None
    }
    B_dict = {
        "id": "B",
        "source": "源码",
        "des": "已实现的软件模块数量",
        "val": None
    }
    res_dict = {
        "val": threshold,
        "sub": [A_dict, B_dict]
    }
    return res_dict


def mre1g(A, B):
    '''
    :param A:为可重复使用而设计和实现的资产的数量
    :param B:系统中资产的数量
    :return:资产的可重用性MRe-1-G
    '''
    A_dict = {
        "id": "A",
        "source": "源码",
        "des": "为可重复使用而设计和实现的资产的数量",
        "val": A
    }
    B_dict = {
        "id": "B",
        "source": "源码",
        "des": "系统中资产的数量",
        "val": B
    }
    res_dict = {
        "val": A/B,
        "sub": [A_dict, B_dict]
    }
    return res_dict


def fcp1g(DesignTree):
    A_dict = {
        "id": "A",
        "type": "设计文档",
        "source": SystemDesignFile + "/需求的可追踪性/表格",
        "des": "缺少的功能数量",
        "val": None
    }
    B_dict = {
        "id": "B",
        "type": "设计文档",
        "source": SystemDesignFile + "/需求的可追踪性/表格",
        "des": "指定的功能数量",
        "val": None
    }
    res = -1
    A = 0
    B = 0
    dict = {}
    root = DesignTree[0]
    name_1 = "需求的可追踪性"
    if name_1 in root.son_text:
        idx = root.son_text.index(name_1)
        node_1 = DesignTree[root.son_id[idx]]

        try:
            table = DesignTree[node_1.son_id[0]].table_info
            if table:
                for val in list(table.values())[1:]:
                    if val[1] not in dict.keys():
                        if val[2]:
                            dict[val[1]] = 1
                        else:
                            dict[val[1]] = 0
                for key in dict.keys():
                    B += 1
                    A += dict[key]
                A_dict = {
                    "id": "A",
                    "type": "设计文档",
                    "source": SystemDesignFile + "/需求的可追踪性/表格",
                    "des": "缺少的功能数量",
                    "val": A
                }
                B_dict = {
                    "id": "B",
                    "type": "设计文档",
                    "source": SystemDesignFile + "/需求的可追踪性/表格",
                    "des": "指定的功能数量",
                    "val": B
                }
                res = 1 - A / B
                res_dict = {
                    "val": res,
                    "sub": [A_dict, B_dict]
                }
        except:
            res_dict = {
                "val": None,
                "sub": [A_dict, B_dict]
            }
            print("找不到表格")
        finally:
            return res_dict
    res_dict = {
        "val": None,
        "sub": [A_dict, B_dict]
    }
    return res_dict


def fap1g(TreeList1, TreeList2, TreeList3):
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": TestReportFile + "/",
        "des": "为实现特定使用目标所需的功能中缺少或不正确功能的数量",
        "val": None
    }
    B_dict = {
        "id": "B",
        "type": "需求文档",
        "source": RequirementFile + "/系统特定目标追踪表/表格",
        "des": "为实现特定使用目标所需的功能数量",
        "val": None
    }
    # res = {}
    targets = rq.func_xx(TreeList3)
    r2c = mt.func4(TreeList1)
    testcases = mt.func3(TreeList2)
    for target in targets.keys():
        B = len(targets[target])
        A = 0
        for requirement in targets[target]:
            target_test = mt.getTestCases(requirement, testcases, r2c)
            for key in target_test.keys():
                if target_test[key] == "不通过":
                    A += 1
        res = 1 - (A * 1.0) / B
        A_dict = {
            "id": "A",
            "type": "测试文档",
            "source": TestReportFile + "/",
            "des": "为实现特定使用目标所需的功能中缺少或不正确功能的数量",
            "val": A
        }
        B_dict = {
            "id": "B",
            "type": "需求文档",
            "source": RequirementFile + "/系统特定目标追踪表/表格",
            "des": "为实现特定使用目标所需的功能数量",
            "val": B
        }
        res_dict = {
            "val": res,
            "sub": [A_dict, B_dict]
        }
        break
    return res_dict


def fap2g(TreeList1, TreeList2, TreeList3):

    res = fap1g(TreeList1, TreeList2, TreeList3)['val']
    A_dict = {
        "id": "A",
        "type": "测试文档",
        "source": "FAp-1-G",
        "des": "特定使用目标FAp-1-G的测量值",
        "val": res
    }
    B_dict = {
        "id": "B",
        "type": "测试文档",
        "source": "FAp-1-G",
        "des": "使用目标的数量",
        "val": 1
    }
    m = 0
    # for k in res.keys():
    #     m += res[k]
    res_dict = {
        "val": res,
        "sub": [A_dict, B_dict]
    }
    return res_dict


def get_all_metrix(files):
    Filepath1 = files[0]
    Filepath2 = files[1]
    Filepath3 = files[2]
    Filepath4 = files[3]
    Filepath5 = files[4]
    Filepath6 = files[5]
    Filepath7 = files[6]

    global TestSpecFile
    TestSpecFile = Filepath1.split("/")[-1] if files[0] else 0
    global TestReportFile
    TestReportFile = Filepath2.split("/")[-1] if files[1] else 0
    global RequirementFile
    RequirementFile = Filepath3.split("/")[-1] if files[2] else 0
    global UserMannelFile
    UserMannelFile = Filepath4.split("/")[-1] if files[3] else 0
    global InterfaceDesignFile
    InterfaceDesignFile = Filepath5.split("/")[-1] if files[4] else 0
    global MaintainFile
    MaintainFile = Filepath6.split("/")[-1] if files[5] else 0
    global SystemDesignFile
    SystemDesignFile = Filepath7.split("/")[-1] if files[6] else 0
    # 获取docx文件路径

    extract_path1 = files[0][:-5] + "_copy" if files[0] else 0
    extract_path2 = files[1][:-5] + "_copy" if files[1] else 0
    extract_path3 = files[2][:-5] + "_copy" if files[2] else 0
    extract_path4 = files[3][:-5] + "_copy" if files[3] else 0
    extract_path5 = files[4][:-5] + "_copy" if files[4] else 0
    extract_path6 = files[5][:-5] + "_copy" if files[5] else 0
    extract_path7 = files[6][:-5] + "_copy" if files[6] else 0
    if extract_path1:
        Tag_order1 = get_order(extract_path1)
        TreeList1 = Parsing_docx(Tag_order1, Filepath1, extract_path1)

    if extract_path2:
        Tag_order2 = get_order(extract_path2)
        TreeList2 = Parsing_docx(Tag_order2, Filepath2, extract_path2)

    if extract_path3:
        Tag_order3 = get_order(extract_path3)
        TreeList3 = Parsing_docx(Tag_order3, Filepath3, extract_path3)

    if extract_path4:
        Tag_order4 = get_order(extract_path4)
        TreeList4 = Parsing_docx(Tag_order4, Filepath4, extract_path4)

    if extract_path5:
        Tag_order5 = get_order(extract_path5)
        TreeList5 = Parsing_docx(Tag_order5, Filepath5, extract_path5)

    if extract_path6:
        Tag_order6 = get_order(extract_path6)
        TreeList6 = Parsing_docx(Tag_order6, Filepath6, extract_path6)
    if extract_path7:
        Tag_order7 = get_order(extract_path7)
        TreeList7 = Parsing_docx(Tag_order7, Filepath7, extract_path7)
    try:
        r2c = match2.func4(TreeList1)
        testcases = match2.func3(TreeList2)
    except:
        pass
    try:
        pin2gs = pin2g(TreeList4, testcases, r2c)
    except:
        pin2gs = {
            'val': None,
            'sub': []
        }
    print("系统安装灵活性 pin2g", pin2gs)
    try:
        pin1gs = pin1g(TreeList4, testcases, r2c)
    except:
        pin1gs = {
            'val': None,
            'sub': []
        }
    print("pin1g", pin1gs)
    try:
        pad3ss = pad3s(testcases, r2c)
    except:
        pad3ss = {
            'val': None,
            'sub': []
        }
    print("pad3s", pad3ss)
    try:
        pad2gs = pad2g(testcases, r2c)
    except:
        pad2gs = {
            'val': None,
            'sub': []
        }
    print("pad2g", pad2gs)
    try:
        pad1gs = pad1g(testcases, r2c)
    except:
        pad1gs = {
            'val': None,
            'sub': []
        }
    print("pad1g", pad1gs)
    try:
        mte3ss = mte3s(TreeList2)
    except:
        mte3ss = {
            'val': None,
            'sub': []
        }
    print("mte3s", mte3ss)
    try:
        mte2ss = mte2s(TreeList2)
    except:
        mte2ss = {
            'val': None,
            'sub': []
        }
    print("mte2s", mte2ss)
    try:
        man3ss = man3s(TreeList4, testcases, r2c)
    except:
        man3ss = {
            'val': None,
            'sub': []
        }
    print("man3s", man3ss)
    try:
        man2ss = man2s(TreeList4, testcases, r2c)
    except:
        man2ss = {
            'val': None,
            'sub': []
        }
    print("man2s", man2ss)
    try:
        man1gs = man1g(TreeList3, testcases, r2c)
    except:
        man1gs = {
            'val': None,
            'sub': []
        }
    print("man1g", man1gs)
    try:
        mre2ss = mre2s(TreeList3, testcases, r2c)
    except:
        mre2ss = {
            'val': None,
            'sub': []
        }
    print("mre2s", mre2ss)
    try:
        sau2ss = sau2s(TreeList5, testcases, r2c)
    except:
        sau2ss = {
            'val': None,
            'sub': []
        }
    print("sau2s", sau2ss)
    try:
        sau1gs = sau1g(TreeList5, testcases, r2c)
    except:
        sau1gs = {
            'val': None,
            'sub': []
        }
    print("sau1g", sau1gs)
    try:
        sac1gs = sac1g(TreeList3, testcases, r2c)
    except:
        sac1gs = {
            'val': None,
            'sub': []
        }
    print("sac1g", sac1gs)
    try:
        sac2ss = sac2s(TreeList3, testcases, r2c)
    except:
        sac2ss = {
            'val': None,
            'sub': []
        }
    print("sac2s", sac2ss)
    try:
        sno1gs = sno1g(TreeList3, testcases, r2c)
    except:
        sno1gs = {
            'val': None,
            'sub': []
        }
    print("sno1g", sno1gs)
    try:
        sin1gs = sin1g(TreeList3, testcases, r2c)
    except:
        sin1gs = {
            'val': None,
            'sub': []
        }
    print("sin1g", sin1gs)
    try:
        sin2gs = sin2g(TreeList3, testcases, r2c)
    except:
        sin2gs = {
            'val': None,
            'sub': []
        }
    print("sin2g", sin2gs)
    try:
        sco3ss = sco3s(TreeList3, testcases, r2c)
    except:
        sco3ss = {
            'val': None,
            'sub': []
        }
    print("sco3s", sco3ss)
    try:
        sco2gs = sco2g(TreeList5, testcases, r2c)
    except:
        sco2gs = {
            'val': None,
            'sub': []
        }
    print("sco2g", sco2gs)
    try:
        sco1gs = sco1g(TreeList5, testcases, r2c)
    except:
        sco1gs = {
            'val': None,
            'sub': []
        }
    print("sco1g", sco1gs)
    try:
        rre2ss = rre2s(TreeList4, testcases, r2c)
    except:
        rre2ss = {
            'val': None,
            'sub': []
        }
    print("rre2s", rre2ss)
    try:
        rre1gs = rre1g(TreeList3, testcases, r2c)
    except:
        rre1gs = {
            'val': None,
            'sub': []
        }
    print("rre1g", rre1gs)
    try:
        rft3ss = rft3s(TreeList3, testcases, r2c)
    except:
        rft3ss = {
            'val': None,
            'sub': []
        }
    print("rft3s", rft3ss)
    try:
        rft1gs = rft1g(TreeList3, testcases, r2c)
    except:
        rft1gs = {
            'val': None,
            'sub': []
        }
    print("rft1g", rft1gs)
    try:
        rav2gs = rav2g(TreeList3, testcases, r2c)
    except:
        rav2gs = {
            'val': None,
            'sub': []
        }
    print("rav2g", rav2gs)
    try:
        rav1gs = rav1g(TreeList3, testcases, r2c)
    except:
        rav1gs = {
            'val': None,
            'sub': []
        }
    print("rav1g", rav1gs)
    try:
        rma4ss = rma4s(TreeList2)
    except:
        rma4ss = {
            'val': None,
            'sub': []
        }
    print("rma4s", rma4ss)
    try:
        rma3gs = rma3g(TreeList3, testcases, r2c)
    except:
        rma3gs = {
            'val': None,
            'sub': []
        }
    print("rma3g", rma3gs)
    try:
        rma2gs = rma2g(TreeList3, testcases, r2c)
    except:
        rma2gs = {
            'val': None,
            'sub': []
        }
    print("rma2g", rma2gs)
    try:
        rma1gs = rma1g(TreeList3, testcases, r2c)
    except:
        rma1gs = {
            'val': None,
            'sub': []
        }
    print("rma1g", rma1gs)
    try:
        uac2ss = uac2s(TreeList4, testcases, r2c)
    except:
        uac2ss = {
            'val': None,
            'sub': []
        }
    print("uac2s", uac2ss)
    try:
        uac1gs = uac1g(TreeList4, testcases, r2c)
    except:
        uac1gs = {
            'val': None,
            'sub': []
        }
    print("uac1g", uac1gs)
    try:
        uin1ss = uin1s(TreeList3, testcases, r2c)
    except:
        uin1ss = {
            'val': None,
            'sub': []
        }
    print("uin1s", uin1ss)
    try:
        uep3ss = uep3s(TreeList4, testcases, r2c)
    except:
        uep3ss = {
            'val': None,
            'sub': []
        }
    print("uep3s", uep3ss)
    try:
        uep2ss = uep2s(testcases, r2c)
    except:
        uep2ss = {
            'val': None,
            'sub': []
        }
    print("uep2s", uep2ss)
    try:
        uep1gs = uep1g(TreeList3, testcases, r2c)
    except:
        uep1gs = {
            'val': None,
            'sub': []
        }
    print("uep1g", uep1gs)
    try:
        uop9ss = uop9s(TreeList4, testcases, r2c)
    except:
        uop9ss = {
            'val': None,
            'sub': []
        }
    print("uop9s", uop9ss)
    try:
        uop8ss = uop8s(TreeList3, testcases, r2c)
    except:
        uop8ss = {
            'val': None,
            'sub': []
        }
    print("uop8s", uop8ss)
    try:
        uop7ss = uop7s(TreeList5, testcases, r2c)
    except:
        uop7ss = {
            'val': None,
            'sub': []
        }
    print("uop7s", uop7ss)
    try:
        uop6ss = uop6s(TreeList3, testcases, r2c)
    except:
        uop6ss = {
            'val': None,
            'sub': []
        }
    print("uop6s", uop6ss)
    try:
        uop5ss = uop5s(TreeList3, testcases, r2c)
    except:
        uop5ss = {
            'val': None,
            'sub': []
        }
    print("uop5s", uop5ss)
    try:
        uop4ss = uop4s(TreeList3, testcases, r2c)
    except:
        uop4ss = {
            'val': None,
            'sub': []
        }
    print("uop4s", uop4ss)
    try:
        uop3ss = uop3s(TreeList3, testcases, r2c)
    except:
        uop3ss = {
            'val': None,
            'sub': []
        }
    print("uop3s", uop3ss)
    try:
        uop2gs = uop2g(TreeList5, testcases, r2c)
    except:
        uop2gs = {
            'val': None,
            'sub': []
        }
    print("uop2g", uop2gs)
    try:
        uop1gs = uop1g(TreeList3, testcases, r2c)
    except:
        uop1gs = {
            'val': None,
            'sub': []
        }
    print("uop1g", uop1gs)
    try:
        ule2ss = ule2s(TreeList5, testcases, r2c)
    except:
        ule2ss = {
            'val': None,
            'sub': []
        }
    print("ule2s", ule2ss)
    try:
        ule1gs = ule1g(TreeList4, TreeList3)
    except:
        ule1gs = {
            'val': None,
            'sub': []
        }
    print("ule1g", ule1gs)
    try:
        uap2gs = uap2g(TreeList3, testcases, r2c)
    except:
        uap2gs = {
            'val': None,
            'sub': []
        }
    print("uap2g", uap2gs)
    try:
        uap1gs = uap1g(TreeList4, TreeList3)
    except:
        uap1gs = {
            'val': None,
            'sub': []
        }
    print("uap1g", uap1gs)
    try:
        ule4ss = ule4s(TreeList4, testcases, r2c)
    except:
        ule4ss = {
            'val': None,
            'sub': []
        }
    print("ule4s", ule4ss)
    try:
        ule3ss = ule3s(testcases, r2c)
    except:
        ule3ss = {
            'val': None,
            'sub': []
        }
    print("ule3s", ule3ss)
    try:
        uap3gs = uap3g(testcases, r2c)
    except:
        uap3gs = {
            'val': None,
            'sub': []
        }
    print("uap3g", uap3gs)
    try:
        mte1gs = mte1g(TreeList2)
    except:
        mte1gs = {
            'val': None,
            'sub': []
        }
    print("mte1g", mte1gs)
    try:
        mmd1gs = mmd1g(TreeList6)
    except:
        mmd1gs = {
            'val': None,
            'sub': []
        }
    print("mmd1g", mmd1gs)
    try:
        mmd2gs = mmd2g(TreeList6)
    except:
        mmd2gs = {
            'val': None,
            'sub': []
        }
    print("mmd2g", mmd2gs)
    try:
        mmd3ss = mmd3s(TreeList6)
    except:
        mmd3ss = {
            'val': None,
            'sub': []
        }
    print("mmd3s", mmd3ss)
    try:
        fcr1gs = fcr1g(TreeList1, TreeList2, TreeList3)
    except:
        fcr1gs = {
            'val': None,
            'sub': []
        }
    print("fcr1g", fcr1gs)
    try:
        ptb1gs = ptb1g(TreeList1, TreeList2)
    except:
        ptb1gs = {
            'val': None,
            'sub': []
        }
    print("Ptb1g", ptb1gs)
    try:
        ptb2gs = ptb2g(TreeList3, ptb1gs['val'])
    except:
        ptb2gs = {
            'val': None,
            'sub': []
        }
    print("ptb2g", ptb2gs)
    try:
        ptb3gs = ptb3g(TreeList1, TreeList2)
    except:
        ptb3gs = {
            'val': None,
            'sub': []
        }
    print("ptb3g", ptb3gs)
    try:
        ptb4gs = ptb4g(TreeList3, ptb3gs['val'])
    except:
        ptb4gs = {
            'val': None,
            'sub': []
        }
    print("ptb4g", ptb4gs)
    try:
        ptb5gs = ptb5g(TreeList1, TreeList2)
    except:
        ptb5gs = {
            'val': None,
            'sub': []
        }
    print("ptb5g", ptb5gs)
    try:
        pru1gs = pru1g(TreeList1, TreeList2)
    except:
        pru1gs = {
            'val': None,
            'sub': []
        }
    print("pru1g", pru1gs)
    try:
        pru2gs = pru2g(TreeList1, TreeList2)
    except:
        pru2gs = {
            'val': None,
            'sub': []
        }
    print("pru2g", pru2gs)
    try:
        pru3gs = pru3g(TreeList1, TreeList2)
    except:
        pru3gs = {
            'val': None,
            'sub': []
        }
    print("pru3g", pru3gs)
    try:
        pru4ss = pru4s(TreeList1, TreeList2)
    except:
        pru4ss = {
            'val': None,
            'sub': []
        }
    print("pru3s", pru4ss)
    try:
        pca1gs = pca1g(TreeList1, TreeList2)
    except:
        pca1gs = {
            'val': None,
            'sub': []
        }
    print("pca1g", pca1gs)
    try:
        pca2gs = pca2g(TreeList1, TreeList2)
    except:
        pca2gs = {
            'val': None,
            'sub': []
        }
    print("pca2g", pca2gs)
    try:
        pca3ss = pca3s(TreeList1, TreeList2)
    except:
        pca3ss = {
            'val': None,
            'sub': []
        }
    print("pca3S", pca3ss)
    try:
        cco1gs = cco1g(TreeList1, TreeList2, TreeList3)
    except:
        cco1gs = {
            'val': None,
            'sub': []
        }
    print("cco1g", cco1gs)
    try:
        cin1gs = cin1g(TreeList1, TreeList2, TreeList3)
    except:
        cin1gs = {
            'val': None,
            'sub': []
        }
    print("cin1g", cin1gs)
    try:
        cin2gs = cin2g(TreeList1, TreeList2, TreeList3)
    except:
        cin2gs = {
            'val': None,
            'sub': []
        }
    print("cin2g", cin2gs)
    try:
        cin3ss = cin3s(TreeList1, TreeList2, TreeList3)
    except:
        cin3ss = {
            'val': None,
            'sub': []
        }
    print("cin3s", cin3ss)
    # uap1gs = uap1g(TreeList3, TreeList4)
    # print("uap1g", uap1gs)
    try:
        prc1gs = prc1g(TreeList4)
    except:
        prc1gs = {
            'val': None,
            'sub': []
        }
    print("prc1g", prc1gs)
    try:
        pre2ss = pre2s(TreeList4)
    except:
        pre2ss = {
            'val': None,
            'sub': []
        }
    print("pre2s", pre2ss)
    try:
        pre3ss = pre3s(TreeList4)
    except:
        pre3ss = {
            'val': None,
            'sub': []
        }
    print("pre3s", pre3ss)
    try:
        pre4ss = pre4s(TreeList4)
    except:
        pre4ss = {
            'val': None,
            'sub': []
        }
    print("PRe_4_S", pre4ss)
    try:
        rft2ss = rft2s(7, 11)
    except:
        rft2ss = {
            'val': None,
            'sub': []
        }
    print("rft2s", rft2ss)
    try:
        mmo2ss = mmo2s(TreeList3)
    except:
        mmo2ss = {
            'val': None,
            'sub': []
        }
    print("mmo2s", mmo2ss)
    try:
        mre1gs = mre1g(2, 5)
    except:
        mre1gs = {
            'val': None,
            'sub': []
        }
    print("mre1g", mre1gs)
    try:
        fcp1gs = fcp1g(TreeList7)
    except:
        fcp1gs = {
            'val': None,
            'sub': []
        }
    print("fcp1g", fcp1gs)
    try:
        fap1gs = fap1g(TreeList1, TreeList2, TreeList3)
    except:
        fap1gs = {
            'val': None,
            'sub': []
        }
    print("fap1g", fap1gs)
    try:
        fap2gs = fap2g(TreeList1, TreeList2, TreeList3)
    except:
        fap2gs = {
            'val': None,
            'sub': []
        }
    print("fap2g", fap2gs)

    zerodict = {
        'val': None,
        'sub': []
    }

    metrix_25000 = {'功能性': {'功能完备性': {'功能覆盖率': fcp1gs}, '功能正确性': {'功能正确性': fcr1gs},
                            '功能适合性': {'使用目标的功能适合性': fap1gs, '系统的功能适合性': fap2gs},
                            '功能性的依从性': {'功能性的依从性': zerodict}},
                    '性能效率': {'时间特性': {'平均响应时间': ptb1gs, '响应时间的充分性': ptb2gs, '平均周转时间': ptb3gs, '周转时间充分性': ptb4gs,
                                      '平均吞吐量': ptb5gs},
                             '资源利用性': {'处理器平均占用率': pru1gs, '内存平均占用率': pru2gs, 'I/O设备平均占用率': pru3gs, '带宽占用率': pru4ss},
                             '容量': {'事务处理容量': pca1gs, '用户访问量': pca2gs, '用户访问增长的充分性': pca3ss},
                             '性能效率的依从性': {'性能效率的依从性': zerodict}},
                    '兼容性': {'共存性': {'与其他产品的共存性': cco1gs},
                            '互操作性': {'数据格式可交换性': cin1gs, '数据交换协议充分性': cin2gs, '外部接口充分性': cin3ss},
                            '兼容性的依从性': {'兼容性的依从性': zerodict}},
                    '易用性': {'可辨识性': {'描述的完整性': uap1gs, '演示覆盖率': uap2gs, '入口点的自描述性': uap3gs},
                            '易学性': {'用户指导完整性': ule1gs, '输入字段的默认值': ule2ss, '差错信息的易理解性': ule3ss, '用户界面的自解释性': ule4ss},
                            '易操作性': {'操作一致性': uop1gs, '消息的明确性': uop2gs, '功能的易定制性': uop3ss, '用户界面的易定制性': uop4ss,
                                     '监视能力': uop5ss, '撤销操作能力': uop6ss, '信息分类的易理解性': uop7ss, '外观一致性': uop8ss,
                                     '输入设备的支持性': uop9ss},
                            '用户差错防御性': {'抵御误操作': uep1gs, '用户输入差错纠正率': uep2ss, '用户差错易恢复性': uep3ss},
                            '用户界面舒适性': {'用户界面外观舒适性': uin1ss}, '易访问性': {'特殊群体的易访问性': uac1gs, '支持的语种充分性': uac2ss},
                            '易用性的依从性': {'易用性的依从性': zerodict}},
                    '可靠性': {'成熟性': {'故障修复率': rma1gs, '平均失效间隔时间(MTBF)': rma2gs, '周期失效率': rma3gs, '测试覆盖率': rma4ss},
                            '可用性': {'系统可用性': rav1gs, '平均宕机时间': rav2gs},
                            '容错性': {'避免失效率': rft1gs, '组件的冗余度': rft2ss, '平均故障通告时间': rft3ss},
                            '易恢复性': {'平均恢复时间': rre1gs, '数据备份完整性': rre2ss},
                            '可靠性的依从性': {'可靠性的依从性': zerodict}},
                    '信息安全性': {'保密性': {'访问控制性': sco1gs, '数据加密正确性': sco2gs, '加密算法的强度': sco3ss},
                              '完整性': {'数据完整性': sin1gs, '内部数据抗讹误性': sin2gs, '缓冲区溢出防止率': 1},
                              '抗抵赖性': {'数字签名使用率': sno1gs}, '可核查性': {'用户审计跟踪的完整性': sac1gs, '系统日志保留满足度': sac2ss},
                              '真实性': {'鉴别机制的充分性': sau1gs, '鉴别规则的符合性': sau2ss},
                              '信息安全性的依从性': {'信息安全性的依从性': zerodict}},
                    '维护性': {'模块化': {'组件间的耦合度': 1, '圈复杂度的充分性': mmo2ss},
                            '可重用性': {'资产的可重用性': mre1gs, '编码规则符合性': mre2ss},
                            '易分析性': {'系统日志完整性': man1gs, '诊断功能有效性': man2ss, '诊断功能充分性': man3ss},
                            '易修改性': {'修改的效率': mmd1gs, '修改的正确性': mmd2gs, '修改的能力': mmd3ss},
                            '易测试性': {'测试功能的完整性': mte1gs, '测试独立性': mte2ss, '测试的重启动性': mte3ss},
                            '维护性的依从性': {'维护性的依从性': zerodict}},
                    '可移植性': {'适应性': {'硬件环境的适应性': pad1gs, '系统软件环境的适应性': pad2gs, '运营环境的适应性': pad3ss},
                             '易安装性': {'安装的时间效率': pin1gs, '安装的灵活性': pin2gs},
                             '易替换性': {'使用相似性': prc1gs, '产品质量等价性': pre2ss, '功能的包容性': pre3ss,
                                      '数据复用/导入能力': pre4ss},
                             '可移植性的依从性': {'可移植性的依从性': zerodict}}}
    # print(metrix_25000)
    return metrix_25000


if __name__ == "__main__":
    path = os.getcwd().replace('\\', '/')
    # Filepath1 = "D:\\master\\master1\\cgui321\\CUnit标准大纲\\测试说明标准大纲.docx"
    # Filepath2 = "D:\\master\\master1\\cgui321\\CUnit标准大纲\\测试报告标准大纲.docx"
    # Filepath3 = "D:\\master\\master1\\cgui321\\CUnit标准大纲\\需求规格说明标准大纲.docx"
    # Filepath4 = "D:\\master\\master1\\cgui321\\CUnit标准大纲\\用户手册标准大纲.docx"
    # Filepath5 = "D:\\master\\master1\\cgui321\\CUnit标准大纲\\接口设计说明标准大纲.docx"
    # Filepath6 = "D:\\master\\master1\\cgui321\\CUnit标准大纲\\维护手册.docx"
    # Filepath7 = "D:\\master\\master1\\cgui321\\CUnit标准大纲\\系统、子系统设计说明标准大纲.docx"
    Filepath1 = path+"/CUnit标准大纲/测试说明标准大纲.docx"
    Filepath2 = path+"/CUnit标准大纲/测试报告标准大纲.docx"
    Filepath3 = path+"/CUnit标准大纲/需求规格说明标准大纲.docx"
    Filepath4 = path+"/CUnit标准大纲/用户手册标准大纲.docx"
    Filepath5 = path+"/CUnit标准大纲/接口设计说明标准大纲.docx"
    Filepath6 = path+"/CUnit标准大纲/维护手册.docx"
    Filepath7 = path+"/CUnit标准大纲/系统、子系统设计说明标准大纲.docx"
    filepath = [Filepath1, Filepath2, Filepath3, Filepath4, Filepath5, Filepath6, Filepath7]
    # filepath = [0]*7
    #
    # # 获取docx文件路径
    # extract_path1 = "D:\\master\\master1\\cgui\\标准大纲2.0\\测试说明标准大纲_copy"
    # extract_path2 = "D:\\master\\master1\\cgui\\标准大纲2.0\\测试报告标准大纲_copy"
    # extract_path3 = "D:\\master\\master1\\cgui\\标准大纲2.0\\需求规格说明标准大纲_copy"
    # extract_path4 = "D:\\master\\master1\\cgui\\标准大纲2.0\\用户手册标准大纲_copy"
    # extract_path5 = "D:\\master\\master1\\cgui\\标准大纲2.0\\接口设计说明标准大纲_copy"
    # extract_path6 = "D:\\master\\master1\\cgui\\标准大纲2.0\\维护手册_copy"
    # extract_path7 = "D:\\master\\master1\\cgui\\标准大纲2.0\\系统、子系统设计说明标准大纲_copy"
    print(get_all_metrix(filepath))
