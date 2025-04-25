import Extract2_14 as ex
import re
def func3(TreeList):
    """
    测试文档：测试通过规则和测试不通过规则
    :param TreeList:
    :return:
    """
    res = {}
    for node in TreeList:
        if node.text == "详细的测试结果":
            for i in node.son_id:
                if TreeList[i].name[0] == "H":
                    test_id = TreeList[i].text.strip(" ")
                    res[test_id] = {}
                    for j in TreeList[i].son_id:
                        if TreeList[j].name[0] != "H":
                            des = ""
                            des += TreeList[j].text
                            res[test_id]["des"] = des
                        if TreeList[j].text == "测试结果小结":
                            table_id = TreeList[j].son_id[0]
                            table_dict = TreeList[table_id].table_info
                            res[test_id]["testcases"] = {}
                            for k in range(1, len(table_dict)):
                                testcase_id = table_dict[k][0]
                                res[test_id]["testcases"][testcase_id] = [table_dict[k][1], table_dict[k][2],
                                                                          table_dict[k][3],
                                                                          table_dict[k][4], table_dict[k][5]]
    return res

def func4(TreeList):
    res={}
    for node in TreeList:
        if node.text == "需求的可追踪性":
            table_id = node.son_id[0]
            table_dict = TreeList[table_id].table_info
            for k in range(1, len(table_dict)):
                require_id = table_dict[k][2]
                if require_id in  res.keys():
                    res[require_id].append(table_dict[k][0])
                else:
                    res[require_id] = [table_dict[k][0]]
    return res


def getTestCases(requirement, testcases, r2c):
    res = {}
    target_testcases = {}
    testcases_ids = r2c[requirement]
    for testcases_id in testcases_ids:
        temp = testcases_id.split("_")
        title = temp[0]+"_"+temp[1]
        target_testcases[testcases_id]= testcases[title]["testcases"][testcases_id]
    # print(target_testcases)
    if requirement == "平均响应时间" or requirement == "平均周转时间"  :
        for tc in target_testcases.keys():
            result = target_testcases[tc][2]
            match2 = re.match(".*?([1-9]\d*\.\d+|0\.\d+|0|[1-9]\d*)(ms|s).*", result)
            if match2 is not None:
                time = float(match2.group(1))
                if match2.group(2) == 's':
                    time *= 1000
                res[tc] = time
    elif requirement == "平均吞吐量":
        for tc in target_testcases.keys():
            result = target_testcases[tc][2]
            match2 = re.findall(r"(?:完成的作业数量为|观察时间的周期为)(\d+)", result)
            if match2:
                temp = {}
                temp["A"] = int(match2[0])
                temp["B"] = int(match2[1])
                res[tc] = temp
    elif requirement == "同时运行的用户数量":
        for tc in target_testcases.keys():
            result = target_testcases[tc][2]
            match2 = re.findall(r"(?:观察时间内完成事务的数量为|观察时间为)(\d+)", result)
            if match2:
                temp = {}
                temp["A"] = int(match2[0])
                temp["B"] = int(match2[1])
                res[tc] = temp
    elif   requirement == "周期失效率" :
        for tc in target_testcases.keys():
            result = target_testcases[tc][2]
            match2 = re.match(".*?([1-9]\d*\.\d+|0\.\d+|0|[1-9]\d*)(%?).*", result)
            if match2 is not None:
                per = float(match2.group(1))
                if match2.group(2) == '%':
                    per /= 100
                res[tc] = per
    # elif requirement == "同时运行的用户数量":
    #     for tc in target_testcases.keys():
    #         result = target_testcases[tc][2]
    #         match2 = re.match(".*?([1-9]\d*).*", result)
    #         if match2 is not None:
    #             res[tc] = int(match2.group(1))
    elif requirement == "系统支持的用户访问量":
        for tc in target_testcases.keys():
            result = target_testcases[tc][2]
            match2 = re.match(".*?([1-9]\d*\.\d+|0\.\d+|0|[1-9]\d*)(次/天|次/小时).*", result)
            if match2 is not None:
                per = float(match2.group(1))
                if match2.group(2) == '次/天':
                    per *= 24
                res[tc] = per
    elif requirement == "用户访问增长充分性":
        for tc in target_testcases.keys():
            result = target_testcases[tc][2]
            match2 = re.findall(r"(?:观察时间内成功增加的用户数量|观察时间为)(\d+)", result)
            if match2:
                temp = {}
                temp["A"] = int(match2[0])
                temp["B"] = int(match2[1])
                res[tc] = temp
    elif requirement == "测试系统运行时间" or  requirement == "平均故障通告时间" or requirement == "平均宕机时间" or requirement == "平均失效间隔":
        for tc in target_testcases.keys():
            result = target_testcases[tc][2]
            match2 = re.match(".*?([1-9]\d*\.\d+|0\.\d+|0|[1-9]\d*)(小时|天).*", result)
            if match2 is not None:
                time = float(match2.group(1))
                if match2.group(2) == '天':
                    time *= 24
                res[tc] = time
    elif requirement == "测试系统运行时间" or requirement == "系统平均恢复时间" or  requirement == "平均故障通告时间":
        for tc in target_testcases.keys():
            result = target_testcases[tc][2]
            match2 = re.match(".*?([1-9]\d*\.\d+|0\.\d+|0|[1-9]\d*)(s|min).*", result)
            if match2 is not None:
                time = float(match2.group(1))
                if match2.group(2) == 'min':
                    time *= 60
                res[tc] = time
    elif requirement == "操作日志保留的时长":
        for tc in target_testcases.keys():
            result = target_testcases[tc][2]
            match2 = re.match(".*?([1-9]\d*\.\d+|0\.\d+|0|[1-9]\d*)(天|月).*", result)
            if match2 is not None:
                time = float(match2.group(1))
                if match2.group(2) == '天':
                    time /= 30
                res[tc] = time
    elif requirement == "带宽平均占用率" or requirement == "I/O设备平均占用率" or requirement == "内存平均占用率" or requirement == "操作日志的数量" or requirement == "操作日志的完整性"or requirement == "故障修复率":
        for tc in target_testcases.keys():
            pre = target_testcases[tc][0]
            result = target_testcases[tc][2]
            match2 = re.match(".*?(0|[1-9]\d*).*", pre)
            match3 = re.match(".*?(0|[1-9]\d*).*", result)
            if match2 is not None and match3 is not None:
                num1 = int(match2.group(1))
                num2 = int(match3.group(1))
                res[tc] = {"pre": num1, "res": num2}
    elif requirement == "处理器平均占用率" or requirement == "系统安装时间":
        for tc in target_testcases.keys():
            pre = target_testcases[tc][0]
            result = target_testcases[tc][2]
            match2 = re.match(".*?([1-9]\d*\.\d+|0\.\d+|0|[1-9]\d*)(s).*", pre)
            match3 = re.match(".*?([1-9]\d*\.\d+|0\.\d+|0|[1-9]\d*)(s).*", result)
            if match2 is not None and match3 is not None:
                num1 = int(match2.group(1))
                num2 = int(match3.group(1))
                res[tc] = {"pre": num1, "res": num2}

    else:
        for tc in target_testcases.keys():
            result = target_testcases[tc][3]
            res[tc] = result

    return res

def func46(TreeList):
    res = []
    for node in TreeList:
        if node.text == "测试结果概述":
            for i in node.son_id:
                if TreeList[i].name[0] == "H" and TreeList[i].text == "对被测试软件的总体评估":

                    # des = ""
                    # for j in TreeList[i].son_id:
                    #     des += TreeList[j].text
                    # match = re.match("(.*测试覆盖率)(是|为|达到)([1-9]\d*\.\d+|0\.\d+|0|[1-9]\d*)(%?)", des)
                    # if match is not None:
                    #     return float(match.group(3)) / 100 if match.group(4) == "%" else float(match.group(3))
                    node1 = TreeList[i]
                    node2 = TreeList[node1.son_id[0]]
                    table = node2.table_info
                    if table:
                        for val in list(table.values())[1:]:
                            res.append(val)

    # print("res",res)
    return res

def func68(TreeList):
    res = {}
    des = ""
    for node in TreeList:
        if node.text == "测试结果概述":
            for i in node.son_id:
                if TreeList[i].name[0] == "H":
                    subtitle = TreeList[i].text.strip(" ")
                    if subtitle == "测试的独立性":
                        for j in TreeList[i].son_id:
                            if TreeList[j].name[0] != "H":
                                des += TreeList[j].text
    match = re.match(".*?(0|[1-9]\d*).*?(0|[1-9]\d*).*?", des)
    res["A"] = int(match.group(1))
    res["B"] = int(match.group(2))
    return res

def func69(TreeList):
    res = {}
    des = ""
    for node in TreeList:
        if node.text == "测试结果概述":
            for i in node.son_id:
                if TreeList[i].name[0] == "H":
                    subtitle = TreeList[i].text.strip(" ")
                    if subtitle == "测试的重启动性":
                        for j in TreeList[i].son_id:
                            if TreeList[j].name[0] != "H":
                                des += TreeList[j].text
    match = re.match(".*?(0|[1-9]\d*).*?(0|[1-9]\d*).*?", des)
    res["A"] = int(match.group(1))
    res["B"] = int(match.group(2))
    return res
if __name__ == '__main__':

    Filepath1 = ex.Get_filepath()  # 获取docx文件路径
    extract_path1, zip_path1, Folderpath1, souce_name1 = ex.Get_xmlmkdir(Filepath1)  # 将docx的克隆文件解压成含xml文件夹
    Tag_order1 = ex.get_order(extract_path1)
    TreeList1 = ex.Parsing_docx(Tag_order1, Filepath1, extract_path1)
    Filepath2 = ex.Get_filepath()  # 获取docx文件路径
    extract_path2, zip_path2, Folderpath2, souce_name2 = ex.Get_xmlmkdir(Filepath2)  # 将docx的克隆文件解压成含xml文件夹
    Tag_order2 = ex.get_order(extract_path2)
    TreeList2 = ex.Parsing_docx(Tag_order2, Filepath2, extract_path2)
    r2c = func4(TreeList1)
    testcases = func3(TreeList2)
    for requirement in r2c.keys():
        print( requirement+":"+str(getTestCases(requirement, testcases, r2c)))



