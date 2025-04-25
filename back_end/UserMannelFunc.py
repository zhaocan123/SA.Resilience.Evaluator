from Extract2_14 import *

def func_23(TreeList):
    '''
    统计与第五章相同章节数-x
    :param TreeList:
    :return: 第五章相同章节节点列表
    '''
    requirement_list = []
    root = TreeList[0]
    checklist = ["能力","约定","处理过程","数据备份","相关处理","错误,故障和紧急情况时的恢复","消息","快速引用指南"]
    for id_1 in root.son_id:
        node_1 = TreeList[id_1]
        for c in checklist:
            if c in node_1.son_text:
                requirement_list.append(node_1)
                break

    return requirement_list


def func_28(TreeList):
    '''
    统计与第五章相同章节数-5.3.x
    :param TreeList:
    :return: 第五章相同章节5.3节点列表
    '''
    res = []
    temp = func_23(TreeList)
    for node in temp:
        name = "处理过程"
        if name in node.son_text:
            idx = node.son_text.index(name)
            node_2 = TreeList[node.son_id[idx]]
            res.append(node_2)

    return res


def func_31(TreeList):
    '''
    统计与第五章相同章节数下步骤数量5.3.x
    :param TreeList:
    :return: 第五章相同章节5.3.x节点列表
    '''
    res = []
    temp = func_28(TreeList)
    for node in temp:
        for id in node.son_id:
            if TreeList[id].name != "Normal":
                res.append(TreeList[id])
     
    return res


def func_39(TreeList):
    '''
    统计与第五章相同章节数包含键盘、鼠标、语音-x
    :param TreeList:
    :return: 第五章相同章节包含键盘、鼠标、语音节点列表
    '''
    res = []
    temp = func_23(TreeList)
    content = ["键盘","鼠标","语音"]
    for node in temp:
        if check_text(node,content, TreeList):
            res.append(node)
    
    return res

def check_text(node, content, TreeList):
    for i in content:
        if i in node.text:
            return True
        else:
            for id in node.son_id:
                son = TreeList[id]
                if check_text(son, content, TreeList):
                    return True

    return False


def func_u1(TreeList):
    '''
    统计与第五章相同章节数包含差错数量-5.6
    :param TreeList:
    :return: 第五章相同章节包含差错数量节点列表
    '''
    res = []
    temp = func_23(TreeList)
    for node in temp:
        name = "错误,故障和紧急情况时的恢复"
        if name in node.son_text:
            idx = node.son_text.index(name)
            node_2 = TreeList[node.son_id[idx]]

            for id_2 in node_2.son_id:
                node_3 = TreeList[id_2]
                if node_3.name != "Normal":
                    res.append(node_3)

    return res


# def func_u1(TreeList):
#     '''
#     统计与第五章相同章节5.8中对特殊群体支持- 5.8.x
#     :param TreeList:
#     :return: 第五章相同章节包含差特殊群体表格列表
#     '''
#     res = []
#     temp = func_23(TreeList)
#     for node in temp:
#         name = "错误,故障和紧急情况时的恢复"
#         if name in node.son_text:
#             idx = node.son_text.index(name)
#             node_2 = TreeList[node.son_id[idx]]
#             print(node_2.son_text)
#
#             for id_2 in node_2.son_id:
#                 node_3 = TreeList[id_2]
#                 if node_3.name != "Normal":
#                     res.append(node_3)
#
#     return res

def func_x1(TreeList):
    '''
    统计与第五章相同章节5.8中对特殊群体支持- 5.8.x
    :param TreeList:
    :return: 第五章相同章节包含差特殊群体表格列表
    '''
    res = []
    temp = func_23(TreeList)
    for node in temp:
        name = "快速引用指南"
        if name in node.son_text:
            idx = node.son_text.index(name)
            node_2 = TreeList[node.son_id[idx]]
            name_2 = "特殊群体支持"
            if name_2 in node_2.son_text:
                idx_2 = node_2.son_text.index(name_2)
                node_3 = TreeList[node_2.son_id[idx_2]]
                # 匹配规则
                try:
                    table = TreeList[node_3.son_id[0]].table_info
                    if table:
                        for val in list(table.values())[1:]:
                            res.append(val)
                    else:
                        for id in node_3.son_id:
                            node_4 = TreeList[id]
                            if node_4.name != "Normal":
                                res.append(node_4.text)

                except:
                    print("x1匹配表格失败")


    return res


def func_42(TreeList):
    '''
    统计系统概述语言种类- 1.2.x
    :param TreeList:
    :return: 系统概述语言种类表格列表
    '''
    res = []
    root = TreeList[0]
    name_1 = "引言"
    if name_1 in root.son_text:
        idx_1 = root.son_text.index(name_1)
        node_1 = TreeList[root.son_id[idx_1]]
        name_2 = "系统概述"
        if name_2 in node_1.son_text:
            idx_2 = node_1.son_text.index(name_2)
            node_2 = TreeList[node_1.son_id[idx_2]]
            name_3 = "语言种类"
            if name_3 in node_2.son_text:
                idx_3 = node_2.son_text.index(name_3)
                node_3 = TreeList[node_2.son_id[idx_3]]
                # 匹配规则
                try:
                    table = TreeList[node_3.son_id[0]].table_info
                    if table:
                        for val in list(table.values())[1:]:
                            res.append(val)

                except:
                    print("42匹配表格失败")


    return res

def func_53(TreeList):
    '''
    统计与第五章相同章节数包含数据备份数量-5.5.x
    :param TreeList:
    :return: 第五章相同章节包含数据备份数量节点列表
    '''
    res = []
    temp = func_23(TreeList)
    for node in temp:
        name = "数据备份"
        if name in node.son_text:
            idx = node.son_text.index(name)
            node_2 = TreeList[node.son_id[idx]]

            for id_2 in node_2.son_id:
                node_3 = TreeList[id_2]
                if node_3.name != "Normal":
                    res.append(node_3)

    return res


def func_67(TreeList):
    '''
    统计与第五章相同章节消息中诊断消息- 5.7.x
    :param TreeList:
    :return: 第五章相同章节包含息中诊断消息表格列表
    '''
    res = []
    temp = func_23(TreeList)
    for node in temp:
        name = "消息"
        if name in node.son_text:
            idx = node.son_text.index(name)
            node_2 = TreeList[node.son_id[idx]]
            name_2 = "诊断消息"
            if name_2 in node_2.son_text:
                idx_2 = node_2.son_text.index(name_2)
                node_3 = TreeList[node_2.son_id[idx_2]]
                # 匹配规则
                try:
                    table = TreeList[node_3.son_id[0]].table_info
                    if table:
                        for val in list(table.values())[1:]:
                            res.append(val)
                    else:
                        for id in node_3.son_id:
                            node_4 = TreeList[id]
                            if node_4.name != "Normal":
                                res.append(node_4.text)

                except:
                    print("67匹配表格失败")


    return res


def func_74(TreeList):
    '''
    ？？？
    系统预期安装时间-3.4.b
    :param TreeList:
    :return: 系统预期安装时间字符串
    '''
    ave_time = 0
    root = TreeList[0]
    name_1 = "软件综述" #一级标题

    if name_1 in root.son_text:
        idx_1 = root.son_text.index(name_1)
        temp_id = root.son_id[idx_1]
        node = TreeList[temp_id]
        name_2 = "软件组织和操作概述"  #??空格
        if name_2 in node.son_text:
            idx_2 = node.son_text.index(name_2)
            temp_id = node.son_id[idx_2]
            node_2 = TreeList[temp_id]
            name_3 = "用户期望的性能特性"
            if name_3 in node_2.son_text:
                idx_3 = node_2.son_text.index(name_3)
                t_id = node_2.son_id[idx_3]
                node_3 = TreeList[t_id]
                name_4 = "预期安装时间"
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
                        print("74匹配平均失效间隔失败")

                else:
                    print("74找不到四级标题", node_3.son_text)
            else:
                print("74找不到三级标题")
        else:
            print("74找不到二级标题", node.son_text)

    else:
        print("74找不到一级标题")

    return ave_time




def func_75(TreeList):
    '''
    统计操作步骤数量-4.1.3.x
    :param TreeList:
    :return: 操作步骤数量节点列表
    '''
    res = []
    root = TreeList[0]
    name_1 = "访问软件" #一级标题

    if name_1 in root.son_text:
        idx_1 = root.son_text.index(name_1)
        temp_id = root.son_id[idx_1]
        node = TreeList[temp_id]
        name_2 = "软件的首次用户"  #??空格
        if name_2 in node.son_text:
            idx_2 = node.son_text.index(name_2)
            temp_id = node.son_id[idx_2]
            node_2 = TreeList[temp_id]
            name_3 = "安装和设置"
            if name_3 in node_2.son_text:
                idx_3 = node_2.son_text.index(name_3)
                t_id = node_2.son_id[idx_3]
                node_3 = TreeList[t_id]
                for id in node_3.son_id:
                    res.append(
                        TreeList[id]
                    )

            else:
                print("75找不到三级标题")
        else:
            print("75找不到二级标题", node.son_text)

    else:
        print("75找不到一级标题")

    return res




if __name__ == '__main__':
    Filepath = Get_filepath()  # 获取docx文件路径
    extract_path, zip_path, Folderpath, souce_name = Get_xmlmkdir(Filepath)  # 将docx的克隆文件解压成含xml文件夹
    Tag_order = get_order(extract_path)
    TreeList = Parsing_docx(Tag_order, Filepath, extract_path)
    # Print_TreeList(TreeList)  # 打印树节点信息
    # Output_to_txt(TreeList, Folderpath, souce_name)  # 存入txt
    # Structural_network(TreeList)  # 生成图

    res_23 = func_23(TreeList)
    print(23)
    Print_TreeList(res_23)
    
    res_28 = func_28(TreeList)
    print(28)
    Print_TreeList(res_28)
    
    res_31 = func_31(TreeList)
    print(31)
    Print_TreeList(res_31)
        
    res_39 = func_39(TreeList)
    print(39)
    Print_TreeList(res_39)
    
    res_u1 = func_u1(TreeList)
    print("u1")
    Print_TreeList(res_u1)
    
    res_x1 = func_x1(TreeList)
    print("x1")
    print(res_x1)
    
    res_42 = func_42(TreeList)
    print("42")
    print(res_42)
        
    res_53 = func_53(TreeList)
    print("53")
    Print_TreeList(res_53)
        
    res_67 = func_67(TreeList)
    print("67")
    print(res_67)