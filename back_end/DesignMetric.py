'''
通过已有信息计算设计质量指标
可修改性: modifiability
    X = 1- (\sum(in+out)/N + \sum(cin + cout)/M)/ (N + M) (in: 入度，扇入列表的长度 out: 出度，扇出列表的长度 N: 函数总数)
可扩展性: scalability
    X = (N_api + M_interface) / (N + M) (N_api: API函数总数，函数的header字段指向某个头文件类型)
易测试性: testability
    X = 1- (\sum(out)/N + \sum(cout)/M) / (N + M) (out: 出度，扇出列表的长度 N: 函数总数)
可替换性: refundability
    Ri = 1/(1+in) (in: 入度，扇入列表的长度)
    Rci = 1/(1+cin) (cin: 入度，扇入列表的长度)
    X = (\sum(Ri) + \sum(Rci)) / (N + M) (N: 函数总数)
易理解性: comprehensibility
    X = (N_comment + M_comment) / (N + M) (N_comment: 包含注释的函数数量)
'''


import json


def getDesignMetric(funcInfo, classInfo):
    # 可修改性
    modifiability = 0.0
    # 可扩展性
    scalability = 0.0
    # 易测试性
    testability = 0.0
    # 可替换性
    refundability = 0.0
    # 易理解性
    comprehensibility = 0.0
    # 头文件类型
    headerType = (".h", ".H", ".hh", ".hpp", ".hxx")
    func_in = 0
    class_in = 0
    classInList = []
    func_out = 0
    class_out = 0
    classOutList = []
    N_api = 0
    M_interface = 0
    M_interface_list = []
    R = 0.0
    Rc = 0.0
    N_comment = 0
    M_comment = 0
    N = 0
    M = 0
    funcNameList = []
    MethodNameList = []
    classNameList = []
    funcInList = []
    funcOutList = []
    RiList = []
    RciList = []
    for func in funcInfo:
        if funcInfo[func]['type'] == 'Function':
            N += 1
            funcNameList.append(func)
            func_in += len(funcInfo[func]["fanIn"])
            funcInList.append(len(funcInfo[func]["fanIn"]))
            func_out += len(funcInfo[func]["fanOut"])
            funcOutList.append(len(funcInfo[func]["fanOut"]))
            if funcInfo[func]["header"].endswith(headerType):
                N_api += 1
            R += 1.0 / (1 + len(funcInfo[func]["fanIn"]))
            RiList.append(round(1.0 / (1 + len(funcInfo[func]["fanIn"])), 3))
            if funcInfo[func]["codeInfo"]["commentLineExp"] > 0:
                N_comment += 1
        else:
            MethodNameList.append(func)

    for cl in classInfo:
        if classInfo[cl]['type'] == 'Class':
            M += 1
            classNameList.append(cl)
            class_in += len(classInfo[cl]["fanIn"])
            classInList.append(len(classInfo[cl]["fanIn"]))
            class_out += len(classInfo[cl]["fanOut"])
            classOutList.append(len(classInfo[cl]["fanOut"]))
            comment_flag = False
            # 接口类
            # if classInfo[cl]['type'] == 'Class':
            vc_flag = True  # true表示是纯虚类
            for var in classInfo[cl]['mem_var']:
                authoritys = var['authority']
                if 'static' not in authoritys:
                    vc_flag = False  # 当有一个非静态成员变量时，不是纯虚类
                    break
            for m_method in classInfo[cl]['mem_method']:
                m_name = m_method['name']
                m_loc = m_method['this_loc']
                m_key = m_loc+":"+m_name
                method = funcInfo[m_key]
                if method['codeInfo']['commentLineExp'] > 0:
                    comment_flag = True
                body_flag = int(method['ifbody'])
                if body_flag == 0:
                    m_text = method['codeText'][-1].replace(" ", "").replace('\t', "").replace("\n", "")
                    if m_text[-2] != "=0":
                        vc_flag = False
                else:
                    if "static" not in method["modify"]:
                        vc_flag = False
            if vc_flag:
                M_interface += 1
                M_interface_list.append(cl)
            Rc += 1.0 / (1 + len(classInfo[cl]["fanIn"]))
            RciList.append(round(1.0 / (1 + len(classInfo[cl]["fanIn"])), 3))
            if len(classInfo[cl]['anno']) > 0 or comment_flag:
                M_comment += 1
    if N == 0 and M == 0:
        return {
            "metrix": {
                "modifiability": {
                    "value": modifiability,
                    "inDegree": 0,
                    "outDegree": 0,
                    "funcNum": 0,
                    "classInDegree": 0,
                    "classOutDegree": 0,
                    "classNum": 0
                },
                "scalability": {
                    "value": scalability,
                    "apiNum": 0,
                    "funcNum": 0,
                    "interfaceNum": 0,
                    "classNum": 0
                },
                "testability": {
                    "value": testability,
                    "outDegree": 0,
                    "funcNum": 0,
                    "classOutDegree": 0,
                    "classNum": 0
                },
                "refundability": {
                    "value": refundability,
                    "R_sum": 0,
                    "funcNum": 0,
                    "Rc_sum": 0,
                    "classNum": 0
                },
                "comprehensibility": {
                    "value": comprehensibility,
                    "commentFunc": 0,
                    "funcNum": 0,
                    "commentClass": 0,
                    "classNum": 0
                },
                "funcNameList": [],
                "methodNameList": [],
                "funcInList": [],
                "funcOutList": [],
                "RiList": [],
                "classInList": [],
                "classOutList": [],
                "RciList": [],
                "xAxis": [],
                "classNameList": [],
                "xcAxis": []
            }
        }
    elif N == 0 and M != 0:
        modifiability = 1 - (1.0 * (class_in + class_out) / M) / (M)
        scalability = 1.0 * (M_interface) / (M)
        testability = 1 - (1.0 * class_out / M) / (M)
        refundability = (Rc) / (M)
        comprehensibility = 1.0 * (M_comment) / (M)
    elif M == 0 and N != 0:
        modifiability = 1 - (1.0 * (func_in + func_out) / N) / (N)
        scalability = 1.0 * (N_api) / (N)
        testability = 1 - (1.0 * func_out / N) / (N)
        refundability = (R) / (N)
        comprehensibility = 1.0 * (N_comment) / (N)
    else:
        modifiability = 1 - (1.0 * (func_in + func_out) / N + 1.0 * (class_in + class_out) / M) / (N + M)
        scalability = 1.0 * (N_api + M_interface) / (N + M)
        testability = 1 - (1.0 * func_out / N + 1.0 * class_out / M) / (N + M)
        refundability = (R + Rc) / (N + M)
        comprehensibility = 1.0 * (N_comment + M_comment) / (N + M)
    return {
        "metrix": {
            "modifiability": {
                "value": round(modifiability, 3),
                "inDegree": func_in,
                "outDegree": func_out,
                "funcNum": N,
                "classInDegree": class_in,
                "classOutDegree": class_out,
                "classNum": M
            },
            "scalability": {
                "value": round(scalability, 3),
                "apiNum": N_api,
                "funcNum": N,
                "interfaceNum": M_interface,
                "classNum": M
            },
            "testability": {
                "value": round(testability, 3),
                "outDegree": func_out,
                "funcNum": N,
                "classOutDegree": class_out,
                "classNum": M
            },
            "refundability": {
                "value": round(refundability, 3),
                "R_sum": R,
                "funcNum": N,
                "Rc_sum": Rc,
                "classNum": M
            },
            "comprehensibility": {
                "value": round(comprehensibility, 3),
                "commentFunc": N_comment,
                "funcNum": N,
                "commentClass": M_comment,
                "classNum": M
            },
            "funcNameList": funcNameList,
            "methodNameList": MethodNameList,
            "funcInList": funcInList,
            "funcOutList": funcOutList,
            "RiList": RiList,
            "classInList": classInList,
            "classOutList": classOutList,
            "RciList": RciList,
            "classNameList": classNameList,
            "xAxis": [i+1 for i in range(N)],
            "xcAxis": [i+1 for i in range(M)]
        }
    }


def test():
    with open(r"D:\Code\VScode\CPP_Support\CPP_support\uploads\CUnit\code\CUnit\funcInfo.json", "r", encoding="utf-8") as f:
        funcInfo = json.load(f)
    with open(r"D:\Code\VScode\CPP_Support\CPP_support\uploads\CUnit\code\CUnit\codeFileInfo.json", "r", encoding="utf-8") as f:
        codeFileInfo = json.load(f)
    with open(r"D:\Code\VScode\CPP_Support\CPP_support\uploads\CUnit\code\CUnit\projectInfo.json", "r", encoding="utf-8") as f:
        projectInfo = json.load(f)
    funcNum = projectInfo["functionNumber"]
    print("funcNum: ", funcNum)
    funcInfoKeys = len(funcInfo)
    print("funcInfoKeys: ", funcInfoKeys)
    t = getDesignMetric(funcInfo)
    print(t)


if __name__ == "__main__":
    test()
