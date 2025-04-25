from Extract2_14 import *

def func_29(TreeList):
    '''
    统计接口默认值-3.x
    :param TreeList:
    :return: 接口节点列表
    '''
    res = []
    root = TreeList[0]
    name_1 = "接口设计" #一级标题
    if name_1 in root.son_text:
        idx_1 = root.son_text.index(name_1)
        node_1 = TreeList[root.son_id[idx_1]]
        for id_2 in node_1.son_id:
            node_2 = TreeList[id_2]
            name_2 = "数据元素集合体特性"
            if name_2 in node_2.son_text:
                idx_2 = node_2.son_text.index(name_2)
                node_3 = TreeList[node_2.son_id[idx_2]]
                name_3 = "默认值"
                if name_3 in node_3.son_text:
                    res.append(node_2)

    return res

def func_33(TreeList):
    '''
    统计消息格式化-3.x
    :param TreeList:
    :return: 接口节点列表
    '''
    res = []
    root = TreeList[0]
    name_1 = "接口设计" #一级标题
    if name_1 in root.son_text:
        idx_1 = root.son_text.index(name_1)
        node_1 = TreeList[root.son_id[idx_1]]
        for id_2 in node_1.son_id:
            node_2 = TreeList[id_2]
            name_2 = "接口通信特性"
            if name_2 in node_2.son_text:
                idx_2 = node_2.son_text.index(name_2)
                node_3 = TreeList[node_2.son_id[idx_2]]
                name_3 = "消息格式化"
                if name_3 in node_3.son_text:
                    idx_3 = node_3.son_text.index(name_3)
                    t_id = node_3.son_id[idx_3]
                    node_4 = TreeList[t_id]
                    try:
                        table = TreeList[node_4.son_id[0]].table_info
                        if table:
                            for val in list(table.values())[1:]:
                                res.append(val)
                        else:
                            for id in node_4.son_id:
                                node_5 = TreeList[id]
                                if node_5.name != "Normal":
                                    res.append(node_5.text)
                    except:
                        pass
                        # print("33找不到表格")
    return res

def func_333(TreeList):
    '''
    统计消息格式化-3.x.x
    :param TreeList:
    :return: 接口节点列表
    '''
    res = []
    root = TreeList[0]
    name_1 = "接口设计" #一级标题
    if name_1 in root.son_text:
        idx_1 = root.son_text.index(name_1)
        node_1 = TreeList[root.son_id[idx_1]]
        for id_2 in node_1.son_id:
            node_2 = TreeList[id_2]
            name_2 = "接口通信特性"
            if name_2 in node_2.son_text:
                idx_2 = node_2.son_text.index(name_2)
                node_3 = TreeList[node_2.son_id[idx_2]]
                name_3 = "消息格式化"
                if name_3 in node_3.son_text:
                    idx_3 = node_3.son_text.index(name_3)
                    t_id = node_3.son_id[idx_3]
                    node_4 = TreeList[t_id]
                    try:
                        for id in node_4.son_id:
                            node_5 = TreeList[id]
                            if node_5.name != "Normal":
                                table = TreeList[node_5.son_id[0]].table_info
                                if table:
                                    for val in list(table.values())[1:]:
                                        res.append(val)

                    except:
                        print("333找不到表格")
    return res

def func_Interface1(TreeList):
    '''
    统计接口类型-3.x
    :param TreeList:
    :return: 接口节点列表
    '''
    res = []
    root = TreeList[0]
    name_1 = "接口设计" #一级标题
    if name_1 in root.son_text:
        idx_1 = root.son_text.index(name_1)
        node_1 = TreeList[root.son_id[idx_1]]
        for id_2 in node_1.son_id:
            node_2 = TreeList[id_2]
            name_2 = "类型"
            if name_2 in node_2.son_text:
                res.append(node_2)

    return res


def func_54(TreeList):
    '''
    统计访问控制-3.x
    :param TreeList:
    :return: 接口True、flase列表
    '''
    res = []
    root = TreeList[0]
    name_1 = "接口设计" #一级标题
    if name_1 in root.son_text:
        idx_1 = root.son_text.index(name_1)
        node_1 = TreeList[root.son_id[idx_1]]
        for id_2 in node_1.son_id:
            node_2 = TreeList[id_2]
            name_2 = "数据元素集合体特性"
            if name_2 in node_2.son_text:
                idx_2 = node_2.son_text.index(name_2)
                node_3 = TreeList[node_2.son_id[idx_2]]
                name_3 = "保密性和私密性"
                if name_3 in node_3.son_text:
                    idx_3 = node_3.son_text.index(name_3)
                    node_4 = TreeList[node_3.son_id[idx_3]]

                    # 匹配规则
                    try:
                        table = TreeList[node_4.son_id[0]].table_info
                        if table:
                            for val in list(table.values())[1:]:
                                if val[1]=="True":
                                    res.append(val[1])

                    except:
                        print("54匹配表格失败")

    return res

def func_56(TreeList):
    '''
    统计数据加密-3.x
    :param TreeList:
    :return: 接口true，false列表
    '''
    res = []
    root = TreeList[0]
    name_1 = "接口设计" #一级标题
    if name_1 in root.son_text:
        idx_1 = root.son_text.index(name_1)
        node_1 = TreeList[root.son_id[idx_1]]
        for id_2 in node_1.son_id:
            node_2 = TreeList[id_2]
            name_2 = "数据元素集合体特性"
            if name_2 in node_2.son_text:
                idx_2 = node_2.son_text.index(name_2)
                node_3 = TreeList[node_2.son_id[idx_2]]
                name_3 = "保密性和私密性"
                if name_3 in node_3.son_text:
                    idx_3 = node_3.son_text.index(name_3)
                    node_4 = TreeList[node_3.son_id[idx_3]]

                    # 匹配规则
                    try:
                        table = TreeList[node_4.son_id[0]].table_info
                        if table:
                            for val in list(table.values())[1:]:
                                if val[2]=="True":
                                    res.append(val[2])

                    except:
                        print("56匹配表格失败")

    return res

def func_ck1(TreeList):
    '''
    统计鉴别机制-3.x
    :param TreeList:
    :return: 鉴别机制列表
    '''
    res = []
    root = TreeList[0]
    name_1 = "接口设计" #一级标题
    if name_1 in root.son_text:
        idx_1 = root.son_text.index(name_1)
        node_1 = TreeList[root.son_id[idx_1]]
        for id_2 in node_1.son_id:
            node_2 = TreeList[id_2]
            name_2 = "接口通信特性"
            if name_2 in node_2.son_text:
                idx_2 = node_2.son_text.index(name_2)
                node_3 = TreeList[node_2.son_id[idx_2]]
                name_3 = "鉴别机制"
                if name_3 in node_3.son_text:
                    idx_3 = node_3.son_text.index(name_3)
                    t_id = node_3.son_id[idx_3]
                    node_4 = TreeList[t_id]
                    try:
                        table = TreeList[node_4.son_id[0]].table_info
                        if table:
                            for val in list(table.values())[1:]:
                                res.append(val)
                        else:
                            for id in node_4.son_id:
                                node_5 = TreeList[id]
                                if node_5.name != "Normal":
                                    res.append(node_5.text)
                    except:
                        print("找不到表格")
    return res

def func_ck2(TreeList):
    '''
    统计鉴别规则-3.x
    :param TreeList:
    :return: 鉴别规则列表
    '''
    res = []
    root = TreeList[0]
    name_1 = "接口设计" #一级标题
    if name_1 in root.son_text:
        idx_1 = root.son_text.index(name_1)
        node_1 = TreeList[root.son_id[idx_1]]
        for id_2 in node_1.son_id:
            node_2 = TreeList[id_2]
            name_2 = "接口通信特性"
            if name_2 in node_2.son_text:
                idx_2 = node_2.son_text.index(name_2)
                node_3 = TreeList[node_2.son_id[idx_2]]
                name_3 = "鉴别规则"
                if name_3 in node_3.son_text:
                    idx_3 = node_3.son_text.index(name_3)
                    t_id = node_3.son_id[idx_3]
                    node_4 = TreeList[t_id]
                    try:
                        table = TreeList[node_4.son_id[0]].table_info
                        if table:
                            for val in list(table.values())[1:]:
                                res.append(val)
                        else:
                            for id in node_4.son_id:
                                node_5 = TreeList[id]
                                if node_5.name != "Normal":
                                    res.append(node_5.text)
                    except:
                        print("找不到表格")
    return res


if __name__ == '__main__':
    Filepath = Get_filepath()  # 获取docx文件路径
    extract_path, zip_path, Folderpath, souce_name = Get_xmlmkdir(Filepath)  # 将docx的克隆文件解压成含xml文件夹
    Tag_order = get_order(extract_path)
    TreeList = Parsing_docx(Tag_order, Filepath, extract_path)
    # Print_TreeList(TreeList)  # 打印树节点信息
    # Output_to_txt(TreeList, Folderpath, souce_name)  # 存入txt
    # Structural_network(TreeList)  # 生成图
    
    res_29 = func_29(TreeList)
    print("29")
    Print_TreeList(res_29)
    
    res_33 = func_33(TreeList)
    print("33")
    Print_TreeList(res_33)
    
    res_x1 = func_Interface1(TreeList)
    print("x1")
    Print_TreeList(res_x1)
    
    res_54 = func_54(TreeList)
    print("54")
    Print_TreeList(res_54)
    