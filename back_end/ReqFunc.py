import re
from Extract2_14 import *


def func_1(TreeList):
    '''
    统计功能需求-3.2.x.y
    :param TreeList:
    :return: 功能需求节点列表
    '''
    requirement_list = []#需求列表
    root = TreeList[0]
    name_1 = "具体需求(运行模式组织1)" #一级标题

    if name_1 in root.son_text:
        idx_1 = root.son_text.index(name_1)
        temp_id = root.son_id[idx_1]
        node = TreeList[temp_id]
        name_2 = " 功能需求"  #??空格
        if name_2 in node.son_text:
            idx_2 = node.son_text.index(name_2)
            temp_id = node.son_id[idx_2]
            node_2 = TreeList[temp_id]

            for t_id in node_2.son_id:
                if t_id:
                    node_3 = TreeList[t_id]
                    for tt_id in node_3.son_id:
                        if tt_id:
                            node_4 = TreeList[tt_id]
                            if node_4.name != 'Normal':
                                requirement_list.append(node_4)

        else:
            print("1找不到二级标题", node.son_text)

    else:
        print("1找不到一级标题")

    return requirement_list


def func_7(TreeList):
    '''
    平均响应时间-3.3.4.1
    :param TreeList:
    :return: 平均响应时间数值
    '''
    ave_time = 0
    root = TreeList[0]
    name_1 = "具体需求(运行模式组织1)" #一级标题

    if name_1 in root.son_text:
        idx_1 = root.son_text.index(name_1)
        temp_id = root.son_id[idx_1]
        node = TreeList[temp_id]
        name_2 = "性能需求"  #??空格
        if name_2 in node.son_text:
            idx_2 = node.son_text.index(name_2)
            temp_id = node.son_id[idx_2]
            node_2 = TreeList[temp_id]
            name_3 = "时间特性"
            if name_3 in node_2.son_text:
                idx_3 = node_2.son_text.index(name_3)
                t_id = node_2.son_id[idx_3]
                node_3 = TreeList[t_id]
                name_4 = "平均响应时间"
                if name_4 in node_3.son_text:
                    idx_4 = node_3.son_text.index(name_4)
                    tt_id = node_3.son_id[idx_4]
                    node_4 = TreeList[tt_id]

                    #匹配规则
                    try:
                        content = node_4.son_text[0]
                        pattern = re.compile(r".*?([1-9]\d*\.\d+|0\.\d+|0|[1-9]\d*)(ms|s).*")
                        ave_time = pattern.findall(content)[0]

                    except:
                        print("7匹配平均响应时间失败",node_4.son_text[0])
                        pass


                else:
                    print("7找不到四级标题", node_3.son_text)
            else:
                print("7找不到三级标题")
        else:
            print("7找不到二级标题", node.son_text)

    else:
        print("7找不到一级标题")

    return ave_time


def func_8(TreeList):
    '''
    平均周转时间-3.3.4.2
    :param TreeList:
    :return:时间
    '''
    ave_time = 0
    root = TreeList[0]
    name_1 = "具体需求(运行模式组织1)" #一级标题

    if name_1 in root.son_text:
        idx_1 = root.son_text.index(name_1)
        temp_id = root.son_id[idx_1]
        node = TreeList[temp_id]
        name_2 = "性能需求"  #??空格
        if name_2 in node.son_text:
            idx_2 = node.son_text.index(name_2)
            temp_id = node.son_id[idx_2]
            node_2 = TreeList[temp_id]
            name_3 = "时间特性"
            if name_3 in node_2.son_text:
                idx_3 = node_2.son_text.index(name_3)
                t_id = node_2.son_id[idx_3]
                node_3 = TreeList[t_id]
                name_4 = "平均周转时间"
                if name_4 in node_3.son_text:
                    idx_4 = node_3.son_text.index(name_4)
                    tt_id = node_3.son_id[idx_4]
                    node_4 = TreeList[tt_id]

                    #匹配规则
                    try:
                        content = node_4.son_text[0]
                        pattern = re.compile(r".*?([1-9]\d*\.\d+|0\.\d+|0|[1-9]\d*)(ms|s).*")
                        ave_time = pattern.findall(content)[0]

                    except:
                        print("8匹配平均周转时间失败",node_4.son_text[0])
                        pass


                else:
                    print("8找不到四级标题", node_3.son_text)
            else:
                print("8找不到三级标题")
        else:
            print("8找不到二级标题", node.son_text)

    else:
        print("找不到一级标题")

    return ave_time


def func_19(TreeList):
    '''
    提取软件名称-3.6.6.1表格
    :param TreeList:
    :return: 软件名称表格列表
    '''
    software_list = []
    root = TreeList[0]
    name_1 = "具体需求(运行模式组织1)" #一级标题

    if name_1 in root.son_text:
        idx_1 = root.son_text.index(name_1)
        temp_id = root.son_id[idx_1]
        node = TreeList[temp_id]
        name_2 = "软件系统属性"  #??空格
        if name_2 in node.son_text:
            idx_2 = node.son_text.index(name_2)
            temp_id = node.son_id[idx_2]
            node_2 = TreeList[temp_id]
            name_3 = " 兼容性"#??
            if name_3 in node_2.son_text:
                idx_3 = node_2.son_text.index(name_3)
                t_id = node_2.son_id[idx_3]
                node_3 = TreeList[t_id]
                name_4 = " 运行时允许共存的软件"#??
                if name_4 in node_3.son_text:
                    idx_4 = node_3.son_text.index(name_4)
                    tt_id = node_3.son_id[idx_4]
                    node_4 = TreeList[tt_id]

                    #匹配规则
                    try:
                        table = TreeList[node_4.son_id[0]].table_info
                        if table:
                            for val in list(table.values())[1:]:
                                software_list.append(val[0])

                        else:
                            for text in node_4.son_text:
                                software_list.append(text)


                    except:
                        print("19匹配共存软件失败")

                else:
                    print("19找不到四级标题", node_3.son_text)
            else:
                print("19找不到三级标题", node_2.son_text)
        else:
            print("19找不到二级标题", node.son_text)

    else:
        print("19找不到一级标题")

    return software_list


def func_20(TreeList):
    '''
    提取软件接口-2.1.4.x表格
    :param TreeList:
    :return: 软件接口表格列表
    '''
    software_list = []
    root = TreeList[0]
    name_1 = "总体描述" #一级标题

    if name_1 in root.son_text:
        idx_1 = root.son_text.index(name_1)
        temp_id = root.son_id[idx_1]
        node = TreeList[temp_id]
        name_2 = "产品描述"
        if name_2 in node.son_text:
            idx_2 = node.son_text.index(name_2)
            temp_id = node.son_id[idx_2]
            node_2 = TreeList[temp_id]
            name_3 = "软件接口"
            if name_3 in node_2.son_text:
                idx_3 = node_2.son_text.index(name_3)
                t_id = node_2.son_id[idx_3]
                node_3 = TreeList[t_id]
                for tt_id in node_3.son_id:
                    node_4 = TreeList[tt_id]
                    if node_4.son_id:
                        table = TreeList[node_4.son_id[0]].table_info
                        # print(table)
                        if table:
                            for val in list(table.values())[1:]:
                                software_list.append(val)

                        else:
                            for text in node_4.son_text:
                                software_list.append(text)



            else:
                print("20找不到三级标题", node_2.son_text)
        else:
            print("20找不到二级标题", node.son_text)

    else:
        print("20找不到一级标题")

    return software_list


def func_21(TreeList):
    '''
    提取软件接口-2.1.5表格
    :param TreeList:
    :return: 软件接口表格列表
    '''
    software_list = []
    root = TreeList[0]
    name_1 = "总体描述" #一级标题

    if name_1 in root.son_text:
        idx_1 = root.son_text.index(name_1)
        temp_id = root.son_id[idx_1]
        node = TreeList[temp_id]
        name_2 = "产品描述"
        if name_2 in node.son_text:
            idx_2 = node.son_text.index(name_2)
            temp_id = node.son_id[idx_2]
            node_2 = TreeList[temp_id]
            name_3 = "通信接口"
            if name_3 in node_2.son_text:
                idx_3 = node_2.son_text.index(name_3)
                t_id = node_2.son_id[idx_3]
                node_3 = TreeList[t_id]
                try:
                    table = TreeList[node_3.son_id[0]].table_info
                    if table:
                        for val in list(table.values())[1:]:
                            software_list.append(val)
                    else:
                        for text in node_3.son_text:
                            software_list.append(text)
                except:
                    print("21找不到表格")
            else:
                print("21找不到三级标题", node_2.son_text)
        else:
            print("21找不到二级标题", node.son_text)

    else:
        print("21找不到一级标题")

    return software_list


def func_22(TreeList):
    '''
    提取外部接口-3.1.x.y
    :param TreeList:
    :return: 软件外部接口节点列表
    '''
    software_list = []
    root = TreeList[0]
    name_1 = "具体需求(运行模式组织1)" #一级标题

    if name_1 in root.son_text:
        idx_1 = root.son_text.index(name_1)
        temp_id = root.son_id[idx_1]
        node = TreeList[temp_id]
        name_2 = "外部接口需求"
        if name_2 in node.son_text:
            idx_2 = node.son_text.index(name_2)
            temp_id = node.son_id[idx_2]
            node_2 = TreeList[temp_id]
            for t_id in node_2.son_id:
                node_3 = TreeList[t_id]
                for tt_id in node_3.son_id:
                    node_4 = TreeList[tt_id]
                    software_list.append(node_4)

        else:
            print("22找不到二级标题", node.son_text)

    else:
        print("22找不到一级标题")

    return software_list


def func_24(TreeList):
    '''
    提取产品功能数量-2.2.x
    :param TreeList:
    :return: 产品功能节点列表
    '''
    software_list = []
    root = TreeList[0]
    name_1 = "总体描述" #一级标题

    if name_1 in root.son_text:
        idx_1 = root.son_text.index(name_1)
        temp_id = root.son_id[idx_1]
        node = TreeList[temp_id]
        name_2 = "产品功能"
        if name_2 in node.son_text:
            idx_2 = node.son_text.index(name_2)
            temp_id = node.son_id[idx_2]
            node_2 = TreeList[temp_id]
            for t_id in node_2.son_id:
                node_3 = TreeList[t_id]
                software_list.append(node_3)


        else:
            print("24找不到二级标题", node.son_text)

    else:
        print("24找不到一级标题")

    return software_list


def func_25(TreeList):
    '''
    提取功能演示-2.2.x
    :param TreeList:
    :return: 产品功能演示节点列表
    '''
    software_list = []
    root = TreeList[0]
    name_1 = "总体描述" #一级标题

    if name_1 in root.son_text:
        idx_1 = root.son_text.index(name_1)
        temp_id = root.son_id[idx_1]
        node = TreeList[temp_id]
        name_2 = "产品功能"
        if name_2 in node.son_text:
            idx_2 = node.son_text.index(name_2)
            temp_id = node.son_id[idx_2]
            node_2 = TreeList[temp_id]
            key_words = "功能演示"
            for son_text in node_2.son_text:
                if key_words in son_text:
                    idx = node_2.son_text.index(son_text)
                    node_3 = TreeList[node_2.son_id[idx]]
                    software_list.append(node_3)


        else:
            print("25找不到二级标题", node.son_text)

    else:
        print("25找不到一级标题")

    return software_list


def func_32(TreeList):
    '''
    提取操作一致性-2.1.7表格
    :param TreeList:
    :return: 操作一致性表格列表
    '''
    software_list = []
    root = TreeList[0]
    name_1 = "总体描述" #一级标题

    if name_1 in root.son_text:
        idx_1 = root.son_text.index(name_1)
        temp_id = root.son_id[idx_1]
        node = TreeList[temp_id]
        name_2 = "产品描述"
        if name_2 in node.son_text:
            idx_2 = node.son_text.index(name_2)
            temp_id = node.son_id[idx_2]
            node_2 = TreeList[temp_id]
            name_3 = "操作"
            if name_3 in node_2.son_text:
                idx_3 = node_2.son_text.index(name_3)
                t_id = node_2.son_id[idx_3]
                node_3 = TreeList[t_id]
                name_4 = "操作一致性任务"
                if name_4 in node_3.son_text:
                    idx_4 = node_3.son_text.index(name_4)
                    tt_id = node_3.son_id[idx_4]
                    node_4 = TreeList[tt_id]
                    try:
                        node_5 = TreeList[node_4.son_id[0]]
                        table = node_5.table_info
                        if table:
                            for val in list(table.values())[1:]:
                                software_list.append(val)
                        else:
                            for text in node_4.son_text:
                                software_list.append(text)
                    except:
                        print("32找不到表格")
                else:
                    print("32找不到四级标题")
            else:
                print("32找不到三级标题")
        else:
            print("32找不到二级标题")

    else:
        print("32找不到一级标题")

    return software_list


def func_34(TreeList):
    '''
    提取用户定制功能-3.7.1表格
    :param TreeList:
    :return: 用户定制功能表格列表
    '''
    software_list = []
    root = TreeList[0]
    name_1 = "具体需求(运行模式组织1)" #一级标题

    if name_1 in root.son_text:
        idx_1 = root.son_text.index(name_1)
        temp_id = root.son_id[idx_1]
        node = TreeList[temp_id]
        name_2 = "其他需求"
        if name_2 in node.son_text:
            idx_2 = node.son_text.index(name_2)
            temp_id = node.son_id[idx_2]
            node_2 = TreeList[temp_id]
            name_3 = "支持用户定制功能"
            if name_3 in node_2.son_text:
                idx_3 = node_2.son_text.index(name_3)
                t_id = node_2.son_id[idx_3]
                node_3 = TreeList[t_id]
                try:
                    node_4 = TreeList[node_3.son_id[0]]
                    table = node_4.table_info
                    if table:
                        for val in list(table.values())[1:]:
                            software_list.append(val)
                    else:
                        for text in node_3.son_text:
                            software_list.append(text)
                except:
                    print("34找不到表格")

            else:
                print("34找不到三级标题")
        else:
            print("34找不到二级标题")

    else:
        print("34找不到一级标题")

    return software_list


def func_35(TreeList):
    '''
    提取用户定制界面-3.7.1表格
    :param TreeList:
    :return: 用户定制界面表格列表
    '''
    software_list = []
    root = TreeList[0]
    name_1 = "具体需求(运行模式组织1)" #一级标题

    if name_1 in root.son_text:
        idx_1 = root.son_text.index(name_1)
        temp_id = root.son_id[idx_1]
        node = TreeList[temp_id]
        name_2 = "其他需求"
        if name_2 in node.son_text:
            idx_2 = node.son_text.index(name_2)
            temp_id = node.son_id[idx_2]
            node_2 = TreeList[temp_id]
            name_3 = "支持用户定制界面"
            if name_3 in node_2.son_text:
                idx_3 = node_2.son_text.index(name_3)
                t_id = node_2.son_id[idx_3]
                node_3 = TreeList[t_id]
                try:
                    node_4 = TreeList[node_3.son_id[0]]
                    table = node_4.table_info
                    if table:
                        for val in list(table.values())[1:]:
                            software_list.append(val)
                    else:
                        for text in node_3.son_text:
                            software_list.append(text)
                except:
                    print("35找不到表格")

            else:
                print("35找不到三级标题")
        else:
            print("35找不到二级标题")

    else:
        print("35找不到一级标题")

    return software_list


def func_36(TreeList):
    '''
    提取状态监视-3.2.x.y
    :param TreeList:
    :return: 状态监视节点列表
    '''
    key_words = "状态监视"
    software_list = []
    root = TreeList[0]
    name_1 = "具体需求(运行模式组织1)" #一级标题

    if name_1 in root.son_text:
        idx_1 = root.son_text.index(name_1)
        temp_id = root.son_id[idx_1]
        node = TreeList[temp_id]
        name_2 = " 功能需求"
        if name_2 in node.son_text:
            idx_2 = node.son_text.index(name_2)
            temp_id = node.son_id[idx_2]
            node_2 = TreeList[temp_id]
            for t_id in node_2.son_id:
                node_3 = TreeList[t_id]
                for tt_id in node_3.son_id:
                    node_4 = TreeList[tt_id]
                    if key_words in node_4.text:
                        software_list.append(node_4)
                    else:
                        for son_text in node_4.son_text:
                            if key_words in son_text:
                                software_list.append(node_4)
                                break


        else:
            print("36找不到二级标题")

    else:
        print("36找不到一级标题")

    return software_list


def func_37(TreeList):
    '''
    提取撤销操作-3.2.x.y
    :param TreeList:
    :return: 撤销操作节点列表
    '''
    key_words = "撤销操作"
    software_list = []
    root = TreeList[0]
    name_1 = "具体需求(运行模式组织1)" #一级标题

    if name_1 in root.son_text:
        idx_1 = root.son_text.index(name_1)
        temp_id = root.son_id[idx_1]
        node = TreeList[temp_id]
        name_2 = " 功能需求"
        if name_2 in node.son_text:
            idx_2 = node.son_text.index(name_2)
            temp_id = node.son_id[idx_2]
            node_2 = TreeList[temp_id]
            for t_id in node_2.son_id:
                node_3 = TreeList[t_id]
                for tt_id in node_3.son_id:
                    node_4 = TreeList[tt_id]
                    if key_words in node_4.text:
                        software_list.append(node_4)
                    else:
                        for son_text in node_4.son_text:
                            if key_words in son_text:
                                software_list.append(node_4)
                                break


        else:
            print("37找不到二级标题")

    else:
        print("37找不到一级标题")

    return software_list


def func_38(TreeList):
    '''
    提取外观一致性-3.7.3表格
    :param TreeList:
    :return: 外观一致性表格列表
    '''

    software_list = []
    root = TreeList[0]
    name_1 = "具体需求(运行模式组织1)" #一级标题

    if name_1 in root.son_text:
        idx_1 = root.son_text.index(name_1)
        temp_id = root.son_id[idx_1]
        node = TreeList[temp_id]
        name_2 = "其他需求"
        if name_2 in node.son_text:
            idx_2 = node.son_text.index(name_2)
            temp_id = node.son_id[idx_2]
            node_2 = TreeList[temp_id]
            name_3 = "界面外观一致性"
            if name_3 in node_2.son_text:
                idx_3 = node_2.son_text.index(name_3)
                t_id = node_2.son_id[idx_3]
                node_3 = TreeList[t_id]
                try:
                    table = TreeList[node_3.son_id[0]].table_info
                    if table:
                        for val in list(table.values())[1:]:
                            software_list.append(val)
                    else:
                        for text in node_3.son_text:
                            software_list.append(text)
                except:
                    print("38找不到表格")
            else:
                print("38找不到三级标题")
        else:
            print("38找不到二级标题")

    else:
        print("38找不到一级标题")

    return software_list


def func_40(TreeList):
    '''
    提取用户特定操作-2.1.7表格
    :param TreeList:
    :return: 用户特定操作表格列表
    '''
    software_list = []
    root = TreeList[0]
    name_1 = "总体描述" #一级标题

    if name_1 in root.son_text:
        idx_1 = root.son_text.index(name_1)
        temp_id = root.son_id[idx_1]
        node = TreeList[temp_id]
        name_2 = "产品描述"
        if name_2 in node.son_text:
            idx_2 = node.son_text.index(name_2)
            temp_id = node.son_id[idx_2]
            node_2 = TreeList[temp_id]
            name_3 = "操作"
            if name_3 in node_2.son_text:
                idx_3 = node_2.son_text.index(name_3)
                t_id = node_2.son_id[idx_3]
                node_3 = TreeList[t_id]
                name_4 = "用户特定的操作"
                if name_4 in node_3.son_text:
                    idx_4 = node_3.son_text.index(name_4)
                    tt_id = node_3.son_id[idx_4]
                    node_4 = TreeList[tt_id]
                    try:
                        node_5 = TreeList[node_4.son_id[0]]
                        table = node_5.table_info
                        if table:
                            for val in list(table.values())[1:]:
                                software_list.append(val)
                        else:
                            for text in node_4.son_text:
                                software_list.append(text)
                    except:
                        print("40找不到表格")
                else:
                    print("40找不到四级标题")
            else:
                print("40找不到三级标题")
        else:
            print("40找不到二级标题")

    else:
        print("40找不到一级标题")

    return software_list


def func_41(TreeList):
    '''
    提取用户界面数量-2.1.2.x
    :param TreeList:
    :return: 用户界面节点列表
    '''
    software_list = []
    root = TreeList[0]
    name_1 = "总体描述" #一级标题

    if name_1 in root.son_text:
        idx_1 = root.son_text.index(name_1)
        temp_id = root.son_id[idx_1]
        node = TreeList[temp_id]
        name_2 = "产品描述"
        if name_2 in node.son_text:
            idx_2 = node.son_text.index(name_2)
            temp_id = node.son_id[idx_2]
            node_2 = TreeList[temp_id]
            name_3 = "用户界面"
            if name_3 in node_2.son_text:
                idx_3 = node_2.son_text.index(name_3)
                t_id = node_2.son_id[idx_3]
                node_3 = TreeList[t_id]
                for tt_id in node_3.son_id:
                    node_4 = TreeList[tt_id]
                    software_list.append(node_4)

            else:
                print("41找不到三级标题")
        else:
            print("41找不到二级标题")

    else:
        print("41找不到一级标题")

    return software_list


def func_43(TreeList):
    '''
    故障修复率-3.6.1.1
    :param TreeList:
    :return: 故障修复率字符串
    '''
    ave_time = 0
    root = TreeList[0]
    name_1 = "具体需求(运行模式组织1)" #一级标题

    if name_1 in root.son_text:
        idx_1 = root.son_text.index(name_1)
        temp_id = root.son_id[idx_1]
        node = TreeList[temp_id]
        name_2 = "软件系统属性"  #??空格
        if name_2 in node.son_text:
            idx_2 = node.son_text.index(name_2)
            temp_id = node.son_id[idx_2]
            node_2 = TreeList[temp_id]
            name_3 = "可靠性"
            if name_3 in node_2.son_text:
                idx_3 = node_2.son_text.index(name_3)
                t_id = node_2.son_id[idx_3]
                node_3 = TreeList[t_id]
                name_4 = "故障修复率"
                if name_4 in node_3.son_text:
                    idx_4 = node_3.son_text.index(name_4)
                    tt_id = node_3.son_id[idx_4]
                    node_4 = TreeList[tt_id]

                    #匹配规则
                    try:
                        content = node_4.son_text[0]
                        pattern = re.compile(r".*?([1-9]\d*\.\d+|0\.\d+|0|[1-9]\d*)(%).*")
                        ave_time =pattern.findall(content)[0]

                    except:
                        print("43匹配故障修复率失败")

                else:
                    print("43找不到四级标题", node_3.son_text)
            else:
                print("43找不到三级标题")
        else:
            print("43找不到二级标题", node.son_text)

    else:
        print("43找不到一级标题")

    return ave_time


def func_44(TreeList):
    '''
    ？？？
    平均失效间隔-3.6.1.2
    :param TreeList:
    :return: 平均失效间隔字符串
    '''
    ave_time = 0
    root = TreeList[0]
    name_1 = "具体需求(运行模式组织1)" #一级标题

    if name_1 in root.son_text:
        idx_1 = root.son_text.index(name_1)
        temp_id = root.son_id[idx_1]
        node = TreeList[temp_id]
        name_2 = "软件系统属性"  #??空格
        if name_2 in node.son_text:
            idx_2 = node.son_text.index(name_2)
            temp_id = node.son_id[idx_2]
            node_2 = TreeList[temp_id]
            name_3 = "可靠性"
            if name_3 in node_2.son_text:
                idx_3 = node_2.son_text.index(name_3)
                t_id = node_2.son_id[idx_3]
                node_3 = TreeList[t_id]
                name_4 = "平均失效间隔"
                if name_4 in node_3.son_text:
                    idx_4 = node_3.son_text.index(name_4)
                    tt_id = node_3.son_id[idx_4]
                    node_4 = TreeList[tt_id]

                    #匹配规则
                    try:
                        content = node_4.son_text[0]
                        pattern = re.compile(r".*?([1-9]\d*\.\d+|0\.\d+|0|[1-9]\d*)(小时|天).*")
                        ave_time =pattern.findall(content)[0]

                    except:
                        print("44匹配平均失效间隔失败")

                else:
                    print("44找不到四级标题", node_3.son_text)
            else:
                print("44找不到三级标题")
        else:
            print("44找不到二级标题", node.son_text)

    else:
        print("44找不到一级标题")

    return ave_time


def func_45(TreeList):
    '''

    周期失效率-3.6.1.3
    :param TreeList:
    :return: 周期失效率字符串
    '''
    ave_time = 0
    root = TreeList[0]
    name_1 = "具体需求(运行模式组织1)" #一级标题

    if name_1 in root.son_text:
        idx_1 = root.son_text.index(name_1)
        temp_id = root.son_id[idx_1]
        node = TreeList[temp_id]
        name_2 = "软件系统属性"  #??空格
        if name_2 in node.son_text:
            idx_2 = node.son_text.index(name_2)
            temp_id = node.son_id[idx_2]
            node_2 = TreeList[temp_id]
            name_3 = "可靠性"
            if name_3 in node_2.son_text:
                idx_3 = node_2.son_text.index(name_3)
                t_id = node_2.son_id[idx_3]
                node_3 = TreeList[t_id]
                name_4 = "周期失效率"
                if name_4 in node_3.son_text:
                    idx_4 = node_3.son_text.index(name_4)
                    tt_id = node_3.son_id[idx_4]
                    node_4 = TreeList[tt_id]

                    #匹配规则
                    try:
                        content = node_4.son_text[0]
                        pattern = re.compile(r".*?([1-9]\d*\.\d+|0\.\d+|0|[1-9]\d*)(%).*")
                        ave_time =pattern.findall(content)[0]

                    except:
                        print("45匹配平均失效间隔失败")

                else:
                    print("45找不到四级标题", node_3.son_text)
            else:
                print("45找不到三级标题")
        else:
            print("45找不到二级标题", node.son_text)

    else:
        print("45找不到一级标题")

    return ave_time


def func_47(TreeList):
    '''
    ？？？
    系统运行时间-3.6.2.1
    :param TreeList:
    :return: 系统运行时间字符串
    '''
    ave_time = 0
    root = TreeList[0]
    name_1 = "具体需求(运行模式组织1)" #一级标题

    if name_1 in root.son_text:
        idx_1 = root.son_text.index(name_1)
        temp_id = root.son_id[idx_1]
        node = TreeList[temp_id]
        name_2 = "软件系统属性"  #??空格
        if name_2 in node.son_text:
            idx_2 = node.son_text.index(name_2)
            temp_id = node.son_id[idx_2]
            node_2 = TreeList[temp_id]
            name_3 = "可用性"
            if name_3 in node_2.son_text:
                idx_3 = node_2.son_text.index(name_3)
                t_id = node_2.son_id[idx_3]
                node_3 = TreeList[t_id]
                name_4 = "系统运行时间"
                if name_4 in node_3.son_text:
                    idx_4 = node_3.son_text.index(name_4)
                    tt_id = node_3.son_id[idx_4]
                    node_4 = TreeList[tt_id]

                    #匹配规则
                    try:
                        content = node_4.son_text[0]
                        pattern = re.compile(r".*?([1-9]\d*\.\d+|0\.\d+|0|[1-9]\d*)(小时|天).*")
                        ave_time =pattern.findall(content)[0]

                    except:
                        print("47匹配平均失效间隔失败")

                else:
                    print("47找不到四级标题", node_3.son_text)
            else:
                print("47找不到三级标题")
        else:
            print("47找不到二级标题", node.son_text)

    else:
        print("47找不到一级标题")

    return ave_time


def func_49(TreeList):
    '''
    ？？？
    平均宕机时间-3.6.2.2
    :param TreeList:
    :return: 平均宕机时间字符串
    '''
    ave_time = 0
    root = TreeList[0]
    name_1 = "具体需求(运行模式组织1)" #一级标题

    if name_1 in root.son_text:
        idx_1 = root.son_text.index(name_1)
        temp_id = root.son_id[idx_1]
        node = TreeList[temp_id]
        name_2 = "软件系统属性"  #??空格
        if name_2 in node.son_text:
            idx_2 = node.son_text.index(name_2)
            temp_id = node.son_id[idx_2]
            node_2 = TreeList[temp_id]
            name_3 = "可用性"
            if name_3 in node_2.son_text:
                idx_3 = node_2.son_text.index(name_3)
                t_id = node_2.son_id[idx_3]
                node_3 = TreeList[t_id]
                name_4 = "平均宕机时间"
                if name_4 in node_3.son_text:
                    idx_4 = node_3.son_text.index(name_4)
                    tt_id = node_3.son_id[idx_4]
                    node_4 = TreeList[tt_id]

                    #匹配规则
                    try:
                        content = node_4.son_text[0]
                        pattern = re.compile(r".*?([1-9]\d*\.\d+|0\.\d+|0|[1-9]\d*)(小时|天).*")
                        ave_time =pattern.findall(content)[0]

                    except:
                        print("49匹配平均失效间隔失败")

                else:
                    print("49找不到四级标题", node_3.son_text)
            else:
                print("49找不到三级标题")
        else:
            print("49找不到二级标题", node.son_text)

    else:
        print("49找不到一级标题")

    return ave_time


def func_50(TreeList):
    '''
    故障模式数量-3.6.1.4
    :param TreeList:
    :return: 故障模式表格列表
    '''
    res = []
    root = TreeList[0]
    name_1 = "具体需求(运行模式组织1)" #一级标题

    if name_1 in root.son_text:
        idx_1 = root.son_text.index(name_1)
        temp_id = root.son_id[idx_1]
        node = TreeList[temp_id]
        name_2 = "软件系统属性"  #??空格
        if name_2 in node.son_text:
            idx_2 = node.son_text.index(name_2)
            temp_id = node.son_id[idx_2]
            node_2 = TreeList[temp_id]
            name_3 = "可靠性"
            if name_3 in node_2.son_text:
                idx_3 = node_2.son_text.index(name_3)
                t_id = node_2.son_id[idx_3]
                node_3 = TreeList[t_id]
                name_4 = "故障模式"
                if name_4 in node_3.son_text:
                    idx_4 = node_3.son_text.index(name_4)
                    tt_id = node_3.son_id[idx_4]
                    node_4 = TreeList[tt_id]

                    #匹配规则
                    try:
                        table = TreeList[node_4.son_id[0]].table_info
                        if table:
                            for val in list(table.values())[1:]:
                                res.append(val)
                        else:
                            for text in node_4.son_text:
                                res.append(text)

                    except:
                        print("50匹配表格失败")

                else:
                    print("50找不到四级标题", node_3.son_text)
            else:
                print("50找不到三级标题")
        else:
            print("50找不到二级标题", node.son_text)

    else:
        print("50找不到一级标题")

    return res


def func_51(TreeList):
    '''
    ？？？
    平均故障通告时间-3.6.1.5
    :param TreeList:
    :return: 平均故障通告时间字符串
    '''
    ave_time = 0
    root = TreeList[0]
    name_1 = "具体需求(运行模式组织1)" #一级标题

    if name_1 in root.son_text:
        idx_1 = root.son_text.index(name_1)
        temp_id = root.son_id[idx_1]
        node = TreeList[temp_id]
        name_2 = "软件系统属性"  #??空格
        if name_2 in node.son_text:
            idx_2 = node.son_text.index(name_2)
            temp_id = node.son_id[idx_2]
            node_2 = TreeList[temp_id]
            name_3 = "可靠性"
            if name_3 in node_2.son_text:
                idx_3 = node_2.son_text.index(name_3)
                t_id = node_2.son_id[idx_3]
                node_3 = TreeList[t_id]
                name_4 = "平均故障通告时间"
                if name_4 in node_3.son_text:
                    idx_4 = node_3.son_text.index(name_4)
                    tt_id = node_3.son_id[idx_4]
                    node_4 = TreeList[tt_id]

                    #匹配规则
                    try:
                        content = node_4.son_text[0]
                        pattern = re.compile(r".*?([1-9]\d*\.\d+|0\.\d+|0|[1-9]\d*)(s|min).*")
                        ave_time =pattern.findall(content)[0]

                    except:
                        print("51匹配平均失效间隔失败")

                else:
                    print("51找不到四级标题", node_3.son_text)
            else:
                print("51找不到三级标题")
        else:
            print("51找不到二级标题", node.son_text)

    else:
        print("51找不到一级标题")

    return ave_time


def func_52(TreeList):
    '''
    ？？？
    平均恢复时间-3.6.1.6
    :param TreeList:
    :return: 平均恢复时间字符串
    '''
    ave_time = 0
    root = TreeList[0]
    name_1 = "具体需求(运行模式组织1)" #一级标题

    if name_1 in root.son_text:
        idx_1 = root.son_text.index(name_1)
        temp_id = root.son_id[idx_1]
        node = TreeList[temp_id]
        name_2 = "软件系统属性"  #??空格
        if name_2 in node.son_text:
            idx_2 = node.son_text.index(name_2)
            temp_id = node.son_id[idx_2]
            node_2 = TreeList[temp_id]
            name_3 = "可靠性"
            if name_3 in node_2.son_text:
                idx_3 = node_2.son_text.index(name_3)
                t_id = node_2.son_id[idx_3]
                node_3 = TreeList[t_id]
                name_4 = "平均恢复时间"
                if name_4 in node_3.son_text:
                    idx_4 = node_3.son_text.index(name_4)
                    tt_id = node_3.son_id[idx_4]
                    node_4 = TreeList[tt_id]

                    #匹配规则
                    try:
                        content = node_4.son_text[0]
                        pattern = re.compile(r".*?([1-9]\d*\.\d+|0\.\d+|0|[1-9]\d*)(s|min).*")
                        ave_time =pattern.findall(content)[0]

                    except:
                        print("52匹配平均恢复时间失败")

                else:
                    print("52找不到四级标题", node_3.son_text)
            else:
                print("52找不到三级标题")
        else:
            print("52找不到二级标题", node.son_text)

    else:
        print("52找不到一级标题")

    return ave_time


def func_58(TreeList):
    '''
    使用的密码技术-3.6.3.1
    :param TreeList:
    :return: 使用的密码技术表格列表
    '''
    res = []
    root = TreeList[0]
    name_1 = "具体需求(运行模式组织1)" #一级标题

    if name_1 in root.son_text:
        idx_1 = root.son_text.index(name_1)
        temp_id = root.son_id[idx_1]
        node = TreeList[temp_id]
        name_2 = "软件系统属性"  #??空格
        if name_2 in node.son_text:
            idx_2 = node.son_text.index(name_2)
            temp_id = node.son_id[idx_2]
            node_2 = TreeList[temp_id]
            name_3 = "安全保密性"
            if name_3 in node_2.son_text:
                idx_3 = node_2.son_text.index(name_3)
                t_id = node_2.son_id[idx_3]
                node_3 = TreeList[t_id]
                name_4 = "使用的密码技术"
                if name_4 in node_3.son_text:
                    idx_4 = node_3.son_text.index(name_4)
                    tt_id = node_3.son_id[idx_4]
                    node_4 = TreeList[tt_id]

                    #匹配规则
                    try:
                        table = TreeList[node_4.son_id[0]].table_info
                        if table:
                            for val in list(table.values())[1:]:
                                res.append(val)
                        else:
                            for text in node_4.son_text:
                                res.append(text)

                    except:
                        print("58匹配表格失败")

                else:
                    print("58找不到四级标题", node_3.son_text)
            else:
                print("58找不到三级标题")
        else:
            print("58找不到二级标题", node.son_text)

    else:
        print("58找不到一级标题")

    return res


def func_60(TreeList):
    '''
    对于关键变量检查数据的完整性-3.6.3.5
    :param TreeList:
    :return: 对于关键变量检查数据的完整性表格列表
    '''
    res = []
    root = TreeList[0]
    name_1 = "具体需求(运行模式组织1)" #一级标题

    if name_1 in root.son_text:
        idx_1 = root.son_text.index(name_1)
        temp_id = root.son_id[idx_1]
        node = TreeList[temp_id]
        name_2 = "软件系统属性"  #??空格
        if name_2 in node.son_text:
            idx_2 = node.son_text.index(name_2)
            temp_id = node.son_id[idx_2]
            node_2 = TreeList[temp_id]
            name_3 = "安全保密性"
            if name_3 in node_2.son_text:
                idx_3 = node_2.son_text.index(name_3)
                t_id = node_2.son_id[idx_3]
                node_3 = TreeList[t_id]
                name_4 = "对于关键变量检查数据的完整性"
                if name_4 in node_3.son_text:
                    idx_4 = node_3.son_text.index(name_4)
                    tt_id = node_3.son_id[idx_4]
                    node_4 = TreeList[tt_id]

                    #匹配规则
                    try:
                        table = TreeList[node_4.son_id[0]].table_info
                        if table:
                            for val in list(table.values())[1:]:
                                res.append(val)
                        else:
                            for text in node_4.son_text:
                                res.append(text)

                    except:
                        print("60匹配表格失败")

                else:
                    print("60找不到四级标题", node_3.son_text)
            else:
                print("60找不到三级标题")
        else:
            print("60找不到二级标题", node.son_text)

    else:
        print("60找不到一级标题")

    return res


def func_61(TreeList):
    '''
    保留某些特定数据组的历史或记录-3.6.3.2
    :param TreeList:
    :return: 保留某些特定数据组的历史或记录表格列表
    '''
    res = []
    root = TreeList[0]
    name_1 = "具体需求(运行模式组织1)" #一级标题

    if name_1 in root.son_text:
        idx_1 = root.son_text.index(name_1)
        temp_id = root.son_id[idx_1]
        node = TreeList[temp_id]
        name_2 = "软件系统属性"  #??空格
        if name_2 in node.son_text:
            idx_2 = node.son_text.index(name_2)
            temp_id = node.son_id[idx_2]
            node_2 = TreeList[temp_id]
            name_3 = "安全保密性"
            if name_3 in node_2.son_text:
                idx_3 = node_2.son_text.index(name_3)
                t_id = node_2.son_id[idx_3]
                node_3 = TreeList[t_id]
                name_4 = "保留某些特定数据组的历史或记录"
                if name_4 in node_3.son_text:
                    idx_4 = node_3.son_text.index(name_4)
                    tt_id = node_3.son_id[idx_4]
                    node_4 = TreeList[tt_id]

                    #匹配规则
                    try:
                        table = TreeList[node_4.son_id[0]].table_info
                        if table:
                            for val in list(table.values())[1:]:
                                res.append(val)
                        else:
                            for text in node_4.son_text:
                                res.append(text)

                    except:
                        print("61匹配表格失败")

                else:
                    print("61找不到四级标题", node_3.son_text)
            else:
                print("61找不到三级标题")
        else:
            print("61找不到二级标题", node.son_text)

    else:
        print("61找不到一级标题")

    return res


def func_62(TreeList):
    '''
    访问能力-3.4.3
    :param TreeList:
    :return: 访问能力表格列表
    '''
    res = []
    root = TreeList[0]
    name_1 = "具体需求(运行模式组织1)" #一级标题

    if name_1 in root.son_text:
        idx_1 = root.son_text.index(name_1)
        temp_id = root.son_id[idx_1]
        node = TreeList[temp_id]
        name_2 = "数据库逻辑需求"  #??空格
        if name_2 in node.son_text:
            idx_2 = node.son_text.index(name_2)
            temp_id = node.son_id[idx_2]
            node_2 = TreeList[temp_id]
            name_3 = "访问能力"
            if name_3 in node_2.son_text:
                idx_3 = node_2.son_text.index(name_3)
                t_id = node_2.son_id[idx_3]
                node_3 = TreeList[t_id]

                #匹配规则
                try:
                    table = TreeList[node_3.son_id[0]].table_info
                    if table:
                        for val in list(table.values())[1:]:
                            res.append(val)
                    else:
                        for text in node_3.son_text:
                            res.append(text)

                except:
                    print("62匹配表格失败")

            else:
                print("62找不到三级标题")
        else:
            print("62找不到二级标题", node.son_text)

    else:
        print("62找不到一级标题")

    return res


def func_63(TreeList):
    '''
    用户审计追踪3.6.7.1
    :param TreeList:
    :return: True、False
    '''
    res = False
    root = TreeList[0]
    name_1 = "具体需求(运行模式组织1)" #一级标题

    if name_1 in root.son_text:
        idx_1 = root.son_text.index(name_1)
        temp_id = root.son_id[idx_1]
        node = TreeList[temp_id]
        name_2 = "软件系统属性"  #??空格
        if name_2 in node.son_text:
            idx_2 = node.son_text.index(name_2)
            temp_id = node.son_id[idx_2]
            node_2 = TreeList[temp_id]
            name_3 = "可审查性"
            if name_3 in node_2.son_text:
                idx_3 = node_2.son_text.index(name_3)
                t_id = node_2.son_id[idx_3]
                node_3 = TreeList[t_id]
                name_4 = "用户审计追踪"
                if name_4 in node_3.son_text:
                    res = True

                else:
                    print("63找不到四级标题", node_3.son_text)
            else:
                print("63找不到三级标题")
        else:
            print("63找不到二级标题", node.son_text)

    else:
        print("63找不到一级标题")

    return res


def func_64(TreeList):
    '''
    ？？？
    系统日志保留时长-3.6.7.2
    :param TreeList:
    :return: 系统日志保留时长字符串
    '''
    ave_time = 0
    root = TreeList[0]
    name_1 = "具体需求(运行模式组织1)" #一级标题

    if name_1 in root.son_text:
        idx_1 = root.son_text.index(name_1)
        temp_id = root.son_id[idx_1]
        node = TreeList[temp_id]
        name_2 = "软件系统属性"  #??空格
        if name_2 in node.son_text:
            idx_2 = node.son_text.index(name_2)
            temp_id = node.son_id[idx_2]
            node_2 = TreeList[temp_id]
            name_3 = "可审查性"
            if name_3 in node_2.son_text:
                idx_3 = node_2.son_text.index(name_3)
                t_id = node_2.son_id[idx_3]
                node_3 = TreeList[t_id]
                name_4 = "系统日志保留时长"
                if name_4 in node_3.son_text:
                    idx_4 = node_3.son_text.index(name_4)
                    tt_id = node_3.son_id[idx_4]
                    node_4 = TreeList[tt_id]

                    #匹配规则
                    try:
                        content = node_4.son_text[0]
                        pattern = re.compile(r".*?([1-9]\d*\.\d+|0\.\d+|0|[1-9]\d*)(天|月).*")
                        ave_time =pattern.findall(content)[0]

                    except:
                        print("64匹配平均失效间隔失败")

                else:
                    print("64找不到四级标题", node_3.son_text)
            else:
                print("64找不到三级标题")
        else:
            print("64找不到二级标题", node.son_text)

    else:
        print("64找不到一级标题")

    return ave_time


def func_65(TreeList):
    '''
    编码规则-3.5.1.x
    :param TreeList:
    :return: 编码规则节点列表
    '''
    key_words = "编码规则"
    software_list = []
    root = TreeList[0]
    name_1 = "具体需求(运行模式组织1)" #一级标题

    if name_1 in root.son_text:
        idx_1 = root.son_text.index(name_1)
        temp_id = root.son_id[idx_1]
        node = TreeList[temp_id]
        name_2 = "设计约束"
        if name_2 in node.son_text:
            idx_2 = node.son_text.index(name_2)
            temp_id = node.son_id[idx_2]
            node_2 = TreeList[temp_id]
            name_3 = "标准依从性"
            if name_3 in node_2.son_text:
                idx_3 = node_2.son_text.index(name_3)
                t_id = node_2.son_id[idx_3]
                node_3 = TreeList[t_id]

                for tt_id in node_3.son_id:
                    node_4 = TreeList[tt_id]
                    if key_words in node_4.text:
                        software_list.append(node_4)
                    else:
                        for son_text in node_4.son_text:
                            if key_words in son_text:
                                software_list.append(node_4)
                                break

            else:
                print("65找不到三级标题")

        else:
            print("65找不到二级标题")

    else:
        print("65找不到一级标题")

    return software_list


def func_66(TreeList):
    '''
    系统日志完整性3.6.7.3
    :param TreeList:
    :return: True、False
    '''
    res = False
    root = TreeList[0]
    name_1 = "具体需求(运行模式组织1)" #一级标题

    if name_1 in root.son_text:
        idx_1 = root.son_text.index(name_1)
        temp_id = root.son_id[idx_1]
        node = TreeList[temp_id]
        name_2 = "软件系统属性"  #??空格
        if name_2 in node.son_text:
            idx_2 = node.son_text.index(name_2)
            temp_id = node.son_id[idx_2]
            node_2 = TreeList[temp_id]
            name_3 = "可审查性"
            if name_3 in node_2.son_text:
                idx_3 = node_2.son_text.index(name_3)
                t_id = node_2.son_id[idx_3]
                node_3 = TreeList[t_id]
                name_4 = "系统日志完整性"
                if name_4 in node_3.son_text:
                    res = True

                else:
                    print("66找不到四级标题", node_3.son_text)
            else:
                print("66找不到三级标题")
        else:
            print("66找不到二级标题", node.son_text)

    else:
        print("66找不到一级标题")

    return res

def func_xx(TreeList):
    res = {}
    for node in TreeList:
        if node.text == "系统特定目标追踪表":
            table_id = node.son_id[0]
            table_dict = TreeList[table_id].table_info
            for k in range(1, len(table_dict)):
                if table_dict[k][0] in res.keys():
                    res[table_dict[k][0]].append(table_dict[k][2])
                else:
                    res[table_dict[k][0]] = [table_dict[k][2]]
    return res

def func_xx2(TreeList):
    try:
        for node in TreeList:
            if node.text == "圈复杂度阈值":
                text = node.son_text[0]
                match = re.findall(r"(?:圈复杂度阈值：)(\d+)", text)
                return match[0]
    except:
        return -1


if __name__ == '__main__':
    Filepath = Get_filepath()  # 获取docx文件路径
    extract_path, zip_path, Folderpath, souce_name = Get_xmlmkdir(Filepath)  # 将docx的克隆文件解压成含xml文件夹
    Tag_order = get_order(extract_path)
    TreeList = Parsing_docx(Tag_order, Filepath, extract_path)
    # Print_TreeList(TreeList)  # 打印树节点信息
    # Output_to_txt(TreeList, Folderpath, souce_name)  # 存入txt
    # Structural_network(TreeList)  # 生成图

    res_1 = func_1(TreeList)
    Print_TreeList(res_1)

    res_7 = func_7(TreeList)
    print(res_7)

    res_8 = func_8(TreeList)
    print(res_8)

    res_19 = func_19(TreeList)
    # print(res_19)
    print("软件列表\n",res_19)

    res_20 = func_20(TreeList)
    print(res_20)

    res_21 = func_21(TreeList)
    print(res_21)

    res_22 = func_22(TreeList)
    Print_TreeList(res_22)

    res_24 = func_24(TreeList)
    print("功能数量：", len(res_24))
    Print_TreeList(res_24)

    res_25 = func_25(TreeList)
    Print_TreeList(res_25)

    res_32 = func_32(TreeList)
    print(res_32)

    res_34 = func_34(TreeList)
    print(res_34)

    res_35 = func_35(TreeList)
    print(res_35)

    res_36 = func_36(TreeList)
    Print_TreeList(res_36)

    res_38 = func_38(TreeList)
    print(res_38)

    res_40 = func_40(TreeList)
    print(res_40)

    res_41 = func_41(TreeList)
    Print_TreeList(res_41)

    res_43 = func_43(TreeList)
    print(res_43)

    res_44 = func_44(TreeList)
    print(res_44)

    res_45 = func_45(TreeList)
    print(res_45)

    res_47 = func_47(TreeList)
    print(res_47)
    
    res_49 = func_49(TreeList)
    print(res_49)
    
    res_50 = func_50(TreeList)
    print(res_50)
    
    res_51 = func_51(TreeList)
    # print(res_51,"\n")
    print("平均故障通告时间：",res_51)

    
    res_52 = func_52(TreeList)
    print(res_52)
    
    res_58 = func_58(TreeList)
    print(res_58)
    
    res_60 = func_60(TreeList)
    print(res_60)
    
    res_61 = func_61(TreeList)
    print(res_61)
    
    res_62 = func_62(TreeList)
    print(res_62)

    res_63 = func_63(TreeList)
    print(res_63)
    
    res_64 = func_64(TreeList)
    print(res_64)
    
    res_65 = func_65(TreeList)
    Print_TreeList(res_65)

    res_66 = func_66(TreeList)
    print(res_66)