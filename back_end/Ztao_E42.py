import os
import tkinter as tk
from tkinter import filedialog
import re
from csv import DictReader
from PincodeExtract_from_list import *
from pin_caculate_metric import *
from utils import get_file_encoding
import pandas as pd
import json


class Require_Node:  # 定义需求节点
    def __init__(self, id, require_name='', require_description='', owning_product='', owning_module='', owning_plan='',
                 source='', close_time='', acceptance_standard='', priority='', current_state='', phase='', category='', segmented_require='', document_name='', standard=''):
        # 下面为Node对象增加n个实例变量
        self.id = id  # 自己的ID
        self.require_name = require_name  # 软件需求或者研发需求名称
        self.require_description = require_description  # 软件需求或者研发需求描述
        self.owning_product = owning_product  # 所属产品
        self.owning_module = owning_module  # 所属模块
        self.owning_plan = owning_plan  # 所属计划
        self.source = source  # 来源
        self.acceptance_standard = acceptance_standard  # 验收标准
        self.priority = priority  # 优先级
        self.current_state = current_state  # 当前状态
        self.phase = phase  # 所处阶段
        self.category = category  # 类别
        self.close_time = close_time  # 关闭日期
        self.segmented_require = segmented_require  # 细分软件需求
        self.specific_require = False  # 是否是特定需求
        self.father_name = ""
        self.its_fathers = []  # 他的父亲有哪些
        self.its_sons = []  # 他的儿子有哪些
        self.associated_use_case_ID = []  # 关联用例ID
        self.associated_mission_ID = []  # 关联任务ID
        self.associated_execute_ID = []  # 关联执行ID
        self.associated_bug_ID = []  # 关联bugID
        self.document_name = document_name
        self.standard = standard

    def use_case_append(self, new_element):
        self.associated_use_case_ID.append(new_element)

    def mission_append(self, new_element):
        self.associated_mission_ID.append(new_element)

    def execute_append(self, new_element):
        self.associated_execute_ID.append(new_element)

    def bug_append(self, new_element):
        self.associated_bug_ID.append(new_element)


class Execute_Node:  # 定义执行节点
    def __init__(self, id, iteration_name='', owning_project='', iteration_state='', progress='', document_name=''):
        # 下面为Node对象增加n个实例变量
        self.id = id  # 自己的ID
        self.iteration_name = iteration_name  # 迭代名称
        self.owning_project = owning_project  # 所属项目
        self.iteration_state = iteration_state  # 迭代状态
        self.progress = progress  # 进度
        self.associated_use_case_ID = []  # 关联用例ID
        self.associated_mission_ID = []  # 关联任务ID
        self.associated_require_ID = []  # 关联需求ID
        self.associated_bug_ID = []  # 关联bugID
        self.document_name = document_name

    def use_case_append(self, new_element):
        self.associated_use_case_ID.append(new_element)

    def mission_append(self, new_element):
        self.associated_mission_ID.append(new_element)

    def require_append(self, new_element):
        self.associated_require_ID.append(new_element)

    def bug_append(self, new_element):
        self.associated_bug_ID.append(new_element)


class Mission_Node:  # 定义任务节点
    def __init__(self, id, mission_name='', mission_description='', mission_category='', owning_execute='',
                 owning_module='', associated_require='', associated_bug='', priority='', mission_state='', progress='',
                 initial_expectation='', total_consumption='', document_name=''):
        # 下面为Node对象增加n个实例变量
        self.id = id  # 自己的ID
        self.mission_name = mission_name  # 任务名称
        self.mission_description = mission_description  # 任务描述
        self.mission_category = mission_category  # 任务类型
        self.owning_execute = owning_execute  # 所属执行
        self.owning_module = owning_module  # 所属模块
        self.associated_require = associated_require  # 相关软件需求
        self.associated_bug = associated_bug  # 来源Bug
        self.priority = priority  # 优先级
        self.initial_expectation = initial_expectation  # 最初预计
        self.total_consumption = total_consumption  # 总计消耗
        self.mission_state = mission_state  # 任务状态
        self.progress = progress  # 进度
        self.associated_use_case_ID = []  # 关联用例ID
        self.associated_execute_ID = []  # 关联执行ID
        self.associated_require_ID = []  # 关联需求ID
        self.associated_bug_ID = []  # 关联bugID
        self.document_name = document_name

    def use_case_append(self, new_element):
        self.associated_use_case_ID.append(new_element)

    def execute_append(self, new_element):
        self.associated_execute_ID.append(new_element)

    def require_append(self, new_element):
        self.associated_require_ID.append(new_element)

    def bug_append(self, new_element):
        self.associated_bug_ID.append(new_element)


class Use_case_Node:  # 定义用例节点
    def __init__(self, id, use_case_name='', owning_product='', owning_module='', associated_require='',
                 actual_situation='', expect='', precondition='', key_word='', step='',
                 priority='', use_case_category='', use_case_state='', use_case_result='', document_name=''):
        # 下面为Node对象增加n个实例变量
        self.id = id  # 自己的ID
        self.use_case_name = use_case_name  # 用例标题
        self.owning_product = owning_product  # 所属产品
        self.owning_module = owning_module  # 所属模块
        self.associated_require = associated_require  # 相关软件需求
        self.expect = expect  # 预期
        self.actual_situation = actual_situation  # 实际情况
        self.priority = priority  # 优先级
        self.step = step  # 步骤
        self.precondition = precondition  # 前置条件
        self.key_word = key_word  # 关键词
        self.use_case_category = use_case_category  # 用例类型
        self.use_case_state = use_case_state  # 用例状态
        self.use_case_result = use_case_result  # 结果
        self.associated_execute_ID = []  # 关联执行ID
        self.associated_mission_ID = []  # 关联任务ID
        self.associated_require_ID = []  # 关联需求ID
        self.associated_bug_ID = []  # 关联bugID
        self.document_name = document_name

    def mission_append(self, new_element):
        self.associated_mission_ID.append(new_element)

    def execute_append(self, new_element):
        self.associated_execute_ID.append(new_element)

    def require_append(self, new_element):
        self.associated_require_ID.append(new_element)

    def bug_append(self, new_element):
        self.associated_bug_ID.append(new_element)


class Bug_Node:  # 定义bug节点
    def __init__(self, id, owning_product='', owning_module='', owning_project='', owning_execute='',
                 associated_require='', associated_mission='', associated_use_case='', bug_name='', priority='',
                 bug_state='', solution='', document_name='',
                 associated_execute_ID=[], associated_mission_ID=[], associated_require_ID=[],
                 associated_use_case_ID=[]):
        # 下面为Node对象增加n个实例变量
        self.id = id  # 自己的ID
        self.owning_product = owning_product  # 所属产品
        self.owning_module = owning_module  # 所属模块
        self.owning_project = owning_project  # 所属项目
        self.owning_execute = owning_execute  # 所属执行
        self.associated_require = associated_require  # 相关需求
        self.associated_mission = associated_mission  # 相关任务
        self.associated_use_case = associated_use_case  # 相关用例
        self.bug_name = bug_name  # bug标题
        self.priority = priority  # 优先级
        self.bug_state = bug_state  # bug状态
        self.solution = solution  # 解决方案
        self.associated_execute_ID = []  # 关联执行ID
        self.associated_mission_ID = []  # 关联任务ID
        self.associated_require_ID = []  # 关联需求ID
        self.associated_use_case_ID = []  # 关联用例ID
        self.document_name = document_name

    def mission_append(self, new_element):
        self.associated_mission_ID.append(new_element)

    def execute_append(self, new_element):
        self.associated_execute_ID.append(new_element)

    def require_append(self, new_element):
        self.associated_require_ID.append(new_element)

    def use_case_append(self, new_element):
        self.associated_use_case_ID.append(new_element)


"""
获取禅道导出的csv文件
"""


def Ztao_Get_Path_list():
    Path_list = []
    root = tk.Tk()
    root.withdraw()
    Filepath = filedialog.askopenfilenames()  # 获得选择好的文件
    if Filepath == '':
        exit()
    else:  # 获取文件路径
        for each_path in Filepath:
            each_path = each_path.replace("\\", "/")  # 路径字符串斜杠替换

            # 仅支持读取csv文件
            (Folderpath, Filename) = os.path.split(each_path)  # 分离文件夹路径和文件名.后缀
            (souce_name, souce_suffix) = os.path.splitext(Filename)  # 分离文件名和后缀
            # if souce_suffix != '.csv':
            #     exit('请选择禅道系统导出的.csv文件')

            Path_list.append(each_path)
    return Path_list


"""
csv文件转字典
"""


def csv_to_dict(filename):
    try:
        encoding = get_file_encoding(filename)
        with open(filename, 'r', encoding=encoding) as read_obj:
            dict_reader = DictReader(read_obj)
            list_of_dict = list(dict_reader)
            # result = json.dumps(list_of_dict, indent=2, ensure_ascii=False)  # json.dumps 序列化时默认使用的ascii编码，想输出真正的中文需要指定ensure_ascii=False
        return list_of_dict
    except IOError as err:
        print("I/O error({0})".format(err))


"""
将字典文件数据转入自建的对象列表中
"""


def data_collation(Path_list):
    # require_document_keys = ['描述', '验收标准', '优先级', '类别', '所属产品', '来源']  # 拥有这些key则被认为是《所有需求》
    # 工作项表
    require_document_keys = ['描述', '验收标准', '优先级', '需求类型', '所属产品', '来源']
    require_document_list = []
    # 测试用例
    # execute_document_keys = ['迭代名称', '所属项目', '迭代负责人', '迭代状态']  # 拥有这些key则被认为是《所有执行》
    execute_document_keys = ['标题', '模块', '维护人', '评审状态']
    execute_document_list = []
    # 测试用例
    # mission_document_keys = ['所属执行', '所属模块', '任务名称', '任务描述', '任务类型']  # 拥有这些key则被认为是《所有任务》
    mission_document_keys = ['编号', '模块', '标题', '步骤描述', '测试类型']
    mission_document_list = []
    # 测试用例
    # use_case_document_keys = ['用例标题', '步骤', '预期', '实际情况', '用例类型', '用例状态', '结果']   # 拥有这些key则被认为是《所有用例》
    use_case_document_keys = ['编号', '步骤描述', '预期结果', '实际结果', '测试类型', '评审状态', '步骤结果']
    use_case_document_list = []
    # bugs
    bug_document_keys = ['Bug编号', 'Bug标题', 'Bug类型', 'Bug状态']  # 拥有这些key则被认为是《所有bug》
    bug_document_list = []

    for each_path in Path_list:  # 遍历不同csv文档
        current_dict = csv_to_dict(each_path)

        # 根据key来判断文档种类
        key_list = []
        for key in current_dict[0].keys():
            key_list.append(key)

        # 文档表头相符则认为读取到相应文档
        # 1.所有需求（软件需求、研发需求）
        (nouse, tmp) = os.path.split(each_path)  # 分离文件夹路径和文件名.后缀
        (document_name, suffix) = os.path.splitext(tmp)  # 分离文件名和后缀
        if set(require_document_keys) <= set(key_list):
            print('读取到需求文档')
            for each_dict in current_dict:  # 遍历文档中的每一条
                Node = Require_Node(id=each_dict['编号'], require_description=each_dict['描述'],
                                    owning_product=None,
                                    owning_module=None, owning_plan=None,
                                    source=None, close_time=None,
                                    acceptance_standard=None, priority=None,
                                    current_state=each_dict['状态'], document_name=document_name,
                                    phase=None, category=each_dict['类别'])

                if set(['软件需求名称']) <= set(key_list):
                    Node.require_name = each_dict['软件需求名称']
                elif set(['研发需求名称']) <= set(key_list):
                    Node.require_name = each_dict['研发需求名称']

                if set(['细分软件需求']) <= set(key_list):
                    Node.segmented_require = each_dict['细分软件需求']
                elif set(['细分研发需求']) <= set(key_list):
                    Node.segmented_require = each_dict['细分研发需求']

                if Node.require_name is not None:  # 没有名称则认为该条不存在
                    require_document_list.append(Node)

            require_document_list = father_son_need_judgment(require_document_list)  # 进行父子需求判断

        # # 2.所有执行
        # if set(execute_document_keys) <= set(key_list):
        #     print('读取到执行文档')
        #     for each_dict in current_dict:  # 遍历文档中的每一条
        #         Node = Execute_Node(id=each_dict['迭代编号'], iteration_name=each_dict['迭代名称'],
        #                             owning_project=each_dict['所属项目'], document_name=document_name,
        #                             iteration_state=each_dict['迭代状态'], progress=each_dict['进度'])
        #         if Node.iteration_name is not None:  # 没有名称则认为该条不存在
        #             execute_document_list.append(Node)
        #     (nouse, tmp) = os.path.split(each_path)  # 分离文件夹路径和文件名.后缀
        #     (execute_document_name, suffix) = os.path.splitext(tmp)  # 分离文件名和后缀
        #
        # # 3.所有任务
        # if set(mission_document_keys) <= set(key_list):
        #     print('读取到任务文档')
        #     for each_dict in current_dict:  # 遍历文档中的每一条
        #         Node = Mission_Node(id=each_dict['编号'], mission_name=each_dict['任务名称'],
        #                             mission_description=each_dict['任务描述'], total_consumption=each_dict['总计消耗'],
        #                             initial_expectation=each_dict['最初预计'], document_name=document_name,
        #                             mission_category=each_dict['任务类型'], owning_execute=each_dict['所属执行'],
        #                             owning_module=each_dict['所属模块'], associated_require=each_dict['相关软件需求'],
        #                             associated_bug=each_dict['来源Bug'], priority=each_dict['优先级'],
        #                             mission_state=each_dict['任务状态'], progress=each_dict['进度'])
        #         if Node.mission_name is not None:  # 没有名称则认为该条不存在
        #             mission_document_list.append(Node)
        #     (nouse, tmp) = os.path.split(each_path)  # 分离文件夹路径和文件名.后缀
        #     (mission_document_name, suffix) = os.path.splitext(tmp)  # 分离文件名和后缀

        # 4.所有用例
        if set(use_case_document_keys) <= set(key_list):
            print('读取到用例文档')
            for each_dict in current_dict:  # 遍历文档中的每一条
                Node = Use_case_Node(id=each_dict['编号'], use_case_name=each_dict['标题'],
                                     owning_product=None, precondition=each_dict['前置条件'],
                                     owning_module=each_dict['模块'], key_word=each_dict['备注'],
                                     actual_situation=each_dict['实际结果'], expect=each_dict['预期结果'], step=None,
                                     priority=each_dict['优先级'], use_case_category=each_dict['测试类型'], document_name=document_name,
                                     use_case_state=None, use_case_result=each_dict['执行结果'])
                if set(['相关软件需求']) <= set(key_list):
                    Node.associated_require = each_dict['相关软件需求']
                elif set(['相关研发需求']) <= set(key_list):
                    Node.associated_require = each_dict['相关研发需求']
                if Node.use_case_name is not None:  # 没有名称则认为该条不存在
                    use_case_document_list.append(Node)
            (nouse, tmp) = os.path.split(each_path)  # 分离文件夹路径和文件名.后缀
            (use_case_document_name, suffix) = os.path.splitext(tmp)  # 分离文件名和后缀

        # 5.所有bug
        if set(bug_document_keys) <= set(key_list):
            print('读取到bug文档')
            for each_dict in current_dict:  # 遍历文档中的每一条
                Node = Bug_Node(id=each_dict['Bug编号'], owning_product=None,
                                owning_module=None, solution=None,
                                owning_project=None, owning_execute=None,
                                associated_require=each_dict['Bug标题'], associated_mission=None,
                                associated_use_case=None, bug_name=each_dict['Bug标题'], document_name=document_name,
                                priority=None, bug_state=each_dict['Bug状态'])
                if Node.bug_name is not None:  # 没有名称则认为该条不存在
                    bug_document_list.append(Node)
            (nouse, tmp) = os.path.split(each_path)  # 分离文件夹路径和文件名.后缀
            (bug_document_name, suffix) = os.path.splitext(tmp)  # 分离文件名和后缀

    all_document_list = [require_document_list, execute_document_list, mission_document_list, use_case_document_list, bug_document_list]
    return all_document_list


"""
根据需求格式判断是否为父需求或子需求
"""


def father_son_need_judgment(require_document_list):
    for node in require_document_list:
        # 先找父需求
        if node.segmented_require != '':
            node.its_sons = re.sub(r'\n', '', node.segmented_require)  # 去除\n
            node.its_sons = re.sub(' ', '', node.its_sons)  # 去除空格
            node.its_sons = re.split(r';', node.its_sons)  # 去除;
            # print(node.its_sons)
            for son_id in node.its_sons:  # 确定父需求后，找到其子需求
                for son_node in require_document_list:
                    if son_id == son_node.id:
                        son_node.its_fathers.append(node.id)
                        break

        # 判断是否是特定需求
        ret = re.match(r"\[.*\]", node.require_name)
        if ret and ret.group() == '[特定需求]':
            node.specific_require = True

    for node in require_document_list:
        if node.require_name != '':
            prefix = node.require_name[0]
        else:
            prefix = ''
        if prefix == '>' and node.its_fathers == []:  # 匹配到子需求
            node.its_fathers.append('此为未知父需求的子需求，需要导入产品需求列表')

    return require_document_list


"""
获取文字中包含的编号信息
"""


def extract_id(id_inxx):
    ret = re.search(r"\(#.*\)", id_inxx)
    if ret is None:
        ret = '0'
    else:
        ret = ret.group()[2:-1]  # 提取(#X)中的数字编号
    return ret


"""
梳理不同文档之间的关联关系
"""


def organizational_relation(all_document_list):
    require_document_list = all_document_list[0]
    execute_document_list = all_document_list[1]
    mission_document_list = all_document_list[2]
    use_case_document_list = all_document_list[3]
    bug_document_list = all_document_list[4]

    for bug_node in bug_document_list:
        # 基于bug文档梳理执行文档关联关系
        execute_id_inbug = bug_node.owning_execute
        # execute_id_inbug = extract_id(execute_id_inbug)
        execute_id_inbug = '23'
        for execute_node in execute_document_list:
            if execute_node.id == execute_id_inbug:  # 找到匹配编号
                if execute_node.id not in bug_node.associated_execute_ID:
                    bug_node.execute_append(execute_node.id)
                if bug_node.id not in execute_node.associated_bug_ID:
                    execute_node.bug_append(bug_node.id)

        # 基于bug文档梳理需求文档关联关系
        require_id_inbug = bug_node.associated_require
        require_id_inbug = extract_id(require_id_inbug)
        for require_node in require_document_list:
            if require_node.id == require_id_inbug:  # 找到匹配编号
                if require_node.id not in bug_node.associated_require_ID:
                    bug_node.require_append(require_node.id)
                if bug_node.id not in require_node.associated_bug_ID:
                    require_node.bug_append(bug_node.id)

        # 基于Bug文档梳理任务文档关系
        mission_id_inbug = bug_node.associated_mission
        # mission_id_inbug = extract_id(mission_id_inbug)
        mission_id_inbug = '23'
        for mission_node in mission_document_list:
            if mission_node.id == mission_id_inbug:  # 找到匹配编号
                if mission_node.id not in bug_node.associated_mission_ID:
                    bug_node.mission_append(mission_node.id)
                if bug_node.id not in mission_node.associated_bug_ID:
                    mission_node.bug_append(bug_node.id)

        # 基于Bug文档梳理用例文档关系
        use_case_id_inbug = bug_node.associated_use_case
        # use_case_id_inbug = extract_id(use_case_id_inbug)
        use_case_id_inbug = '23'

        for use_case_node in use_case_document_list:
            if use_case_node.id == use_case_id_inbug:  # 找到匹配编号
                if use_case_node.id not in bug_node.associated_use_case_ID:
                    bug_node.use_case_append(use_case_node.id)
                if bug_node.id not in use_case_node.associated_bug_ID:
                    use_case_node.bug_append(bug_node.id)

    for use_case_node in use_case_document_list:
        # 基于用例文档梳理需求文档关系
        require_id_inusecase = use_case_node.associated_require
        require_id_inusecase = extract_id(require_id_inusecase)
        for require_node in require_document_list:
            if require_node.id == require_id_inusecase:  # 找到匹配编号
                if require_node.id not in use_case_node.associated_require_ID:
                    use_case_node.require_append(require_node.id)
                if use_case_node.id not in require_node.associated_use_case_ID:
                    require_node.use_case_append(use_case_node.id)

    for mission_node in mission_document_list:
        # 基于任务文档梳理执行文档关系
        execute_id_inmission = mission_node.owning_execute
        execute_id_inmission = extract_id(execute_id_inmission)
        for execute_node in execute_document_list:
            if execute_node.id == execute_id_inmission:  # 找到匹配编号
                if execute_node.id not in mission_node.associated_execute_ID:
                    mission_node.execute_append(execute_node.id)
                if mission_node.id not in execute_node.associated_mission_ID:
                    execute_node.mission_append(mission_node.id)

        # 基于任务文档梳理需求文档关系
        require_id_inmission = mission_node.associated_require
        require_id_inmission = extract_id(require_id_inmission)
        for require_node in require_document_list:
            if require_node.id == require_id_inmission:
                if require_node.id not in mission_node.associated_require_ID:
                    mission_node.require_append(require_node.id)
                if mission_node.id not in require_node.associated_mission_ID:
                    require_node.mission_append(mission_node.id)

        # 基于任务文档梳理bug文档关系
        bug_id_inmission = mission_node.associated_bug
        bug_id_inmission = extract_id(bug_id_inmission)
        for bug_node in bug_document_list:
            if bug_node.id == bug_id_inmission:
                if bug_node.id not in mission_node.associated_bug_ID:
                    mission_node.bug_append(bug_node.id)
                if mission_node.id not in bug_node.associated_mission_ID:
                    bug_node.mission_append(mission_node.id)

    all_document_list = [require_document_list, execute_document_list, mission_document_list, use_case_document_list,
                         bug_document_list]

    return all_document_list


"""
补全需求和执行、执行和bug之间的关系
"""


def completion_relation(all_document_list):
    require_document_list = all_document_list[0]
    execute_document_list = all_document_list[1]
    mission_document_list = all_document_list[2]
    use_case_document_list = all_document_list[3]
    bug_document_list = all_document_list[4]

    # 补全 需求——执行
    for require_node in require_document_list:
        if require_node.associated_mission_ID:
            for mission_ID in require_node.associated_mission_ID:
                for mission_node in mission_document_list:
                    if mission_node.id == mission_ID:
                        if mission_node.associated_execute_ID:
                            for execute_ID in mission_node.associated_execute_ID:
                                if execute_ID not in require_node.associated_execute_ID:  # 将执行关联到需求中
                                    require_node.execute_append(execute_ID)
                                    # 相应的，需求也要关联到执行当中
                                    for execute_node in execute_document_list:
                                        if execute_node.id == execute_ID:
                                            if require_node.id not in execute_node.associated_require_ID:
                                                execute_node.require_append(require_node.id)

    # 补全 执行——bug
    for execute_node in execute_document_list:
        if execute_node.associated_mission_ID:
            for mission_ID in execute_node.associated_mission_ID:
                for mission_node in mission_document_list:
                    if mission_node.id == mission_ID:
                        if mission_node.associated_bug_ID:
                            for bug_ID in mission_node.associated_bug_ID:
                                if bug_ID not in execute_node.associated_bug_ID:  # 将bug关联到执行当中
                                    execute_node.bug_append(bug_ID)
                                    # 相应的，执行也要关联到bug当中
                                    for bug_node in bug_document_list:
                                        if bug_node.id == bug_ID:
                                            if execute_node.id not in bug_node.associated_execute_ID:
                                                bug_node.execute_append(execute_node.id)

    all_document_list = [require_document_list, execute_document_list, mission_document_list, use_case_document_list,
                         bug_document_list]

    return all_document_list


def caculate_all_metric(require_document_list, use_case_document_list, mission_document_list, bug_document_list):
    fcr1g = fcr1g_cd(require_document_list, use_case_document_list)
    fcp1g = fcp1g_cd(require_document_list)
    fap1g = fap1g_cd(require_document_list, use_case_document_list)
    fap2g = fap2g_cd(require_document_list, use_case_document_list)
    ptb1g = ptb1g_cd(require_document_list, use_case_document_list)  # 标准化为毫秒
    ptb2g = ptb2g_cd(require_document_list, use_case_document_list)
    ptb3g = ptb3g_cd(require_document_list, use_case_document_list)
    ptb4g = ptb4g_cd(require_document_list, use_case_document_list)
    ptb5g = ptb5g_cd(require_document_list, use_case_document_list)
    pru1g = pru1g_cd(require_document_list, use_case_document_list)
    pru2g = pru2g_cd(require_document_list, use_case_document_list)
    pru3g = pru3g_cd(require_document_list, use_case_document_list)
    pru4s = pru4s_cd(require_document_list, use_case_document_list)
    pca1g = pca1g_cd(require_document_list, use_case_document_list)
    pca2g = pca2g_cd(require_document_list, use_case_document_list)
    pca3s = pca3s_cd(require_document_list, use_case_document_list)
    cco1g = cco1g_cd(require_document_list, use_case_document_list)
    cin1g = cin1g_cd(require_document_list, use_case_document_list)
    cin2g = cin2g_cd(require_document_list, use_case_document_list)
    cin3s = cin3s_cd(require_document_list, use_case_document_list)
    uap1g = uap1g_cd(require_document_list, use_case_document_list)
    uap2s = uap2s_cd(require_document_list, use_case_document_list)
    uap3s = uap3s_cd(require_document_list, use_case_document_list)
    ule1g = ule1g_cd(require_document_list, use_case_document_list)
    ule2s = ule2s_cd(require_document_list, use_case_document_list)
    ule3s = ule3s_cd(require_document_list, use_case_document_list)
    ule4s = ule4s_cd(require_document_list, use_case_document_list)
    uop1g = uop1g_cd(require_document_list, use_case_document_list)
    uop2g = uop2g_cd(require_document_list, use_case_document_list)
    uop3s = uop3s_cd(require_document_list, use_case_document_list)
    uop4s = uop4s_cd(require_document_list, use_case_document_list)
    uop5s = uop5s_cd(require_document_list, use_case_document_list)
    uop6s = uop6s_cd(require_document_list, use_case_document_list)
    uop7s = uop7s_cd(require_document_list, use_case_document_list)
    uop8s = uop8s_cd(require_document_list, use_case_document_list)
    uop9s = uop9s_cd(require_document_list, use_case_document_list)
    uep1g = uep1g_cd(require_document_list, use_case_document_list)
    uep2s = uep2s_cd(require_document_list, use_case_document_list)
    uep3s = uep3s_cd(require_document_list, use_case_document_list)
    uin1s = uin1s_cd(require_document_list, use_case_document_list)
    uac1g = uac1g_cd(require_document_list, use_case_document_list)
    uac2s = uac2s_cd(require_document_list, use_case_document_list)
    rma1g = rma1g_cd(require_document_list, bug_document_list)
    rma2g = rma2g_cd(require_document_list, use_case_document_list)
    rma3g = rma3g_cd(require_document_list, use_case_document_list)
    rma4s = rma4s_cd(require_document_list, use_case_document_list)
    rav1g = rav1g_cd(require_document_list, use_case_document_list)
    rav2g = rav2g_cd(require_document_list, use_case_document_list)
    rft1g = rft1g_cd(require_document_list, use_case_document_list)
    rft2s = rft2s_cd()
    rft3s = rft3s_cd(require_document_list, use_case_document_list)
    rre1g = rre1g_cd(require_document_list, use_case_document_list)
    rre2s = rre2s_cd(require_document_list, use_case_document_list)
    sco1g = sco1g_cd(require_document_list, use_case_document_list)
    sco2g = sco2g_cd(require_document_list, use_case_document_list)
    sco3s = sco3s_cd(require_document_list, use_case_document_list)
    sin1g = sin1g_cd(require_document_list, use_case_document_list)
    sin2g = sin2g_cd(require_document_list, use_case_document_list)
    sin3s = sin3s_cd()
    sno1g = sno1g_cd(require_document_list, use_case_document_list)
    sac1g = sac1g_cd(require_document_list, use_case_document_list)
    sac2s = sac2s_cd(require_document_list, use_case_document_list)
    sau1g = sau1g_cd(require_document_list, use_case_document_list)
    sau2s = sau2s_cd(require_document_list, use_case_document_list)
    mmo1g = mmo1g_cd()
    mmo2s = mmo2s_cd(require_document_list)
    mre1g = mre1g_cd()
    mre2s = mre2s_cd(require_document_list, use_case_document_list)
    man1g = man1g_cd(require_document_list, use_case_document_list)
    man2s = man2s_cd(require_document_list, use_case_document_list)
    man3s = man3s_cd(require_document_list, use_case_document_list)
    mmd1g = mmd1g_cd(require_document_list, use_case_document_list)
    mmd2g = mmd2g_cd(require_document_list, use_case_document_list)
    mmd3s = mmd3s_cd(require_document_list)
    mte1g = mte1g_cd(require_document_list, use_case_document_list)
    mte2s = mte2s_cd(use_case_document_list)
    mte3s = mte3s_cd(use_case_document_list)
    pad1g = pad1g_cd(require_document_list, use_case_document_list)
    pad2g = pad2g_cd(require_document_list, use_case_document_list)
    pad3s = pad3s_cd(require_document_list, use_case_document_list)
    pin1g = pin1g_cd(require_document_list, use_case_document_list)
    pin2g = pin2g_cd(require_document_list, use_case_document_list)
    pre1g = pre1g_cd(require_document_list, use_case_document_list)
    pre2s = pre2s_cd(require_document_list, use_case_document_list)
    pre3s = pre3s_cd(require_document_list, use_case_document_list)
    pre4s = pre4s_cd(require_document_list, use_case_document_list)

    pass_dict = {}
    for i in use_case_document_list:
        if i.use_case_result.startswith('通过'):
            pass_dict[i.id] = [1, i.document_name]
        else:
            pass_dict[i.id] = [0, i.document_name]

    list1 = []
    list2 = []
    list3 = []
    list4 = []
    list5 = []
    list6 = []
    list7 = []
    list8 = []
    for r in require_document_list:
        if r.standard:
            if '功能' in r.category:
                list1.extend(r.associated_use_case_ID)
            elif '性能' in r.category:
                list2.extend(r.associated_use_case_ID)
            elif '兼容性' in r.category:
                list3.extend(r.associated_use_case_ID)
            elif '易用性' in r.category:
                list4.extend(r.associated_use_case_ID)
            elif '可靠性' in r.category:
                list5.extend(r.associated_use_case_ID)
            elif '安全性' in r.category:
                list6.extend(r.associated_use_case_ID)
            elif '可维护性' in r.category:
                list7.extend(r.associated_use_case_ID)
            elif '可移植性' in r.category:
                list8.extend(r.associated_use_case_ID)
    fcl1g = fcl1g_cd(list1, pass_dict, use_case_document_list)
    pcl1g = pcl1g_cd(list2, pass_dict, use_case_document_list)
    ccl1g = ccl1g_cd(list3, pass_dict, use_case_document_list)
    ucl1g = ucl1g_cd(list4, pass_dict, use_case_document_list)
    rcl1g = rcl1g_cd(list5, pass_dict, use_case_document_list)
    scl1g = scl1g_cd(list6, pass_dict, use_case_document_list)
    mcl1g = mcl1g_cd(list7, pass_dict, use_case_document_list)
    pcp1g = pcp1g_cd(list8, pass_dict, use_case_document_list)

    metrix_25000_cd = {'功能性': {'功能完备性': {'功能覆盖率': fcp1g}, '功能正确性': {'功能正确性': fcr1g},
                               '功能适合性': {'使用目标的功能适合性': fap1g, '系统的功能适合性': fap2g},
                               '功能性的依从性': {'功能性的依从性': fcl1g}},
                       '性能效率': {'时间特性': {'平均响应时间': ptb1g, '响应时间的充分性': ptb2g, '平均周转时间': ptb3g, '周转时间充分性': ptb4g,
                                         '平均吞吐量': ptb5g},
                                '资源利用性': {'处理器平均占用率': pru1g, '内存平均占用率': pru2g, 'I/O设备平均占用率': pru3g, '带宽占用率': pru4s},
                                '容量': {'事务处理容量': pca1g, '用户访问量': pca2g, '用户访问增长的充分性': pca3s},
                                '性能效率的依从性': {'性能效率的依从性': pcl1g}},
                       '兼容性': {'共存性': {'与其他产品的共存性': cco1g},
                               '互操作性': {'数据格式可交换性': cin1g, '数据交换协议充分性': cin2g, '外部接口充分性': cin3s},
                               '兼容性的依从性': {'兼容性的依从性': ccl1g}},
                       '易用性': {'可辨识性': {'描述的完整性': uap1g, '演示覆盖率': uap2s, '入口点的自描述性': uap3s},
                               '易学性': {'用户指导完整性': ule1g, '输入字段的默认值': ule2s, '差错信息的易理解性': ule3s, '用户界面的自解释性': ule4s},
                               '易操作性': {'操作一致性': uop1g, '消息的明确性': uop2g, '功能的易定制性': uop3s, '用户界面的易定制性': uop4s,
                                        '监视能力': uop5s, '撤销操作能力': uop6s, '信息分类的易理解性': uop7s, '外观一致性': uop8s,
                                        '输入设备的支持性': uop9s},
                               '用户差错防御性': {'抵御误操作': uep1g, '用户输入差错纠正率': uep2s, '用户差错易恢复性': uep3s},
                               '用户界面舒适性': {'用户界面外观舒适性': uin1s}, '易访问性': {'特殊群体的易访问性': uac1g, '支持的语种充分性': uac2s},
                               '易用性的依从性': {'易用性的依从性': ucl1g}},
                       '可靠性': {'成熟性': {'故障修复率': rma1g, '平均失效间隔时间(MTBF)': rma2g, '周期失效率': rma3g, '测试覆盖率': rma4s},
                               '可用性': {'系统可用性': rav1g, '平均宕机时间': rav2g},
                               '容错性': {'避免失效率': rft1g, '组件的冗余度': rft2s, '平均故障通告时间': rft3s},
                               '易恢复性': {'平均恢复时间': rre1g, '数据备份完整性': rre2s},
                               '可靠性的依从性': {'可靠性的依从性': rcl1g}},
                       '信息安全性': {'保密性': {'访问控制性': sco1g, '数据加密正确性': sco2g, '加密算法的强度': sco3s},
                                 '完整性': {'数据完整性': sin1g, '内部数据抗讹误性': sin2g, '缓冲区溢出防止率': sin3s},
                                 '抗抵赖性': {'数字签名使用率': sno1g}, '可核查性': {'用户审计跟踪的完整性': sac1g, '系统日志保留满足度': sac2s},
                                 '真实性': {'鉴别机制的充分性': sau1g, '鉴别规则的符合性': sau2s},
                                 '信息安全性的依从性': {'信息安全性的依从性': scl1g}},
                       '维护性': {'模块化': {'组件间的耦合度': mmo1g, '圈复杂度的充分性': mmo2s},
                               '可重用性': {'资产的可重用性': mre1g, '编码规则符合性': mre2s},
                               '易分析性': {'系统日志完整性': man1g, '诊断功能有效性': man2s, '诊断功能充分性': man3s},
                               '易修改性': {'修改的效率': mmd1g, '修改的正确性': mmd2g, '修改的能力': mmd3s},
                               '易测试性': {'测试功能的完整性': mte1g, '测试独立性': mte2s, '测试的重启动性': mte3s},
                               '维护性的依从性': {'维护性的依从性': mcl1g}},
                       '可移植性': {'适应性': {'硬件环境的适应性': pad1g, '系统软件环境的适应性': pad2g, '运营环境的适应性': pad3s},
                                '易安装性': {'安装的时间效率': pin1g, '安装的灵活性': pin2g},
                                '易替换性': {'使用相似性': pre1g, '产品质量等价性': pre2s, '功能的包容性': pre3s,
                                         '数据复用/导入能力': pre4s},
                                '可移植性的依从性': {'可移植性的依从性': pcp1g}}}

    # print(metrix_25000_cd)
    for key1 in metrix_25000_cd.keys():
        for key2 in metrix_25000_cd[key1].keys():
            for key3 in metrix_25000_cd[key1][key2].keys():
                tmp = []
                # print(key1, key2, key3)
                for sub in metrix_25000_cd[key1][key2][key3]["sub"]:
                    if sub is None:
                        tmp.append(None)
                        continue
                    try:
                        if sub["val"] is None:
                            tmp.append({
                                "id": sub["id"],
                                "type": sub["type"],
                                "source": sub["source"],
                                "des": sub["des"],
                                "val": 0.0
                            })

                        elif isinstance(sub["val"], list):
                            for i in range(len(sub["val"])):
                                tmp.append({
                                    "id": sub["id"]+str(i),
                                    "type": sub["type"],
                                    "source": sub["source"],
                                    "des": sub["des"],
                                    "val": float(sub["val"][i])
                                })
                        else:
                            tmp.append({
                                "id": sub["id"],
                                "type": sub["type"],
                                "source": sub["source"],
                                "des": sub["des"],
                                "val": float(sub["val"])
                            })
                    except:
                        pass
                metrix_25000_cd[key1][key2][key3]["sub"] = tmp

    return metrix_25000_cd


def read_xlsx(filelist):
    require_document_keys = ['描述', '优先级', '需求类型', '需求来源']
    require_document_list = []

    # 测试用例
    # use_case_document_keys = ['用例标题', '步骤', '预期', '实际情况', '用例类型', '用例状态', '结果']   # 拥有这些key则被认为是《所有用例》
    use_case_document_keys = ['编号', '步骤描述', '预期结果', '实际结果', '测试类型', '步骤结果']
    use_case_document_list = []

    bug_document_list = []

    bugid = 0
    for path in filelist:
        fp = pd.read_excel(
            io=path,
            sheet_name=0,
            keep_default_na=False  # 传入列表，指定Sheet索引
        )
        table = fp
        key_list = list(table)
        (nouse, tmp) = os.path.split(path)  # 分离文件夹路径和文件名.后缀
        (document_name, suffix) = os.path.splitext(tmp)  # 分离文件名和后缀
        if set(require_document_keys) <= set(key_list):
            print('读取到需求文档')
            son = {}
            for i in table.itertuples():
                if getattr(i, '工作项类型') == '需求':
                    status = None
                    if getattr(i, '完成时间'):
                        status = '已关闭'
                    Node = Require_Node(id=str(getattr(i, '编号')), require_description=getattr(i, '描述'),
                                        require_name=getattr(i, '标题'),
                                        owning_product=None,
                                        owning_module=None, owning_plan=None,
                                        source=None, close_time=None,
                                        acceptance_standard=None, priority=None,
                                        current_state=status, document_name=document_name, segmented_require=None,
                                        phase=None, category=getattr(i, '需求类型'), standard=getattr(i, '备注'))
                    if Node.require_name is not None:  # 没有名称则认为该条不存在
                        require_document_list.append(Node)
                    if getattr(i, '标题').startswith("[特定需求]"):
                        Node.specific_require = True
                    if getattr(i, '父工作项') != "":
                        if getattr(i, '父工作项') in son.keys():
                            son[getattr(i, '父工作项')].append(str(getattr(i, '编号')))
                        else:
                            son[getattr(i, '父工作项')] = [str(getattr(i, '编号'))]
                elif getattr(i, '工作项类型') == '缺陷':
                    Node = Bug_Node(id=str(bugid), owning_product=None,
                                    owning_module=None, solution=getattr(i, '状态'),
                                    owning_project=None, owning_execute=None,
                                    associated_require=getattr(i, '标题'), associated_mission=None,
                                    associated_use_case=None, bug_name=getattr(i, '标题'),
                                    document_name=document_name,
                                    priority=None, bug_state=None)
                    if Node.bug_name is not None:  # 没有名称则认为该条不存在
                        bug_document_list.append(Node)
            for item in require_document_list:
                if item.require_name in son.keys():
                    item.its_sons = son[item.require_name]
        elif set(use_case_document_keys) <= set(key_list):
            print('读取到用例文档')
            for i in table.itertuples():
                Node = Use_case_Node(id=str(getattr(i, '编号')), use_case_name=getattr(i, '标题'),
                                     associated_require=getattr(i, '标题'),
                                     owning_product=None, precondition=getattr(i, '前置条件'),
                                     owning_module=None, key_word=getattr(i, '备注'),
                                     actual_situation=getattr(i, '实际结果'), expect=getattr(i, '预期结果'), step=getattr(i, '步骤描述'),
                                     priority=None, use_case_category=None, document_name=document_name,
                                     use_case_state=None, use_case_result=getattr(i, '执行结果'))

                if Node.use_case_name is not None:  # 没有名称则认为该条不存在
                    use_case_document_list.append(Node)
            # (nouse, tmp) = os.path.split(each_path)  # 分离文件夹路径和文件名.后缀
            # (use_case_document_name, suffix) = os.path.splitext(tmp)  # 分离文件名和后缀

    for bug_node in bug_document_list:
        require_id_inbug = bug_node.associated_require
        # print(type(require_id_inbug),require_id_inbug, bug_node.bug_name)
        require_id_inbug = extract_id(require_id_inbug)
        for require_node in require_document_list:
            if require_node.id == require_id_inbug:  # 找到匹配编号
                if require_node.id not in bug_node.associated_require_ID:
                    bug_node.require_append(require_node.id)
                if bug_node.id not in require_node.associated_bug_ID:
                    require_node.bug_append(bug_node.id)

        # use_case_id_inbug = bug_node.associated_use_case
        # use_case_id_inbug = extract_id(use_case_id_inbug)
        # for use_case_node in use_case_document_list:
        #     if use_case_node.id == use_case_id_inbug:  # 找到匹配编号
        #         if use_case_node.id not in bug_node.associated_use_case_ID:
        #             bug_node.use_case_append(use_case_node.id)
        #         if bug_node.id not in use_case_node.associated_bug_ID:
        #             use_case_node.bug_append(bug_node.id)

    for use_case_node in use_case_document_list:
        # 基于用例文档梳理需求文档关系
        require_id_inusecase = use_case_node.associated_require
        require_id_inusecase = extract_id(require_id_inusecase)
        for require_node in require_document_list:
            if require_node.id == require_id_inusecase:  # 找到匹配编号
                if require_node.id not in use_case_node.associated_require_ID:
                    use_case_node.require_append(require_node.id)
                if use_case_node.id not in require_node.associated_use_case_ID:
                    require_node.use_case_append(use_case_node.id)

    all_document_list = [require_document_list, use_case_document_list, bug_document_list]
    return all_document_list


if __name__ == '__main__':
    Path_list = Ztao_Get_Path_list()  # 获取各csv文档路径
    all_document_list = read_xlsx(Path_list)
    metrix = caculate_all_metric(all_document_list[0], all_document_list[1], [], all_document_list[2])
    print(metrix)
    with open('./pincodemetrix.json', 'w', encoding="utf-8") as f:
        json.dump(metrix, f, indent=4, ensure_ascii=False)
    # print(all_document_list)

    # all_document_list = data_collation(Path_list)  # 读取各csv文档，得到各文档信息列表（5个文档分别对应需求、执行、任务、用例、Bug文档）
    #
    # all_document_list = organizational_relation(all_document_list)  # 组织各文档之间的关联关系
    #
    # all_document_list = completion_relation(all_document_list)
    #
    # # 各文档列表
    # require_document_list = all_document_list[0]
    # execute_document_list = all_document_list[1]
    # mission_document_list = all_document_list[2]
    # use_case_document_list = all_document_list[3]
    # bug_document_list = all_document_list[4]
    #
    # metrix = caculate_all_metric(require_document_list, use_case_document_list, mission_document_list, bug_document_list)
    # print('')
