import copy
import os

from flask import jsonify, Blueprint, request, Response, send_from_directory

import AHP
from badsmell import BadSmell
from metric import *
from ExtractModule import *
from project import *
from app import app
import metricCheck
import change_PLCG
from taskModel import *
from attack_surface_info import *
from FaultRateCal import get_fault_dict
from plantuml import PlantUML

home_api = Blueprint('home_api', __name__, static_folder=app.config.get("STATIC_FOLDER"))
STATIC_FOLDER = app.config.get("STATIC_FOLDER")
MIN_MAX_METRICS = ["性能效率-时间特性-平均响应时间", "性能效率-时间特性-响应时间的充分性", "性能效率-时间特性-平均周转时间", "性能效率-时间特性-周转时间的充分性", "性能效率-时间特性-平均吞吐量", "性能效率-资源利用性-I/O设备平均占用率", "性能效率-容量-事务处理容量", "性能效率-容量-用户访问量", "性能效率-容量-用户访问增长的充分性",
                   "可靠性-成熟性-平均失效间隔时间(MTBF)", "可靠性-成熟性-周期失效率", "可靠性-可用性-系统可用性", "可靠性-可用性-平均宕机时间", "可靠性-容错性-组件的冗余度", "可靠性-容错性-平均故障通告时间", "可靠性-易恢复性-平均恢复时间", "信息安全性-可核查性-系统日志保留满足度", "维护性-易修改性-修改的效率", "可移植性-易安装性-安装的时间效率"]


@home_api.route('/getAllProject')
def getALLproject():
    with app.app_context():
        all = query1()
    res = {"projects": []}
    for d in all:
        task = get_task(d[3])
        project = {"name": d[0], "path": d[1], "projectType": d[2], "task_id": d[3], "ready": task["done"] == 1,
                   "failed": task["done"] == -1}
        res["projects"].append(project)
    return jsonify(res), 200


@home_api.route('/task_progress/<int:task_id>', methods=['GET'])
def progress(task_id):
    """
    ???????????????
    :param task_id:
    :return:
    """
    progress = get_task(task_id)
    done = progress["done"]
    for k in progress.keys():
        if k != "done" and progress[k] == 0:
            done = -1
    if progress is not None:
        if done == -1:
            return jsonify({"task_id": task_id, "progress": done, "fileList": []})
        return jsonify({"task_id": task_id, "progress": done})
    else:
        return jsonify({"error": "Task not found"}), 404


@home_api.get("/projectInfo/<projectname>")
def projectInfo(projectname):
    """
    ?????????
    """
    data = ProjectInfoExtract(projectname)
    # print(data)
    return jsonify(data)


@home_api.get("/codeInfo/<projectname>")
def codeInfo(projectname):
    """
    ????????????????
    """
    data = CodeAnalyseExtract(projectname)
    # print("codeinfo", data)
    return jsonify(data)


@home_api.get("/codeInfo/fileAnalyse/<projectname>")
def fileAnalyse(projectname):
    """
    ???????????????? ?????????
    :params
        selectFile: ????????????
    """
    # TODO:
    selectFile = request.args.get("selectFile")
    type = request.args.get("type")
    data = FileAnalyseExtract(projectname, selectFile, type)
    return jsonify(data)


@home_api.post("/defect_rate_calculation/C/uploadFile/<projectname>")
def uploadCFile(projectname):
    """
    ???????? ???????????????
    params:
        file: ????????
    """
    file = request.files.get("file")
    upload_path = app.config.get("UPLOADS_DEFAULT_DEST")
    if not os.path.exists(upload_path + "/" + projectname):
        return jsonify({"msg": "error"}), 400
    filePath = upload_path + "/" + projectname + "/rcf"
    if not os.path.exists(filePath):
        os.mkdir(filePath)
    # print(file.filename)
    static_path = app.config.get("STATIC_FOLDER")
    os.chmod(filePath, 0o755)
    file.save(filePath+"/"+file.filename)
    # ????????
    data = get_fault_dict(filePath+"/"+file.filename, static_path+"/c.rcf")
    # print(data)
    return jsonify(data)


@home_api.post("/defect_rate_calculation/CPP/uploadFile/<projectname>")
def uploadCPPFile(projectname):
    """
    ???????? ???????????????
    params:
        file: ????????
    """
    file = request.files.get("file")
    upload_path = app.config.get("UPLOADS_DEFAULT_DEST")
    if not os.path.exists(upload_path + "/" + projectname):
        return jsonify({"msg": "error"}), 400
    filePath = upload_path + "/" + projectname + "/rcf"
    if not os.path.exists(filePath):
        os.mkdir(filePath)
    # print(file.filename)
    static_path = app.config.get("STATIC_FOLDER")
    os.chmod(filePath, 0o755)
    file.save(filePath+"/"+file.filename)
    # ????????
    data = get_fault_dict(filePath+"/"+file.filename, static_path+"/cpp.rcf")
    # print(data)
    return jsonify(data)


@home_api.post("/defect_rate_calculation/inputWeight/<projectname>")
def inputWeight(projectname):
    """
    ???????? ????????????????
    params:
        weight1??weight2??weight3 ???????
    """
    weight1 = request.get_json().get("weight1")
    weight2 = request.get_json().get("weight2")
    weight3 = request.get_json().get("weight3")

    data = [
        {"value": 48, "name": '可选类缺陷'},
        {"value": 735, "name": '建议类缺陷'},
        {"value": 580, "name": '强制类缺陷'}
    ]
    return jsonify(data)


@home_api.get("/bad_ratio_detect/detection_results/<badType>/<projectName>/<page>")
def send_bad_semll(badType, projectName, page):
    """
    依据请求的类型和页数返回数据
    """
    data = BadSmell.query.filter(BadSmell.project_name == projectName).first()
    if badType == "c_overLongFunc":
        new_data = json.loads(str(data.c_overLongFunc, "UTF-8").replace("\'", '\"')) if data.c_overLongFunc is not None else None
        new_data = new_data['detectionResults'][(int(page)-1)*20:int(page)*20]
    elif badType == "c_overLongParam":
        new_data = json.loads(str(data.c_overLongParam, "UTF-8").replace("\'", '\"')) if data.c_overLongParam is not None else None
        new_data = new_data['detectionResults'][(int(page)-1)*20:int(page)*20]
    elif badType == "c_overCommentLineFunc":
        new_data = json.loads(str(data.c_overCommentLineFunc, "UTF-8").replace("\'", '\"')) if data.c_overCommentLineFunc is not None else None
        new_data = new_data['detectionResults'][(int(page)-1)*20:int(page)*20]
    elif badType == "c_overDeepCall":
        new_data = json.loads(str(data.c_overDeepCall, "UTF-8").replace("\'", '\"')) if data.c_overDeepCall is not None else None
        new_data = new_data['detectionResults'][(int(page)-1)*20:int(page)*20]
    elif badType == "c_overInOutDegreeFunc":
        new_data = json.loads(str(data.c_overInOutDegreeFunc, "UTF-8").replace("\'", '\"')) if data.c_overInOutDegreeFunc is not None else None
        new_data = new_data['detectionResults'][(int(page)-1)*20:int(page)*20]
    elif badType == "c_funcCopy":
        new_data = json.loads(str(data.c_funcCopy, "UTF-8").replace("\'", '\"')) if data.c_funcCopy is not None else None
        new_data = new_data['detectionResults'][(int(page)-1)*20:int(page)*20]
    elif badType == "c_overCyclComplexityFunc":
        new_data = json.loads(str(data.c_overCyclComplexityFunc, "UTF-8").replace("\'", '\"')) if data.c_overCyclComplexityFunc is not None else None
        new_data = new_data['detectionResults'][(int(page)-1)*20:int(page)*20]
    elif badType == "cpp_overLongFunc":
        new_data = json.loads(str(data.cpp_overLongFunc, "UTF-8").replace("\'", '\"')) if data.cpp_overLongFunc is not None else None
        new_data = new_data['detectionResults'][(int(page)-1)*20:int(page)*20]
    elif badType == "cpp_overLongParam":
        new_data = json.loads(str(data.cpp_overLongParam, "UTF-8").replace("\'", '\"')) if data.cpp_overLongParam is not None else None
        new_data = new_data['detectionResults'][(int(page)-1)*20:int(page)*20]
    elif badType == "cpp_overCommentLineFunc":
        new_data = json.loads(str(data.cpp_overCommentLineFunc, "UTF-8").replace("\'", '\"')) if data.cpp_overCommentLineFunc is not None else None
        new_data = new_data['detectionResults'][(int(page)-1)*20:int(page)*20]
    elif badType == "cpp_overDeepCall":
        new_data = json.loads(str(data.cpp_overDeepCall, "UTF-8").replace("\'", '\"')) if data.cpp_overDeepCall is not None else None
        new_data = new_data['detectionResults'][(int(page)-1)*20:int(page)*20]
    elif badType == "cpp_overInOutDegreeFunc":
        new_data = json.loads(str(data.cpp_overInOutDegreeFunc, "UTF-8").replace("\'", '\"')) if data.cpp_overInOutDegreeFunc is not None else None
        new_data = new_data['detectionResults'][(int(page)-1)*20:int(page)*20]
    elif badType == "cpp_funcCopy":
        new_data = json.loads(str(data.cpp_funcCopy, "UTF-8").replace("\'", '\"')) if data.cpp_funcCopy is not None else None
        new_data = new_data['detectionResults'][(int(page)-1)*20:int(page)*20]
    elif badType == "cpp_overCyclComplexityFunc":
        new_data = json.loads(str(data.cpp_overCyclComplexityFunc, "UTF-8").replace("\'", '\"')) if data.cpp_overCyclComplexityFunc is not None else None
        new_data = new_data['detectionResults'][(int(page)-1)*20:int(page)*20]
    elif badType == "cpp_lazyClass":
        new_data = json.loads(str(data.cpp_lazyClass, "UTF-8").replace("\'", '\"')) if data.cpp_lazyClass is not None else None
        new_data = new_data['detectionResults'][(int(page)-1)*20:int(page)*20]
    elif badType == "cpp_largeClass":
        new_data = json.loads(str(data.cpp_largeClass, "UTF-8").replace("\'", '\"')) if data.cpp_largeClass is not None else None
        new_data = new_data['detectionResults'][(int(page)-1)*20:int(page)*20]
    elif badType == "cpp_shotgunSurgery":
        new_data = json.loads(str(data.cpp_shotgunSurgery, "UTF-8").replace("\'", '\"')) if data.cpp_shotgunSurgery is not None else None
        new_data = new_data['detectionResults'][(int(page)-1)*20:int(page)*20]
    elif badType == "cpp_featureEnvy":
        new_data = json.loads(str(data.cpp_featureEnvy, "UTF-8").replace("\'", '\"')) if data.cpp_featureEnvy is not None else None
        new_data = new_data['detectionResults'][(int(page)-1)*20:int(page)*20]
    elif badType == "cpp_dataClass":
        new_data = json.loads(str(data.cpp_dataClass, "UTF-8").replace("\'", '\"')) if data.cpp_dataClass is not None else None
        new_data = new_data['detectionResults'][(int(page)-1)*20:int(page)*20]
    return jsonify({"detectionResults": new_data})


@home_api.post("/bad_ratio_detect/setThreshold/<projectname>")
def setThreshold(projectname):
    """
    ????????? ??????????????
    params:
        threshold: ????????
    """
    threshold = request.get_json()
    data = BadSmellDetection(projectname, threshold)
    return jsonify(data)


@home_api.get("/change_information_detection/<projectname>")
def change_information_detection(projectname):
    """
    ?????????
    params:
        selectedVersion: ???????????
    """
    selectedVersion = request.args.get("selectedVersion")
    data = ChangeInfoDetection(projectname, selectedVersion)
    return jsonify(data)


@home_api.post("/design_refactor_suggestion/<projectname>")
def design_refactor_suggestion(projectname):
    """
    ???????????
    params:
        threshold: ????????
    """
    threshold = request.get_json()
    data = getAdvice(projectname, threshold)
    # print(data)
    return jsonify({"suggestionTable": data})


@home_api.route('/metricSelected/<projectname>', methods=['post'])
def metricSelected(projectname):
    a = dict(request.get_json())
    add_or_update_metric(projectname, metricSelected=a['metricTree'])
    return jsonify({"msg": "success"}), 200


@home_api.route('/getDesignMetric/<projectname>', methods=['get'])
def designMetic(projectname):
    _, _, _, _, _, _, _, h = query2(projectname)
    return jsonify(h), 200


@home_api.route('/metricWeight/<projectname>', methods=['get'])
def metricWeight(projectname):
    responseDict = {}
    item = query_metric(projectname)
    if item.metricSelected is not None:
        a, b, c, d, e, f, g, _ = query2(projectname)
        res = copy.deepcopy(f)
        temp_res = {}
        for key1 in res.keys():
            temp_res[key1] = {}
            for key2 in res[key1].keys():
                temp_res[key1][key2] = {}
                for key3 in res[key1][key2].keys():
                    # print(key1, key2,key3)
                    temp_res[key1][key2][key3] = res[key1][key2][key3]['val']
        mat = json.loads(str(item.metricSelected, "UTF-8").replace("\'", "\"")) if item.metricSelected is not None else None
        ret = metricCheck.get_metric_checked(temp_res, mat)
        if len(ret) == 0:
            responseDict["metricSelected"] = 0
        else:
            responseDict["metricSelected"] = 1
        responseDict["metricTree"] = ret
    else:
        responseDict["metricSelected"] = -1
        responseDict["metricTree"] = {}
    return jsonify(responseDict), 200


@home_api.route("/getMinMaxMetrics/<projectName>", methods=['get'])
def getMinMaxMetrics(projectName):
    responseDict = {}
    item = query_metric(projectName)
    nowMetricSelected = json.loads(str(item.metricSelected, "UTF-8").replace("\'", "\"")) if item.metricSelected is not None else None
    a, b, c, d, e, f, g, _ = query2(projectName)
    for key1 in nowMetricSelected.keys():
        for key2 in nowMetricSelected[key1].keys():
            for key3 in nowMetricSelected[key1][key2].keys():
                tmp = key1 + "-" + key2 + "-" + key3
                if f[key1][key2][key3]['val'] is None:
                    f[key1][key2][key3]['val'] = 0.0
                if tmp in MIN_MAX_METRICS or f[key1][key2][key3]['val'] > 1.0:
                    if f[key1][key2][key3]['val'] == 0.0:
                        continue
                    if key1 not in responseDict.keys():
                        responseDict[key1] = {}
                    if key2 not in responseDict[key1].keys():
                        responseDict[key1][key2] = {}
                    if key3 not in responseDict[key1][key2].keys():
                        responseDict[key1][key2][key3] = {"val": f[key1][key2][key3]['val']}

    return jsonify(responseDict), 200


@home_api.route('/weightCheck/<projectname>', methods=['post'])
def weightCheck(projectname):
    a = dict(request.get_json())
    responseDict = {}
    metricWeight = a["metricWeight"]
    # print(metricWeight)
    errorMetric = []
    rstMetricWeight = {}
    for key in metricWeight.keys():
        strData = metricWeight[key]["data"]
        # numData = eval(strData)
        numData = strData
        weightRst = AHP.cal_weight(numData)
        if weightRst is None:
            errorMetric.append(key)
        else:
            rstMetricWeight[key] = {}
            for idx in range(len(weightRst)):
                # if key == "信息安全性":
                #     print("--------", key)
                rstMetricWeight[key][metricWeight[key]["index"][idx]] = float(weightRst[idx])
    if len(errorMetric) == 0:
        responseDict["weightFlag"] = 1
        responseDict["data"] = {}
        add_or_update_metric(projectname, metricWeight=rstMetricWeight)
    else:
        responseDict["weightFlag"] = 0
        levelOne = ['功能性', '性能效率', '兼容性',
                    '易用性', '可靠性', '信息安全性', '维护性', '可移植性']
        responseDict["data"] = {"levelZero": [i for i in errorMetric if i == "软件总质量"], "levelOne": [i for i in errorMetric if i in levelOne], "levelTwo": [
            i for i in errorMetric if i not in levelOne and i != "软件总质量"]}
    return jsonify(responseDict), 200


@app.route('/getSelectedMetrics/<projectname>', methods=['post'])
def getSelectedMetrics(projectname):
    responseDict = {}
    # if os.path.exists(path + "/data/" + projectname + "/" + projectname + "metricSelected.json"):
    # if os.path.exists(path + "/data/" + projectname + "/" + projectname + "metricResult.json"):
    #     responseDict["metricCalculated"] = 1
    #     with open(path + "/data/" + projectname + "/" + projectname + "metricResult.json", "r",
    #               encoding="utf-8") as f:
    #         content = json.load(f)
    #     responseDict["data"] = content["data"]
    #     return jsonify(responseDict), 200
    # else:
    # ??????????
    minMaxMetrics = dict(request.get_json())
    item = query_metric(projectname)
    mat = json.loads(str(item.metricSelected, "UTF-8").replace("\'", "\"")) if item.metricSelected is not None else None
    # ??25010?????????
    a, b, c, d, e, f, g, _ = query2(projectname)
    res = copy.deepcopy(f)
    for key1 in mat.keys():
        for key2 in mat[key1].keys():
            for key3 in mat[key1][key2].keys():
                if key1 in minMaxMetrics.keys():
                    if key2 in minMaxMetrics[key1].keys():
                        if key3 in minMaxMetrics[key1][key2].keys():
                            mat[key1][key2][key3] = (float(minMaxMetrics[key1][key2][key3]['val']) - float(minMaxMetrics[key1][key2][key3]['min'])) / (float(minMaxMetrics[key1][key2][key3]['max']) - float(minMaxMetrics[key1][key2][key3]['min']))
                            res[key1][key2][key3]['val'] = mat[key1][key2][key3]
                        else:
                            mat[key1][key2][key3] = res[key1][key2][key3]['val']
                    else:
                        mat[key1][key2][key3] = res[key1][key2][key3]['val']
                else:
                    mat[key1][key2][key3] = res[key1][key2][key3]['val']
    # ????????????????
    metricWeight = json.loads(str(item.metricWeight, "UTF-8").replace("\'", "\"")) if item.metricWeight is not None else None
    levelOne = ['功能性', '性能效率', '兼容性',
                '易用性', '可靠性', '信息安全性', '维护性', '可移植性']
    parentMetric = list(metricWeight.keys())
    parentLevelZero = [i for i in parentMetric if i == "软件总质量"]
    parentLevelOne = [i for i in parentMetric if i in levelOne]
    parentLevelTwo = [i for i in parentMetric if i not in levelOne and i != "软件总质量"]

    temp_mat = {}
    for key1 in mat.keys():
        # 去除没有选择的一级指标
        if key1 in parentLevelOne:
            temp_mat[key1] = {
                "name": key1,
                "sub": {}
            }
            # 初始化一级指标的值
            tmp_val_one = 0.0
            for key2 in mat[key1].keys():
                if key2 in parentLevelTwo:
                    # 添加选择的二级指标
                    temp_mat[key1]["sub"][key2] = {
                        "name": key2,
                        "sub": {}
                    }
                    # 初始化二级指标的值
                    tmp_val = 0.0
                    for key3 in mat[key1][key2].keys():
                        wm = list(metricWeight[key2].keys())
                        if key3 in wm:
                            temp_mat[key1]["sub"][key2]["sub"][key3] = {
                                "name": key3,
                                "val": mat[key1][key2][key3],
                                "weight": metricWeight[key2][key3]
                            }
                            if mat[key1][key2][key3] is None:
                                tmp_val += 0.0 * metricWeight[key2][key3]
                            else:
                                if key3 in metricCheck.MIN_REVERSE_LIST:
                                    tmp_val += (1.0 - mat[key1][key2][key3]) * \
                                        metricWeight[key2][key3]
                                else:
                                    tmp_val += mat[key1][key2][key3] * \
                                        metricWeight[key2][key3]
                        else:
                            temp_mat[key1]["sub"][key2]["sub"][key3] = {
                                "name": key3,
                                "val": mat[key1][key2][key3],
                                "weight": 0.0
                            }
                    temp_mat[key1]["sub"][key2]['val'] = tmp_val
                else:
                    # ??????????????
                    temp_mat[key1]["sub"][key2] = {
                        "name": key2,
                        "sub": {},
                        "val": 0.0
                    }
                wm_one = list(metricWeight[key1].keys())
                if key2 in wm_one:
                    temp_mat[key1]["sub"][key2]['weight'] = metricWeight[key1][key2]
                    tmp_val_one += temp_mat[key1]["sub"][key2]['val'] * \
                        metricWeight[key1][key2]
                else:
                    temp_mat[key1]["sub"][key2]['weight'] = 0.0
            temp_mat[key1]['val'] = tmp_val_one
        # else:
        #     # ?????????????
        #     temp_mat[key1] = {
        #         "name": key1,
        #         "sub": {}
        #     }

    # metricWeight ??????{???????{????????}}
    # ???????
    responseDict["metricCalculated"] = 1
    responseDict["data"] = []
    soft_quality = {"name": "软件总质量", "sub": [], "subMetric": [], "val": 0.0}
    # print("temp_mat", temp_mat)
    for key1 in temp_mat.keys():
        responseDict["data"].append({
            "name": key1,
            "val": temp_mat[key1]['val'],
            "sub": [],
            "subMetric": []
        })
        for key2 in temp_mat[key1]["sub"].keys():
            # print(key1,key2)
            responseDict["data"][-1]["sub"].append({
                "id": key2,
                "value": temp_mat[key1]["sub"][key2]['val'],
                "weight": temp_mat[key1]["sub"][key2]['weight']
            })
            responseDict["data"][-1]["subMetric"].append({
                "name": key2,
                "val": temp_mat[key1]["sub"][key2]['val'],
                "sub": [],
                "subMetric": []
            })
            for key3 in mat[key1][key2].keys():
                if key3 in temp_mat[key1]["sub"][key2]["sub"].keys():
                    tmp_weight = temp_mat[key1]["sub"][key2]["sub"][key3]['weight']
                else:
                    tmp_weight = 0.0
                responseDict["data"][-1]["subMetric"][-1]["sub"].append({
                    "id": key3,
                    "value": res[key1][key2][key3]['val'],
                    "weight": tmp_weight
                })
                responseDict["data"][-1]["subMetric"][-1]["subMetric"].append({
                    "name": key3,
                    "val": res[key1][key2][key3]['val'],
                    "sub": res[key1][key2][key3]['sub']
                })
    for dict_key1 in responseDict["data"]:
        soft_quality["sub"].append({
            "id": dict_key1["name"],
            "value": dict_key1['val'],
            "weight": metricWeight["软件总质量"][dict_key1["name"]]
        })
        soft_quality["subMetric"].append(dict_key1)
        soft_quality["val"] = soft_quality["val"] + dict_key1['val'] * metricWeight["软件总质量"][dict_key1["name"]]
    add_or_update_metric(projectname, metricResult=responseDict["data"])
    responseDict["data"] = [soft_quality]
    # else:
    #     responseDict["metricCalculated"] = 0
    return jsonify(responseDict), 200


@home_api.get("/get_all_same_project/<projectname>")
def get_all_version_info(projectname):
    """
    ????????????????????
    """
    print(request.args.get("projectType"))
    projectType = int(request.args.get("projectType"))
    with app.app_context():
        all = query1()
    projects = list()
    for p in all:
        if p[2] == projectType and p[0] != projectname:
            projects.append(p[0])
    return jsonify(projects)


@home_api.get('/CFG/<projectname>')
def cfg_json(projectname):
    with app.app_context():
        a, b, c, d, e, f, g, _ = query2(projectname)
        return jsonify(eval(e["cfg_js"]))


@home_api.get('/PDG/<projectname>')
def pdg_json(projectname):
    with app.app_context():
        a, b, c, d, e, f, g, _ = query2(projectname)
        return jsonify(eval(e["pdg_js"]))


@home_api.get('/CG/<projectname>')
def CG_json(projectname):
    print("CGjiemian")
    with app.app_context():
        a, b, c, d, e, f, g, _ = query2(projectname)
        return jsonify(eval(e["CG_js"]))


@home_api.get('/GRAPH_SHOW/<projectname>')
def write_cfg_svg(projectname):
    graph_type = request.args.get("graph_type")
    file_path = request.args.get("file_path")
    function_name = request.args.get("function_name")
    # print("graph_type", graph_type)
    # print("file_path", file_path)
    # print("function_name", function_name)
    with app.app_context():
        a, b, c, d, e, f, g, _ = query2(projectname)
        current_graphs = e[graph_type]
        svg_string = current_graphs[file_path][function_name]
        with open(app.config.get("EXE_PATH") + "/static/graph_show.svg", 'w') as f:
            f.write(svg_string.decode())
    return jsonify({})


@home_api.get('/FILE_CG_SHOW/<projectname>')
def change_js2(projectname):
    # file_path = request.args.get("file_path")
    with app.app_context():
        a, b, c, d, e, f, g, _ = query2(projectname)

        new_flcg = e['FLCG']
        with open(app.config.get("EXE_PATH") + "/static/FLCG.js", 'w') as f:
            f.write("var graph = ")
            json.dump(new_flcg, f, indent=4)
    return jsonify({})


@home_api.get('/FUNCTION_CG_SHOW/<projectname>')
def change_js(projectname):
    file_path = request.args.get("file_path")
    if file_path == None:
        file_path = app.config.get("UPLOADS_DEFAULT_DEST") + "/" + projectname
    with app.app_context():
        a, b, c, d, e, f, g, _ = query2(projectname)

        new_plcg = change_PLCG.change_PLCG(c, e, file_path)
        with open(app.config.get("EXE_PATH") + "/static/PLCG.js", 'w') as f:
            f.write("var graph = ")
            json.dump(new_plcg, f, indent=4)
    return jsonify({})


@home_api.get('/cfg_graph.html')
def cfg_pdg_graph():
    with open(app.config.get("EXE_PATH") + "/static/cfg_graph.html", 'rb') as f:
        fileas = f.read()
        resp = Response(fileas)
    return resp


@home_api.get('/sdg.html')
def sdg_graph():
    with open(app.config.get("EXE_PATH") + "/static/sdg.html", 'rb') as f:
        fileas = f.read()
        resp = Response(fileas)
    return resp


@home_api.get('/comp.html')
def comp_graph():
    with open(app.config.get("EXE_PATH") + "/static/comp.html", 'rb') as f:
        fileas = f.read()
        resp = Response(fileas)
    return resp


@home_api.get('/Class.html')
def class_graph():
    with open(app.config.get("EXE_PATH") + "/static/Class.html", 'rb') as f:
        fileas = f.read()
        resp = Response(fileas)
    return resp


@home_api.get('/CLASS_SHOW/<projectname>')
def class_call_back(projectname):
    with app.app_context():
        a, b, c, d, e, f, g, _ = query2(projectname)
        class_json = e["class_js"]
        with open(app.config.get("EXE_PATH") + "/static/class.js", 'w') as f:
            f.write("var graph=")
            json.dump(class_json, f, indent=4)
    return jsonify({})


@home_api.get('/FLCG.dot.html')
def flcg_graph():
    with open(app.config.get("EXE_PATH") + "/static/FLCG.dot.html", 'rb') as f:
        fileas = f.read()
        resp = Response(fileas)
    return resp


@home_api.get('/PLCG.dot.html')
def plcg_graph():
    with open(app.config.get("EXE_PATH") + "/static/PLCG.dot.html", 'rb') as f:
        fileas = f.read()
        resp = Response(fileas)
    return resp


@home_api.get('/pipe-filter.html')
def pipe_filter_graph():
    with open(app.config.get("EXE_PATH") + "/static/pipe-filter.html", 'rb') as f:
        fileas = f.read()
        resp = Response(fileas)
    return resp


@home_api.get('/CALLBACK_SHOW/<projectname>')
def call_back_js(projectname):
    with app.app_context():
        a, b, c, d, e, f, g, _ = query2(projectname)
        call_back_json = e["callback_js"]
        with open(app.config.get("EXE_PATH") + "/static/callback.js", 'w') as f:
            f.write("var comp=")
            f.write(call_back_json)
    return jsonify({})


@home_api.get('/callback.html')
def call_back_html():
    with open(app.config.get("EXE_PATH") + "/static/callback.html", 'rb') as f:
        fileas = f.read()
        resp = Response(fileas)
    return resp


@home_api.get('/LEVEL_SHOW/<projectname>')
def level_js(projectname):
    with app.app_context():
        a, b, c, d, e, f, g, _ = query2(projectname)
        layer_graph_json = e["layer_js"]
        with open(app.config.get("EXE_PATH") + "/static/layer.js", 'w') as f:  # 测试用
            f.write("var layer_graph=")
            f.write(layer_graph_json)
    return jsonify({})


@home_api.get('/level.html')
def level_html():
    with open(app.config.get("EXE_PATH") + "/static/level.html", 'rb') as f:
        fileas = f.read()
        resp = Response(fileas)
    return resp


@home_api.get('/PIPEFILTER_SHOW/<projectname>')
def pipe_filter_svg(projectname):
    with app.app_context():
        a, b, c, d, e, f, g, _ = query2(projectname)
        pipe_filter_svg = e["pipe_filter_svg"]
        with open(app.config.get("EXE_PATH") + "/static/pipe_filter.svg", 'wb') as f:
            f.write(pipe_filter_svg)
    return jsonify({})


@home_api.get('/pipe_filter.html')
def pipe_filter_html():
    with open(app.config.get("EXE_PATH") + "/static/pipe_filter.html", 'rb') as f:
        fileas = f.read()
        resp = Response(fileas)
    return resp


@home_api.get('/SDG_SHOW/<projectname>')
def sdg_svg(projectname):
    with app.app_context():
        a, b, c, d, e, f, g, _ = query2(projectname)
        sdg_svg = e["sdg_svg"]
        with open(app.config.get("EXE_PATH") + "/static/sdg.svg", 'wb') as f:
            f.write(sdg_svg)
    return jsonify({})


@home_api.get('/sdg.html')
def sdg_html():
    with open(app.config.get("EXE_PATH") + "/static/sdg.html", 'rb') as f:
        fileas = f.read()
        resp = Response(fileas)
    return resp


@home_api.get('/attack.html')
def attack_html():
    with open(app.config.get("EXE_PATH") + "/static/attack.html", 'rb') as f:
        fileas = f.read()
        resp = Response(fileas)
    return resp

@home_api.get('/activity_uml.html')
def activity_uml_html():
    with open(app.config.get("EXE_PATH") + "/static/activity_uml.html", 'rb') as f:
        fileas = f.read()
        resp = Response(fileas)
    return resp

@home_api.get('/comp_uml.html')
def comp_uml_html():
    with open(app.config.get("EXE_PATH") + "/static/comp_uml.html", 'rb') as f:
        fileas = f.read()
        resp = Response(fileas)
    return resp


@home_api.get('/COMP_SHOW/<projectname>')
def comp_js(projectname):
    with app.app_context():
        a, b, c, d, e, f, g, _ = query2(projectname)
        comp_js = e["comp_js"]
        with open(app.config.get("EXE_PATH") + "/static/comp.js", 'w') as f:
            f.write("var comp = ")
            json.dump(comp_js, f, indent=4)
    return jsonify({})

@home_api.get('/ATTACK_SHOW/<projectname>')
def attack_js(projectname):
    # write current file info into graph
    with app.app_context():
        a, b, c, d, e, f, g, _ = query2(projectname)
        # wsd_infos = e["wsd_infos"]
        # activity_uml = wsd_infos["activity"]
        # comp_uml = wsd_infos["comp"]
        with app.app_context():
            a, b, c, d, e, f, g, _ = query2(projectname)
            attack_js = e["attack_js"]
            with open(app.config.get("EXE_PATH") + "/static/attack.js", 'w') as f:
                f.write(attack_js)
    return jsonify({})

@home_api.get('/UML_SHOW/<projectname>')
def uml_show(projectname):
    # write current file info into graph
    with app.app_context():
        a, b, c, d, e, f, g, _ = query2(projectname)
        # wsd_infos = e["wsd_infos"]
        # activity_uml = wsd_infos["activity"]
        # comp_uml = wsd_infos["comp"]
        if a["REL_TYPE"] == "UML":
            activity_uml = a["uml_info"]["activity_diagram_path"]# "/temp_grad/test_back/activity.wsd"
            comp_uml = a["uml_info"]["comp_diagram_path"]# "/temp_grad/test_back/activity.wsd"
            PlantUML("http://www.plantuml.com/plantuml/img/").processes_file(activity_uml, outfile="static/activity_uml.png")
            PlantUML("http://www.plantuml.com/plantuml/img/").processes_file(comp_uml, outfile="static/comp_uml.png")
    return jsonify({})


@home_api.get('/ATTACK_SURFACE_IFNO/<projectname>')
def getAttackSurfaceInfo(projectname):
    project_info, b, c, d, e, f, g, _ = query2(projectname)
    attackSurfaceInfo_res = attackSurfaceInfoExtract(project_info)
    return jsonify(attackSurfaceInfo_res)

@home_api.get('/RESILIENCE_REPORT_INFO/<projectname>')
def getResilienceReport(projectname):
    project_info, b, c, d, e, f, g, _ = query2(projectname)
    resilience_report_info = resilienceInfoExtacrt(project_info)
    return jsonify(resilience_report_info)