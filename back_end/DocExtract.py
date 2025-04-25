import calculateWord
import Ztao_E4
from Extract_16 import *
import CalculateWordXG
import Ztao_E42
# from graph_information_extraction import *


def generate_file(path):
    Filepath = path  # 获取docx文件路径
    (Folderpath, Filename) = os.path.split(Filepath)  # 分离文件夹路径和文件名.后缀
    # 为了后续copy文件改为zip并解压，删除已经存在的同名文件
    (souce_name, souce_suffix) = os.path.splitext(Filename)  # 分离文件名和后缀
    if souce_suffix != '.docx':
        exit('请选择docx文档')
    extract_path = Folderpath + '/' + souce_name + '_copy'
    zip_path = Folderpath + '/' + souce_name + '_copy.zip'
    Delete_Copy(extract_path, zip_path)  # 删除该路径下的文件
    print('docx文件路径:', Filepath)
    extract_path, zip_path, Folderpath, souce_name = Get_xmlmkdir(
        Filepath)  # 将docx的克隆文件解压成含xml文件夹
    TreeList = Parsing_xml(extract_path)  # 将xml字符串中的各结点信息存入列表中
    Print_TreeList(TreeList)  # 打印列表中各结点
    df = TreeList_to_df(TreeList)  # 将结点信息存入dataframe中
    to_excel_nomerger(df, Filepath)
    Output_to_txt(TreeList, Folderpath, souce_name)  # 生成txt文件


def get_None_25000():
    tmp = {
        'val': None,
        'sub': []
    }
    metrix_25000 = {'功能性': {'功能完备性': {'功能覆盖率': tmp}, '功能正确性': {'功能正确性': tmp},
                            '功能适合性': {'使用目标的功能适合性': tmp, '系统的功能适合性': tmp}},
                    '性能效率': {'时间特性': {'平均响应时间': tmp, '响应时间的充分性': tmp, '平均周转时间': tmp, '周转时间充分性': tmp,
                                      '平均吞吐量': tmp},
                             '资源利用性': {'处理器平均占用率': tmp, '内存平均占用率': tmp, 'I/O设备平均占用率': tmp, '带宽占用率': tmp},
                             '容量': {'事务处理容量': tmp, '用户访问量': tmp, '用户访问增长的充分性': tmp}},
                    '兼容性': {'共存性': {'与其他产品的共存性': tmp},
                            '互操作性': {'数据格式可交换性': tmp, '数据交换协议充分性': tmp, '外部接口充分性': tmp}},
                    '易用性': {'可辨识性': {'描述的完整性': tmp, '演示覆盖率': tmp, '入口点的自描述性': tmp},
                            '易学性': {'用户指导完整性': tmp, '输入字段的默认值': tmp, '差错信息的易理解性': tmp, '用户界面的自解释性': tmp},
                            '易操作性': {'操作一致性': tmp, '消息的明确性': tmp, '功能的易定制性': tmp, '用户界面的易定制性': tmp,
                                     '监视能力': tmp, '撤销操作能力': tmp, '信息分类的易理解性': tmp, '外观一致性': tmp,
                                     '输入设备的支持性': tmp},
                            '用户差错防御性': {'抵御误操作': tmp, '用户输入差错纠正率': tmp, '用户差错易恢复性': tmp},
                            '用户界面舒适性': {'用户界面外观舒适性': tmp}, '易访问性': {'特殊群体的易访问性': tmp, '支持的语种充分性': tmp}},
                    '可靠性': {'成熟性': {'故障修复率': tmp, '平均失效间隔时间(MTBF)': tmp, '周期失效率': tmp, '测试覆盖率': tmp},
                            '可用性': {'系统可用性': tmp, '平均宕机时间': tmp},
                            '容错性': {'避免失效率': tmp, '组件的冗余度': tmp, '平均故障通告时间': tmp},
                            '易恢复性': {'平均恢复时间': tmp, '数据备份完整性': tmp}},
                    '信息安全性': {'保密性': {'访问控制性': tmp, '数据加密正确性': tmp, '加密算法的强度': tmp},
                              '完整性': {'数据完整性': tmp, '内部数据抗讹误性': tmp, '缓冲区溢出防止率': 1},
                              '抗抵赖性': {'数字签名使用率': tmp}, '可核查性': {'用户审计跟踪的完整性': tmp, '系统日志保留满足度': tmp},
                              '真实性': {'鉴别机制的充分性': tmp, '鉴别规则的符合性': tmp}},
                    '维护性': {'模块化': {'组件间的耦合度': 1, '圈复杂度的充分性': tmp},
                            '可重用性': {'资产的可重用性': tmp, '编码规则符合性': tmp},
                            '易分析性': {'系统日志完整性': tmp, '诊断功能有效性': tmp, '诊断功能充分性': tmp},
                            '易修改性': {'修改的效率': tmp, '修改的正确性': tmp, '修改的能力': tmp},
                            '易测试性': {'测试功能的完整性': tmp, '测试独立性': tmp, '测试的重启动性': tmp}},
                    '可移植性': {'适应性': {'硬件环境的适应性': tmp, '系统软件环境的适应性': tmp, '运营环境的适应性': tmp},
                             '易安装性': {'安装的时间效率': tmp, '安装的灵活性': tmp},
                             '易替换性': {'使用相似性': tmp, '产品质量等价性': tmp, '功能的包容性': tmp,
                                      '数据复用/导入能力': tmp}}}
    return metrix_25000


def docextract(input):
    if input['cddocs']:
        pathlist = input['cddocs']
        for i in pathlist:
            i = i.replace("\\", "/")

        # 读取各csv文档，得到各文档信息列表（5个文档分别对应需求、执行、任务、用例、Bug文档）
        all_document_list = Ztao_E4.data_collation(pathlist)

        all_document_list = Ztao_E4.organizational_relation(
            all_document_list)  # 组织各文档之间的关联关系

        all_document_list = Ztao_E4.completion_relation(all_document_list)

        # 各文档列表
        require_document_list = all_document_list[0]
        execute_document_list = all_document_list[1]
        mission_document_list = all_document_list[2]
        use_case_document_list = all_document_list[3]
        bug_document_list = all_document_list[4]

        matrix25000 = Ztao_E4.caculate_all_metric(
            require_document_list, use_case_document_list, mission_document_list, bug_document_list)
        return matrix25000
    elif input['pdocs']:
        pathlist = input['pdocs']
        for i in pathlist:
            i = i.replace("\\", "/")
        all_document_list = Ztao_E42.read_xlsx(pathlist)
        matrix25000 = Ztao_E42.caculate_all_metric(all_document_list[0], all_document_list[1], [], all_document_list[2])
        return matrix25000
    else:

        pathlist = [0]*len(input['fileSelect'])
        # idx = path.rfind('/')
        # tmp = path[:idx]
        cflag = 0
        for file in input['fileSelect']:
            file["path"] = file["path"].replace("\\", "/")
            if "TMMi" in file['type']:
                cflag = 1
                if file['type'] == 'TMMi需求文档':
                    pathlist[0] = file['path']
                elif file['type'] == 'TMMi需求跟踪矩阵':
                    pathlist[1] = file['path']
                elif file['type'] == 'TMMi验收测试用例':
                    pathlist[2] = file['path']
                elif file['type'] == 'TMMi软件详细设计说明':
                    pathlist[3] = file['path']
                elif file['type'] == 'TMMi可靠性测试方案':
                    pathlist[4] = file['path']
                elif file['type'] == 'TMMi维护性测试方案':
                    pathlist[5] = file['path']
            else:
                if file['type'] == '需求文档':
                    # idx = file['path'].find('/')
                    pathlist[2] = file['path']
                elif file['type'] == '接口设计文档':
                    # idx = file['path'].find('/')
                    pathlist[4] = file['path']
                elif file['type'] == '测试说明文档':
                    # idx = file['path'].find('/')
                    pathlist[0] = file['path']
                elif file['type'] == '测试报告文档':
                    # idx = file['path'].find('/')
                    pathlist[1] = file['path']
                elif file['type'] == '维护文档':
                    # idx = file['path'].find('/')
                    pathlist[5] = file['path']
                elif file['type'] == '系统设计文档':
                    # idx = file['path'].find('/')
                    pathlist[6] = file['path']
                elif file['type'] == '用户手册':
                    # idx = file['path'].find('/')
                    pathlist[3] = file['path']
        # for path in pathlist:
        #     generate_file(path)
        if cflag == 1:
            matrix25000 = CalculateWordXG.get_all_metrix(pathlist)
        else:
            for path in pathlist:
                generate_file(path)
            matrix25000 = calculateWord.get_all_metrix(pathlist)
        return matrix25000


def UpdataMetrix(metrix, buffer_overflow, codeFileInfo, funcInfo, Component_redundancy, Standalone_components):
    '''
    将源码计算的指标加入到25010中
    :param metrix: 初始25010
    :param var_assess: 陈晨源码计算：CodeExtract-codeextract
    :param moduledata: 陈晨源码计算：CodeExtract-codeextract
    :param projectname: 项目名称
    :return:
    '''
    # 缓冲区溢出防止率，没问题
    try:
        p = 0
        i = 0
        for key in buffer_overflow.keys():
            p += buffer_overflow[key][0]
            i += buffer_overflow[key][1]
        val = [p, i]  # 0:经过边界值检查的访问数量 1:软件模块中带有用户输入的内存访问数量
        metrix["信息安全性"]["完整性"]["缓冲区溢出防止率"] = dict()
        metrix["信息安全性"]["完整性"]["缓冲区溢出防止率"]["val"] = val[0]/val[1]
        A_dict = {
            "id": "A",
            "source": "源码",
            "des": "在带有用户输入的内存访问中,经过边界值检查的访问数量",
            "val": val[0]
        }
        B_dict = {
            "id": "B",
            "source": "源码",
            "des": "软件模块中带有用户输入的内存访问数量",
            "val": val[1]
        }
        metrix["信息安全性"]["完整性"]["缓冲区溢出防止率"]["sub"] = [A_dict, B_dict]
    except:
        A_dict = {
            "id": "A",
            "source": "源码",
            "des": "在带有用户输入的内存访问中,经过边界值检查的访问数量",
            "val": None
        }
        B_dict = {
            "id": "B",
            "source": "源码",
            "des": "软件模块中带有用户输入的内存访问数量",
            "val": None
        }
        metrix["信息安全性"]["完整性"]["缓冲区溢出防止率"] = dict()
        metrix["信息安全性"]["完整性"]["缓冲区溢出防止率"]["val"] = None
        metrix["信息安全性"]["完整性"]["缓冲区溢出防止率"]["sub"] = [A_dict, B_dict]

    # 圈复杂度的充分性，没问题
    overmodule = 0
    module_num = 0
    print(metrix["维护性"]["模块化"]["圈复杂度的充分性"])
    headerType = (".h", ".H", ".hh", ".hpp", ".hxx")
    for file in codeFileInfo.keys():
        if file.endswith(headerType):
            module_num += 1
    try:
        cycleparm = int(metrix["维护性"]["模块化"]["圈复杂度的充分性"]['val'])
        for file in codeFileInfo.keys():
            if file.endswith(headerType):
                if codeFileInfo[file]['cyclComplexity'] > cycleparm:
                    overmodule += 1
        data_dict = dict()
        module_par = 1 - overmodule / module_num
        data_dict["val"] = module_par
        A_dict = {
            "id": "A",
            "source": "源码+需求文档",
            "des": "圈复杂度的得分超过规定阈值的软件模块数量",
            "val": overmodule
        }
        B_dict = {
            "id": "B",
            "source": "源码",
            "des": "已实现的软件模块数量",
            "val": module_num
        }
        data_dict['sub'] = [A_dict, B_dict]
        metrix["维护性"]["模块化"]["圈复杂度的充分性"] = data_dict
    except:
        data_dict = dict()
        data_dict['val'] = None
        A_dict = {
            "id": "A",
            "source": "源码+需求文档",
            "des": "圈复杂度的得分超过规定阈值的软件模块数量",
            "val": None
        }
        B_dict = {
            "id": "B",
            "source": "源码",
            "des": "已实现的软件模块数量",
            "val": module_num
        }
        data_dict['sub'] = [A_dict, B_dict]
        metrix["维护性"]["模块化"]["圈复杂度的充分性"] = data_dict

    # 编码规则符合性
    A = 0
    B_dict = {
        "id": "B",
        "source": "源码",
        "des": "已实现的软件模功数量",
        "val": None
    }

    try:
        for i in metrix["维护性"]['可重用性']['编码规则符合性']["sub"]:
            if i is None:
                continue
            if i['id'] == 'A':
                A = i['val']
            elif i['id'] == 'B':
                B_dict = i
        data_dict = dict()
        code_par = A / module_num
        A_dict = {
            "id": "A",
            "source": "源码",
            "des": "符合特定系统编码规则的软件模块数量",
            "val": A
        }
        B_dict = {
            "id": "B",
            "source": "源码",
            "des": "已实现的软件模功数量",
            "val": module_num
        }
        data_dict["val"] = code_par
        data_dict['sub'] = [A_dict, B_dict]
        metrix["维护性"]["可重用性"]["编码规则符合性"] = data_dict
    except:
        data_dict = dict()
        data_dict['val'] = None
        A_dict = {
            "id": "A",
            "source": "源码",
            "des": "符合特定系统编码规则的软件模块数量",
            "val": None
        }

        data_dict['sub'] = [A_dict, B_dict]
        metrix["维护性"]["可重用性"]["编码规则符合性"] = data_dict

    # 组件的冗余度
    A_dict = {
        "id": "A",
        "source": "源码",
        "des": "冗余安装系统组件的数量",
        "val": None
    }
    B_dict = {
        "id": "B",
        "source": "源码",
        "des": "系统组件数量",
        "val": None
    }
    metrix["可靠性"]["容错性"]['组件的冗余度'] = dict()
    metrix["可靠性"]["容错性"]['组件的冗余度']['val'] = None
    metrix["可靠性"]["容错性"]['组件的冗余度']['sub'] = [A_dict, B_dict]
    # 269-284行为测试代码
    A_dict = {
        "id": "A",
        "source": "源码",
        "des": "冗余安装系统组件的数量",
        "val": Component_redundancy[0]
    }
    B_dict = {
        "id": "B",
        "source": "源码",
        "des": "系统组件数量",
        "val": Component_redundancy[1]
    }
    metrix["可靠性"]["容错性"]['组件的冗余度'] = dict()

    # forder = path+"/Design_recovery/project/" + projectname
    # # forder = "flask_back_end/Design_recovery/project/" + projectname
    # file_path = forder + '/graphs/clustered_sdg.dot_GNwithoutcomp.dot'
    # redundant_comp, comp_list = get_Redundant_components(file_path, forder)
    # A_dict = {
    #     "id": "A",
    #     "source": "源码",
    #     "des": "冗余安装系统组件的数量",
    #     "val": len(redundant_comp)
    # }
    # B_dict = {
    #     "id": "B",
    #     "source": "源码",
    #     "des": "系统组件数量",
    #     "val": len(comp_list)
    # }
    # # self.matrix["可靠性"]["容错性"]['组件的冗余度'] = len(redundant_comp)/len(comp_list)
    metrix["可靠性"]["容错性"]['组件的冗余度']['val'] = 0 if Component_redundancy[1] == 0 else Component_redundancy[0]/Component_redundancy[1]
    metrix["可靠性"]["容错性"]['组件的冗余度']['sub'] = [A_dict, B_dict]

    # # 组件间的耦合度
    metrix['维护性']['模块化']['组件间的耦合度'] = dict()
    A_dict = {
        "id": "A",
        "source": "源码",
        "des": "所实现的对其他组件没有产生影响的组件数量",
        "val": Standalone_components[0]
    }
    B_dict = {
        "id": "B",
        "source": "源码",
        "des": "需要独立的组件数量",
        "val": Standalone_components[1]
    }
    metrix['维护性']['模块化']['组件间的耦合度']['val'] = None
    metrix['维护性']['模块化']['组件间的耦合度']['sub'] = [A_dict, B_dict]
    # 320-335行为测试代码
    # metrix['维护性']['模块化']['组件间的耦合度'] = dict()
    # A_dict = {
    #     "id": "A",
    #     "source": "源码",
    #     "des": "所实现的对其他组件没有产生影响的组件数量",
    #     "val": None
    # }
    # B_dict = {
    #     "id": "B",
    #     "source": "源码",
    #     "des": "需要独立的组件数量",
    #     "val": None
    # }
    # Standalone_components_list, comp_list = get_Standalone_components(
    #     file_path)
    # A_dict = {
    #     "id": "A",
    #     "source": "源码",
    #     "des": "所实现的对其他组件没有产生影响的组件数量",
    #     "val": len(Standalone_components_list)
    # }
    # B_dict = {
    #     "id": "B",
    #     "source": "源码",
    #     "des": "需要独立的组件数量",
    #     "val": len(comp_list)
    # }
    # # matrix['可维护性']['模块化']['组件间的耦合度'] = len(Standalone_components_list)/len(comp_list)
    metrix['维护性']['模块化']['组件间的耦合度']['val'] = 0 if Standalone_components[1] == 0 else Standalone_components[0]/Standalone_components[1]
    metrix['维护性']['模块化']['组件间的耦合度']['sub'] = [A_dict, B_dict]

    # # 资产的可重用性
    func_num = 0
    large_in_degree_num = 0
    for func, info in funcInfo.items():
        func_num += 1
        if len(info['fanIn']) > 1:
            large_in_degree_num += 1

    metrix['维护性']['可重用性']['资产的可重用性'] = dict()
    A_dict = {
        "id": "A",
        "source": "源码",
        "des": "为可重复使用而设计和实现的资产的数量",
        "val": large_in_degree_num
    }
    B_dict = {
        "id": "B",
        "source": "源码",
        "des": "系统中资产的数量",
        "val": func_num
    }
    metrix['维护性']['可重用性']['资产的可重用性']['val'] = large_in_degree_num/func_num
    metrix['维护性']['可重用性']['资产的可重用性']['sub'] = [A_dict, B_dict]
    # 369-384行为测试代码
    # metrix['维护性']['可重用性']['资产的可重用性'] = dict()
    # A_dict = {
    #     "id": "A",
    #     "source": "源码",
    #     "des": "为可重复使用而设计和实现的资产的数量",
    #     "val": None
    # }
    # B_dict = {
    #     "id": "B",
    #     "source": "源码",
    #     "des": "系统中资产的数量",
    #     "val": None
    # }
    # file_path = forder + '/graphs/PLCG.dot'
    # in_degree_1, asset_num = cal_Reusability_of_assets(file_path)
    # # self.matrix['可维护性']['可复用性']['资产的可重用性'] = len(in_degree_1)/asset_nu
    # metrix['维护性']['可重用性']['资产的可重用性']['val'] = len(in_degree_1)/asset_num
    # A_dict = {
    #     "id": "A",
    #     "source": "源码",
    #     "des": "为可重复使用而设计和实现的资产的数量",
    #     "val": len(in_degree_1)
    # }
    # B_dict = {
    #     "id": "B",
    #     "source": "源码",
    #     "des": "系统中资产的数量",
    #     "val": asset_num
    # }
    # metrix['维护性']['可重用性']['资产的可重用性']['sub'] = [A_dict, B_dict]

    return metrix
