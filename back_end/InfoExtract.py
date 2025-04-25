import copy


def InfoExtract(Info):
    result = {}
    projectInfo = Info['projectInfo']

    fileProp = []
    # for filetype in projectInfo['fileTypes'].keys():
    #     temp = {}
    #     temp['name'] = filetype
    #     temp['value'] = len(projectInfo['fileTypes'][filetype])
    #     fileProp.append(copy.deepcopy(temp))
    filetypedict = {}
    for fileType in projectInfo['fileTypes'].keys():
        if fileType == 'other':
            continue
        for filename in projectInfo['fileTypes'][fileType]:
            suffix = filename.split('.')[-1]
            if suffix in filetypedict:
                filetypedict[suffix] += 1

            else:
                filetypedict[suffix] = 1

    for key in filetypedict.keys():
        temp = {}
        temp['name'] = key
        temp['value'] = filetypedict[key]
        fileProp.append(copy.deepcopy(temp))
    # fileProp.append({'name': 'other',
    #                  'value': len(projectInfo['fileTypes']['other'])
    #                  })

    result['fileProp'] = fileProp
    result['dirNumber'] = 10
    result['fileNumber'] = projectInfo['fileNumber']
    result['functionNumber'] = projectInfo['functionNumber']
    result['codeLine'] = projectInfo['codeInfo']['codeLine']
    result['codeLineExp'] = projectInfo['codeInfo']['codeLineExp']
    result['commentLine'] = projectInfo['codeInfo']['commentLine']
    result['commentLineExp'] = projectInfo['codeInfo']['commentLineExp']
    result['NoneLine'] = result['codeLine'] - result['codeLineExp'] + result['commentLine'] - result['commentLineExp']
    if projectInfo['codeInfo']['codeLine']:
        result['codeLineExpProp'] = str(round(projectInfo['codeInfo']['codeLineExp'] / projectInfo['codeInfo']['codeLine'], 4)*100)[:5] + '%'
        result['emptyLineProp'] = str(round(result['NoneLine'] / projectInfo['codeInfo']['projectLine'], 4)*100)[:5] + '%'
        result['commentLineExpProp'] = str(round(projectInfo['codeInfo']['commentLineExp'] / projectInfo['codeInfo']['codeLine'], 4)*100)[:5] + '%'
    else:
        result['codeLineExpProp'] = '0%'
        result['emptyLineProp'] = '0%'
        result['commentLineExpProp'] = '0%'


    # TODO： 需要在这里添加 攻击面相关信息
        # 韧性评估结果
        # 潜在攻击相关信息
    result['libraryCount'] = 0
    result['dataInCount'] = 0
    result['dataOutCount'] = 0
    result['unTrustedDataCount'] = 0
    result['attackSetSize'] = 0
    result['attackSetCat'] = 0
    result['resilienceResult'] = 0.5
    return result
