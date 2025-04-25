import json
import copy


def getproject(oldproject, newproject, oldindex, newindex):
    '''

    :param oldproject: 项目信息
    :param newproject:
    :return:
    '''
    systemLevel = dict()
    versionSelected = {}
    projectName = oldproject['projectInfo']['projectName']
    fileNumber = oldproject['projectInfo']['fileNumber']
    functionNumber = oldproject['projectInfo']['functionNumber']
    loc = oldproject['projectInfo']['codeInfo']['codeLine']
    versionSelected['name'] = projectName
    versionSelected['fileNum'] = fileNumber
    versionSelected['functionNum'] = functionNumber
    versionSelected['codeNum'] = loc
    systemLevel['versionSelected'] = versionSelected
    versionLatest = {}
    projectName = newproject['projectInfo']['projectName']
    fileNumber = newproject['projectInfo']['fileNumber']
    functionNumber = newproject['projectInfo']['functionNumber']
    loc = newproject['projectInfo']['codeInfo']['codeLine']
    versionLatest['name'] = projectName
    versionLatest['fileNum'] = fileNumber
    versionLatest['functionNum'] = functionNumber
    versionLatest['codeNum'] = loc
    systemLevel['versionLatest'] = versionLatest

    # oldpath = 'saolei725010.json'
    # newpath = 'saolei7250101.json'
    systemLevel['indexInformation'], systemLevel['designInformation'] = get_index_info(oldindex, newindex)
    return systemLevel


def getprojectCPP(oldproject, newproject, oldindex, newindex):
    '''

    :param oldproject: 项目信息
    :param newproject:
    :return:
    '''
    systemLevel = dict()
    versionSelected = {}
    projectName = oldproject['projectInfo']['projectName']
    fileNumber = oldproject['projectInfo']['fileNumber']
    classNumber = 0
    for i in oldproject['codeFileInfo'].keys():
        # print(i)
        classNumber += len(oldproject['codeFileInfo'][i]['classList'])
    loc = oldproject['projectInfo']['codeInfo']['codeLine']
    versionSelected['name'] = projectName
    versionSelected['fileNum'] = fileNumber
    versionSelected['classNum'] = classNumber
    versionSelected['codeNum'] = loc
    systemLevel['versionSelected'] = versionSelected
    versionLatest = {}
    projectName = newproject['projectInfo']['projectName']
    fileNumber = newproject['projectInfo']['fileNumber']
    classNumber = 0
    for i in newproject['codeFileInfo']:
        classNumber += len(newproject['codeFileInfo'][i]['classList'])
    loc = newproject['projectInfo']['codeInfo']['codeLine']
    versionLatest['name'] = projectName
    versionLatest['fileNum'] = fileNumber
    versionLatest['classNum'] = classNumber
    versionLatest['codeNum'] = loc
    systemLevel['versionLatest'] = versionLatest

    # oldpath = 'saolei725010.json'
    # newpath = 'saolei7250101.json'
    systemLevel['indexInformation'], systemLevel['designInformation'] = get_index_info(oldindex, newindex)
    return systemLevel


def get_index_info(oldindex, newindex):
    '''
    25010指标
    :param oldindex:
    :param newindex:
    :return:
    '''

    oldvalue = {}
    # f = open(oldpath, 'r')
    # content = f.read()
    # olddata = json.loads(content)
    # f.close()
    get_index_value(oldindex['25010'], oldvalue)
    newvalue = {}
    # f = open(newpath, 'r')
    # content = f.read()
    # newdata = json.loads(content)
    # f.close()
    get_index_value(newindex['25010'], newvalue)

    indexInformation = []

    for key in oldvalue.keys():
        if key in newvalue.keys():
            tmp = {}
            tmp['indexName'] = key
            tmp['versionSelected'] = oldvalue[key]
            tmp['versionLatest'] = newvalue[key]
            tmp['trend'] = 2
            if oldvalue[key] > newvalue[key]:
                tmp['trend'] = 0
            elif oldvalue[key] < newvalue[key]:
                tmp['trend'] = 1
            # tmp['standardValue'] = '(0,1)'
            tmp['minimumValue'] = 0
            tmp['maximumValue'] = 1
            tmp['result'] = 0
            if 0 <= oldvalue[key] <= 1 and 0 <= newvalue[key] <= 1:
                tmp['result'] = 1
            indexInformation.append(copy.deepcopy(tmp))
        else:
            tmp = {}
            tmp['indexName'] = key
            tmp['versionSelected'] = oldvalue[key]
            tmp['versionLatest'] = None
            tmp['trend'] = 0
            tmp['minimumValue'] = 0
            tmp['maximumValue'] = 1
            tmp['result'] = 0
            indexInformation.append(copy.deepcopy(tmp))

    for key in newvalue.keys():
        if key not in oldvalue.keys():
            tmp = {}
            tmp['indexName'] = key
            tmp['versionSelected'] = None
            tmp['versionLatest'] = newvalue[key]
            tmp['trend'] = 1
            tmp['minimumValue'] = 0
            tmp['maximumValue'] = 1
            tmp['result'] = 0
            indexInformation.append(copy.deepcopy(tmp))

    # 获取设计质量指标
    design_metrics_keys = ["modifiability", "scalability", "testability", "refundability", "comprehensibility"]
    oldvalue = {}
    for key in design_metrics_keys:
        oldvalue[key] = oldindex['design_metrics']['metrix'][key]['value']
    newvalue = {}
    for key in design_metrics_keys:
        newvalue[key] = newindex['design_metrics']['metrix'][key]['value']

    designInformation = []
    for key in oldvalue.keys():
        if key in newvalue.keys():
            tmp = {}
            tmp['indexName'] = key
            tmp['versionSelected'] = oldvalue[key]
            tmp['versionLatest'] = newvalue[key]
            tmp['trend'] = 2
            if oldvalue[key] > newvalue[key]:
                tmp['trend'] = 0
            elif oldvalue[key] < newvalue[key]:
                tmp['trend'] = 1
            tmp['minimumValue'] = 0
            tmp['maximumValue'] = 1
            tmp['result'] = 0
            if 0 <= oldvalue[key] <= 1 and 0 <= newvalue[key] <= 1:
                tmp['result'] = 1
            designInformation.append(copy.deepcopy(tmp))
        else:
            tmp = {}
            tmp['indexName'] = key
            tmp['versionSelected'] = oldvalue[key]
            tmp['versionLatest'] = None
            tmp['trend'] = 0
            tmp['minimumValue'] = 0
            tmp['maximumValue'] = 1
            tmp['result'] = 0
            designInformation.append(copy.deepcopy(tmp))
    for key in newvalue.keys():
        if key not in oldvalue.keys():
            tmp = {}
            tmp['indexName'] = key
            tmp['versionSelected'] = None
            tmp['versionLatest'] = newvalue[key]
            tmp['trend'] = 1
            tmp['minimumValue'] = 0
            tmp['maximumValue'] = 1
            tmp['result'] = 0
            designInformation.append(copy.deepcopy(tmp))

    return indexInformation, designInformation


def get_index_value(data, value_dict):

    for key in data.keys():
        if 'val' in data[key].keys():
            if data[key]['val'] is not None:
                value_dict[key] = round(data[key]['val'], 3)
        else:
            get_index_value(data[key], value_dict)


if __name__ == '__main__':
    f = open('main.json', 'r')
    content = f.read()
    a = json.loads(content)
    olddata = a
    f.close()
    f = open('main1.json', 'r')
    content = f.read()
    a = json.loads(content)
    newdata = a
    f.close()
    projectlevel = getproject(olddata, newdata)
    print(projectlevel)
    projectlevelCPP = getprojectCPP(olddata, newdata)
    print(projectlevelCPP)

    data = json.dumps(projectlevel, indent=4, ensure_ascii=False)
    with open('code/pre/projectinfo.json', 'w', newline='\n') as f:
        f.write(data)
