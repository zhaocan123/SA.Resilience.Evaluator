import re
from copy import deepcopy


# 检查列表中是否全为数字，并且转为float
def template_whether_not_str(list):
    num_list = []
    if list:
        for num in list:
            if is_number(num):
                num_list.append(float(num))
            else:
                return []
    return num_list


# 提取 我希望***， 中间的字符串
def template_what_i_hope(S):
    ret = re.findall(r"，我(.+?)，", S)
    result = ''
    if ret:
        result = ret[0]
    return result


def fcr1g_cd_A(require_document_list, use_case_document_list):
    current_document_name = ''
    if require_document_list and use_case_document_list:
        current_document_name = use_case_document_list[0].document_name
        count = 0
        for require_node in require_document_list:
            if require_node.category == '功能' and require_node.associated_use_case_ID:
                isfailure = False
                for use_case_ID in require_node.associated_use_case_ID:
                    for use_case_node in use_case_document_list:
                        if use_case_node.id == use_case_ID:
                            if use_case_node.use_case_result != '通过' or use_case_node.associated_bug_ID != []:
                                isfailure = True
                                break
                if isfailure:
                    count = count + 1
    else:
        count = None
    if current_document_name != '':
        current_document_name = current_document_name + '/结果/失败'
    sub = {
        'id':'A',
        'type':'需求文档',
        'source':current_document_name,
        'des':'功能不正确的数量',
        'val':count
    }
    return sub


def fcr1g_cd_B(require_document_list):
    current_document_name = ''
    if require_document_list:
        current_document_name = require_document_list[0].document_name
        count = 0
        for node in require_document_list:
            if node.category == '功能':
                count = count + 1
    else:
        count = None
    if current_document_name != '':
        current_document_name = current_document_name + '/类别/功能'
    sub = {
        'id': 'B',
        'type': '需求文档',
        'source': current_document_name,
        'des': '考虑的功能数量',
        'val': count
    }
    return sub


def fcp1g_cd_B(require_document_list):
    current_document_name = ''
    if require_document_list:
        current_document_name = require_document_list[0].document_name
        count = 0
        for require_node in require_document_list:
            if require_node.category == '功能' and require_node.its_fathers == []:
                count = count + 1
    else:
        count = None
    if current_document_name != '':
        current_document_name = current_document_name + '/类别/功能'
    sub = {
        'id': 'B',
        'type': '需求文档',
        'source': current_document_name,
        'des': '指定的功能数量',
        'val': count
    }
    return sub


def fcp1g_cd_A(require_document_list):
    current_document_name = ''
    if require_document_list:
        current_document_name = require_document_list[0].document_name
        count = 0
        for require_node in require_document_list:
            if require_node.category == '功能' and require_node.its_fathers == [] and require_node.current_state != '已关闭':
                count = count + 1
    else:
        count = None
    if current_document_name != '':
        current_document_name = current_document_name + '/当前状态/已关闭'
    sub = {
        'id': 'A',
        'type': '需求文档',
        'source': current_document_name,
        'des': '缺少的功能数量',
        'val': count
    }
    return sub


def fap1g_cd_B(require_document_list):
    current_document_name = ''
    if require_document_list:
        current_document_name = require_document_list[0].document_name
        all_specific_require = []
        for require_node in require_document_list:
            if require_node.category == '功能' and require_node.specific_require:
                if require_node.its_sons:
                    all_specific_require.append(str(len(require_node.its_sons)))
                else:
                    all_specific_require.append('1')
    else:
        all_specific_require = None
    if current_document_name != '':
        current_document_name = current_document_name + '/类别/功能'
    sub = {
        'id': 'B',
        'type': '需求文档',
        'source': current_document_name,
        'des': '为实现特定使用目标所需的功能数量',
        'val': all_specific_require
    }
    return sub


def fap1g_cd_A(require_document_list, use_case_document_list):
    current_document_name = ''
    if require_document_list and use_case_document_list:
        current_document_name = require_document_list[0].document_name
        bad_specific_require = []
        for require_node in require_document_list:
            if require_node.category == '功能' and require_node.specific_require:
                count = 0
                if require_node.its_sons:  # 如果有子需求
                    for son_require_ID in require_node.its_sons:
                        for require_node in require_document_list:
                            if require_node.id == son_require_ID:
                                if require_node.current_state != '已关闭':
                                    count = count + 1
                                elif require_node.current_state == '已关闭' and require_node.associated_use_case_ID:
                                    isfailure = False
                                    for use_case_ID in require_node.associated_use_case_ID:
                                        for use_case_node in use_case_document_list:
                                            if use_case_node.id == use_case_ID and use_case_node.use_case_result == '失败':
                                                isfailure = True
                                                break
                                    if isfailure:
                                        count = count + 1
                else:  # 没有子需求
                    if require_node.current_state != '已关闭':
                        count = count + 1
                    elif require_node.current_state == '已关闭' and require_node.associated_use_case_ID:
                        isfailure = False
                        for use_case_ID in require_node.associated_use_case_ID:
                            for use_case_node in use_case_document_list:
                                if use_case_node.id == use_case_ID and use_case_node.use_case_result == '失败':
                                    isfailure = True
                                    break
                        if isfailure:
                            count = count + 1
                bad_specific_require.append(str(count))
    else:
        bad_specific_require = None
    if current_document_name != '':
        current_document_name = current_document_name + '/类别/功能'
    sub = {
        'id': 'A',
        'type': '需求文档',
        'source': current_document_name,
        'des': '为实现特定使用目标所需的功能中缺少或不正确功能的数量',
        'val': bad_specific_require
    }
    return sub


def ptb1g_cd_Ai(require_document_list, use_case_document_list):
    current_document_name = ''
    current_des = ''
    all_response_time_list = []
    current_id_list = []
    for require_node in require_document_list:
        current_document_name = use_case_document_list[0].document_name
        if require_node.category == '性能' and require_node.require_description.find('响应时间') != -1:
            current_des = template_what_i_hope(require_node.require_description)
            if require_node.associated_use_case_ID:
                for use_case_ID in require_node.associated_use_case_ID:
                    for use_case_node in use_case_document_list:
                        if use_case_node.id == use_case_ID:
                            actual_situation = re.split(r'\n', use_case_node.actual_situation)  # 去除\n
                            for each_situation in actual_situation:
                                each_situation = re.sub('\d+\.', '', each_situation)  # 去除前面的编号
                                response_time_list_ms = re.findall(r"\d+ms|\d+毫秒", each_situation)  # 提取毫秒
                                response_time_list_s = re.findall(r"\d+s|\d+秒", each_situation)  # 提取秒
                                # 统一标准化为毫秒
                                if response_time_list_ms:
                                    for each_ms in response_time_list_ms:
                                        ret = re.match(r"\d+", each_ms)
                                        ms_time = float(ret.group())
                                    all_response_time_list.append(ms_time)
                                    current_id_list.append(use_case_node.id)
                                    break
                                if response_time_list_s:
                                    for each_s in response_time_list_s:
                                        ret = re.match(r"\d+", each_s)
                                        s_time = float(ret.group())
                                    all_response_time_list.append(s_time * 1000)
                                    current_id_list.append(use_case_node.id)
                                    break
    all_response_time_list = template_whether_not_str(all_response_time_list)

    current_document_name_list = []
    if current_document_name != '':
        for current_id in current_id_list:
            current_document_name_list.append(current_document_name + '/编号/' + current_id)
    Ai = []
    for i, current_document_name in enumerate(current_document_name_list):
        Ai.append(
            {
                'id': 'A' + str(i),
                'type': '用例文档',
                'source': current_document_name,
                'des': '第i次测量时系统响应一个特定用户任务或系统任务花费的时间',
                'val': all_response_time_list[i]
            }
        )
    return Ai


def get_threshold(s):
    template = 0
    ret = []
    if s.find('小于') != -1:
        ret = re.findall(r"小于(.+)，这样可以", s)  # 贪婪
        template = 1  # 匹配模板1
    elif s.find('大于') != -1:
        ret = re.findall(r"大于(.+)，这样可以", s)  # 贪婪
        template = 2  # 匹配模板2
    elif s.find('之间') != -1:
        ret = re.findall(r"在(.+)和(.+)之间，这样可以", s)  # 贪婪
        template = 3  # 匹配模板2
    threshold = ret
    threshold_float = []
    for each_num in threshold:
        num = re.match(r"\d+.\d+|\d+", each_num)
        num = num.group()
        num = float(num)
        if each_num.find('s') != -1 or each_num.find('秒') != -1:
            num = num * 1000
        elif each_num.find('h') != -1 or each_num.find('时') != -1 or each_num.find('小时') != -1:
            num = num * 1000 * 3600
        elif each_num.find('d') != -1 or each_num.find('天') != -1:
            num = num * 1000 * 3600 * 24
        elif each_num.find('分钟') != -1:
            num = num * 1000 * 60
        threshold_float.append(num)
    return threshold_float, template


# 提取需求描述中的阈值
def template_threshold_etc(require_document_list, category_input, description_kind):
    current_document_name = ''
    current_id = ''
    current_des = ''
    if require_document_list:
        current_document_name = require_document_list[0].document_name
        threshold = []  # 阈值
        template = 0  # 匹配到的模板
        development_value = ''
        for require_node in require_document_list:
            if require_node.category == category_input and require_node.require_description.find(
                    description_kind) != -1:
                current_id = require_node.id
                current_des = template_what_i_hope(require_node.require_description)
                threshold, template = get_threshold(require_node.require_description)
                development_value = re.findall(r"这样可以(.+)。", require_node.require_description)
                break
    else:
        threshold = None
        template = 0
        development_value = None
    if current_document_name != '':
        current_document_name = current_document_name + '/编号/' + current_id
    sub = {
        'id': '',
        'type': '需求文档',
        'source': current_document_name,
        'des': current_des,
        'val': threshold
    }
    return sub, template, development_value


def ptb2g_cd_B(require_document_list):
    threshold, template, development_value = template_threshold_etc(require_document_list, '性能', '响应时间')
    threshold['id'] = 'B'
    threshold['des'] = '规定的任务响应时间'
    return threshold, template, development_value


# 提取用例实际情况中的数值（根据关键字符确定要寻找什么数值）
def template_extract_situation_num(require_document_list, use_case_document_list, category_input, require_kind, find_what):  # 从实际情况中提取数字
    current_document_name = ''
    current_id = ''
    current_des = ''
    current_id_list = []
    if require_document_list and use_case_document_list:
        current_document_name = use_case_document_list[0].document_name
        need_in_situation = []
        for require_node in require_document_list:
            if require_node.category == category_input and require_node.require_description.find(require_kind) != -1:
                current_des = '关联的测试用例中' + find_what + '值'
                if require_node.associated_use_case_ID:
                    for use_case_ID in require_node.associated_use_case_ID:
                        for use_case_node in use_case_document_list:
                            if use_case_node.id == use_case_ID and use_case_node.actual_situation != '':
                                actual_situation = re.split(r'\n|，|。', use_case_node.actual_situation)  # 去除\n
                                for each_situation in actual_situation:
                                    if each_situation.find(find_what) != -1:
                                        if is_number(each_situation[0]):
                                            each_situation = re.sub('\d+\.', '', each_situation,
                                                                    1)  # 替换掉1. 并且只替换第一个（防止有效数字为1.X之类的被替换掉）

                                        # 判断实际情况中是不是描述时间（时分秒）
                                        ret_hms = re.findall(r"(\d+?)时(\d+?)分(\d+?)秒", each_situation)
                                        if ret_hms:
                                            for each_time in ret_hms:
                                                time = float(each_time[0]) * 3600 + float(each_time[1]) * 60 + float(
                                                    each_time[2])
                                                time = time * 1000  # 统一成毫秒
                                                need_in_situation.append(time)
                                                if use_case_node.id not in current_id_list:
                                                    current_id_list.append(use_case_node.id)
                                            break

                                        # 判断实际情况中是不是描述时间（分秒）
                                        ret_m_s = re.findall(r"(\d+?)分(\d+?)秒", each_situation)
                                        if ret_m_s:
                                            for each_time in ret_m_s:
                                                time = float(each_time[0]) * 60 + float(each_time[1])
                                                time = time * 1000  # 统一成毫秒
                                                need_in_situation.append(time)
                                                if use_case_node.id not in current_id_list:
                                                    current_id_list.append(use_case_node.id)
                                            break

                                        # 判断实际情况中是不是描述时间（秒）
                                        ret_s = re.findall(r"\d+.\d+s|\d+s|\d+.\d+秒|\d+秒", each_situation)
                                        if ret_s:
                                            for each_time in ret_s:
                                                time = re.match(r'\d+.\d+|\d+', each_time)
                                                time = float(time.group()) * 1000  # 统一成毫秒
                                                need_in_situation.append(time)
                                                if use_case_node.id not in current_id_list:
                                                    current_id_list.append(use_case_node.id)
                                            break

                                        # 判断实际情况中是不是描述时间（毫秒）
                                        ret_ms = re.findall(r"\d+.\d+ms|\d+ms|\d+.\d+毫秒|\d+毫秒", each_situation)
                                        if ret_ms:
                                            for each_time in ret_ms:
                                                time = re.match(r'\d+.\d+|\d+', each_time)
                                                time = float(time.group())
                                                need_in_situation.append(time)
                                                if use_case_node.id not in current_id_list:
                                                    current_id_list.append(use_case_node.id)
                                            break

                                        # 判断实际情况中是不是描述百分比（%）
                                        ret_percent = re.findall(r"\d+.\d+%|\d+%|百分之\d+.\d+|百分之\d+", each_situation)
                                        if ret_percent:
                                            for each_percent in ret_percent:
                                                time = re.match(r'\d+.\d+|\d+', each_percent)
                                                time_group = time.group()
                                                time = float(time_group) * 0.01
                                                need_in_situation.append(time)
                                                if use_case_node.id not in current_id_list:
                                                    current_id_list.append(use_case_node.id)
                                            break

                                        # 判断实际情况中是不是描述时间（小时）
                                        ret_h = re.findall(r"\d+.\d+h|\d+h|\d+.\d+小时|\d+小时", each_situation)
                                        if ret_h:
                                            for each_time in ret_h:
                                                time = re.match(r'\d+.\d+|\d+', each_time)
                                                time = float(time.group()) * 3600 * 1000  # 统一成毫秒
                                                need_in_situation.append(time)
                                                if use_case_node.id not in current_id_list:
                                                    current_id_list.append(use_case_node.id)
                                            break

                                        # 判断实际情况中是不是描述时间（分钟）
                                        ret_m = re.findall(r"\d+.\d+分钟|\d+分钟|\d+.\d+min|\d+min", each_situation)
                                        if ret_m:
                                            for each_time in ret_m:
                                                time = re.match(r'\d+.\d+|\d+', each_time)
                                                time = float(time.group()) * 60 * 1000  # 统一成毫秒
                                                need_in_situation.append(time)
                                                if use_case_node.id not in current_id_list:
                                                    current_id_list.append(use_case_node.id)
                                            break

                                        # 判断实际情况中是不是描述时间（天）
                                        ret_d = re.findall(r"\d+.\d+天|\d+天|\d+.\d+d|\d+d", each_situation)
                                        if ret_d:
                                            for each_time in ret_d:
                                                time = re.match(r'\d+.\d+|\d+', each_time)
                                                time = float(time.group()) * 24 * 3600 * 1000  # 统一成毫秒
                                                need_in_situation.append(time)
                                                if use_case_node.id not in current_id_list:
                                                    current_id_list.append(use_case_node.id)
                                            break

                                        # 如果没有单位
                                        if ret_hms == [] and ret_s == [] and ret_ms == [] and ret_percent == []:
                                            ret = re.findall(r"\d+.\d+|\d+", each_situation)
                                            for each_one in ret:
                                                one = float(each_one)
                                                need_in_situation.append(one)
                                                if use_case_node.id not in current_id_list:
                                                    current_id_list.append(use_case_node.id)
                break
    else:
        need_in_situation = None
    current_document_name_list = []
    if current_document_name != '':
        for current_id in current_id_list:
            current_document_name_list.append(current_document_name + '/编号/' + current_id)
    Ni = []
    for i, current_document_name in enumerate(current_document_name_list):
        Ni.append(
            {
                'id': str(i),
                'type': '用例文档',
                'source': current_document_name,
                'des': current_des,
                'val': need_in_situation[i]
            }
        )
    return Ni


def ptb3g_cd_Ai(require_document_list, use_case_document_list):
    need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '性能', '周转时间', '开始时刻')
    for each_one in need_in_situation:
        each_one['des'] = '作业或异步进程' + str(int(each_one['id'])+1) + '的开始时刻'
        each_one['id'] = 'A' + each_one['id']
    return need_in_situation


"""
def ptb3g_cd_Ai(require_document_list, use_case_document_list):
    need_in_situation = []
    for require_node in require_document_list:
        if require_node.category == '性能' and require_node.require_description.find('周转时间') != -1:
            if require_node.associated_use_case_ID:
                for use_case_ID in require_node.associated_use_case_ID:
                    for use_case_node in use_case_document_list:
                        if use_case_node.id == use_case_ID and use_case_node.actual_situation != '':
                            actual_situation = re.split(r'\n', use_case_node.actual_situation)  # 去除\n
                            for each_situation in actual_situation:
                                if each_situation.find('开始时刻') != -1:
                                    each_situation = re.sub('\d+\.', '', each_situation)  # 去除前面的编号
                                    result = re.findall(r"\d+", each_situation)
                                    if result:
                                        need_in_situation.append(result[0])
                                    break
            break
    return need_in_situation
"""


def ptb3g_cd_Bi(require_document_list, use_case_document_list):
    need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '性能', '周转时间', '完成时刻')
    for each_one in need_in_situation:
        each_one['des'] = '作业或异步进程' + str(int(each_one['id']) + 1) + '的完成时刻'
        each_one['id'] = 'B' + each_one['id']
    return need_in_situation


def ptb3g_cd_Xi(require_document_list, use_case_document_list):
    need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '性能', '周转时间', '周转时间')
    for each_one in need_in_situation:
        each_one['des'] = '作业或异步进程' + str(int(each_one['id']) + 1) + '的开始时刻'
        each_one['id'] = 'X' + each_one['id']
    return need_in_situation

"""
def ptb3g_cd_n(require_document_list, use_case_document_list):
    n = 0
    for require_node in require_document_list:
        if require_node.category == '性能' and require_node.require_description.find('我希望系统周转时间') != -1:
            if require_node.associated_use_case_ID:
                for use_case_ID in require_node.associated_use_case_ID:
                    for use_case_node in use_case_document_list:
                        if use_case_node.id == use_case_ID and use_case_node.actual_situation != '':
                            actual_situation = re.split(r'\n', use_case_node.actual_situation)  # 去除\n
                            for each_situation in actual_situation:
                                if each_situation.find('周转时间') != -1:
                                    each_situation = re.sub('\d+\.', '', each_situation)  # 去除前面的编号
                                    result = re.findall(r"\d+", each_situation)
                                    if result:
                                        n = n + 1
                                    break
            break
    return n
"""


def ptb4g_cd_B(require_document_list):
    threshold, template, development_value = template_threshold_etc(require_document_list, '性能', '我希望系统周转时间')
    threshold['id'] = 'B'
    threshold['des'] = '规定的作业或异步进程的周转时间'
    return threshold, template, development_value


def ptb5g_cd_Ai(require_document_list, use_case_document_list):
    need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '性能', '我希望系统吞吐量', '作业数量')
    for each_one in need_in_situation:
        each_one['des'] = '第' + str(int(each_one['id']) + 1) + '次观察时间内完成的作业数量'
        each_one['id'] = 'A' + each_one['id']
    return need_in_situation


def ptb5g_cd_Bi(require_document_list, use_case_document_list):
    need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '性能', '我希望系统吞吐量', '时间周期')
    for each_one in need_in_situation:
        each_one['des'] = '第' + str(int(each_one['id']) + 1) + '次观察时间的周期'
        each_one['id'] = 'B' + each_one['id']
    return need_in_situation


def ptb5g_cd_Xi(require_document_list, use_case_document_list):
    need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '性能', '我希望系统吞吐量', '吞吐量')
    for each_one in need_in_situation:
        each_one['des'] = '第' + str(int(each_one['id']) + 1) + '次观察的吞吐量'
        each_one['id'] = 'X' + each_one['id']
    return need_in_situation


def pru1g_cd_Ai(require_document_list, use_case_document_list):
    need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '性能', '我希望系统处理器占用率', '处理器使用时间')
    for each_one in need_in_situation:
        each_one['des'] = '第' + str(int(each_one['id']) + 1) + '次观察中，处理器执行一组给定任务所用的时间'
        each_one['id'] = 'A' + each_one['id']
    return need_in_situation


def pru1g_cd_Bi(require_document_list, use_case_document_list):
    need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '性能', '我希望系统处理器占用率', '任务运行时间')
    for each_one in need_in_situation:
        each_one['des'] = '第' + str(int(each_one['id']) + 1) + '次观察中，执行任务的运行时间'
        each_one['id'] = 'B' + each_one['id']
    return need_in_situation


def pru1g_cd_Xi(require_document_list, use_case_document_list):
    need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '性能', '我希望系统处理器占用率', '处理器占用率')
    for each_one in need_in_situation:
        each_one['des'] = '第' + str(int(each_one['id']) + 1) + '次观察中，处理器平均占用率'
        each_one['id'] = 'X' + each_one['id']
    return need_in_situation


def pru2g_cd_Ai(require_document_list, use_case_document_list):
    need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '性能', '我希望系统内存占用率', '实际内存')
    for each_one in need_in_situation:
        each_one['des'] = '第' + str(int(each_one['id']) + 1) + '次样本处理中执行一组给定任务所占用的实际内存大小'
        each_one['id'] = 'A' + each_one['id']
    return need_in_situation


def pru2g_cd_Bi(require_document_list, use_case_document_list):
    need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '性能', '我希望系统内存占用率', '可用内存')
    for each_one in need_in_situation:
        each_one['des'] = '第' + str(int(each_one['id']) + 1) + '样本处理期间可用于执行任务的内存大小'
        each_one['id'] = 'B' + each_one['id']
    return need_in_situation


def pru2g_cd_Xi(require_document_list, use_case_document_list):
    need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '性能', '我希望系统内存占用率', '内存占用率')
    for each_one in need_in_situation:
        each_one['des'] = '第' + str(int(each_one['id']) + 1) + '次观察中的内存平均占用率'
        each_one['id'] = 'X' + each_one['id']
    return need_in_situation


def pru3g_cd_Ai(require_document_list, use_case_document_list):
    need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '性能', '我希望系统I/O设备占用率', '占用时间')
    for each_one in need_in_situation:
        each_one['des'] = '第' + str(int(each_one['id']) + 1) + '次观察中,执行一组给定任务所占用I/O设备的持续时间'
        each_one['id'] = 'A' + each_one['id']
    return need_in_situation


def pru3g_cd_Bi(require_document_list, use_case_document_list):
    need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '性能', '我希望系统I/O设备占用率', '所需时间')
    for each_one in need_in_situation:
        each_one['des'] = '第' + str(int(each_one['id']) + 1) + '次观察中,执行任务所需I/O设备的持续时间'
        each_one['id'] = 'B' + each_one['id']
    return need_in_situation


def pru3g_cd_Xi(require_document_list, use_case_document_list):
    need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '性能', '我希望系统I/O设备占用率', '占用率')
    for each_one in need_in_situation:
        each_one['des'] = '第' + str(int(each_one['id']) + 1) + '次观察中的I/O设备平均占用率'
        each_one['id'] = 'X' + each_one['id']
    return need_in_situation


def pru4s_cd_A(require_document_list, use_case_document_list):
    need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '性能', '我希望系统带宽占用率', '传输带宽')
    for each_one in need_in_situation:
        each_one['des'] = '第' + str(int(each_one['id']) + 1) + '次观察中,执行一组给定任务时测得的实际传输带宽'
        each_one['id'] = 'A' + each_one['id']
    return need_in_situation


def pru4s_cd_B(require_document_list, use_case_document_list):
    need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '性能', '我希望系统带宽占用率', '可用带宽')
    for each_one in need_in_situation:
        each_one['des'] = '第' + str(int(each_one['id']) + 1) + '次观察中,执行一组任务时可用带宽容量'
        each_one['id'] = 'B' + each_one['id']
    return need_in_situation


def pru4s_cd_X(require_document_list, use_case_document_list):
    need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '性能', '我希望系统带宽占用率', '带宽占用率')
    for each_one in need_in_situation:
        each_one['des'] = '第' + str(int(each_one['id']) + 1) + '次观察中,执行一组任务的带宽占用率'
        each_one['id'] = 'X' + each_one['id']
    return need_in_situation


def pca1g_cd_A(require_document_list, use_case_document_list):
    need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '性能', '我希望系统事务处理容量', '完成事务')
    for each_one in need_in_situation:
        each_one['des'] = '第' + str(int(each_one['id']) + 1) + '次观察中,观察时间内完成事务的数量'
        each_one['id'] = 'A' + each_one['id']
    return need_in_situation


def pca1g_cd_B(require_document_list, use_case_document_list):
    need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '性能', '我希望系统事务处理容量', '观察时长')
    for each_one in need_in_situation:
        each_one['des'] = '第' + str(int(each_one['id']) + 1) + '次观察中的观察时间'
        each_one['id'] = 'B' + each_one['id']
    return need_in_situation


def pca1g_cd_X(require_document_list, use_case_document_list):
    need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '性能', '我希望系统事务处理容量', '事务处理容量')
    for each_one in need_in_situation:
        each_one['des'] = '第' + str(int(each_one['id']) + 1) + '次观察中的事务处理容量'
        each_one['id'] = 'X' + each_one['id']
    return need_in_situation


def pca2g_cd_Ai(require_document_list, use_case_document_list):
    need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '性能', '我希望系统用户访问量', '访问用户')
    for each_one in need_in_situation:
        each_one['des'] = '第' + str(int(each_one['id']) + 1) + '次观察中,同时访问系统的最大用户数量'
        each_one['id'] = 'A' + each_one['id']
    return need_in_situation


def pca3s_cd_A(require_document_list, use_case_document_list):
    need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '功能', '我希望系统用户访问增长', '新增用户数')
    for each_one in need_in_situation:
        each_one['des'] = '第' + str(int(each_one['id']) + 1) + '次观察中,观察时间内成果增加的用户数量'
        each_one['id'] = 'A' + each_one['id']
    return need_in_situation


def pca3s_cd_B(require_document_list, use_case_document_list):
    need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '功能', '我希望系统用户访问增长', '观察时长')
    for each_one in need_in_situation:
        each_one['des'] = '第' + str(int(each_one['id']) + 1) + '次观察中的观察时间'
        each_one['id'] = 'B' + each_one['id']
    return need_in_situation


def pca3s_cd_X(require_document_list, use_case_document_list):
    need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '功能', '我希望系统用户访问增长', '访问增长')
    for each_one in need_in_situation:
        each_one['des'] = '第' + str(int(each_one['id']) + 1) + '次观察中的用户访问增长值'
        each_one['id'] = 'B' + each_one['id']
    return need_in_situation


def get_data_from_description(S):
    ret = re.findall(r"：(.+)，", S)  # 贪婪
    ret = re.split(r'、', ret[0])
    return ret


# 提取需求描述中的在通过用例测试的数据项，返回列表长度
def template_extract_situation_list(require_document_list, use_case_document_list, category_input, description_kind):  # 提取通过测试的数据项列表长度
    current_document_name = ''
    current_id = ''
    current_des = '需求描述中的在通过用例测试的数据项:'
    if require_document_list and use_case_document_list:
        current_document_name = use_case_document_list[0].document_name
        actual_data_list = []
        for require_node in require_document_list:
            if require_node.category == category_input and require_node.require_description.find(
                    description_kind) != -1:
                require_data_list = get_data_from_description(require_node.require_description)
                if require_node.associated_use_case_ID:
                    for use_case_ID in require_node.associated_use_case_ID:
                        for use_case_node in use_case_document_list:
                            if use_case_node.id == use_case_ID and use_case_node.actual_situation != '': # and use_case_node.use_case_result == '通过':
                                current_id = use_case_node.id
                                actual_situation = re.split(r'\n', use_case_node.actual_situation)  # 去除\n
                                for each_situation in actual_situation:
                                    current_des = current_des + each_situation
                                    for find_what in require_data_list:
                                        if each_situation.find(find_what) != -1:
                                            if find_what not in actual_data_list:
                                                actual_data_list.append(find_what)
                break
        L = len(actual_data_list)
    else:
        L = None
    if current_document_name != '':
        current_document_name = current_document_name + '/用例编号/' + current_id
    sub = {
        'id': '',
        'type': '用例文档',
        'source': current_document_name,
        'des': current_des,
        'val': L
    }
    return sub


# 返回需求描述中的数据项列表长度
def template_extract_situation_list_len(require_document_list, category_input, description_kind):  # 数据项列表长度
    current_document_name = ''
    current_id = ''
    current_des = ''
    require_data_list = []
    for require_node in require_document_list:
        current_document_name = require_document_list[0].document_name
        if require_node.category == category_input and require_node.require_description.find(description_kind) != -1:
            current_id = require_node.id
            current_des = template_what_i_hope(require_node.require_description)
            require_data_list = get_data_from_description(require_node.require_description)
            break
    if require_data_list:
        L = len(require_data_list)
    else:
        L = None
    if current_document_name != '':
        current_document_name = current_document_name + '/编号/' + current_id
    sub = {
        'id': '',
        'type': '需求文档',
        'source': current_document_name,
        'des': current_des,
        'val': L
    }
    return sub


# 没通过测试用例的数据项列表长度
def template_whether_data_nopass(require_document_list, use_case_document_list, category_input, description_kind):  # 仅判断数据项是否不通过，返回其列表长度
    current_document_name = ''
    current_id = ''
    current_des = ''
    if require_document_list and use_case_document_list:
        current_document_name = require_document_list[0].document_name
        actual_data_pass = []
        require_data_list = []
        for require_node in require_document_list:
            if require_node.category == category_input and require_node.require_description.find(
                    description_kind) != -1:
                current_id = require_node.id
                current_des = template_what_i_hope(require_node.require_description)
                require_data_list = get_data_from_description(require_node.require_description)
                if require_node.associated_use_case_ID:
                    for use_case_ID in require_node.associated_use_case_ID:
                        for use_case_node in use_case_document_list:
                            if use_case_node.id == use_case_ID and use_case_node.actual_situation != '' and use_case_node.use_case_result != '通过':
                                actual_situation = re.split(r'\n', use_case_node.actual_situation)  # 去除\n
                                for each_situation in actual_situation:
                                    for find_what in require_data_list:
                                        if each_situation.find(find_what) != -1:
                                            if find_what not in actual_data_pass:
                                                actual_data_pass.append(find_what)
                break
        actual_data_nopass = []
        for data in require_data_list:
            if data not in actual_data_pass:
                actual_data_nopass.append(data)
        L = len(actual_data_nopass)
    else:
        L = None
    if current_document_name != '':
        current_document_name = current_document_name + '/编号/' + current_id
    sub = {
        'id': '',
        'type': '需求文档',
        'source': current_document_name,
        'des': current_des,
        'val': L
    }
    return sub


def cco1g_cd_A(require_document_list, use_case_document_list):
    L = template_extract_situation_list(require_document_list, use_case_document_list, '其他', '与以下软件共享运行环境')
    L['id'] = 'A'
    L['des'] = '与该产品可共存的其他规定的软件产品数量'
    return L


def cco1g_cd_B(require_document_list):
    L = template_extract_situation_list_len(require_document_list, '其他', '与以下软件共享运行环境')
    L['id'] = 'B'
    L['des'] = '在运行环境中，该产品需要与其他软件产品共存的数量'
    return L


def cin1g_cd_A(require_document_list, use_case_document_list):
    L = template_extract_situation_list(require_document_list, use_case_document_list, '接口', '以下数据格式交换数据')
    L['id'] = 'A'
    L['des'] = '与其他软件或系统可交换数据格式的数量'
    return L


def cin1g_cd_B(require_document_list):
    L = template_extract_situation_list_len(require_document_list, '接口', '以下数据格式交换数据')
    L['id'] = 'B'
    L['des'] = '需要交换数据格式的数量'
    return L


def cin2g_cd_A(require_document_list, use_case_document_list):
    L = template_extract_situation_list(require_document_list, use_case_document_list, '接口', '以下协议交换数据')
    L['id'] = 'A'
    L['des'] = '实际支持数据交换协议的数量'
    return L


def cin2g_cd_B(require_document_list):
    L = template_extract_situation_list_len(require_document_list, '接口', '以下协议交换数据')
    L['id'] = 'B'
    L['des'] = '规定支持的数据交换协议数量'
    return L


def cin3s_cd_A(require_document_list, use_case_document_list):
    L = template_extract_situation_list(require_document_list, use_case_document_list, '接口', '支持以下外部接口')
    L['id'] = 'A'
    L['des'] = '有效的外部接口数量'
    return L


def cin3s_cd_B(require_document_list):
    L = template_extract_situation_list_len(require_document_list, '接口', '支持以下外部接口')
    L['id'] = 'B'
    L['des'] = '规定的外部接口数量'
    return L


def uap1g_cd_A(require_document_list, use_case_document_list):
    L = template_extract_situation_list(require_document_list, use_case_document_list, '体验', '以下场景中系统使用方法')
    L['id'] = 'A'
    L['des'] = '在产品描述或用户文档中所描述的使用场景数量'
    return L


def uap1g_cd_B(require_document_list):
    L = template_extract_situation_list_len(require_document_list, '体验', '以下场景中系统使用方法')
    L['id'] = 'B'
    L['des'] = '产品的使用场景数量'
    return L


def uap2s_cd_A(require_document_list, use_case_document_list):
    L = template_extract_situation_list(require_document_list, use_case_document_list, '体验', '以下任务提供演示功能')
    L['id'] = 'A'
    L['des'] = '具有演示功能的任务的数量'
    return L


def uap2s_cd_B(require_document_list):
    L = template_extract_situation_list_len(require_document_list, '体验', '以下任务提供演示功能')
    L['id'] = 'B'
    L['des'] = '期望能从演示功能中获益的任务数量'
    return L


def uap3s_cd_A(require_document_list, use_case_document_list):
    need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '体验', '系统网站的引导页数量', '引导页数')
    for each_one in need_in_situation:
        each_one['des'] = '第' + str(int(each_one['id']) + 1) + '次观察中，能说明网站目的的引导页数量'
        each_one['id'] = 'A' + each_one['id']
    return need_in_situation


def uap3s_cd_B(require_document_list):
    threshold, template, development_value = template_threshold_etc(require_document_list, '体验', '系统网站的引导页数量')
    threshold['id'] = 'B'
    threshold['des'] = '网站中引导页的数量'
    return threshold, template, development_value


def ule1g_cd_A(require_document_list, use_case_document_list):
    L = template_extract_situation_list(require_document_list, use_case_document_list, '体验', '用户文档和帮助机制中能描述以下功能')
    L['id'] = 'A'
    L['des'] = '在用户文档和/或帮助机制中按要求描述的功能数量'
    return L


def ule1g_cd_B(require_document_list):
    L = 0
    current_document_name = ''
    for require_node in require_document_list:
        current_document_name = require_document_list[0].document_name
        if require_node.category == '功能':
            L = L + 1
    if require_document_list == []:
        L = None
    if current_document_name != '':
        current_document_name = current_document_name + '/类别/功能'
    sub = {
        'id': 'B',
        'type': '需求文档',
        'source': current_document_name,
        'des': '要求实现的功能总数量',
        'val': L
    }
    return sub


def ule2s_cd_A(require_document_list, use_case_document_list):
    L = template_extract_situation_list(require_document_list, use_case_document_list, '体验', '以下输入字段能自动填充默认值')
    L['id'] = 'A'
    L['des'] = '运行过程中自动填充默认值的输入字段数量'
    return L


def ule2s_cd_B(require_document_list):
    L = template_extract_situation_list_len(require_document_list, '体验', '以下输入字段能自动填充默认值')
    L['id'] = 'B'
    L['des'] = '具有默认值的输入字段的数量'
    return L


def ule3s_cd_A(require_document_list, use_case_document_list):
    L = template_extract_situation_list(require_document_list, use_case_document_list, '体验', '提供出错原因和可能解决方法')
    L['id'] = 'A'
    L['des'] = '给出差错发生原因及可能解决方法的差错信息数量'
    return L


def ule3s_cd_B(require_document_list):
    L = template_extract_situation_list_len(require_document_list, '体验', '提供出错原因和可能解决方法')
    L['id'] = 'B'
    L['des'] = '差错信息的数量'
    return L


def ule4s_cd_A(require_document_list, use_case_document_list):
    need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '体验', '完成常规任务所需信息元素和步骤的数量', '用户可理解的信息元素和步骤')
    for each_one in need_in_situation:
        each_one['des'] = '第' + str(int(each_one['id']) + 1) + '次观察中，以用户可以理解的方式所呈现信息元素和步骤的数量'
        each_one['id'] = 'A' + each_one['id']
    return need_in_situation


def ule4s_cd_B(require_document_list):
    threshold, template, development_value = template_threshold_etc(require_document_list, '体验', '完成常规任务所需信息元素和步骤的数量')
    threshold['id'] = 'B'
    threshold['des'] = '对于新用户来说完成常规任务所需信息元素和步骤的数量'
    return threshold, template, development_value


def uop1g_cd_A(require_document_list, use_case_document_list):
    L = template_extract_situation_list(require_document_list, use_case_document_list, '体验', '操作结果与外观具有一致性')
    L['id'] = 'A'
    L['des'] = '不一致的特定交互式任务数量'
    return L


def uop1g_cd_B(require_document_list):
    L = template_extract_situation_list_len(require_document_list, '体验', '操作结果与外观具有一致性')
    L['id'] = 'B'
    L['des'] = '需要一致的交互任务的数量'
    return L


# 仅判断用例结果为通过的模板，统计通过数量，仅通过
def template_use_case_pass(require_document_list, use_case_document_list, category_input, description_kind):
    current_document_name = ''
    current_id = ''

    if require_document_list and use_case_document_list:
        n = 0
        for require_node in require_document_list:
            if require_node.category == category_input and require_node.require_description.find(
                    description_kind) != -1:
                current_id = require_node.id
                if require_node.associated_use_case_ID:
                    for use_case_ID in require_node.associated_use_case_ID:
                        for use_case_node in use_case_document_list:
                            current_document_name = use_case_document_list[0].document_name
                            if use_case_ID == use_case_node.id and use_case_node.use_case_result == '通过':
                                n = n + 1
                break
    else:
        n = None
    if current_document_name != '':
        current_document_name = current_document_name + '/结果/通过'
    sub = {
        'id': '',
        'type': '用例文档',
        'source': current_document_name,
        'des': '需求关联的用例通过的数量',
        'val': n
    }
    return sub


# 仅统计关联的用例数
def template_associated_use_case_num(require_document_list, category_input, description_kind):
    current_document_name = ''
    current_id = ''
    current_des = ''
    if require_document_list:
        current_document_name = require_document_list[0].document_name
        n = 0
        for require_node in require_document_list:
            if require_node.category == category_input and require_node.require_description.find(
                    description_kind) != -1:
                current_id = require_node.id
                current_des = template_what_i_hope(require_node.require_description)
                if require_node.associated_use_case_ID:
                    n = len(require_node.associated_use_case_ID)
                break
    else:
        n = None
    if current_document_name != '':
        current_document_name = current_document_name + '/编号/' + current_id
    sub = {
        'id': '',
        'type': '需求文档',
        'source': current_document_name,
        'des': current_des + '，需求关联的用例数量',
        'val': n
    }
    return sub


def uop2g_cd_A(require_document_list, use_case_document_list):
    n = template_use_case_pass(require_document_list, use_case_document_list, '体验', '给用户传达正确结果或指令')
    n['id'] = 'A'
    n['des'] = '传达给用户正确结果或指令的消息数量'
    return n


def uop2g_cd_B(require_document_list):
    n = template_associated_use_case_num(require_document_list, '体验', '给用户传达正确结果或指令')
    n['id'] = 'B'
    n['des'] = '实现的消息数量'
    return n


def uop3s_cd_A(require_document_list, use_case_document_list):
    L = template_extract_situation_list(require_document_list, use_case_document_list, '体验', '功能和操作规程支持用户定制')
    L['id'] = 'A'
    L['des'] = '为用户使用方便而提供的可被定制的功能和操作规程的数量'
    return L


def uop3s_cd_B(require_document_list):
    L = template_extract_situation_list_len(require_document_list, '体验', '功能和操作规程支持用户定制')
    L['id'] = 'B'
    L['des'] = '用户能够受益于定制的功能和操作规程的数量'
    return L


def uop4s_cd_A(require_document_list, use_case_document_list):
    L = template_extract_situation_list(require_document_list, use_case_document_list, '体验', '用户界面元素支持用户定制')
    L['id'] = 'A'
    L['des'] = '可以定制的用户界面的元素数量'
    return L


def uop4s_cd_B(require_document_list):
    L = template_extract_situation_list_len(require_document_list, '体验', '用户界面元素支持用户定制')
    L['id'] = 'B'
    L['des'] = '期望能够受益于定制的用户界面元素数量'
    return L


def uop5s_cd_A(require_document_list, use_case_document_list):
    L = template_extract_situation_list(require_document_list, use_case_document_list, '体验', '能够监视以下功能状态')
    L['id'] = 'A'
    L['des'] = '具有状态监视能力的功能数量'
    return L


def uop5s_cd_B(require_document_list):
    L = template_extract_situation_list_len(require_document_list, '体验', '能够监视以下功能状态')
    L['id'] = 'B'
    L['des'] = '期望受益于监视能力的功能数量'
    return L


def uop6s_cd_A(require_document_list, use_case_document_list):
    L = template_extract_situation_list(require_document_list, use_case_document_list, '体验', '支持撤销操作或重新确认')
    L['id'] = 'A'
    L['des'] = '提供撤销操作或重新确认的任务数量'
    return L


def uop6s_cd_B(require_document_list):
    L = template_extract_situation_list_len(require_document_list, '体验', '支持撤销操作或重新确认')
    L['id'] = 'B'
    L['des'] = '用户能够重新确认或撤销操作中获益的任务数量'
    return L


def uop7s_cd_A(require_document_list, use_case_document_list):
    L = template_extract_situation_list(require_document_list, use_case_document_list, '体验', '使用以下信息结构')
    L['id'] = 'A'
    L['des'] = '对于预期用户来说，熟悉和方便的信息结构数量'
    return L


def uop7s_cd_B(require_document_list):
    L = template_extract_situation_list_len(require_document_list, '体验', '使用以下信息结构')
    L['id'] = 'B'
    L['des'] = '使用的信息结构数量'
    return L


def uop8s_cd_A(require_document_list, use_case_document_list):
    need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '体验', '具有相似项且外观相似的比例', '具有相似项但外观不同的用户界面')
    for each_one in need_in_situation:
        each_one['des'] = '第' + str(int(each_one['id']) + 1) + '次测试中，具有相似项但外观不同的用户界面的数量'
        each_one['id'] = 'A' + each_one['id']
    return need_in_situation


def uop8s_cd_B(require_document_list, use_case_document_list):
    need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '体验', '具有相似项且外观相似的比例', '具有相似项的用户界面')
    for each_one in need_in_situation:
        each_one['des'] = '第' + str(int(each_one['id']) + 1) + '次测试中，具有相似项的用户界面的数量'
        each_one['id'] = 'B' + each_one['id']
    return need_in_situation


def uop8s_cd_X(require_document_list, use_case_document_list):
    need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '体验', '具有相似项且外观相似的比例', '具有相似项且外观相似')
    for each_one in need_in_situation:
        each_one['des'] = '第' + str(int(each_one['id']) + 1) + '次测试中，具有相似项且外观相似的比例值'
        each_one['id'] = 'X' + each_one['id']
    return need_in_situation


def uop9s_cd_A(require_document_list, use_case_document_list):
    L = template_extract_situation_list(require_document_list, use_case_document_list, '体验', '通过键盘、鼠标或语音等方法启动以下任务')
    L['id'] = 'A'
    L['des'] = '可由所有适当的输入方法启动任务的数量'
    return L


def uop9s_cd_B(require_document_list):
    L = template_extract_situation_list_len(require_document_list, '体验', '通过键盘、鼠标或语音等方法启动以下任务')
    L['id'] = 'B'
    L['des'] = '系统支持的任务数量'
    return L


def uep1g_cd_A(require_document_list, use_case_document_list):
    L = template_extract_situation_list(require_document_list, use_case_document_list, '体验', '以下用户操作时抵御误操作')
    L['id'] = 'A'
    L['des'] = '实际操作中可以防止导致系统故障的用户操作和输入的数量'
    return L


def uep1g_cd_B(require_document_list):
    L = template_extract_situation_list_len(require_document_list, '体验', '以下用户操作时抵御误操作')
    L['id'] = 'B'
    L['des'] = '可以防止导致系统故障的用户操作和输入的数量'
    return L


def uep2s_cd_A(require_document_list, use_case_document_list):
    L = template_extract_situation_list(require_document_list, use_case_document_list, '体验', '检测到以下输入差错时提示纠正')
    L['id'] = 'A'
    L['des'] = '系统提供建议的修改值的输入差错数量'
    return L


def uep2s_cd_B(require_document_list):
    L = template_extract_situation_list_len(require_document_list, '体验', '检测到以下输入差错时提示纠正')
    L['id'] = 'B'
    L['des'] = '检测到的输入差错数量'
    return L


def uep3s_cd_A(require_document_list, use_case_document_list):  # 需求应该包含子需求
    current_document_name = ''
    current_id = ''
    current_des = ''
    n = 0
    for require_node in require_document_list:
        current_document_name = require_document_list[0].document_name
        if require_node.category == '体验' and require_node.require_description.find('检测用户操作的差错可以进行纠正') != -1:
            current_id = require_node.id
            current_des = template_what_i_hope(require_node.require_description)
            if require_node.associated_use_case_ID:
                for use_case_ID in require_node.associated_use_case_ID:
                    for use_case_node in use_case_document_list:
                        if use_case_node.id == use_case_ID and use_case_node.use_case_result == '通过':
                            n = n + 1
            if require_node.its_sons:
                for son_id in require_node.its_sons:
                    for require_son_node in require_document_list:
                        if son_id == require_son_node.id:
                            if require_son_node.associated_use_case_ID:
                                for use_case_ID in require_son_node.associated_use_case_ID:
                                    for use_case_node in use_case_document_list:
                                        if use_case_node.id == use_case_ID and use_case_node.use_case_result == '通过':
                                            n = n + 1
            break
    if current_document_name != '':
        current_document_name = current_document_name + '/编号/' + current_id
    sub = {
        'id': 'A',
        'type': '需求文档',
        'source': current_document_name,
        'des': '由系统恢复的用户差错数量，这些用户差错是经设计并测试的',
        'val': n
    }
    return sub


def uep3s_cd_B(require_document_list, use_case_document_list):
    current_document_name = ''
    current_id = ''
    current_des = ''
    n = 0
    for require_node in require_document_list:
        current_document_name = require_document_list[0].document_name
        if require_node.category == '体验' and require_node.require_description.find('检测用户操作的差错可以进行纠正') != -1:
            current_id = require_node.id
            if require_node.associated_use_case_ID:
                for use_case_ID in require_node.associated_use_case_ID:
                    for use_case_node in use_case_document_list:
                        if use_case_node.id == use_case_ID:
                            n = n + 1
            if require_node.its_sons:
                for son_id in require_node.its_sons:
                    for require_son_node in require_document_list:
                        if son_id == require_son_node.id:
                            if require_son_node.associated_use_case_ID:
                                for use_case_ID in require_son_node.associated_use_case_ID:
                                    for use_case_node in use_case_document_list:
                                        if use_case_node.id == use_case_ID:
                                            n = n + 1
            break
    if current_document_name != '':
        current_document_name = current_document_name + '/编号/' + current_id
    sub = {
        'id': 'B',
        'type': '需求文档',
        'source': current_document_name,
        'des': '操作过程中可能发生的用户差错数量',
        'val': n
    }
    return sub


def uin1s_cd_A(require_document_list, use_case_document_list):  # 需求应该包含子需求
    current_document_name = ''
    current_id = ''
    current_des = ''
    n = 0
    for require_node in require_document_list:
        current_document_name = require_document_list[0].document_name
        if require_node.category == '体验' and require_node.require_description.find('显示界面外观舒适可以令人愉悦') != -1:
            current_id = require_node.id
            current_des = template_what_i_hope(require_node.require_description)
            if require_node.associated_use_case_ID:
                for use_case_ID in require_node.associated_use_case_ID:
                    for use_case_node in use_case_document_list:
                        if use_case_node.id == use_case_ID and use_case_node.use_case_result == '通过':
                            n = n + 1
            if require_node.its_sons:
                for son_id in require_node.its_sons:
                    for require_son_node in require_document_list:
                        if son_id == require_son_node.id:
                            if require_son_node.associated_use_case_ID:
                                for use_case_ID in require_son_node.associated_use_case_ID:
                                    for use_case_node in use_case_document_list:
                                        if use_case_node.id == use_case_ID and use_case_node.use_case_result == '通过':
                                            n = n + 1
            break
    if current_document_name != '':
        current_document_name = current_document_name + '/编号/' + current_id
    sub = {
        'id': 'A',
        'type': '需求文档',
        'source': current_document_name,
        'des': '在外观舒适性上令人愉悦的显示界面数量',
        'val': n
    }
    return sub


def uin1s_cd_B(require_document_list, use_case_document_list):
    current_document_name = ''
    current_id = ''
    n = 0
    for require_node in require_document_list:
        current_document_name = require_document_list[0].document_name
        if require_node.category == '体验' and require_node.require_description.find('显示界面外观舒适可以令人愉悦') != -1:
            current_id = require_node.id
            if require_node.associated_use_case_ID:
                for use_case_ID in require_node.associated_use_case_ID:
                    for use_case_node in use_case_document_list:
                        if use_case_node.id == use_case_ID:
                            n = n + 1
            if require_node.its_sons:
                for son_id in require_node.its_sons:
                    for require_son_node in require_document_list:
                        if son_id == require_son_node.id:
                            if require_son_node.associated_use_case_ID:
                                for use_case_ID in require_son_node.associated_use_case_ID:
                                    for use_case_node in use_case_document_list:
                                        if use_case_node.id == use_case_ID:
                                            n = n + 1
            break
    if current_document_name != '':
        current_document_name = current_document_name + '/用例编号'
    sub = {
        'id': 'B',
        'type': '用例文档',
        'source': current_document_name,
        'des': '显示界面数量',
        'val': n
    }
    return sub


def uac1g_cd_A(require_document_list, use_case_document_list):
    L = template_extract_situation_list(require_document_list, use_case_document_list, '体验', '以下功能可以支持特殊群体使用')
    L['id'] = 'A'
    L['des'] = '特殊群体用户成功使用的功能数量'
    return L


def uac1g_cd_B(require_document_list):
    L = template_extract_situation_list_len(require_document_list, '体验', '以下功能可以支持特殊群体使用')
    L['id'] = 'B'
    L['des'] = '实现的功能数量'
    return L


def uac2s_cd_A(require_document_list, use_case_document_list):
    L = template_extract_situation_list(require_document_list, use_case_document_list, '体验', '支持以下语种')
    L['id'] = 'A'
    L['des'] = '实际支持的语种数量'
    return L


def uac2s_cd_B(require_document_list):
    L = template_extract_situation_list_len(require_document_list, '体验', '支持以下语种')
    L['id'] = 'B'
    L['des'] = '需要支持的语种数量'
    return L


def rma1g_cd_A(require_document_list, bug_document_list):
    current_document_name = ''
    current_id = ''
    current_des = ''
    n = 0
    for require_node in require_document_list:
        if require_node.category == '其他' and require_node.require_description.find('可靠性相关的故障修复率') != -1:
            current_id = require_node.id
            current_des = template_what_i_hope(require_node.require_description)
            if require_node.associated_bug_ID:
                for bug_ID in require_node.associated_bug_ID:
                    for bug_node in bug_document_list:
                        current_document_name = bug_document_list[0].document_name
                        if bug_ID == bug_node.id and bug_node.solution == '已解决':
                            n = n + 1
    if current_document_name != '':
        current_document_name = current_document_name + '/Bug编号'
    sub = {
        'id': 'A',
        'type': 'Bug文档',
        'source': current_document_name,
        'des': '设计/编码/测试阶段修复的与可靠性相关故障数',
        'val': n
    }
    return sub


def rma1g_cd_B(require_document_list, bug_document_list):
    current_document_name = ''
    current_id = ''
    n = 0
    for require_node in require_document_list:
        if require_node.category == '其他' and require_node.require_description.find('可靠性相关的故障修复率') != -1:
            current_id = require_node.id
            if require_node.associated_bug_ID:
                for bug_ID in require_node.associated_bug_ID:
                    for bug_node in bug_document_list:
                        current_document_name = bug_document_list[0].document_name
                        if bug_ID == bug_node.id:
                            n = n + 1
    if current_document_name != '':
        current_document_name = current_document_name + '/Bug编号'
    sub = {
        'id': 'B',
        'type': 'Bug文档',
        'source': current_document_name,
        'des': '设计/编码/测试阶段检测到的与可靠性相关的故障数',
        'val': n
    }
    return sub


def rma2g_cd_A(require_document_list, use_case_document_list):
    need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '其他', '平均失效间隔时间', '运行时间')
    if need_in_situation == []:
        need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '其他',
                                                           '平均失效间隔时间', '观察周期时长')
    for each_one in need_in_situation:
        each_one['des'] = '第' + str(int(each_one['id']) + 1) + '次测试中的运行时间'
        each_one['id'] = 'A' + each_one['id']
    return need_in_situation


def rma2g_cd_B(require_document_list, use_case_document_list):
    need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '其他', '平均失效间隔时间', '失效次数')
    if need_in_situation == []:
        need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '其他',
                                                           '平均失效间隔时间', '失效数量')
    for each_one in need_in_situation:
        each_one['des'] = '第' + str(int(each_one['id']) + 1) + '次测试中，实际发生的系统/软件失效次数'
        each_one['id'] = 'B' + each_one['id']
    return need_in_situation


def rma2g_cd_X(require_document_list, use_case_document_list):
    need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '其他', '平均失效间隔时间', '平均失效间隔')
    for each_one in need_in_situation:
        each_one['des'] = '第' + str(int(each_one['id']) + 1) + '次测试中，平均失效间隔（MTBF）'
        each_one['id'] = 'X' + each_one['id']
    return need_in_situation


def rma3g_cd_A(require_document_list, use_case_document_list):
    need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '其他', '周期失效率', '失效数量')
    for each_one in need_in_situation:
        each_one['des'] = '第' + str(int(each_one['id']) + 1) + '次观察中，在观察时间内检测到的失效数量'
        each_one['id'] = 'A' + each_one['id']
    return need_in_situation


def rma3g_cd_B(require_document_list, use_case_document_list):
    need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '其他', '周期失效率', '观察周期')
    for each_one in need_in_situation:
        each_one['des'] = '第' + str(int(each_one['id']) + 1) + '次观察中的观察持续周期数'
        each_one['id'] = 'B' + each_one['id']
    return need_in_situation


def rma3g_cd_X(require_document_list, use_case_document_list):
    need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '其他', '周期失效率', '周期失效率')
    for each_one in need_in_situation:
        each_one['des'] = '第' + str(int(each_one['id']) + 1) + '次观察中的周期失效率'
        each_one['id'] = 'X' + each_one['id']
    return need_in_situation


def get_all_description_data(require_document_list, use_case_document_list):
    data_kind_dict = {'功能': ['用户文档和帮助机制中能描述以下功能', '为以下功能和操作规程支持用户定制', '能够监视以下功能状态', '可以支持特殊群体使用', '提供以下诊断功能', '系统以下用户功能的执行', '的以下产品功能'],
                      '场景': ['用户手册包含以下场景中系统使用方法'],
                      '任务': ['为以下任务提供演示功能', '以下交互式任务中操作结果与外观具有一致性', '以下任务中支持撤销操作或重新确认', '可以通过键盘、鼠标或语音等方法启动以下任务']}
    data_use_case = {}
    for data_kind_key in data_kind_dict:
        data_use_case[data_kind_key] = []
        kind_list = data_kind_dict[data_kind_key]
        for description_kind in kind_list:
            for require_node in require_document_list:
                if require_node.require_description.find(description_kind) != -1:
                    require_data_list = get_data_from_description(require_node.require_description)
                    data_betest_list = []
                    # 建立一个列表，里面存入的每个小列表为[data, 1或0，1++]，1则是关联了用例，0则没有，最后一位是一个data关联的用例个数
                    for data in require_data_list:
                        data_betest_list.append([data, 0])  # 默认是没关联
                    if require_node.associated_use_case_ID:
                        for use_case_ID in require_node.associated_use_case_ID:
                            for use_case_node in use_case_document_list:
                                if use_case_node.id == use_case_ID:
                                    actual_situation = re.split(r'\n', use_case_node.actual_situation)  # 去除\n
                                    for each_situation in actual_situation:
                                        for each_data_betest in data_betest_list:
                                            if each_situation.find(each_data_betest[0]) != -1:  # 找到关联用例了
                                                each_data_betest[1] = 1
                    for each_data_betest in data_betest_list:
                        no_exist = True
                        for each_one in data_use_case[data_kind_key]:
                            if each_one[0] == each_data_betest[0]:
                                each_one[1] = each_one[1] + each_data_betest[1]
                                each_one[2] = each_one[2] + 1
                                no_exist = False
                                break
                        if no_exist:
                            data_use_case[data_kind_key].append([each_data_betest[0], each_data_betest[1], 1])
                    break
    return data_use_case


def rma4s_cd_A(require_document_list, use_case_document_list):
    current_document_name = ''
    if require_document_list:
        current_document_name = require_document_list[0].document_name
    data_use_case = get_all_description_data(require_document_list, use_case_document_list)
    test_cover = ['功能', '场景', '任务']
    L = 0
    for test in test_cover:
        for key in data_use_case:
            if key == test:
                for each_list in data_use_case[key]:
                    L = L + each_list[1]/each_list[2]
                break
    if current_document_name != '':
        current_document_name = current_document_name + '/类别/(功能/场景/任务)'
    sub = {
        'id': 'A',
        'type': '需求文档',
        'source': current_document_name,
        'des': '实际所执行的系统或软件能力、运行场景或功能的数量',
        'val': L
    }
    return sub


def rma4s_cd_B(require_document_list, use_case_document_list):
    current_document_name = ''
    if require_document_list:
        current_document_name = require_document_list[0].document_name
    data_use_case = get_all_description_data(require_document_list, use_case_document_list)
    test_cover = ['功能', '场景', '任务']
    L = 0
    for test in test_cover:
        for key in data_use_case:
            if key == test:
                L = L + len(data_use_case[key])
    if current_document_name != '':
        current_document_name = current_document_name + '/类别/(功能/场景/任务)'
    sub = {
        'id': 'B',
        'type': '需求文档',
        'source': current_document_name,
        'des': '预期包含的系统或软件能力、运行场景或功能的数量',
        'val': L
    }
    return sub


def rav1g_cd_A(require_document_list, use_case_document_list):
    need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '其他', '内运行时间', '实际运行时间')
    for each_one in need_in_situation:
        each_one['des'] = '第' + str(int(each_one['id']) + 1) + '测试中，实际提供的系统运行时间'
        each_one['id'] = 'A' + each_one['id']
    return need_in_situation


def rav1g_cd_B(require_document_list):
    threshold, template, development_value = template_threshold_etc(require_document_list, '其他', '内运行时间')
    threshold['id'] = 'B'
    threshold['des'] = '操作计划中规定的系统运行时间'
    return threshold, template, development_value


def rav2g_cd_A(require_document_list, use_case_document_list):
    need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '其他', '平均宕机时间', '总的宕机时间')
    for each_one in need_in_situation:
        each_one['des'] = '第' + str(int(each_one['id']) + 1) + '次测试中，总的宕机时间'
        each_one['id'] = 'A' + each_one['id']
    return need_in_situation


def rav2g_cd_B(require_document_list, use_case_document_list):
    need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '其他', '平均宕机时间', '宕机的次数')
    for each_one in need_in_situation:
        each_one['des'] = '第' + str(int(each_one['id']) + 1) + '次测试中，观察到的宕机数量'
        each_one['id'] = 'B' + each_one['id']
    return need_in_situation


def rav2g_cd_X(require_document_list, use_case_document_list):
    need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '其他', '平均宕机时间', '平均宕机时间')
    for each_one in need_in_situation:
        each_one['des'] = '第' + str(int(each_one['id']) + 1) + '次测试中的平均宕机时间'
        each_one['id'] = 'X' + each_one['id']
    return need_in_situation


def rft1g_cd_A(require_document_list, use_case_document_list):
    n = template_use_case_pass(require_document_list, use_case_document_list, '其他', '能控制的故障模式数量')
    n['id'] = 'A'
    n['des'] = '避免发生关键和严重失效的次数（以测试用例为单位计算的数量）'
    return n


def rft1g_cd_B(require_document_list):
    n = template_associated_use_case_num(require_document_list, '其他', '能控制的故障模式数量')
    n['id'] = 'B'
    n['des'] = '测试中执行的故障模式（几乎导致失效）的测试用例数量'
    return n


def rft2s_cd_A():
    n = None
    return n


def rft2s_cd_B():
    n = None
    return n


def rft3s_cd_Ai(require_document_list, use_case_document_list):
    need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '其他', '发生故障到报告故障的时间间隔', '报告时刻')
    for each_one in need_in_situation:
        each_one['des'] = '系统报告故障' + str(int(each_one['id']) + 1) + '的时刻'
        each_one['id'] = 'A' + each_one['id']
    return need_in_situation


def rft3s_cd_Bi(require_document_list, use_case_document_list):
    need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '其他', '发生故障到报告故障的时间间隔', '故障被检测')
    for each_one in need_in_situation:
        each_one['des'] = '故障' + str(int(each_one['id']) + 1) + '被检测到的时刻'
        each_one['id'] ='B' + each_one['id']
    return need_in_situation


def rft3s_cd_Xi(require_document_list, use_case_document_list):
    need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '其他', '发生故障到报告故障的时间间隔', '时间间隔')
    for each_one in need_in_situation:
        each_one['des'] = '第' + str(int(each_one['id']) + 1) + '次测试中，系统平均故障通告时间'
        each_one['id'] = 'X' + each_one['id']
    return need_in_situation


def rre1g_cd_Ai(require_document_list, use_case_document_list):
    need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '其他', '从失效中恢复所需时间', '花费的总时间')
    for each_one in need_in_situation:
        each_one['des'] = '由于第' + str(int(each_one['id']) + 1) + '次失效而重新启动，并恢复宕机的软件/系统所花费的总时间'
        each_one['id'] = 'A' + each_one['id']
    return need_in_situation


def rre2s_cd_A(require_document_list, use_case_document_list):
    L = template_extract_situation_list(require_document_list, use_case_document_list, '其他', '以下数据项定期备份')
    L['id'] = 'A'
    L['des'] = '实际定期备份数据项的数量'
    return L


def rre2s_cd_B(require_document_list):
    L = template_extract_situation_list_len(require_document_list, '其他', '以下数据项定期备份')
    L['id'] = 'B'
    L['des'] = '需要备份的数据项的数量'
    return L


def sco1g_cd_A(require_document_list, use_case_document_list):
    L = template_whether_data_nopass(require_document_list, use_case_document_list, '安全', '以下数据项设置访问控制')
    L['id'] = 'A'
    L['des'] = '未经授权可访问的保密数据项的数量'
    return L


def sco1g_cd_B(require_document_list):
    L = template_extract_situation_list_len(require_document_list, '安全', '以下数据项设置访问控制')
    L['id'] = 'B'
    L['des'] = '需要访问控制的保密数据项的数量'
    return L


def sco2g_cd_A(require_document_list, use_case_document_list):
    L = template_extract_situation_list(require_document_list, use_case_document_list, '安全', '以下数据项设置加密/解密')
    L['id'] = 'A'
    L['des'] = '正确加密/解密的数据项数量'
    return L


def sco2g_cd_B(require_document_list):
    L = template_extract_situation_list_len(require_document_list, '安全', '以下数据项设置加密/解密')
    L['id'] = 'B'
    L['des'] = '需要加密/解密的数据项数量'
    return L


def sco3s_cd_A(require_document_list, use_case_document_list):
    n = template_use_case_pass(require_document_list, use_case_document_list, '安全', '使用的加密/解密算法经过严格审查')
    n['id'] = 'A'
    n['des'] = '使用时遭到破坏或存在不可接受风险的加密算法的数量'
    return n


def sco3s_cd_B(require_document_list):
    n = template_associated_use_case_num(require_document_list, '安全', '使用的加密/解密算法经过严格审查')
    n['id'] = 'B'
    n['des'] = '所使用的加密算法的数量'
    return n


def sin1g_cd_A(require_document_list, use_case_document_list):
    L = template_extract_situation_list(require_document_list, use_case_document_list, '安全', '能够避免遭受破坏和篡改')
    L['id'] = 'A'
    L['des'] = '因未经授权访问而破坏或篡改数据项的数量'
    return L


def sin1g_cd_B(require_document_list):
    L = template_extract_situation_list_len(require_document_list, '安全', '能够避免遭受破坏和篡改')
    L['id'] = 'B'
    L['des'] = '需要避免数据破坏或篡改的数据项数量'
    return L


def sin2g_cd_A(require_document_list, use_case_document_list):
    L = template_extract_situation_list(require_document_list, use_case_document_list, '安全', '采用以下方法用于数据抗讹误')
    L['id'] = 'A'
    L['des'] = '实际用于数据抗讹误性方法的数量'
    return L


def sin2g_cd_B(require_document_list):
    L = template_extract_situation_list_len(require_document_list, '安全', '采用以下方法用于数据抗讹误')
    L['id'] = 'B'
    L['des'] = '可用及推荐的用于数据讹误性方法的数量'
    return L


def sin3s_cd_A():
    n = None
    return n


def sin3s_cd_B():
    n = None
    return n


def sno1g_cd_A(require_document_list, use_case_document_list):
    L = template_extract_situation_list(require_document_list, use_case_document_list, '安全', '以下事务中使用数字签名确保抗抵赖性')
    L['id'] = 'A'
    L['des'] = '实际使用数字签名确保抗抵赖性事务的数量'
    return L


def sno1g_cd_B(require_document_list):
    L = template_extract_situation_list_len(require_document_list, '安全', '以下事务中使用数字签名确保抗抵赖性')
    L['id'] = 'B'
    L['des'] = '使用数字签名要求抗抵赖性事务的数量'
    return L


def sac1g_cd_A(require_document_list, use_case_document_list):
    need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '安全', '对系统或数据的访问以日志形式记录', '日志记录的访问次数')
    for each_one in need_in_situation:
        each_one['des'] = '第' + str(int(each_one['id']) + 1) + '次测试中，所有日志记录的访问次数'
        each_one['id'] = 'A' + each_one['id']
    return need_in_situation


def sac1g_cd_B(require_document_list, use_case_document_list):
    current_document_name = ''
    current_des = ''
    current_id_list = []
    if require_document_list and use_case_document_list:
        current_document_name = use_case_document_list[0].document_name
        need_in_situation = []
        for require_node in require_document_list:
            if require_node.category == '安全' and require_node.require_description.find('对系统或数据的访问以日志形式记录') != -1:
                current_id = require_node.id
                current_des = template_what_i_hope(require_node.require_description)
                if require_node.associated_use_case_ID:
                    for use_case_ID in require_node.associated_use_case_ID:
                        for use_case_node in use_case_document_list:
                            if use_case_node.id == use_case_ID and use_case_node.step != '':
                                actual_situation = re.split(r'\n|，|。', use_case_node.step)  # 去除\n
                                for each_situation in actual_situation:
                                    if each_situation.find('系统或数据的访问') != -1:
                                        if is_number(each_situation[0]):
                                            each_situation = re.sub('\d+\.', '', each_situation,
                                                                    1)  # 替换掉1. 并且只替换第一个（防止有效数字为1.X之类的被替换掉）

                                        # 如果没有单位
                                        ret = re.findall(r"\d+.\d+|\d+", each_situation)
                                        for each_one in ret:
                                            one = float(each_one)
                                            need_in_situation.append(one)
                                            if use_case_node.id not in current_id_list:
                                                current_id_list.append(use_case_node.id)
                break
    else:
        need_in_situation = None

    current_document_name_list = []
    if current_document_name != '':
        for current_id in current_id_list:
            current_document_name_list.append(current_document_name + '.编号.' + current_id)
    Ni = []
    for i, current_document_name in enumerate(current_document_name_list):
        Ni.append(
            {
                'id': 'B'+str(i),
                'type': '用例文档',
                'source': current_document_name,
                'des': '对系统或数据的访问次数',
                'val': need_in_situation[i]
            }
        )
    return Ni


def sac2s_cd_A(require_document_list, use_case_document_list):
    need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '安全', '日志存储在稳定存储器中时间', '日志实际存储时间')
    for each_one in need_in_situation:
        each_one['des'] = '第' + str(int(each_one['id']) + 1) + '次测试中，系统日志实际存储在稳定存储器中的时间'
        each_one['id'] = 'A' + each_one['id']
    return need_in_situation


def sac2s_cd_B(require_document_list):
    threshold, template, development_value = template_threshold_etc(require_document_list, '安全', '日志存储在稳定存储器中时间')
    threshold['id'] = 'B'
    threshold['des'] = '要求系统日志存储在稳定存储器中的时间'
    return threshold, template, development_value


def sau1g_cd_A(require_document_list, use_case_document_list):
    L = template_extract_situation_list(require_document_list, use_case_document_list, '安全', '提供以下鉴别机制')
    L['id'] = 'A'
    L['des'] = '提供鉴别机制的数量（例如用户ID/密码或IC卡）'
    return L


def sau1g_cd_B(require_document_list):
    L = template_extract_situation_list_len(require_document_list, '安全', '提供以下鉴别机制')
    L['id'] = 'B'
    L['des'] = '规定的鉴别机制数量'
    return L


def sau2s_cd_A(require_document_list, use_case_document_list):
    L = template_extract_situation_list(require_document_list, use_case_document_list, '安全', '包含以下鉴别规则')
    L['id'] = 'A'
    L['des'] = '已实现的鉴别规则的数量'
    return L


def sau2s_cd_B(require_document_list):
    L = template_extract_situation_list_len(require_document_list, '安全', '包含以下鉴别规则')
    L['id'] = 'B'
    L['des'] = '规定的鉴别规则的数量'
    return L


def mmo1g_cd_A():
    n = None
    return n


def mmo1g_cd_B():
    n = None
    return n


def mmo2s_cd_A():
    n = None
    return n


def mmo2s_cd_B():
    n = None
    return n


def mre1g_cd_A():
    n = None
    return n


def mre1g_cd_B():
    n = None
    return n


def mre2s_cd_A(require_document_list, use_case_document_list):
    L = template_extract_situation_list(require_document_list, use_case_document_list, '改进', '模块的实现遵循以下编码规则')
    L['id'] = 'A'
    L['des'] = '符合特定系统编码规则的软件模块数量'
    return L


def mre2s_cd_B():
    n = None
    return n

def mmo2s_cd_Xi(require_document_list):
    threshold, template, development_value = template_threshold_etc(require_document_list, '改进', '模块的圈复杂度得分')
    threshold['id'] = 'Xi'
    threshold['des'] = '模块要求的圈复杂度得分'
    return threshold, template, development_value

def man1g_cd_A(require_document_list, use_case_document_list):
    need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '改进', '操作期间记录审计追踪所需的日志', '日志条数')
    sum = 0
    if need_in_situation:
        for each_one in need_in_situation:
            sum += 1
        need_in_situation = need_in_situation[0]
        need_in_situation['val'] = sum
        need_in_situation['id'] = 'A'
        need_in_situation['des'] = '实际记录在系统中的日志条数'
    else:
        need_in_situation = []
    return need_in_situation


def man1g_cd_B(require_document_list, use_case_document_list):
    current_document_name = ''
    current_id = ''
    current_des = ''
    need_in_situation = []
    for require_node in require_document_list:
        current_document_name = require_document_list[0].document_name
        if require_node.category == '改进' and require_node.require_description.find('操作期间记录审计追踪所需的日志') != -1:
            current_id = require_node.id
            current_des = template_what_i_hope(require_node.require_description)
            if require_node.associated_use_case_ID:
                for use_case_ID in require_node.associated_use_case_ID:
                    for use_case_node in use_case_document_list:
                        if use_case_node.id == use_case_ID and use_case_node.expect != '':
                            expect = re.split(r'\n|，|。', use_case_node.expect)  # 去除\n
                            for each_situation in expect:
                                if each_situation.find('日志条数') != -1:
                                    if is_number(each_situation[0]):
                                        each_situation = re.sub('\d+\.', '', each_situation,
                                                                1)  # 替换掉1. 并且只替换第一个（防止有效数字为1.X之类的被替换掉）

                                    # 如果没有单位
                                    ret = re.findall(r"\d+.\d+|\d+", each_situation)
                                    for each_one in ret:
                                        one = float(each_one)
                                        need_in_situation.append(one)
            break
    if need_in_situation:
        B = sum(need_in_situation)
    else:
        B = 0
    if current_document_name != '':
        current_document_name = current_document_name + '/编号/' + current_id
    sub = {
        'id': 'B',
        'type': '需求文档',
        'source': current_document_name,
        'des': '操作期间审计跟踪所需的日志条数',
        'val': B
    }
    return sub


def man2s_cd_A(require_document_list, use_case_document_list):
    n = template_use_case_pass(require_document_list, use_case_document_list, '改进', '实现的诊断功能可以生成有效的原因分析')
    n['id'] = 'A'
    n['des'] = '对原因分析有效的诊断功能数量'
    return n


def man2s_cd_B(require_document_list):
    n = template_associated_use_case_num(require_document_list, '改进', '实现的诊断功能可以生成有效的原因分析')
    n['id'] = 'B'
    n['des'] = '已实现的诊断功能数量'
    return n


def man3s_cd_A(require_document_list, use_case_document_list):
    L = template_extract_situation_list(require_document_list, use_case_document_list, '改进', '提供以下诊断功能')
    L['id'] = 'A'
    L['des'] = '已实现的诊断功能数量'
    return L


def man3s_cd_B(require_document_list):
    L = template_extract_situation_list_len(require_document_list, '改进', '提供以下诊断功能')
    L['id'] = 'B'
    L['des'] = '需要实现的诊断功能数量'
    return L


# 从字符串中提取数字
def template_get_num_from_str(each_num):
    num = re.match(r"\d+", each_num)
    num = num.group()
    num = float(num)
    if each_num.find('s') != -1 or each_num.find('秒') != -1:
        num = num * 1000
    elif each_num.find('h') != -1 or each_num.find('时') != -1 or each_num.find('小时') != -1:
        num = num * 1000 * 3600
    elif each_num.find('d') != -1 or each_num.find('天') != -1:
        num = num * 1000 * 3600 * 24
    elif each_num.find('分钟') != -1:
        num = num * 1000 * 60
    return num


def mmd1g_cd_Ai(require_document_list, mission_document_list):
    current_document_name = ''
    current_id = ''
    current_des = ''
    actual_data_list = []
    current_id_list = []
    for require_node in require_document_list:
        if require_node.category == '改进' and require_node.require_description.find('对以下项目进行维护升级') != -1:
            current_id = require_node.id
            current_des = template_what_i_hope(require_node.require_description)
            if require_node.its_sons:
                for son_id in require_node.its_sons:
                    for son_node in require_document_list:
                        if son_node.id == son_id:
                            if son_node.associated_mission_ID:
                                for mission_ID in son_node.associated_mission_ID:
                                    for mission_node in mission_document_list:
                                        current_document_name = mission_document_list[0].document_name
                                        if mission_node.id == mission_ID:
                                            num = template_get_num_from_str(mission_node.initial_expectation)
                                            actual_data_list.append(num)
                                            if mission_node.id not in current_id_list:
                                                current_id_list.append(mission_node.id)
                            break

    current_document_name_list = []
    if current_document_name != '':
        for current_id in current_id_list:
            current_document_name_list.append(current_document_name + '/编号/' + current_id)
    Ni = []
    for i, current_document_name in enumerate(current_document_name_list):
        Ni.append(
            {
                'id': 'A'+str(i),
                'type': '任务文档',
                'source': current_document_name,
                'des': '对一个指定类型的修改'+str(i+1)+'所消耗的总工作时间',
                'val': actual_data_list[i]
            }
        )
    return Ni


def mmd1g_cd_Bi(require_document_list, mission_document_list):
    current_document_name = ''
    current_id = ''
    current_des = ''
    actual_data_list = []
    current_id_list = []
    for require_node in require_document_list:
        if require_node.category == '改进' and require_node.require_description.find('对以下项目进行维护升级') != -1:
            current_id = require_node.id
            if require_node.its_sons:
                for son_id in require_node.its_sons:
                    for son_node in require_document_list:
                        if son_node.id == son_id:
                            if son_node.associated_mission_ID:
                                for mission_ID in son_node.associated_mission_ID:
                                    for mission_node in mission_document_list:
                                        current_document_name = mission_document_list[0].document_name
                                        if mission_node.id == mission_ID:
                                            num = template_get_num_from_str(mission_node.total_consumption)
                                            actual_data_list.append(num)
                                            if mission_node.id not in current_id_list:
                                                current_id_list.append(mission_node.id)
                            break

    current_document_name_list = []
    if current_document_name != '':
        for current_id in current_id_list:
            current_document_name_list.append(current_document_name + '/编号/' + current_id)
    Ni = []
    for i, current_document_name in enumerate(current_document_name_list):
        Ni.append(
            {
                'id': 'B'+str(i),
                'type': '任务文档',
                'source': current_document_name,
                'des': '对一个指定类型的修改'+str(i+1)+'所消耗的预期时间',
                'val': actual_data_list[i]
            }
        )
    return Ni


def mmd1g_cd_n(require_document_list):
    current_document_name = ''
    current_id = ''
    n = 0
    for require_node in require_document_list:
        current_document_name = require_document_list[0].document_name
        if require_node.category == '改进' and require_node.require_description.find('对以下项目进行维护升级') != -1:
            current_id = require_node.id
            if require_node.its_sons:
                for son_id in require_node.its_sons:
                    for son_node in require_document_list:
                        if son_node.id == son_id:
                            if son_node.associated_mission_ID:
                                n = n + len(son_node.associated_mission_ID)
                            break
    if current_document_name != '':
        current_document_name = current_document_name + '.编号.' + current_id
    sub = {
        'id': 'n',
        'type': '需求文档',
        'source': current_document_name,
        'des': '测量的修改数量',
        'val': n
    }
    return sub


def mmd2g_cd_A(require_document_list, use_case_document_list):
    current_document_name = ''
    current_id = ''
    current_des = ''
    bug_beassociated = []
    for require_node in require_document_list:
        if require_node.category == '改进' and require_node.require_description.find('对以下项目进行维护升级') != -1:
            current_id = require_node.id
            if require_node.its_sons:
                for son_id in require_node.its_sons:
                    for son_node in require_document_list:
                        if son_node.id == son_id:
                            if son_node.associated_use_case_ID:
                                for use_case_ID in son_node.associated_use_case_ID:
                                    for use_case_node in use_case_document_list:
                                        current_document_name = use_case_document_list[0].document_name
                                        if use_case_node.id == use_case_ID and use_case_node.associated_bug_ID:
                                            for bug_ID in use_case_node.associated_bug_ID:
                                                if bug_ID not in bug_beassociated:
                                                    bug_beassociated.append(bug_ID)
                            break
    L = len(bug_beassociated)
    if current_document_name != '':
        current_document_name = current_document_name + '/用例编号'
    sub = {
        'id': 'A',
        'type': '用例文档',
        'source': current_document_name,
        'des': '在实施后的规定时间内，导致事故或失效发生的修改数量',
        'val': L
    }
    return sub

def mmd2g_cd_B(require_document_list):
    current_document_name = ''
    current_id = ''
    n = 0
    for require_node in require_document_list:
        current_document_name = require_document_list[0].document_name
        if require_node.category == '改进' and require_node.require_description.find('对以下项目进行维护升级') != -1:
            current_id = require_node.id
            if require_node.its_sons:
                for son_id in require_node.its_sons:
                    for son_node in require_document_list:
                        if son_node.id == son_id:
                            if son_node.associated_use_case_ID:
                                n = n + len(son_node.associated_use_case_ID)
                            break
    if current_document_name != '':
        current_document_name = current_document_name + '/编号/' + current_id
    sub = {
        'id': 'B',
        'type': '需求文档',
        'source': current_document_name,
        'des': '实施的修改数量',
        'val': n
    }
    return sub


def is_number(s):
    if s is not None:
        try:
            float(s)
            return True
        except ValueError:
            pass
        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass
    return False


# 获取时间信息，存储为字典
def template_get_time_dict(S):
    S = str(S)
    ret = re.split(r'/| |:|：|-|_|年|月|日|号', S)
    if ' ' in ret:
        ret.remove(' ')
    elif '' in ret:
        ret.remove('')
    dict = None
    if len(ret) <= 6:
        while len(ret) < 6:
            if len(ret) <= 2:
                ret.append('1')
            else:
                ret.append('0')
        if len(ret[5]) == 2 and ret[5][0] == '0':
            ret[5] = ret[5][1]
        dict = {'year': ret[0], 'month': ret[1], 'day': ret[2], 'hour': ret[3], 'minute': ret[4], 'second': ret[5]}
    for key in dict:
        if not is_number(dict[key]):
            dict = None
            break
    return dict


# 比较时间大小，dict1 大于 dict2 则为 True
def template_compare_time(dict1, dict2):
    if int(dict1['year']) > int(dict2['year']):
        result = 1
    elif int(dict1['year']) < int(dict2['year']):
        result = 2
    else:
        if int(dict1['month']) > int(dict2['month']):
            result = 1
        elif int(dict1['month']) < int(dict2['month']):
            result = 2
        else:
            if int(dict1['day']) > int(dict2['day']):
                result = 1
            elif int(dict1['day']) < int(dict2['day']):
                result = 2
            else:
                if int(dict1['hour']) > int(dict2['hour']):
                    result = 1
                elif int(dict1['hour']) < int(dict2['hour']):
                    result = 2
                else:
                    if int(dict1['minute']) > int(dict2['minute']):
                        result = 1
                    elif int(dict1['minute']) < int(dict2['minute']):
                        result = 2
                    else:
                        if int(dict1['second']) > int(dict2['second']):
                            result = 1
                        else:
                            result = 2
    if result == 1:
        result = True
    else:
        result = False
    return result


def mmd3s_cd_A(require_document_list):
    current_document_name = ''
    current_id = ''
    n = 0
    for require_node in require_document_list:
        current_document_name = require_document_list[0].document_name
        if require_node.category == '改进' and require_node.require_description.find('对以下项目进行维护升级') != -1:
            current_id = require_node.id
            ret = re.findall(r"我希望在(.+)到(.+)内对以下项目进行维护升级", require_node.require_description)  # 贪婪
            begin_time = template_get_time_dict(ret[0][0])
            end_time = template_get_time_dict(ret[0][1])
            if require_node.its_sons:
                for son_ID in require_node.its_sons:
                    for son_node in require_document_list:
                        if son_ID == son_node.id:
                            close_time = template_get_time_dict(son_node.close_time)
                            if template_compare_time(end_time, close_time):
                                n = n + 1
            break
    if current_document_name != '':
        current_document_name = current_document_name + '/编号/' + current_id
    sub = {
        'id': 'A',
        'type': '需求文档',
        'source': current_document_name,
        'des': '在指定的持续时间内实际做出修改的项目数',
        'val': n
    }
    return sub


def mmd3s_cd_B(require_document_list):
    L = template_extract_situation_list_len(require_document_list, '改进', '对以下项目进行维护升级')
    L['id'] = 'B'
    L['des'] = '在指定的持续时间内要求修改的项目数'
    return L


def mte1g_cd_A(require_document_list, use_case_document_list):
    need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '改进', '系统中测试功能的数量', '已实现的测试功能')
    for each_one in need_in_situation:
        each_one['des'] = '第' + str(int(each_one['id']) + 1) + '次测试中，按照规定已实现的测试功能数量'
        each_one['id'] = 'A' + each_one['id']
    return need_in_situation


def mte1g_cd_B(require_document_list):
    threshold, template, development_value = template_threshold_etc(require_document_list, '改进', '系统中测试功能的数量')
    threshold['id'] = 'B'
    threshold['des'] = '需要的测试功能的数量'
    return threshold, template, development_value


def mte2s_cd_A(use_case_document_list):
    current_document_name = ''
    n = 0
    for use_case_node in use_case_document_list:
        current_document_name = use_case_document_list[0].document_name
        if use_case_node.precondition:
            if use_case_node.precondition.find('测试依赖的系统') != -1:
                if use_case_node.key_word:
                    if use_case_node.key_word.find('桩模拟') != -1:
                        n = n + 1
    if current_document_name != '':
        current_document_name = current_document_name + '/预期'
    sub = {
        'id': 'A',
        'type': '用例文档',
        'source': current_document_name,
        'des': '在依赖其他系统测试时，能被桩模拟的测试数量',
        'val': n
    }
    return sub


def mte2s_cd_B(use_case_document_list):
    current_document_name = ''
    n = 0
    for use_case_node in use_case_document_list:
        current_document_name = use_case_document_list[0].document_name
        if use_case_node.precondition:
            if use_case_node.precondition.find('测试依赖的系统') != -1:
                n = n + 1
    if current_document_name != '':
        current_document_name = current_document_name + '/预期'
    sub = {
        'id': 'B',
        'type': '用例文档',
        'source': current_document_name,
        'des': '依赖其他系统的测试数量',
        'val': n
    }
    return sub


def mte3s_cd_A(use_case_document_list):
    current_document_name = ''
    n = 0
    for use_case_node in use_case_document_list:
        current_document_name = use_case_document_list[0].document_name
        if use_case_node.key_word:
            if use_case_node.key_word.find('可重启动') != -1 and use_case_node.associated_bug_ID == []:
                n = n + 1
    if current_document_name != '':
        current_document_name = current_document_name + '/关键词'
    sub = {
        'id': 'A',
        'type': '用例文档',
        'source': current_document_name,
        'des': '在逐步检测的期望点，维护方能够暂停并重启执行中的测试运行的事例数',
        'val': n
    }
    return sub


def mte3s_cd_B(use_case_document_list):
    current_document_name = ''
    n = 0
    for use_case_node in use_case_document_list:
        current_document_name = use_case_document_list[0].document_name
        if use_case_node.key_word:
            if use_case_node.key_word.find('可重启动') != -1:
                n = n + 1
    if current_document_name != '':
        current_document_name = current_document_name + '/关键词'
    sub = {
        'id': 'A',
        'type': '用例文档',
        'source': current_document_name,
        'des': '执行中的测试运行能被暂停的事例数',
        'val': n
    }
    return sub



def pad1g_cd_A(require_document_list, use_case_document_list):
    current_document_name = ''
    current_id = ''
    n = 0
    for require_node in require_document_list:
        if require_node.category == '其他' and require_node.require_description.find('以下硬件环境中功能达到要求') != -1:
            current_id = require_node.id
            if require_node.associated_use_case_ID:
                for use_case_ID in require_node.associated_use_case_ID:
                    for use_case_node in use_case_document_list:
                        current_document_name = use_case_document_list[0].document_name
                        if use_case_node.id == use_case_ID and use_case_node.use_case_result != '通过':
                            n = n + 1
            break
    if current_document_name != '':
        current_document_name = current_document_name + '/结果'
    sub = {
        'id': 'A',
        'type': '测试文档',
        'source': current_document_name,
        'des': '测试期间未完成或结果没有达到要求的功能数量',
        'val': n
    }
    return sub


def pad1g_cd_B(require_document_list, use_case_document_list):
    current_document_name = ''
    current_id = ''
    n = 0
    for require_node in require_document_list:
        current_document_name = require_document_list[0].document_name
        if require_node.category == '其他' and require_node.require_description.find('以下硬件环境中功能达到要求') != -1:
            current_id = require_node.id
            if require_node.associated_use_case_ID:
                for use_case_ID in require_node.associated_use_case_ID:
                    for use_case_node in use_case_document_list:
                        if use_case_node.id == use_case_ID:
                            n = n + 1
            break
    if current_document_name != '':
        current_document_name = current_document_name + '/编号' + current_id
    sub = {
        'id': 'B',
        'type': '需求文档',
        'source': current_document_name,
        'des': '不同硬件环境中需要测试的功能数量',
        'val': n
    }
    return sub


def pad2g_cd_A(require_document_list, use_case_document_list):
    current_document_name = ''
    current_id = ''
    n = 0
    for require_node in require_document_list:
        if require_node.category == '其他' and require_node.require_description.find('以下软件环境中功能达到要求') != -1:
            current_id = require_node.id
            if require_node.associated_use_case_ID:
                for use_case_ID in require_node.associated_use_case_ID:
                    for use_case_node in use_case_document_list:
                        current_document_name = use_case_document_list[0].document_name
                        if use_case_node.id == use_case_ID and use_case_node.use_case_result != '通过':
                            n = n + 1
            break
    if current_document_name != '':
        current_document_name = current_document_name + '/结果'
    sub = {
        'id': 'A',
        'type': '测试文档',
        'source': current_document_name,
        'des': '测试期间未完成或结果没有达到要求的功能数量',
        'val': n
    }
    return sub


def pad2g_cd_B(require_document_list, use_case_document_list):
    current_document_name = ''
    current_id = ''
    n = 0
    for require_node in require_document_list:
        current_document_name = require_document_list[0].document_name
        if require_node.category == '其他' and require_node.require_description.find('以下软件环境中功能达到要求') != -1:
            current_id = require_node.id
            if require_node.associated_use_case_ID:
                for use_case_ID in require_node.associated_use_case_ID:
                    for use_case_node in use_case_document_list:
                        if use_case_node.id == use_case_ID:
                            n = n + 1
            break
    if current_document_name != '':
        current_document_name = current_document_name + '/编号' + current_id
    sub = {
        'id': 'B',
        'type': '需求文档',
        'source': current_document_name,
        'des': '不同系统软件环境下需要测试的功能数量',
        'val': n
    }
    return sub


def pad3s_cd_A(require_document_list, use_case_document_list):
    current_document_name = ''
    current_id = ''
    n = 0
    for require_node in require_document_list:
        if require_node.category == '其他' and require_node.require_description.find('以下运营环境中功能达到要求') != -1:
            current_id = require_node.id
            if require_node.associated_use_case_ID:
                for use_case_ID in require_node.associated_use_case_ID:
                    for use_case_node in use_case_document_list:
                        current_document_name = use_case_document_list[0].document_name
                        if use_case_node.id == use_case_ID and use_case_node.use_case_result != '通过':
                            n = n + 1
            break
    if current_document_name != '':
        current_document_name = current_document_name + '/结果'
    sub = {
        'id': 'A',
        'type': '测试文档',
        'source': current_document_name,
        'des': '在带有用户环境的运营测试中，测试期间没有完成或结果没有达到要求的功能数量',
        'val': n
    }
    return sub


def pad3s_cd_B(require_document_list, use_case_document_list):
    current_document_name = ''
    current_id = ''
    n = 0
    for require_node in require_document_list:
        current_document_name = require_document_list[0].document_name
        if require_node.category == '其他' and require_node.require_description.find('以下运营环境中功能达到要求') != -1:
            current_id = require_node.id
            if require_node.associated_use_case_ID:
                for use_case_ID in require_node.associated_use_case_ID:
                    for use_case_node in use_case_document_list:
                        if use_case_node.id == use_case_ID:
                            n = n + 1
            break
    if current_document_name != '':
        current_document_name = current_document_name + '/编号' + current_id
    sub = {
        'id': 'B',
        'type': '需求文档',
        'source': current_document_name,
        'des': '在不同运营环境中测试中的功能数量',
        'val': n
    }
    return sub


def pin1g_cd_Ai(require_document_list, use_case_document_list):
    need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '其他', '安装所需时间', '安装消耗的总时间')
    for each_one in need_in_situation:
        each_one['des'] = '第' + str(int(each_one['id']) + 1) + '次安装所消耗的总工作时间'
        each_one['id'] = 'A' + each_one['id']
    return need_in_situation


def pin1g_cd_Bi(require_document_list, use_case_document_list):  # 从实际情况中提取数字
    current_document_name = ''
    current_id = ''
    need_in_situation = []
    current_id_list = []
    for require_node in require_document_list:
        if require_node.category == '其他' and require_node.require_description.find('安装所需时间') != -1:
            current_id = require_node.id
            if require_node.associated_use_case_ID:
                for use_case_ID in require_node.associated_use_case_ID:
                    for use_case_node in use_case_document_list:
                        current_document_name = use_case_document_list[0].document_name
                        if use_case_node.id == use_case_ID and use_case_node.expect != '':
                            actual_expect = re.split(r'\n', use_case_node.expect)  # 去除\n
                            for each_expect in actual_expect:
                                if each_expect.find('安装的预期时间') != -1:
                                    if is_number(each_expect[0]):
                                        each_expect = re.sub('\d+\.', '', each_expect,
                                                                1)  # 替换掉1. 并且只替换第一个（防止有效数字为1.X之类的被替换掉）

                                        # 判断实际情况中是不是描述时间（时分秒）
                                    ret_hms = re.findall(r"(\d+?)时(\d+?)分(\d+?)秒", each_expect)
                                    if ret_hms:
                                        for each_time in ret_hms:
                                            time = float(each_time[0]) * 3600 + float(each_time[1]) * 60 + float(
                                                each_time[2])
                                            time = time * 1000  # 统一成毫秒
                                            need_in_situation.append(time)
                                            if use_case_node.id not in current_id_list:
                                                current_id_list.append(use_case_node.id)
                                        break

                                    # 判断实际情况中是不是描述时间（分秒）
                                    ret_m_s = re.findall(r"(\d+?)分(\d+?)秒", each_expect)
                                    if ret_m_s:
                                        for each_time in ret_m_s:
                                            time = float(each_time[0]) * 60 + float(each_time[1])
                                            time = time * 1000  # 统一成毫秒
                                            need_in_situation.append(time)
                                            if use_case_node.id not in current_id_list:
                                                current_id_list.append(use_case_node.id)
                                        break

                                    # 判断实际情况中是不是描述时间（秒）
                                    ret_s = re.findall(r"\d+.\d+s|\d+s|\d+.\d+秒|\d+秒", each_expect)
                                    if ret_s:
                                        for each_time in ret_s:
                                            time = re.match(r'\d+.\d+|\d+', each_time)
                                            time = float(time.group()) * 1000  # 统一成毫秒
                                            need_in_situation.append(time)
                                            if use_case_node.id not in current_id_list:
                                                current_id_list.append(use_case_node.id)
                                        break

                                    # 判断实际情况中是不是描述时间（毫秒）
                                    ret_ms = re.findall(r"\d+.\d+ms|\d+ms|\d+.\d+毫秒|\d+毫秒", each_expect)
                                    if ret_ms:
                                        for each_time in ret_ms:
                                            time = re.match(r'\d+.\d+|\d+', each_time)
                                            time = float(time.group())
                                            need_in_situation.append(time)
                                            if use_case_node.id not in current_id_list:
                                                current_id_list.append(use_case_node.id)
                                        break

                                    # 判断实际情况中是不是描述百分比（%）
                                    ret_percent = re.findall(r"\d+.\d+%|\d+%|百分之\d+.\d+|百分之\d+", each_expect)
                                    if ret_percent:
                                        for each_percent in ret_percent:
                                            time = re.match(r'\d+.\d+|\d+', each_percent)
                                            time_group = time.group()
                                            time = float(time_group) * 0.01
                                            need_in_situation.append(time)
                                            if use_case_node.id not in current_id_list:
                                                current_id_list.append(use_case_node.id)
                                        break

                                    # 判断实际情况中是不是描述时间（小时）
                                    ret_h = re.findall(r"\d+.\d+h|\d+h|\d+.\d+小时|\d+小时", each_expect)
                                    if ret_h:
                                        for each_time in ret_h:
                                            time = re.match(r'\d+.\d+|\d+', each_time)
                                            time = float(time.group()) * 3600 * 1000  # 统一成毫秒
                                            need_in_situation.append(time)
                                            if use_case_node.id not in current_id_list:
                                                current_id_list.append(use_case_node.id)
                                        break

                                    # 判断实际情况中是不是描述时间（分钟）
                                    ret_m = re.findall(r"\d+.\d+分钟|\d+分钟|\d+.\d+min|\d+min", each_expect)
                                    if ret_m:
                                        for each_time in ret_m:
                                            time = re.match(r'\d+.\d+|\d+', each_time)
                                            time = float(time.group()) * 60 * 1000  # 统一成毫秒
                                            need_in_situation.append(time)
                                            if use_case_node.id not in current_id_list:
                                                current_id_list.append(use_case_node.id)
                                        break

                                    # 判断实际情况中是不是描述时间（天）
                                    ret_d = re.findall(r"\d+.\d+天|\d+天|\d+.\d+d|\d+d", each_expect)
                                    if ret_d:
                                        for each_time in ret_d:
                                            time = re.match(r'\d+.\d+|\d+', each_time)
                                            time = float(time.group()) * 24 * 3600 * 1000  # 统一成毫秒
                                            need_in_situation.append(time)
                                            if use_case_node.id not in current_id_list:
                                                current_id_list.append(use_case_node.id)
                                        break

                                    # 如果没有单位
                                    if ret_hms == [] and ret_s == [] and ret_ms == [] and ret_percent == []:
                                        ret = re.findall(r"\d+.\d+|\d+", each_expect)
                                        for each_one in ret:
                                            one = float(each_one)
                                            need_in_situation.append(one)
                                            if use_case_node.id not in current_id_list:
                                                current_id_list.append(use_case_node.id)
                            break
            break
    current_document_name_list = []
    if current_document_name != '':
        for current_id in current_id_list:
            current_document_name_list.append(current_document_name + '/编号/' + current_id)
    Ni = []
    for i, current_document_name in enumerate(current_document_name_list):
        Ni.append(
            {
                'id': 'B'+str(i),
                'type': '用例文档',
                'source': current_document_name,
                'des': '第'+str(i+1)+'次安装的预期时间',
                'val': need_in_situation[i]
            }
        )
    return Ni


def pin1g_cd_n(require_document_list):
    n = template_associated_use_case_num(require_document_list, '其他', '安装所需时间')
    n['id'] = 'n'
    n['des'] = '测量的安装次数'
    return n


def pin2g_cd_A(require_document_list, use_case_document_list):
    need_in_situation = template_extract_situation_num(require_document_list, use_case_document_list, '其他', '自定义安装规程的数量', '成功自定义的安装规程数')
    for each_one in need_in_situation:
        each_one['des'] = '第' + str(int(each_one['id']) + 1) + '次测试中，用户成功自定义安装的规程的数量'
        each_one['id'] = 'A' + each_one['id']
    return need_in_situation


def pin2g_cd_B(require_document_list):
    threshold, template, development_value = template_threshold_etc(require_document_list, '其他', '自定义安装规程的数量')
    threshold['id'] = 'B'
    threshold['des'] = '为使用方便，用户尝试自定义安装规程的数量'
    return threshold, template, development_value


def pre1g_cd_A(require_document_list, use_case_document_list):
    L = template_extract_situation_list(require_document_list, use_case_document_list, '其他', '以下用户功能的执行与')
    L['id'] = 'A'
    L['des'] = '替换原软件产品后，本软件产品在没有任何额外学习或变通的情况下，能够执行的用户功能数量'
    return L


def pre1g_cd_B(require_document_list):
    L = template_extract_situation_list_len(require_document_list, '其他', '以下用户功能的执行与')
    L['id'] = 'B'
    L['des'] = '替换原软件产品后，本软件产品中用户功能数量'
    return L


def pre2s_cd_A(require_document_list, use_case_document_list):
    L = template_extract_situation_list(require_document_list, use_case_document_list, '其他', '以下质量测度优于或等于')
    L['id'] = 'A'
    L['des'] = '优于或等于被替换产品的新产品质量测度数量'
    return L


def pre2s_cd_B(require_document_list):
    L = template_extract_situation_list_len(require_document_list, '其他', '以下质量测度优于或等于')
    L['id'] = 'B'
    L['des'] = '被替换软件产品中的质量测度数量'
    return L


def pre3s_cd_A(require_document_list, use_case_document_list):
    L = template_extract_situation_list(require_document_list, use_case_document_list, '其他', '的以下产品功能')
    L['id'] = 'A'
    L['des'] = '结果与被替换软件产品相似的产品功能数量'
    return L


def pre3s_cd_B(require_document_list):
    L = template_extract_situation_list_len(require_document_list, '其他', '的以下产品功能')
    L['id'] = 'B'
    L['des'] = '被替换软件产品中需要使用的功能数量'
    return L


def pre4s_cd_A(require_document_list, use_case_document_list):
    L = template_extract_situation_list(require_document_list, use_case_document_list, '其他', '一样使用以下数据')
    L['id'] = 'A'
    L['des'] = '能像被替换软件产品一样继续使用的数据数量'
    return L


def pre4s_cd_B(require_document_list):
    L = template_extract_situation_list_len(require_document_list, '其他', '一样使用以下数据')
    L['id'] = 'B'
    L['des'] = '被替换软件产品中需要继续使用的数据数量'
    return L
