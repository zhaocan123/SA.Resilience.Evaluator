import json
import copy
MIN_REVERSE_LIST = ['平均响应时间', '响应时间的充分性', '平均周转时间', '周转时间的充分性', '处理器平均占用率', '内存平均占用率', 'I/O设备平均占用率',
                    '带宽占用率', '周期失效率', '平均宕机时间', '组件的冗余度', '平均故障通告时间', '平均恢复时间', '修改的效率', '安装的时间效率']


def get_metric_checked(metric_25000, metric_selected):
    temp = {}
    for level_one in metric_selected.keys():
        for level_two in metric_selected[level_one].keys():
            for level_three in metric_selected[level_one][level_two].keys():
                if metric_25000[level_one][level_two][level_three] is not None:
                    if level_one not in temp.keys():
                        temp[level_one] = {}
                    if level_two not in temp[level_one].keys():
                        temp[level_one][level_two] = {}
                    temp[level_one][level_two][level_three] = metric_25000[level_one][level_two][level_three]
    return temp


def get_over_one(metric):
    over_one = ["平均响应时间", "响应时间的充分性", "平均周转时间", "周转时间充分性",
                "平均吞吐量", "事务处理容量", "用户访问量", "用户访问增长的充分性",
                "平均失效间隔时间(MTBF)", "周期失效率", "平均故障通告时间", "平均恢复时间", "修改的效率", "安装的时间效率"]
    ret = []
    for level_one in metric:
        for level_two in level_one["subMetric"]:
            for level_three in level_two["subMetric"]:
                if level_three["name"] in over_one:
                    ret.append(level_three["name"])
    return ret


def normalization(metric, over_one_value):
    for level_one in metric:
        for level_two in level_one["subMetric"]:
            for level_three in level_two["subMetric"]:
                if level_three["name"] in over_one_value.keys():
                    val = level_three["val"]
                    min_val = over_one_value[level_three["name"]]["min"]
                    max_val = over_one_value[level_three["name"]]["max"]
                    level_three["normalized_val"] = (val-min_val)/(max_val-min_val)
    return metric


metric_25000_test = {
    '功能性': {
        '功能完备性': {
            '功能覆盖率': None
        },
        '功能正确性': {
            '功能正确性 ': None
        },
        '功能适合性': {
            '使用目标的功能适合性': None,
            '系统的功能适合性': None
        }
    },
    '性能效率': {
        '时间特性': {
            '平均响应时间': None,
            '响应时间的充分性': None,
            '平均周转时间': None,
            '周转时间充分性': None,
            '平均吞吐量': None
        },
        '资源利用性': {
            '处理器平均占用率': None,
            '内存平均占用率': None,
            'I/O设备平均占用率': None,
            '带宽占用率': None
        },
        '容量': {
            '事务处理容量': 1,
            '用户访问量': 1,
            '用户访问增长的充分性': 1
        }
    }
}


metric_selected = {
    '功能性': {
        '功能完备性': {
            '功能覆盖率': 1
        },
        '功能正确性': {
            '功能正确性 ': 1
        },
        '功能适合性': {
            '使用目标的功能适合性': 2,
            '系统的功能适合性': 1
        }
    },
    '性能效率': {
        '时间特性': {
            '平均响应时间': 2,
            '响应时间的充分性': 1,
            '平均周转时间': 2,
            '周转时间充分性': 0.0,
            '平均吞吐量': 3
        },
        '资源利用性': {
            '处理器平均占用率': 1,
            '内存平均占用率': 1,
            'I/O设备平均占用率': 2,
            '带宽占用率': 1
        },
        '容量': {
            '事务处理容量': 1,
            '用户访问量': 1,
            '用户访问增长的充分性': 1
        }
    }
}


# rst = get_metric_checked(metric_25000_test, metric_selected)
# print(json.dumps(rst, indent=2, ensure_ascii=False))
