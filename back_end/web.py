# import ExtractModule
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources=r'/*', supports_credentials=True)


@app.get("/")
def index():
    return "Hello"


@app.get("/getAllProject")
def getAllProject():
    """
    首页获取所有项目信息
    """
    data = {
        "projects": [
            {
                "name": "CUnit V1.9.2",
                "path": "D:/Software/frontend/C_Quality_Evaluator_APP/app/data/CUnit",
                "projectType": 2,
                "ready": True,
                "failed": False,
                "task_id": "1"
            },
            {
                "name": "VLC V0.8.7",
                "path": "D:/Software/frontend/C_Quality_Evaluator_APP/app/data/VLC",
                "projectType": 0,
                "ready": True,
                "failed": False,
                "task_id": "1"
            }
        ]
    }
    return jsonify(data)


@app.get("/get_project_percentage/<projectname>")
def get_project_percentage(projectname):
    data = {
        "ready": False,
        "failed": False,
        "percentage": 33.3
    }
    return jsonify(data)


@app.get("/projectInfo/<projectname>")
def projectInfo(projectname):
    """
    项目信息提取
    """
    data = {
        "fileProp": [
            {
                "name": ".h",
                "value": 156
            },
            {
                "name": ".c",
                "value": 230
            },
            {
                "name": ".cpp",
                "value": 42
            },
            {
                "name": "other_file",
                "value": 60
            }
        ],
        "fileNumber": 130,
        "functionNumber": 2000,
        "codeLine": 2683,
        "codeLineExp": 646,
        "commentLine": 1896,
        "commentLineExp": 1546,
        "codeLineExpProp": "86.3%",
        "emptyLineProp": "3.2%",
        "commentLineExpProp": "10.5%"
    }
    return jsonify(data)


@app.get("/codeInfo/<projectname>")
def codeInfo(projectname):
    """
    代码解析及信息提取
    """
    data = {
        "c_info": {
            "cFileProp": "93.2%",
            "funcTotal": "99",
            "functionLine": {
                "maxLineFunc": "xxx()",
                "maxLineFuncPath": "xx/xxx/xxx()",
                "maxLine": 50,
                "minLineFunc": "xxx()",
                "minLineFuncPath": "xx/xxx/xxx()",
                "minLine": 1,
                "avgLine": 15
            },
            "fileLine": {
                "maxLineFile": "xxx.c",
                "maxLineFilePath": "xx/xxx/xxx.c",
                "maxLine": 50,
                "minLineFile": "xxx.h",
                "minLineFilePath": "xx/xxx/xxx.h",
                "minLine": 1,
                "avgLine": 15
            },
            "defineFuncFile": {
                "maxFuncFile": "xxx.c",
                "maxFuncFilePath": "xx/xxx/xxx.c",
                "maxFunc": 50,
                "minFuncFile": "xxx.h",
                "minFuncFilePath": "xx/xxx/xxx.h",
                "minFunc": 1,
                "avgFunc": 15
            },
            "filePathList": [
                "D:/xxx/xx/test1.c",
                "D:/xxx/xx/test2.c",
                "D:/xxx/xx/test3.c",
                "D:/xxx/xx/test4.c",
            ]
        },
        "c_plus_info": {
            "cppFileProp": "88.6%",
            "classTotal": "120",
            "classMember": {
                "maxMemberClass": "xxx",
                "maxMemberClassPath": "xx/xxx/xxx",
                "maxMember": 50,
                "minMemberClass": "xxx",
                "minMemberClassPath": "xx/xxx/xxx",
                "minMember": 1,
                "avgMember": 15
            },
            "fileLine": {
                "maxLineFile": "xxx.cpp",
                "maxLineFilePath": "xx/xxx/xxx.cpp",
                "maxLine": 50,
                "minLineFile": "xxx.h",
                "minLineFilePath": "xx/xxx/xxx.h",
                "minLine": 1,
                "avgLine": 15
            },
            "defineClassFile": {
                "maxClassFile": "xxx.cpp",
                "maxClassFilePath": "xx/xxx/xxx.cpp",
                "maxClass": 50,
                "minClassFile": "xxx.h",
                "minClassFilePath": "xx/xxx/xxx.h",
                "minClass": 1,
                "avgClass": 15
            },
            "filePathList": [
                "D:/xxx/xx/test1.cpp",
                "D:/xxx/xx/test2.cpp",
                "D:/xxx/xx/test3.cpp",
                "D:/xxx/xx/test4.cpp",
            ]
        }
    }
    return jsonify(data)


@app.get("/codeInfo/fileAnalyse/<projectname>")
def fileAnalyse(projectname):
    """
    代码解析及信息提取 文件信息提取
    :params
        selectFile: 选择的文件路径
        type: c_info C代码分析，c_plus_info C++代码分析
    """
    selectFile = request.args.get("selectFile")
    type = request.args.get("type")

    data = [
        {
            "funcName": "func1",
            "returnVal": "int",
            "params": "(int a, char b)",
            "outDegree": 3,
            "inDegree": 5,
            "filePath": "code/xxx/xxx"
        },
        {
            "funcName": "func2",
            "returnVal": "void",
            "params": "(int a, float b)",
            "outDegree": 2,
            "inDegree": 3,
            "filePath": "code/xxx/xxx"
        },
        {
            "funcName": "func1",
            "returnVal": "int",
            "params": "(int a, char b)",
            "outDegree": 3,
            "inDegree": 5,
            "filePath": "code/xxx/xxx"
        },
        {
            "funcName": "func2",
            "returnVal": "void",
            "params": "(int a, float b)",
            "outDegree": 2,
            "inDegree": 3,
            "filePath": "code/xxx/xxx"
        },
        {
            "funcName": "func1",
            "returnVal": "int",
            "params": "(int a, char b)",
            "outDegree": 3,
            "inDegree": 5,
            "filePath": "code/xxx/xxx"
        },
        {
            "funcName": "func2",
            "returnVal": "void",
            "params": "(int a, float b)",
            "outDegree": 2,
            "inDegree": 3,
            "filePath": "code/xxx/xxx"
        },
        {
            "funcName": "func1",
            "returnVal": "int",
            "params": "(int a, char b)",
            "outDegree": 3,
            "inDegree": 5,
            "filePath": "code/xxx/xxx"
        },
        {
            "funcName": "func2",
            "returnVal": "void",
            "params": "(int a, float b)",
            "outDegree": 2,
            "inDegree": 3,
            "filePath": "code/xxx/xxx"
        },
    ]
    return jsonify(data)


@app.post("/defect_rate_calculation/C/uploadFile/<projectname>")
def uploadFileC(projectname):
    """
    缺陷率计算 选择文件获取计算结果
    params:
        file: 选择的文件
    """
    file = request.files.get("file")  # 上传的文件
    data = {
        "overviewData": {
            "thousand_defect_num": 1418.18,
            "defect_concentration": 5416.381241342132,
            "file_defect_rate": "88.33%",
            "function_defect_rate": "13.45%"
        },
        "detectTypeData": {
            "forced_defect": {
                "total_defect_num": 3416,
                "defect_proportion": "60.64%",
                "thousand_defect_num": 268,
                "defect_concentration": 268.53,
                "file_defect_rate": "60.64%",
                "function_defect_rate": "60.64%"
            },
            "optional_defect": {
                "total_defect_num": 2568,
                "defect_proportion": "60.64%",
                "thousand_defect_num": "860.02",
                "defect_concentration": "860.02",
                "file_defect_rate": "60.64%",
                "function_defect_rate": "60.64%"
            },
            "suggested_defect": {
                "total_defect_num": 1096,
                "defect_proportion": "60.64%",
                "thousand_defect_num": "478.68",
                "defect_concentration": "60.64%",
                "file_defect_rate": "60.64%",
                "function_defect_rate": "60.64%"
            }
        },
        "forcedTable": [
            {
                "standard": "过程名重用",
                "source": "GJB 4.1.1.1",
                "num": 2
            },
            {
                "standard": "标号名名重用",
                "source": "GJB 4.1.1.2",
                "num": 5
            },
            {
                "standard": "THEN语句为空",
                "source": "GJB 4.3.1.1",
                "num": 1
            },
            {
                "standard": "过程名重用",
                "source": "GJB 4.1.1.1",
                "num": 2
            },
            {
                "standard": "标号名名重用",
                "source": "GJB 4.1.1.2",
                "num": 5
            },
            {
                "standard": "THEN语句为空",
                "source": "GJB 4.3.1.1",
                "num": 1
            },
            {
                "standard": "过程名重用",
                "source": "GJB 4.1.1.1",
                "num": 2
            },
            {
                "standard": "标号名名重用",
                "source": "GJB 4.1.1.2",
                "num": 5
            },
            {
                "standard": "THEN语句为空",
                "source": "GJB 4.3.1.1",
                "num": 1
            },
            {
                "standard": "过程名重用",
                "source": "GJB 4.1.1.1",
                "num": 2
            },
            {
                "standard": "标号名名重用",
                "source": "GJB 4.1.1.2",
                "num": 5
            },
            {
                "standard": "THEN语句为空",
                "source": "GJB 4.3.1.1",
                "num": 1
            },
            {
                "standard": "过程名重用",
                "source": "GJB 4.1.1.1",
                "num": 2
            },
            {
                "standard": "标号名名重用",
                "source": "GJB 4.1.1.2",
                "num": 5
            },
            {
                "standard": "THEN语句为空",
                "source": "GJB 4.3.1.1",
                "num": 1
            },
            {
                "standard": "过程名重用",
                "source": "GJB 4.1.1.1",
                "num": 2
            },
            {
                "standard": "标号名名重用",
                "source": "GJB 4.1.1.2",
                "num": 5
            },
            {
                "standard": "THEN语句为空",
                "source": "GJB 4.3.1.1",
                "num": 1
            },
        ],
        "optionalTable": [
            {
                "standard": "过程名重用",
                "source": "GJB 4.1.1.1",
                "num": 2
            },
            {
                "standard": "标号名名重用",
                "source": "GJB 4.1.1.2",
                "num": 5
            },
            {
                "standard": "THEN语句为空",
                "source": "GJB 4.3.1.1",
                "num": 1
            },
            {
                "standard": "过程名重用",
                "source": "GJB 4.1.1.1",
                "num": 2
            },
            {
                "standard": "标号名名重用",
                "source": "GJB 4.1.1.2",
                "num": 5
            },
            {
                "standard": "THEN语句为空",
                "source": "GJB 4.3.1.1",
                "num": 1
            },
            {
                "standard": "过程名重用",
                "source": "GJB 4.1.1.1",
                "num": 2
            },
            {
                "standard": "标号名名重用",
                "source": "GJB 4.1.1.2",
                "num": 5
            },
            {
                "standard": "THEN语句为空",
                "source": "GJB 4.3.1.1",
                "num": 1
            },
            {
                "standard": "过程名重用",
                "source": "GJB 4.1.1.1",
                "num": 2
            },
            {
                "standard": "标号名名重用",
                "source": "GJB 4.1.1.2",
                "num": 5
            },
            {
                "standard": "THEN语句为空",
                "source": "GJB 4.3.1.1",
                "num": 1
            },
            {
                "standard": "过程名重用",
                "source": "GJB 4.1.1.1",
                "num": 2
            },
            {
                "standard": "标号名名重用",
                "source": "GJB 4.1.1.2",
                "num": 5
            },
            {
                "standard": "THEN语句为空",
                "source": "GJB 4.3.1.1",
                "num": 1
            },
            {
                "standard": "过程名重用",
                "source": "GJB 4.1.1.1",
                "num": 2
            },
            {
                "standard": "标号名名重用",
                "source": "GJB 4.1.1.2",
                "num": 5
            },
            {
                "standard": "THEN语句为空",
                "source": "GJB 4.3.1.1",
                "num": 1
            },
        ],
        "suggestedTable": [
            {
                "standard": "过程名重用",
                "source": "GJB 4.1.1.1",
                "num": 2
            },
            {
                "standard": "标号名名重用",
                "source": "GJB 4.1.1.2",
                "num": 5
            },
            {
                "standard": "THEN语句为空",
                "source": "GJB 4.3.1.1",
                "num": 1
            },
            {
                "standard": "过程名重用",
                "source": "GJB 4.1.1.1",
                "num": 2
            },
            {
                "standard": "标号名名重用",
                "source": "GJB 4.1.1.2",
                "num": 5
            },
            {
                "standard": "THEN语句为空",
                "source": "GJB 4.3.1.1",
                "num": 1
            },
            {
                "standard": "过程名重用",
                "source": "GJB 4.1.1.1",
                "num": 2
            },
            {
                "standard": "标号名名重用",
                "source": "GJB 4.1.1.2",
                "num": 5
            },
            {
                "standard": "THEN语句为空",
                "source": "GJB 4.3.1.1",
                "num": 1
            },
            {
                "standard": "过程名重用",
                "source": "GJB 4.1.1.1",
                "num": 2
            },
            {
                "standard": "标号名名重用",
                "source": "GJB 4.1.1.2",
                "num": 5
            },
            {
                "standard": "THEN语句为空",
                "source": "GJB 4.3.1.1",
                "num": 1
            },
            {
                "standard": "过程名重用",
                "source": "GJB 4.1.1.1",
                "num": 2
            },
            {
                "standard": "标号名名重用",
                "source": "GJB 4.1.1.2",
                "num": 5
            },
            {
                "standard": "THEN语句为空",
                "source": "GJB 4.3.1.1",
                "num": 1
            },
            {
                "standard": "过程名重用",
                "source": "GJB 4.1.1.1",
                "num": 2
            },
            {
                "standard": "标号名名重用",
                "source": "GJB 4.1.1.2",
                "num": 5
            },
            {
                "standard": "THEN语句为空",
                "source": "GJB 4.3.1.1",
                "num": 1
            },
        ],
    }
    return jsonify(data)


@app.post("/defect_rate_calculation/CPP/uploadFile/<projectname>")
def uploadFileCpp(projectname):
    """
    缺陷率计算 选择文件获取计算结果
    params:
        file: 选择的文件
    """
    file = request.files.get("file")  # 上传的文件
    data = {
        "overviewData": {
            "thousand_defect_num": 1418.18,
            "defect_concentration": 5416.381241342132,
            "file_defect_rate": "88.33%",
            "function_defect_rate": "13.45%"
        },
        "detectTypeData": {
            "forced_defect": {
                "total_defect_num": 3416,
                "defect_proportion": "60.64%",
                "thousand_defect_num": 268,
                "defect_concentration": 268.53,
                "file_defect_rate": "60.64%",
                "function_defect_rate": "60.64%"
            },
            "optional_defect": {
                "total_defect_num": 2568,
                "defect_proportion": "60.64%",
                "thousand_defect_num": "860.02",
                "defect_concentration": "860.02",
                "file_defect_rate": "60.64%",
                "function_defect_rate": "60.64%"
            },
            "suggested_defect": {
                "total_defect_num": 1096,
                "defect_proportion": "60.64%",
                "thousand_defect_num": "478.68",
                "defect_concentration": "60.64%",
                "file_defect_rate": "60.64%",
                "function_defect_rate": "60.64%"
            }
        },
        "forcedTable": [
            {
                "standard": "过程名重用",
                "source": "GJB 4.1.1.1",
                "num": 2
            },
            {
                "standard": "标号名名重用",
                "source": "GJB 4.1.1.2",
                "num": 5
            },
            {
                "standard": "THEN语句为空",
                "source": "GJB 4.3.1.1",
                "num": 1
            },
            {
                "standard": "过程名重用",
                "source": "GJB 4.1.1.1",
                "num": 2
            },
            {
                "standard": "标号名名重用",
                "source": "GJB 4.1.1.2",
                "num": 5
            },
            {
                "standard": "THEN语句为空",
                "source": "GJB 4.3.1.1",
                "num": 1
            },
            {
                "standard": "过程名重用",
                "source": "GJB 4.1.1.1",
                "num": 2
            },
            {
                "standard": "标号名名重用",
                "source": "GJB 4.1.1.2",
                "num": 5
            },
            {
                "standard": "THEN语句为空",
                "source": "GJB 4.3.1.1",
                "num": 1
            },
            {
                "standard": "过程名重用",
                "source": "GJB 4.1.1.1",
                "num": 2
            },
            {
                "standard": "标号名名重用",
                "source": "GJB 4.1.1.2",
                "num": 5
            },
            {
                "standard": "THEN语句为空",
                "source": "GJB 4.3.1.1",
                "num": 1
            },
            {
                "standard": "过程名重用",
                "source": "GJB 4.1.1.1",
                "num": 2
            },
            {
                "standard": "标号名名重用",
                "source": "GJB 4.1.1.2",
                "num": 5
            },
            {
                "standard": "THEN语句为空",
                "source": "GJB 4.3.1.1",
                "num": 1
            },
            {
                "standard": "过程名重用",
                "source": "GJB 4.1.1.1",
                "num": 2
            },
            {
                "standard": "标号名名重用",
                "source": "GJB 4.1.1.2",
                "num": 5
            },
            {
                "standard": "THEN语句为空",
                "source": "GJB 4.3.1.1",
                "num": 1
            },
        ],
        "optionalTable": [
            {
                "standard": "过程名重用",
                "source": "GJB 4.1.1.1",
                "num": 2
            },
            {
                "standard": "标号名名重用",
                "source": "GJB 4.1.1.2",
                "num": 5
            },
            {
                "standard": "THEN语句为空",
                "source": "GJB 4.3.1.1",
                "num": 1
            },
            {
                "standard": "过程名重用",
                "source": "GJB 4.1.1.1",
                "num": 2
            },
            {
                "standard": "标号名名重用",
                "source": "GJB 4.1.1.2",
                "num": 5
            },
            {
                "standard": "THEN语句为空",
                "source": "GJB 4.3.1.1",
                "num": 1
            },
            {
                "standard": "过程名重用",
                "source": "GJB 4.1.1.1",
                "num": 2
            },
            {
                "standard": "标号名名重用",
                "source": "GJB 4.1.1.2",
                "num": 5
            },
            {
                "standard": "THEN语句为空",
                "source": "GJB 4.3.1.1",
                "num": 1
            },
            {
                "standard": "过程名重用",
                "source": "GJB 4.1.1.1",
                "num": 2
            },
            {
                "standard": "标号名名重用",
                "source": "GJB 4.1.1.2",
                "num": 5
            },
            {
                "standard": "THEN语句为空",
                "source": "GJB 4.3.1.1",
                "num": 1
            },
            {
                "standard": "过程名重用",
                "source": "GJB 4.1.1.1",
                "num": 2
            },
            {
                "standard": "标号名名重用",
                "source": "GJB 4.1.1.2",
                "num": 5
            },
            {
                "standard": "THEN语句为空",
                "source": "GJB 4.3.1.1",
                "num": 1
            },
            {
                "standard": "过程名重用",
                "source": "GJB 4.1.1.1",
                "num": 2
            },
            {
                "standard": "标号名名重用",
                "source": "GJB 4.1.1.2",
                "num": 5
            },
            {
                "standard": "THEN语句为空",
                "source": "GJB 4.3.1.1",
                "num": 1
            },
        ],
        "suggestedTable": [
            {
                "standard": "过程名重用",
                "source": "GJB 4.1.1.1",
                "num": 2
            },
            {
                "standard": "标号名名重用",
                "source": "GJB 4.1.1.2",
                "num": 5
            },
            {
                "standard": "THEN语句为空",
                "source": "GJB 4.3.1.1",
                "num": 1
            },
            {
                "standard": "过程名重用",
                "source": "GJB 4.1.1.1",
                "num": 2
            },
            {
                "standard": "标号名名重用",
                "source": "GJB 4.1.1.2",
                "num": 5
            },
            {
                "standard": "THEN语句为空",
                "source": "GJB 4.3.1.1",
                "num": 1
            },
            {
                "standard": "过程名重用",
                "source": "GJB 4.1.1.1",
                "num": 2
            },
            {
                "standard": "标号名名重用",
                "source": "GJB 4.1.1.2",
                "num": 5
            },
            {
                "standard": "THEN语句为空",
                "source": "GJB 4.3.1.1",
                "num": 1
            },
            {
                "standard": "过程名重用",
                "source": "GJB 4.1.1.1",
                "num": 2
            },
            {
                "standard": "标号名名重用",
                "source": "GJB 4.1.1.2",
                "num": 5
            },
            {
                "standard": "THEN语句为空",
                "source": "GJB 4.3.1.1",
                "num": 1
            },
            {
                "standard": "过程名重用",
                "source": "GJB 4.1.1.1",
                "num": 2
            },
            {
                "standard": "标号名名重用",
                "source": "GJB 4.1.1.2",
                "num": 5
            },
            {
                "standard": "THEN语句为空",
                "source": "GJB 4.3.1.1",
                "num": 1
            },
            {
                "standard": "过程名重用",
                "source": "GJB 4.1.1.1",
                "num": 2
            },
            {
                "standard": "标号名名重用",
                "source": "GJB 4.1.1.2",
                "num": 5
            },
            {
                "standard": "THEN语句为空",
                "source": "GJB 4.3.1.1",
                "num": 1
            },
        ],
    }
    return jsonify(data)


@app.post("/bad_ratio_detect/setThreshold/<projectname>")
def setThreshold(projectname):
    """
    坏味率计算 输入阈值获取结果
    params:
        threshold: 设置的阈值
    """
    threshold = request.get_json()
    data = {
        "c_info": {
            "statisticTable": [
                # 坏味名称个数统计表
                {
                    "name": "长函数代码坏味",  # 代码坏味名称
                    "num": 13,  # 坏味个数
                },
                {
                    "name": "长参数代码坏味",
                    "num": 16,
                },
                {
                    "name": "注释代码坏味",
                    "num": 2,
                },
                {
                    "name": "过深函数调用代码坏味",
                    "num": 8,
                },
                {
                    "name": "扇入扇出代码坏味",
                    "num": 9,
                },
                {
                    "name": "代码克隆代码坏味",
                    "num": 10,
                },
            ],
            "DT": 16.9,
            "NPF": 23,
            "NCFBS": 55,
            "NCF": 47,
            "RNCF": 34.67,  # 百分比
            "RNCFBS": 35.67,  # 百分比
            "fileBadvalue": [
                {
                    "filename": "a.c",
                    "badSmellNum": 10,  # 坏味数量
                    "badSmellKindNum": 2,  # 坏味种类数量
                },
                {
                    "filename": "b.c",
                    "badSmellNum": 12,  # 坏味数量
                    "badSmellKindNum": 3,  # 坏味种类数量
                }
            ],
            "result": [
                {
                    "key": "longFunc",  # 条目的key值
                    "totalNum": 300,  # 结果总数
                    "name": "长函数",  # 名字
                    "def": "代码长度超过规定阈值的函数",  # 定义
                    "threshold": 100,  # 阈值
                    "title": {
                        # 与表头对应关系 key:表头名称
                        "fileName": "文件名",
                        "funcName": "函数名",
                        "funcLength": "函数长度",
                    },
                    # 初始给20条
                    "detectionResults": [
                        {
                            # 具体数据后端定义
                            "fileName": "a.c",
                            "funcName": "func_a",
                            "funcLength": "102",
                        },
                        {
                            # 具体数据后端定义
                            "fileName": "b.c",
                            "funcName": "func_b",
                            "funcLength": "103",
                        },
                        {
                            # 具体数据后端定义
                            "fileName": "c.c",
                            "funcName": "func_c",
                            "funcLength": "104",
                        }
                    ],  # 检测结果
                    "otherInfo": [
                        {
                            "name": "坏味检测时间",
                            "value": "1.89秒",
                        },
                        {
                            "name": "含坏味文件数",
                            "value": "11个",
                        },
                        {
                            "name": "该坏味文件占比",
                            "value": "0.15",
                        },
                        {
                            "name": "最长文件长度",
                            "value": "494行",
                        },
                        {
                            "name": "坏味检测时间",
                            "value": "1.89秒",
                        },
                        {
                            "name": "含坏味文件数",
                            "value": "11个",
                        },
                        {
                            "name": "该坏味文件占比",
                            "value": "0.15",
                        },
                        {
                            "name": "最长文件长度",
                            "value": "494行",
                        },
                    ],
                },
                {
                    "name": "长参数",  # 名字
                    "def": "函数参数个数超过规定阈值",  # 定义
                    "threshold": 5,  # 阈值
                    "title": {
                        # 与表头对应关系 key:表头名称
                        "fileName": "文件名",
                        "funcName": "函数名",
                        "paraLength": "参数长度",
                    },
                    "detectionResults": [
                        {
                            # 具体数据后端定义
                            "fileName": "a.c",
                            "funcName": "func_a",
                            "paraLength": "102",
                        },
                        {
                            # 具体数据后端定义
                            "fileName": "b.c",
                            "funcName": "func_b",
                            "paraLength": "103",
                        },
                        {
                            # 具体数据后端定义
                            "fileName": "c.c",
                            "funcName": "func_c",
                            "paraLength": "104",
                        },
                    ],  # 检测结果
                    "otherInfo": [
                        {
                            "name": "坏味检测时间",
                            "value": "0.62秒",
                        },
                        {
                            "name": "含坏味文件数",
                            "value": "3个",
                        },
                        {
                            "name": "该坏味文件占比",
                            "value": "0.04",
                        },
                        {
                            "name": "最长参数长度",
                            "value": "16个",
                        },
                        {
                            "name": "坏味检测时间",
                            "value": "1.89秒",
                        },
                        {
                            "name": "含坏味文件数",
                            "value": "11个",
                        },
                        {
                            "name": "该坏味文件占比",
                            "value": "0.15",
                        },
                        {
                            "name": "最长文件长度",
                            "value": "494行",
                        },
                    ],
                },
                {
                    "name": "长函数",  # 名字
                    "def": "代码长度超过规定阈值的函数",  # 定义
                    "threshold": 100,  # 阈值
                    "title": {
                        # 与表头对应关系 key:表头名称
                        "fileName": "文件名",
                        "funcName": "函数名",
                        "funcLength": "函数长度",
                    },
                    "detectionResults": [
                        {
                            # 具体数据后端定义
                            "fileName": "c.c",
                            "funcName": "func_c",
                            "funcLength": "104",
                        },
                        {
                            # 具体数据后端定义
                            "fileName": "a.c",
                            "funcName": "func_a",
                            "funcLength": "102",
                        },
                        {
                            # 具体数据后端定义
                            "fileName": "b.c",
                            "funcName": "func_b",
                            "funcLength": "103",
                        },
                        {
                            # 具体数据后端定义
                            "fileName": "c.c",
                            "funcName": "func_c",
                            "funcLength": "104",
                        },
                        {
                            # 具体数据后端定义
                            "fileName": "a.c",
                            "funcName": "func_a",
                            "funcLength": "102",
                        },
                        {
                            # 具体数据后端定义
                            "fileName": "b.c",
                            "funcName": "func_b",
                            "funcLength": "103",
                        },
                        {
                            # 具体数据后端定义
                            "fileName": "c.c",
                            "funcName": "func_c",
                            "funcLength": "104",
                        },
                    ],  # 检测结果
                    "otherInfo": [
                        {
                            "name": "坏味检测时间",
                            "value": "1.89秒",
                        },
                        {
                            "name": "含坏味文件数",
                            "value": "11个",
                        },
                        {
                            "name": "该坏味文件占比",
                            "value": "0.15",
                        },
                        {
                            "name": "最长文件长度",
                            "value": "494行",
                        },
                        {
                            "name": "坏味检测时间",
                            "value": "1.89秒",
                        },
                        {
                            "name": "含坏味文件数",
                            "value": "11个",
                        },
                        {
                            "name": "该坏味文件占比",
                            "value": "0.15",
                        },
                        {
                            "name": "最长文件长度",
                            "value": "494行",
                        },
                    ],
                },
                {
                    "name": "长参数",  # 名字
                    "def": "函数参数个数超过规定阈值",  # 定义
                    "threshold": 5,  # 阈值
                    "title": {
                        # 与表头对应关系 key:表头名称
                        "fileName": "文件名",
                        "funcName": "函数名",
                        "paraLength": "参数长度",
                    },
                    "detectionResults": [
                        {
                            # 具体数据后端定义
                            "fileName": "a.c",
                            "funcName": "func_a",
                            "paraLength": "102",
                        },
                        {
                            # 具体数据后端定义
                            "fileName": "b.c",
                            "funcName": "func_b",
                            "paraLength": "103",
                        },
                        {
                            # 具体数据后端定义
                            "fileName": "c.c",
                            "funcName": "func_c",
                            "paraLength": "104",
                        },
                    ],  # 检测结果
                    "otherInfo": [
                        {
                            "name": "坏味检测时间",
                            "value": "0.62秒",
                        },
                        {
                            "name": "含坏味文件数",
                            "value": "3个",
                        },
                        {
                            "name": "该坏味文件占比",
                            "value": "0.04",
                        },
                        {
                            "name": "最长参数长度",
                            "value": "16个",
                        },
                        {
                            "name": "坏味检测时间",
                            "value": "1.89秒",
                        },
                        {
                            "name": "含坏味文件数",
                            "value": "11个",
                        },
                        {
                            "name": "该坏味文件占比",
                            "value": "0.15",
                        },
                        {
                            "name": "最长文件长度",
                            "value": "494行",
                        },
                    ],
                },
            ]
        },
        "c_plus_info": {
            "statisticTable": [
                # 坏味名称个数统计表
                {
                    "name": "过长类代码坏味",  # 代码坏味名称
                    "num": 18,  # 坏味个数
                },
                {
                    "name": "长参数代码坏味",
                    "num": 4,
                },
                {
                    "name": "注释代码坏味",
                    "num": 5,
                },
                {
                    "name": "过深函数调用代码坏味",
                    "num": 19,
                },
                {
                    "name": "扇入扇出代码坏味",
                    "num": 18,
                },
                {
                    "name": "代码克隆代码坏味",
                    "num": 18,
                },
                {
                    "name": "过长类代码坏味",  # 代码坏味名称
                    "num": 18,  # 坏味个数
                },
                {
                    "name": "长参数代码坏味",
                    "num": 4,
                },
                {
                    "name": "注释代码坏味",
                    "num": 5,
                },
                {
                    "name": "过深函数调用代码坏味",
                    "num": 19,
                },
                {
                    "name": "扇入扇出代码坏味",
                    "num": 18,
                },
                {
                    "name": "代码克隆代码坏味",
                    "num": 18,
                },
            ],
            "DT": 16.33,
            "NPF": 75,
            "NCFBS": 14,
            "NCF": 67,
            "RNCF": 54.67,  # 百分比
            "RNCFBS": 12.67,  # 百分比
            "fileBadvalue": [
                {
                    "filename": "a.c",
                    "badSmellNum": 8,  # 坏味数量
                    "badSmellKindNum": 4,  # 坏味种类数量
                },
                {
                    "filename": "b.c",
                    "badSmellNum": 9,  # 坏味数量
                    "badSmellKindNum": 6,  # 坏味种类数量
                }
            ],
            "result": [
                {
                    "key": "longFunc",  # 条目的key值
                    "totalNum": 300,  # 结果总数
                    "name": "长函数",  # 名字
                    "def": "代码长度超过规定阈值的函数",  # 定义
                    "threshold": 100,  # 阈值
                    "title": {
                        # 与表头对应关系 key:表头名称
                        "fileName": "文件名",
                        "funcName": "函数名",
                        "funcLength": "函数长度",
                    },
                    "detectionResults": [
                        {
                            # 具体数据后端定义
                            "fileName": "a.c",
                            "funcName": "func_a",
                            "funcLength": "102",
                        },
                        {
                            # 具体数据后端定义
                            "fileName": "b.c",
                            "funcName": "func_b",
                            "funcLength": "103",
                        },
                        {
                            # 具体数据后端定义
                            "fileName": "c.c",
                            "funcName": "func_c",
                            "funcLength": "104",
                        },
                        {
                            # 具体数据后端定义
                            "fileName": "a.c",
                            "funcName": "func_a",
                            "funcLength": "102",
                        },
                        {
                            # 具体数据后端定义
                            "fileName": "b.c",
                            "funcName": "func_b",
                            "funcLength": "103",
                        },
                        {
                            # 具体数据后端定义
                            "fileName": "c.c",
                            "funcName": "func_c",
                            "funcLength": "104",
                        },
                        {
                            # 具体数据后端定义
                            "fileName": "a.c",
                            "funcName": "func_a",
                            "funcLength": "102",
                        },
                        {
                            # 具体数据后端定义
                            "fileName": "b.c",
                            "funcName": "func_b",
                            "funcLength": "103",
                        },
                        {
                            # 具体数据后端定义
                            "fileName": "c.c",
                            "funcName": "func_c",
                            "funcLength": "104",
                        }
                    ],  # 检测结果
                    "otherInfo": [
                        {
                            "name": "坏味检测时间",
                            "value": "1.89秒",
                        },
                        {
                            "name": "含坏味文件数",
                            "value": "11个",
                        },
                        {
                            "name": "该坏味文件占比",
                            "value": "0.15",
                        },
                        {
                            "name": "最长文件长度",
                            "value": "494行",
                        },
                        {
                            "name": "坏味检测时间",
                            "value": "1.89秒",
                        },
                        {
                            "name": "含坏味文件数",
                            "value": "11个",
                        },
                        {
                            "name": "该坏味文件占比",
                            "value": "0.15",
                        },
                        {
                            "name": "最长文件长度",
                            "value": "494行",
                        },
                    ],
                },
                {
                    "name": "长参数",  # 名字
                    "def": "函数参数个数超过规定阈值",  # 定义
                    "threshold": 5,  # 阈值
                    "title": {
                        # 与表头对应关系 key:表头名称
                        "fileName": "文件名",
                        "funcName": "函数名",
                        "paraLength": "参数长度",
                    },
                    "detectionResults": [
                        {
                            # 具体数据后端定义
                            "fileName": "a.c",
                            "funcName": "func_a",
                            "paraLength": "102",
                        },
                        {
                            # 具体数据后端定义
                            "fileName": "b.c",
                            "funcName": "func_b",
                            "paraLength": "103",
                        },
                        {
                            # 具体数据后端定义
                            "fileName": "c.c",
                            "funcName": "func_c",
                            "paraLength": "104",
                        },
                    ],  # 检测结果
                    "otherInfo": [
                        {
                            "name": "坏味检测时间",
                            "value": "0.62秒",
                        },
                        {
                            "name": "含坏味文件数",
                            "value": "3个",
                        },
                        {
                            "name": "该坏味文件占比",
                            "value": "0.04",
                        },
                        {
                            "name": "最长参数长度",
                            "value": "16个",
                        },
                        {
                            "name": "坏味检测时间",
                            "value": "1.89秒",
                        },
                        {
                            "name": "含坏味文件数",
                            "value": "11个",
                        },
                        {
                            "name": "该坏味文件占比",
                            "value": "0.15",
                        },
                        {
                            "name": "最长文件长度",
                            "value": "494行",
                        },
                    ],
                },
                {
                    "name": "长函数",  # 名字
                    "def": "代码长度超过规定阈值的函数",  # 定义
                    "threshold": 100,  # 阈值
                    "title": {
                        # 与表头对应关系 key:表头名称
                        "fileName": "文件名",
                        "funcName": "函数名",
                        "funcLength": "函数长度",
                    },
                    "detectionResults": [
                        {
                            # 具体数据后端定义
                            "fileName": "c.c",
                            "funcName": "func_c",
                            "funcLength": "104",
                        },
                        {
                            # 具体数据后端定义
                            "fileName": "a.c",
                            "funcName": "func_a",
                            "funcLength": "102",
                        },
                        {
                            # 具体数据后端定义
                            "fileName": "b.c",
                            "funcName": "func_b",
                            "funcLength": "103",
                        },
                        {
                            # 具体数据后端定义
                            "fileName": "c.c",
                            "funcName": "func_c",
                            "funcLength": "104",
                        },
                        {
                            # 具体数据后端定义
                            "fileName": "a.c",
                            "funcName": "func_a",
                            "funcLength": "102",
                        },
                        {
                            # 具体数据后端定义
                            "fileName": "b.c",
                            "funcName": "func_b",
                            "funcLength": "103",
                        },
                        {
                            # 具体数据后端定义
                            "fileName": "c.c",
                            "funcName": "func_c",
                            "funcLength": "104",
                        },
                    ],  # 检测结果
                    "otherInfo": [
                        {
                            "name": "坏味检测时间",
                            "value": "1.89秒",
                        },
                        {
                            "name": "含坏味文件数",
                            "value": "11个",
                        },
                        {
                            "name": "该坏味文件占比",
                            "value": "0.15",
                        },
                        {
                            "name": "最长文件长度",
                            "value": "494行",
                        },
                        {
                            "name": "坏味检测时间",
                            "value": "1.89秒",
                        },
                        {
                            "name": "含坏味文件数",
                            "value": "11个",
                        },
                        {
                            "name": "该坏味文件占比",
                            "value": "0.15",
                        },
                        {
                            "name": "最长文件长度",
                            "value": "494行",
                        },
                    ],
                },
                {
                    "name": "长参数",  # 名字
                    "def": "函数参数个数超过规定阈值",  # 定义
                    "threshold": 5,  # 阈值
                    "title": {
                        # 与表头对应关系 key:表头名称
                        "fileName": "文件名",
                        "funcName": "函数名",
                        "paraLength": "参数长度",
                    },
                    "detectionResults": [
                        {
                            # 具体数据后端定义
                            "fileName": "a.c",
                            "funcName": "func_a",
                            "paraLength": "102",
                        },
                        {
                            # 具体数据后端定义
                            "fileName": "b.c",
                            "funcName": "func_b",
                            "paraLength": "103",
                        },
                        {
                            # 具体数据后端定义
                            "fileName": "c.c",
                            "funcName": "func_c",
                            "paraLength": "104",
                        },
                    ],  # 检测结果
                    "otherInfo": [
                        {
                            "name": "坏味检测时间",
                            "value": "0.62秒",
                        },
                        {
                            "name": "含坏味文件数",
                            "value": "3个",
                        },
                        {
                            "name": "该坏味文件占比",
                            "value": "0.04",
                        },
                        {
                            "name": "最长参数长度",
                            "value": "16个",
                        },
                        {
                            "name": "坏味检测时间",
                            "value": "1.89秒",
                        },
                        {
                            "name": "含坏味文件数",
                            "value": "11个",
                        },
                        {
                            "name": "该坏味文件占比",
                            "value": "0.15",
                        },
                        {
                            "name": "最长文件长度",
                            "value": "494行",
                        },
                    ],
                },
            ]
        }
    }
    return jsonify(data)


@app.get("/bad_ratio_detect/detection_results/<key>/<projectname>/<pageNum>")
def detection_results(key, projectname, pageNum):
    data = {
        # 20条
        "detectionResults": [
            {
                # 具体数据后端定义
                "fileName": "a.c",
                "funcName": "func_a",
                "funcLength": "102",
            },
            {
                # 具体数据后端定义
                "fileName": "b.c",
                "funcName": "func_b",
                "funcLength": "103",
            },
            {
                # 具体数据后端定义
                "fileName": "c.c",
                "funcName": "func_c",
                "funcLength": "104",
            }
        ],
        "totalNum": 300  # 总数目
    }


@app.get("/change_information_detection/<projectname>")
def change_information_detection(projectname):
    """
    变更信息检测
    params:
        selectedVersion: 选择的版本名称
    """
    selectedVersion = request.args.get("selectedVersion")

    data = {
        # c信息，没有则给空字典{}
        "c_info": {
            # 系统级别变更信息
            "systemLevel": {
                # 当前版本
                "versionLatest": {
                    "name": "version 1.3",  # 版本名称
                    "fileNum": 36,  # 文件数
                    "functionNum": 1101,  # 函数数
                    "codeNum": 35754  # 代码行数
                },
                # 选择的旧版本
                "versionSelected": {
                    "name": "version 1.0",  # 版本名称
                    "fileNum": 39,  # 文件数
                    "functionNum": 1298,  # 函数数
                    "codeNum": 36890  # 代码行数
                },
                # 设计质量
                "designInformation": [
                    {
                        "indexName": "modifiability",
                        "result": 0,
                        "minimumValue": 0,  # 范围最小值
                        "maximumValue": 0.5,  # 范围最大值
                        "trend": 2,
                        "versionLatest": 0.981,
                        "versionSelected": 0.981
                    },
                    {
                        "indexName": "scalability",
                        "result": 0,
                        "minimumValue": 0,  # 范围最小值
                        "maximumValue": 1,  # 范围最大值
                        "trend": 2,
                        "versionLatest": 0.435,
                        "versionSelected": 0.435
                    },
                    {
                        "indexName": "testability",
                        "result": 0,
                        "minimumValue": 0,  # 范围最小值
                        "maximumValue": 1,  # 范围最大值
                        "trend": 2,
                        "versionLatest": 0.991,
                        "versionSelected": 0.991
                    },
                    {
                        "indexName": "refundability",
                        "result": 0,
                        "minimumValue": 0,  # 范围最小值
                        "maximumValue": 1,  # 范围最大值
                        "trend": 2,
                        "versionLatest": 0.495,
                        "versionSelected": 0.495
                    },
                    {
                        "indexName": "comprehensibility",
                        "result": 0,
                        "minimumValue": 0,  # 范围最小值
                        "maximumValue": 1,  # 范围最大值
                        "trend": 2,
                        "versionLatest": 0.291,
                        "versionSelected": 0.291
                    }
                ],
                # 指标信息表
                "indexInformation": [
                    {
                        "indexName": "易理解性",  # 指标名称
                        "versionSelected": 0.288,  # 选择的版本值
                        "versionLatest": 0.367,  # 当前的版本值
                        "minimumValue": 0,  # 范围最小值
                        "maximumValue": 1,  # 范围最大值
                        "trend": 1,  # 趋势：0降低，1升高
                        "result": 1  # 检测结果: 0不合格，1合格
                    },
                    {
                        "indexName": "可替换性",  # 指标名称
                        "versionSelected": 0.288,  # 选择的版本值
                        "versionLatest": 0.367,  # 当前的版本值
                        "minimumValue": 0,  # 范围最小值
                        "maximumValue": 1,  # 范围最大值
                        "trend": 0,  # 趋势：0降低，1升高
                        "result": 0
                    },
                    {
                        "indexName": "易理解性1",  # 指标名称
                        "versionSelected": 0.288,  # 选择的版本值
                        "versionLatest": 0.367,  # 当前的版本值
                        "minimumValue": 0,  # 范围最小值
                        "maximumValue": 1,  # 范围最大值
                        "trend": 2,  # 趋势：0降低，1升高
                        "result": 1
                    },
                    {
                        "indexName": "可替换性1",  # 指标名称
                        "versionSelected": 0.288,  # 选择的版本值
                        "versionLatest": 0.367,  # 当前的版本值
                        "minimumValue": 0,  # 范围最小值
                        "maximumValue": 1,  # 范围最大值
                        "trend": 0,  # 趋势：0降低，1升高
                        "result": 1
                    },
                    {
                        "indexName": "易理解性2",  # 指标名称
                        "versionSelected": 0.288,  # 选择的版本值
                        "versionLatest": 0.367,  # 当前的版本值
                        "minimumValue": 0,  # 范围最小值
                        "maximumValue": 1,  # 范围最大值
                        "trend": 1,  # 趋势：0降低，1升高
                        "result": 1
                    },
                    {
                        "indexName": "可替换性2",  # 指标名称
                        "versionSelected": 0.288,  # 选择的版本值
                        "versionLatest": 0.367,  # 当前的版本值
                        "minimumValue": 0,  # 范围最小值
                        "maximumValue": 1,  # 范围最大值
                        "trend": 1,  # 趋势：0降低，1升高
                        "result": 1
                    },
                    {
                        "indexName": "易理解性3",  # 指标名称
                        "versionSelected": 0.288,  # 选择的版本值
                        "versionLatest": 0.367,  # 当前的版本值
                        "minimumValue": 0,  # 范围最小值
                        "maximumValue": 1,  # 范围最大值
                        "trend": 0,  # 趋势：0降低，1升高
                        "result": 1
                    },
                    {
                        "indexName": "可替换性3",  # 指标名称
                        "versionSelected": 0.288,  # 选择的版本值
                        "versionLatest": 0.367,  # 当前的版本值
                        "minimumValue": 0,  # 范围最小值
                        "maximumValue": 1,  # 范围最大值
                        "trend": 2,  # 趋势：0降低，1升高
                        "result": 0
                    },
                    {
                        "indexName": "易理解性4",  # 指标名称
                        "versionSelected": 0.288,  # 选择的版本值
                        "versionLatest": 0.367,  # 当前的版本值
                        "minimumValue": 0,  # 范围最小值
                        "maximumValue": 1,  # 范围最大值
                        "trend": 0,  # 趋势：0降低，1升高
                        "result": 1
                    },
                    {
                        "indexName": "可替换性4",  # 指标名称
                        "versionSelected": 0.288,  # 选择的版本值
                        "versionLatest": 0.367,  # 当前的版本值
                        "minimumValue": 0,  # 范围最小值
                        "maximumValue": 1,  # 范围最大值
                        "trend": 0,  # 趋势：0降低，1升高
                        "result": 1
                    },
                    # 其他指标
                ]
            },
            # 文件级别变更信息
            "fileLevel": {
                "updateFileNum": 25,  # 修改的文件数
                "deleteFileNum": 3,  # 删除的文件数
                "insertFileNum": 5,  # 新增的文件数
                # 文件数
                "selectedFileTree": [
                    {
                        "id": 1,
                        "label": "test1",
                        "type": "dir",
                        "children": [
                            {
                                "id": 3,
                                "label": "test1-1.c",
                                "type": "file",
                                "status": 0,
                                "fileInfo": {
                                    "funcNum": 3,
                                    "globalVariableNum": 1,
                                    "fileSize": "2.3KB",
                                    "outDegree": 2,
                                    "inDegree": 5,
                                    "annotationLine": 10
                                }
                            },
                            {
                                "id": 4,
                                "label": "test1-2",
                                "type": "dir",
                                "children": [

                                    {
                                        "id": 7,
                                        "label": "test1-2-1.c",
                                        "type": "file",
                                        "status": 1,
                                        "fileInfo": {
                                            "funcNum": 3,
                                            "globalVariableNum": 1,
                                            "fileSize": "2.3KB",
                                            "outDegree": 2,
                                            "inDegree": 5,
                                            "annotationLine": 10
                                        }
                                    },
                                    {
                                        "id": 8,
                                        "label": "test1-2-2.c",
                                        "type": "file",
                                        "status": 2,
                                        "fileInfo": {
                                            "funcNum": 3,
                                            "globalVariableNum": 1,
                                            "fileSize": "2.3KB",
                                            "outDegree": 2,
                                            "inDegree": 5,
                                            "annotationLine": 10
                                        }
                                    }
                                ]
                            }
                        ],
                    },
                    {
                        "id": 2,
                        "label": "test2",
                        "type": "dir",
                        "children": [
                            {
                                "id": 2,
                                "label": "test2-1",
                                "type": "dir",
                                "children": [
                                    {
                                        "id": 5,
                                        "label": "test2-1-1.c",
                                        "type": "file",
                                        "status": 2,
                                        "fileInfo": {
                                            "funcNum": 3,
                                            "globalVariableNum": 1,
                                            "fileSize": "2.3KB",
                                            "outDegree": 2,
                                            "inDegree": 5,
                                            "annotationLine": 10
                                        }
                                    },
                                    {
                                        "id": 6,
                                        "label": "test2-1-2.c",
                                        "type": "file",
                                        "status": 3,
                                        "fileInfo": {
                                            "funcNum": 3,
                                            "globalVariableNum": 1,
                                            "fileSize": "2.3KB",
                                            "outDegree": 2,
                                            "inDegree": 5,
                                            "annotationLine": 10
                                        }
                                    }
                                ]
                            },
                            {
                                "id": 5,
                                "label": "test2-2.c",
                                "type": "file",
                                "status": 0,
                                "fileInfo": {
                                    "funcNum": 3,
                                    "globalVariableNum": 1,
                                    "fileSize": "2.3KB",
                                    "outDegree": 2,
                                    "inDegree": 5,
                                    "annotationLine": 10
                                }
                            },
                            {
                                "id": 6,
                                "label": "test2-3.c",
                                "type": "file",
                                "status": 3,
                                "fileInfo": {
                                    "funcNum": 3,
                                    "globalVariableNum": 1,
                                    "fileSize": "2.3KB",
                                    "outDegree": 2,
                                    "inDegree": 5,
                                    "annotationLine": 10
                                }
                            }
                        ]
                    },
                    {
                        "id": 1,
                        "label": "test1",
                        "type": "dir",
                        "children": [
                            {
                                "id": 3,
                                "label": "test1-1.c",
                                "type": "file",
                                "status": 0,
                                "fileInfo": {
                                    "funcNum": 3,
                                    "globalVariableNum": 1,
                                    "fileSize": "2.3KB",
                                    "outDegree": 2,
                                    "inDegree": 5,
                                    "annotationLine": 10
                                }
                            },
                            {
                                "id": 4,
                                "label": "test1-2",
                                "type": "dir",
                                "children": [

                                    {
                                        "id": 7,
                                        "label": "test1-2-1.c",
                                        "type": "file",
                                        "status": 1,
                                        "fileInfo": {
                                            "funcNum": 3,
                                            "globalVariableNum": 1,
                                            "fileSize": "2.3KB",
                                            "outDegree": 2,
                                            "inDegree": 5,
                                            "annotationLine": 10
                                        }
                                    },
                                    {
                                        "id": 8,
                                        "label": "test1-2-2.c",
                                        "type": "file",
                                        "status": 2,
                                        "fileInfo": {
                                            "funcNum": 3,
                                            "globalVariableNum": 1,
                                            "fileSize": "2.3KB",
                                            "outDegree": 2,
                                            "inDegree": 5,
                                            "annotationLine": 10
                                        }
                                    }
                                ]
                            }
                        ],
                    },
                    {
                        "id": 2,
                        "label": "test2",
                        "type": "dir",
                        "children": [
                            {
                                "id": 2,
                                "label": "test2-1",
                                "type": "dir",
                                "children": [
                                    {
                                        "id": 5,
                                        "label": "test2-1-1.c",
                                        "type": "file",
                                        "status": 2,
                                        "fileInfo": {
                                            "funcNum": 3,
                                            "globalVariableNum": 1,
                                            "fileSize": "2.3KB",
                                            "outDegree": 2,
                                            "inDegree": 5,
                                            "annotationLine": 10
                                        }
                                    },
                                    {
                                        "id": 6,
                                        "label": "test2-1-2.c",
                                        "type": "file",
                                        "status": 3,
                                        "fileInfo": {
                                            "funcNum": 3,
                                            "globalVariableNum": 1,
                                            "fileSize": "2.3KB",
                                            "outDegree": 2,
                                            "inDegree": 5,
                                            "annotationLine": 10
                                        }
                                    }
                                ]
                            },
                            {
                                "id": 5,
                                "label": "test2-2.c",
                                "type": "file",
                                "status": 0,
                                "fileInfo": {
                                    "funcNum": 3,
                                    "globalVariableNum": 1,
                                    "fileSize": "2.3KB",
                                    "outDegree": 2,
                                    "inDegree": 5,
                                    "annotationLine": 10
                                }
                            },
                            {
                                "id": 6,
                                "label": "test2-3.c",
                                "type": "file",
                                "status": 3,
                                "fileInfo": {
                                    "funcNum": 3,
                                    "globalVariableNum": 1,
                                    "fileSize": "2.3KB",
                                    "outDegree": 2,
                                    "inDegree": 5,
                                    "annotationLine": 10
                                }
                            }
                        ]
                    },
                    {
                        "id": 1,
                        "label": "test1",
                        "type": "dir",
                        "children": [
                            {
                                "id": 3,
                                "label": "test1-1.c",
                                "type": "file",
                                "status": 0,
                                "fileInfo": {
                                    "funcNum": 3,
                                    "globalVariableNum": 1,
                                    "fileSize": "2.3KB",
                                    "outDegree": 2,
                                    "inDegree": 5,
                                    "annotationLine": 10
                                }
                            },
                            {
                                "id": 4,
                                "label": "test1-2",
                                "type": "dir",
                                "children": [

                                    {
                                        "id": 7,
                                        "label": "test1-2-1.c",
                                        "type": "file",
                                        "status": 1,
                                        "fileInfo": {
                                            "funcNum": 3,
                                            "globalVariableNum": 1,
                                            "fileSize": "2.3KB",
                                            "outDegree": 2,
                                            "inDegree": 5,
                                            "annotationLine": 10
                                        }
                                    },
                                    {
                                        "id": 8,
                                        "label": "test1-2-2.c",
                                        "type": "file",
                                        "status": 2,
                                        "fileInfo": {
                                            "funcNum": 3,
                                            "globalVariableNum": 1,
                                            "fileSize": "2.3KB",
                                            "outDegree": 2,
                                            "inDegree": 5,
                                            "annotationLine": 10
                                        }
                                    }
                                ]
                            }
                        ],
                    },
                    {
                        "id": 2,
                        "label": "test2",
                        "type": "dir",
                        "children": [
                            {
                                "id": 2,
                                "label": "test2-1",
                                "type": "dir",
                                "children": [
                                    {
                                        "id": 5,
                                        "label": "test2-1-1.c",
                                        "type": "file",
                                        "status": 2,
                                        "fileInfo": {
                                            "funcNum": 3,
                                            "globalVariableNum": 1,
                                            "fileSize": "2.3KB",
                                            "outDegree": 2,
                                            "inDegree": 5,
                                            "annotationLine": 10
                                        }
                                    },
                                    {
                                        "id": 6,
                                        "label": "test2-1-2.c",
                                        "type": "file",
                                        "status": 3,
                                        "fileInfo": {
                                            "funcNum": 3,
                                            "globalVariableNum": 1,
                                            "fileSize": "2.3KB",
                                            "outDegree": 2,
                                            "inDegree": 5,
                                            "annotationLine": 10
                                        }
                                    }
                                ]
                            },
                            {
                                "id": 5,
                                "label": "test2-2.c",
                                "type": "file",
                                "status": 0,
                                "fileInfo": {
                                    "funcNum": 3,
                                    "globalVariableNum": 1,
                                    "fileSize": "2.3KB",
                                    "outDegree": 2,
                                    "inDegree": 5,
                                    "annotationLine": 10
                                }
                            },
                            {
                                "id": 6,
                                "label": "test2-3.c",
                                "type": "file",
                                "status": 3,
                                "fileInfo": {
                                    "funcNum": 3,
                                    "globalVariableNum": 1,
                                    "fileSize": "2.3KB",
                                    "outDegree": 2,
                                    "inDegree": 5,
                                    "annotationLine": 10
                                }
                            }
                        ]
                    }
                ],
                "latestFileTree": [
                    {
                        "id": 1,
                        "label": "test1",
                        "type": "dir",
                        "children": [
                            {
                                "id": 3,
                                "label": "test1-1.c",
                                "type": "file",
                                "status": 1,
                                "fileInfo": {
                                    "funcNum": 3,
                                    "globalVariableNum": 1,
                                    "fileSize": "2.3KB",
                                    "outDegree": 2,
                                    "inDegree": 5,
                                    "annotationLine": 10
                                }
                            },
                            {
                                "id": 4,
                                "label": "test1-2",
                                "type": "dir",
                                "children": [

                                    {
                                        "id": 7,
                                        "label": "test1-2-1.c",
                                        "type": "file",
                                        "status": 0,
                                        "fileInfo": {
                                            "funcNum": 3,
                                            "globalVariableNum": 1,
                                            "fileSize": "2.3KB",
                                            "outDegree": 2,
                                            "inDegree": 5,
                                            "annotationLine": 10
                                        }
                                    },
                                    {
                                        "id": 8,
                                        "label": "test1-2-2.c",
                                        "type": "file",
                                        "status": 3,
                                        "fileInfo": {
                                            "funcNum": 3,
                                            "globalVariableNum": 1,
                                            "fileSize": "2.3KB",
                                            "outDegree": 2,
                                            "inDegree": 5,
                                            "annotationLine": 10
                                        }
                                    }
                                ]
                            }
                        ],
                    },
                    {
                        "id": 2,
                        "label": "test2",
                        "type": "dir",
                        "children": [
                            {
                                "id": 2,
                                "label": "test2-1",
                                "type": "dir",
                                "children": [
                                    {
                                        "id": 5,
                                        "label": "test2-1-1.c",
                                        "type": "file",
                                        "status": 2,
                                        "fileInfo": {
                                            "funcNum": 3,
                                            "globalVariableNum": 1,
                                            "fileSize": "2.3KB",
                                            "outDegree": 2,
                                            "inDegree": 5,
                                            "annotationLine": 10
                                        }
                                    },
                                    {
                                        "id": 6,
                                        "label": "test2-1-2.c",
                                        "type": "file",
                                        "status": 1,
                                        "fileInfo": {
                                            "funcNum": 3,
                                            "globalVariableNum": 1,
                                            "fileSize": "2.3KB",
                                            "outDegree": 2,
                                            "inDegree": 5,
                                            "annotationLine": 10
                                        }
                                    }
                                ]
                            },
                            {
                                "id": 5,
                                "label": "test2-2.c",
                                "type": "file",
                                "status": 0,
                                "fileInfo": {
                                    "funcNum": 3,
                                    "globalVariableNum": 1,
                                    "fileSize": "2.3KB",
                                    "outDegree": 2,
                                    "inDegree": 5,
                                    "annotationLine": 10
                                }
                            },
                            {
                                "id": 6,
                                "label": "test2-3.c",
                                "type": "file",
                                "status": 2,
                                "fileInfo": {
                                    "funcNum": 3,
                                    "globalVariableNum": 1,
                                    "fileSize": "2.3KB",
                                    "outDegree": 2,
                                    "inDegree": 5,
                                    "annotationLine": 10
                                }
                            }
                        ]
                    },
                    {
                        "id": 1,
                        "label": "test1",
                        "type": "dir",
                        "children": [
                            {
                                "id": 3,
                                "label": "test1-1.c",
                                "type": "file",
                                "status": 1,
                                "fileInfo": {
                                    "funcNum": 3,
                                    "globalVariableNum": 1,
                                    "fileSize": "2.3KB",
                                    "outDegree": 2,
                                    "inDegree": 5,
                                    "annotationLine": 10
                                }
                            },
                            {
                                "id": 4,
                                "label": "test1-2",
                                "type": "dir",
                                "children": [

                                    {
                                        "id": 7,
                                        "label": "test1-2-1.c",
                                        "type": "file",
                                        "status": 0,
                                        "fileInfo": {
                                            "funcNum": 3,
                                            "globalVariableNum": 1,
                                            "fileSize": "2.3KB",
                                            "outDegree": 2,
                                            "inDegree": 5,
                                            "annotationLine": 10
                                        }
                                    },
                                    {
                                        "id": 8,
                                        "label": "test1-2-2.c",
                                        "type": "file",
                                        "status": 3,
                                        "fileInfo": {
                                            "funcNum": 3,
                                            "globalVariableNum": 1,
                                            "fileSize": "2.3KB",
                                            "outDegree": 2,
                                            "inDegree": 5,
                                            "annotationLine": 10
                                        }
                                    }
                                ]
                            }
                        ],
                    },
                    {
                        "id": 1,
                        "label": "test1",
                        "type": "dir",
                        "children": [
                            {
                                "id": 3,
                                "label": "test1-1.c",
                                "type": "file",
                                "status": 1,
                                "fileInfo": {
                                    "funcNum": 3,
                                    "globalVariableNum": 1,
                                    "fileSize": "2.3KB",
                                    "outDegree": 2,
                                    "inDegree": 5,
                                    "annotationLine": 10
                                }
                            },
                            {
                                "id": 4,
                                "label": "test1-2",
                                "type": "dir",
                                "children": [

                                    {
                                        "id": 7,
                                        "label": "test1-2-1.c",
                                        "type": "file",
                                        "status": 0,
                                        "fileInfo": {
                                            "funcNum": 3,
                                            "globalVariableNum": 1,
                                            "fileSize": "2.3KB",
                                            "outDegree": 2,
                                            "inDegree": 5,
                                            "annotationLine": 10
                                        }
                                    },
                                    {
                                        "id": 8,
                                        "label": "test1-2-2.c",
                                        "type": "file",
                                        "status": 3,
                                        "fileInfo": {
                                            "funcNum": 3,
                                            "globalVariableNum": 1,
                                            "fileSize": "2.3KB",
                                            "outDegree": 2,
                                            "inDegree": 5,
                                            "annotationLine": 10
                                        }
                                    }
                                ]
                            }
                        ],
                    },
                ]
            },
            # 函数级别变更信息
            "functionLevel": {
                # 参数个数
                "paramNum": {
                    "totalNum": 10,  # 变更总数
                    "totalProp": "46.58%",  # 变更占比
                    "increaseNum": 66,  # 增加数
                    "increaseProp": "32.6%",  # 增加占比
                    "decreaseNum": 34,  # 降低数
                    "decreaseProp": "18.3%",  # 降低占比
                    # 变更信息列表
                    "changeinfoList": [
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 666,  # 选择的旧版本指标值
                            "latestValue": 888  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 123,  # 选择的旧版本指标值
                            "latestValue": 156  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 355,  # 选择的旧版本指标值
                            "latestValue": 400  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 666,  # 选择的旧版本指标值
                            "latestValue": 888  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 123,  # 选择的旧版本指标值
                            "latestValue": 156  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 355,  # 选择的旧版本指标值
                            "latestValue": 400  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 666,  # 选择的旧版本指标值
                            "latestValue": 888  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 123,  # 选择的旧版本指标值
                            "latestValue": 156  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 355,  # 选择的旧版本指标值
                            "latestValue": 400  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 666,  # 选择的旧版本指标值
                            "latestValue": 888  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 123,  # 选择的旧版本指标值
                            "latestValue": 156  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 355,  # 选择的旧版本指标值
                            "latestValue": 400  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 666,  # 选择的旧版本指标值
                            "latestValue": 888  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 123,  # 选择的旧版本指标值
                            "latestValue": 156  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 355,  # 选择的旧版本指标值
                            "latestValue": 400  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 666,  # 选择的旧版本指标值
                            "latestValue": 888  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 123,  # 选择的旧版本指标值
                            "latestValue": 156  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 355,  # 选择的旧版本指标值
                            "latestValue": 400  # 当前版本指标值
                        },
                    ]
                },
                # 变量个数
                "variableNum": {
                    "totalNum": 3,  # 变更总数
                    "totalProp": "46.58%",  # 变更占比
                    "increaseNum": 66,  # 增加数
                    "increaseProp": "32.6%",  # 增加占比
                    "decreaseNum": 34,  # 降低数
                    "decreaseProp": "18.3%",  # 降低占比
                    # 变更信息列表
                    "changeinfoList": [
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 888,  # 选择的旧版本指标值
                            "latestValue": 777  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 189,  # 选择的旧版本指标值
                            "latestValue": 156  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 323,  # 选择的旧版本指标值
                            "latestValue": 689  # 当前版本指标值
                        }
                    ]
                },
                # 圈复杂度
                "cyclomaticComplexity": {
                    "totalNum": 13,  # 变更总数
                    "totalProp": "46.58%",  # 变更占比
                    "increaseNum": 66,  # 增加数
                    "increaseProp": "32.6%",  # 增加占比
                    "decreaseNum": 34,  # 降低数
                    "decreaseProp": "18.3%",  # 降低占比
                    # 变更信息列表
                    "changeinfoList": [
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 666,  # 选择的旧版本指标值
                            "latestValue": 888  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 355,  # 选择的旧版本指标值
                            "latestValue": 400  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 123,  # 选择的旧版本指标值
                            "latestValue": 156  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 588,  # 选择的旧版本指标值
                            "latestValue": 573  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 123,  # 选择的旧版本指标值
                            "latestValue": 156  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 355,  # 选择的旧版本指标值
                            "latestValue": 400  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 666,  # 选择的旧版本指标值
                            "latestValue": 888  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 123,  # 选择的旧版本指标值
                            "latestValue": 156  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 355,  # 选择的旧版本指标值
                            "latestValue": 400  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 666,  # 选择的旧版本指标值
                            "latestValue": 888  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 123,  # 选择的旧版本指标值
                            "latestValue": 156  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 355,  # 选择的旧版本指标值
                            "latestValue": 400  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 666,  # 选择的旧版本指标值
                            "latestValue": 888  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 123,  # 选择的旧版本指标值
                            "latestValue": 156  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 355,  # 选择的旧版本指标值
                            "latestValue": 400  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 666,  # 选择的旧版本指标值
                            "latestValue": 888  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 123,  # 选择的旧版本指标值
                            "latestValue": 156  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 355,  # 选择的旧版本指标值
                            "latestValue": 400  # 当前版本指标值
                        },
                    ]
                },
                # 代码行
                "codeNum": {
                    "totalNum": 3,  # 变更总数
                    "totalProp": "46.58%",  # 变更占比
                    "increaseNum": 66,  # 增加数
                    "increaseProp": "32.6%",  # 增加占比
                    "decreaseNum": 34,  # 降低数
                    "decreaseProp": "18.3%",  # 降低占比
                    # 变更信息列表
                    "changeinfoList": [
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 888,  # 选择的旧版本指标值
                            "latestValue": 777  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 189,  # 选择的旧版本指标值
                            "latestValue": 156  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 323,  # 选择的旧版本指标值
                            "latestValue": 689  # 当前版本指标值
                        }
                    ]
                },
                # 出度
                "outDegree": {
                    "totalNum": 3,  # 变更总数
                    "totalProp": "46.58%",  # 变更占比
                    "increaseNum": 66,  # 增加数
                    "increaseProp": "32.6%",  # 增加占比
                    "decreaseNum": 34,  # 降低数
                    "decreaseProp": "18.3%",  # 降低占比
                    # 变更信息列表
                    "changeinfoList": [
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 888,  # 选择的旧版本指标值
                            "latestValue": 777  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 189,  # 选择的旧版本指标值
                            "latestValue": 156  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 323,  # 选择的旧版本指标值
                            "latestValue": 689  # 当前版本指标值
                        }
                    ]
                },
                # 入度
                "inDegree": {
                    "totalNum": 3,  # 变更总数
                    "totalProp": "46.58%",  # 变更占比
                    "increaseNum": 66,  # 增加数
                    "increaseProp": "32.6%",  # 增加占比
                    "decreaseNum": 34,  # 降低数
                    "decreaseProp": "18.3%",  # 降低占比
                    # 变更信息列表
                    "changeinfoList": [
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 888,  # 选择的旧版本指标值
                            "latestValue": 777  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 189,  # 选择的旧版本指标值
                            "latestValue": 156  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 323,  # 选择的旧版本指标值
                            "latestValue": 689  # 当前版本指标值
                        }
                    ]
                }
            }
        },
        # C++信息，没有则给空字典{}
        "c_plus_info": {
            # 系统级别变更信息
            "systemLevel": {
                # 当前版本
                "versionLatest": {
                    "name": "version 1.5",  # 版本名称
                    "fileNum": 45,  # 文件数
                    "classNum": 208,  # 类个数
                    "codeNum": 4654  # 代码行数
                },
                # 选择的旧版本
                "versionSelected": {
                    "name": "version 1.1",  # 版本名称
                    "fileNum": 48,  # 文件数
                    "classNum": 298,  # 类个数
                    "codeNum": 6890  # 代码行数
                },
                # 设计质量
                "designInformation": [
                    {
                        "indexName": "modifiability",
                        "result": 0,
                        "minimumValue": 0,  # 范围最小值
                        "maximumValue": 0.5,  # 范围最大值
                        "trend": 2,
                        "versionLatest": 0.981,
                        "versionSelected": 0.981
                    },
                    {
                        "indexName": "scalability",
                        "result": 0,
                        "minimumValue": 0,  # 范围最小值
                        "maximumValue": 1,  # 范围最大值
                        "trend": 2,
                        "versionLatest": 0.435,
                        "versionSelected": 0.435
                    },
                    {
                        "indexName": "testability",
                        "result": 0,
                        "minimumValue": 0,  # 范围最小值
                        "maximumValue": 1,  # 范围最大值
                        "trend": 2,
                        "versionLatest": 0.991,
                        "versionSelected": 0.991
                    },
                    {
                        "indexName": "refundability",
                        "result": 0,
                        "minimumValue": 0,  # 范围最小值
                        "maximumValue": 1,  # 范围最大值
                        "trend": 2,
                        "versionLatest": 0.495,
                        "versionSelected": 0.495
                    },
                    {
                        "indexName": "comprehensibility",
                        "result": 0,
                        "minimumValue": 0,  # 范围最小值
                        "maximumValue": 1,  # 范围最大值
                        "trend": 2,
                        "versionLatest": 0.291,
                        "versionSelected": 0.291
                    }
                ],
                # 指标信息表
                "indexInformation": [
                    {
                        "indexName": "易理解性",  # 指标名称
                        "versionSelected": 0.288,  # 选择的版本值
                        "versionLatest": 0.367,  # 当前的版本值
                        "trend": 0,  # 趋势：0降低，1升高
                    },
                    {
                        "indexName": "可替换性",  # 指标名称
                        "versionSelected": 0.288,  # 选择的版本值
                        "versionLatest": 0.367,  # 当前的版本值
                        "trend": 0,  # 趋势：0降低，1升高
                    },
                    {
                        "indexName": "易理解性1",  # 指标名称
                        "versionSelected": 0.288,  # 选择的版本值
                        "versionLatest": 0.367,  # 当前的版本值
                        "trend": 0,  # 趋势：0降低，1升高
                    },
                    {
                        "indexName": "可替换性1",  # 指标名称
                        "versionSelected": 0.288,  # 选择的版本值
                        "versionLatest": 0.367,  # 当前的版本值
                        "trend": 0,  # 趋势：0降低，1升高
                    },
                    {
                        "indexName": "易理解性2",  # 指标名称
                        "versionSelected": 0.288,  # 选择的版本值
                        "versionLatest": 0.367,  # 当前的版本值
                        "trend": 0,  # 趋势：0降低，1升高
                    },
                    {
                        "indexName": "可替换性2",  # 指标名称
                        "versionSelected": 0.288,  # 选择的版本值
                        "versionLatest": 0.367,  # 当前的版本值
                        "trend": 0,  # 趋势：0降低，1升高
                    },
                    # 其他指标
                ]
            },
            # 文件级别变更信息
            "fileLevel": {
                "updateFileNum": 25,  # 修改的文件数
                "deleteFileNum": 3,  # 删除的文件数
                "insertFileNum": 5,  # 新增的文件数
                # 文件树
                "selectedFileTree": [
                    {
                        "id": 1,
                        "label": "test1",
                        "type": "dir",
                        "children": [
                            {
                                "id": 3,
                                "label": "test1-1.c",
                                "type": "file",
                                "status": 0,
                                "fileInfo": {
                                    "funcNum": 3,  # 函数数量
                                    "globalVariableNum": 1,  # 全局变量数
                                    "fileSize": "2.3KB",  # 文件大小
                                    "fileUpdateTime": "2023/7/25 14:11:32",  # 文件修改时间
                                    "cyclomaticComplexity": 5,  # 圈复杂度
                                    "outDegree": 2,  # 出度
                                    "inDegree": 5,  # 入度
                                    "annotationLine": 10  # 注释行数
                                }
                            },
                            {
                                "id": 4,
                                "label": "test1-2",
                                "type": "dir",
                                "children": [

                                    {
                                        "id": 7,
                                        "label": "test1-2-1.c",
                                        "type": "file",
                                        "status": 1
                                    },
                                    {
                                        "id": 8,
                                        "label": "test1-2-2.c",
                                        "type": "file",
                                        "status": 2
                                    }
                                ]
                            }
                        ],
                    },
                    {
                        "id": 2,
                        "label": "test2",
                        "type": "dir",
                        "children": [
                            {
                                "id": 2,
                                "label": "test2-1",
                                "type": "dir",
                                "children": [
                                    {
                                        "id": 5,
                                        "label": "test2-1-1.c",
                                        "type": "file",
                                        "status": 2
                                    },
                                    {
                                        "id": 6,
                                        "label": "test2-1-2.c",
                                        "type": "file",
                                        "status": 3
                                    }
                                ]
                            },
                            {
                                "id": 5,
                                "label": "test2-2.c",
                                "type": "file",
                                "status": 0
                            },
                            {
                                "id": 6,
                                "label": "test2-3.c",
                                "type": "file",
                                "status": 3
                            }
                        ]
                    }
                ],
                "latestFileTree": [
                    {
                        "id": 1,
                        "label": "test1",
                        "type": "dir",
                        "children": [
                            {
                                "id": 3,
                                "label": "test1-1.c",
                                "type": "file",
                                "status": 0
                            },
                            {
                                "id": 4,
                                "label": "test1-2",
                                "type": "dir",
                                "children": [

                                    {
                                        "id": 7,
                                        "label": "test1-2-1.c",
                                        "type": "file",
                                        "status": 1
                                    },
                                    {
                                        "id": 8,
                                        "label": "test1-2-2.c",
                                        "type": "file",
                                        "status": 2
                                    }
                                ]
                            }
                        ],
                    },
                    {
                        "id": 2,
                        "label": "test2",
                        "type": "dir",
                        "children": [
                            {
                                "id": 2,
                                "label": "test2-1",
                                "type": "dir",
                                "children": [
                                    {
                                        "id": 5,
                                        "label": "test2-1-1.c",
                                        "type": "file",
                                        "status": 2
                                    },
                                    {
                                        "id": 6,
                                        "label": "test2-1-2.c",
                                        "type": "file",
                                        "status": 3
                                    }
                                ]
                            },
                            {
                                "id": 5,
                                "label": "test2-2.c",
                                "type": "file",
                                "status": 0
                            },
                            {
                                "id": 6,
                                "label": "test2-3.c",
                                "type": "file",
                                "status": 3
                            }
                        ]
                    }
                ]
            },
            # 类级别变更信息
            "classLevel": {
                # 成员变量个数
                "memberVariableNum": {
                    "totalNum": 10,  # 变更总数
                    "totalProp": "46.58%",  # 变更占比
                    "increaseNum": 66,  # 增加数
                    "increaseProp": "32.6%",  # 增加占比
                    "decreaseNum": 34,  # 降低数
                    "decreaseProp": "18.3%",  # 降低占比
                    # 变更信息列表
                    "changeinfoList": [
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 666,  # 选择的旧版本指标值
                            "latestValue": 888  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 123,  # 选择的旧版本指标值
                            "latestValue": 156  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 355,  # 选择的旧版本指标值
                            "latestValue": 400  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 666,  # 选择的旧版本指标值
                            "latestValue": 888  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 123,  # 选择的旧版本指标值
                            "latestValue": 156  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 355,  # 选择的旧版本指标值
                            "latestValue": 400  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 666,  # 选择的旧版本指标值
                            "latestValue": 888  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 123,  # 选择的旧版本指标值
                            "latestValue": 156  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 355,  # 选择的旧版本指标值
                            "latestValue": 400  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 666,  # 选择的旧版本指标值
                            "latestValue": 888  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 123,  # 选择的旧版本指标值
                            "latestValue": 156  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 355,  # 选择的旧版本指标值
                            "latestValue": 400  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 666,  # 选择的旧版本指标值
                            "latestValue": 888  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 123,  # 选择的旧版本指标值
                            "latestValue": 156  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 355,  # 选择的旧版本指标值
                            "latestValue": 400  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 666,  # 选择的旧版本指标值
                            "latestValue": 888  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 123,  # 选择的旧版本指标值
                            "latestValue": 156  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 355,  # 选择的旧版本指标值
                            "latestValue": 400  # 当前版本指标值
                        },
                    ]
                },
                # 成员方法个数
                "memberFunctionNum": {
                    "totalNum": 3,  # 变更总数
                    "totalProp": "46.58%",  # 变更占比
                    "increaseNum": 66,  # 增加数
                    "increaseProp": "32.6%",  # 增加占比
                    "decreaseNum": 34,  # 降低数
                    "decreaseProp": "18.3%",  # 降低占比
                    # 变更信息列表
                    "changeinfoList": [
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 888,  # 选择的旧版本指标值
                            "latestValue": 777  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 189,  # 选择的旧版本指标值
                            "latestValue": 156  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 323,  # 选择的旧版本指标值
                            "latestValue": 689  # 当前版本指标值
                        }
                    ]
                },
                # 基类个数
                "classNum": {
                    "totalNum": 13,  # 变更总数
                    "totalProp": "46.58%",  # 变更占比
                    "increaseNum": 66,  # 增加数
                    "increaseProp": "32.6%",  # 增加占比
                    "decreaseNum": 34,  # 降低数
                    "decreaseProp": "18.3%",  # 降低占比
                    # 变更信息列表
                    "changeinfoList": [
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 666,  # 选择的旧版本指标值
                            "latestValue": 888  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 355,  # 选择的旧版本指标值
                            "latestValue": 400  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 123,  # 选择的旧版本指标值
                            "latestValue": 156  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 588,  # 选择的旧版本指标值
                            "latestValue": 573  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 123,  # 选择的旧版本指标值
                            "latestValue": 156  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 355,  # 选择的旧版本指标值
                            "latestValue": 400  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 666,  # 选择的旧版本指标值
                            "latestValue": 888  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 123,  # 选择的旧版本指标值
                            "latestValue": 156  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 355,  # 选择的旧版本指标值
                            "latestValue": 400  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 666,  # 选择的旧版本指标值
                            "latestValue": 888  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 123,  # 选择的旧版本指标值
                            "latestValue": 156  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 355,  # 选择的旧版本指标值
                            "latestValue": 400  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 666,  # 选择的旧版本指标值
                            "latestValue": 888  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 123,  # 选择的旧版本指标值
                            "latestValue": 156  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 355,  # 选择的旧版本指标值
                            "latestValue": 400  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 666,  # 选择的旧版本指标值
                            "latestValue": 888  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 123,  # 选择的旧版本指标值
                            "latestValue": 156  # 当前版本指标值
                        },
                        {
                            "functionPath": "/aaa/bbb/ccc/xxx/func1()",  # 函数路径
                            "selectedValue": 355,  # 选择的旧版本指标值
                            "latestValue": 400  # 当前版本指标值
                        },
                    ]
                },
                # 出度
                "outDegree": {},
                # 入度
                "inDegree": {}
            }
        }
    }
    return jsonify(data)


@app.post("/design_refactor_suggestion/<projectname>")
def design_refactor_suggestion(projectname):
    """
    设计恢复建议
    params:
        threshold: 设置的阈值
    """
    threshold = request.get_json()

    data = {
        "suggestionTable": [
            {
                "suggestion": "易理解性和函数的圈复杂度负相关，函数圈复杂度越高则越难理解。建议降低当前软件版本中函数的复杂度以提高软件的易理解性。",
                "details": [
                    {
                        "funcName": "a",
                        "path": "C:\\Users\\86151\\Desktoplscrcpy-master app srccli.c",
                        "info": {
                            "cyclomaticComplexity": {
                                "value": 10,
                                "label": "圈复杂度"
                            },
                            "aaa": {
                                "value": 6,
                                "label": "指标名1"
                            },
                            "cyclomaticComplexity1": {
                                "value": 10,
                                "label": "圈复杂度"
                            },
                            "aaa1": {
                                "value": 6,
                                "label": "指标名"
                            },
                        }
                    },
                    {
                        "funcName": "a",
                        "path": "C:\\Users\\86151\\Desktoplscrcpy-master app srccli.c",
                        "info": {
                            "cyclomaticComplexity": {
                                "value": 6,
                                "label": "圈复杂度"
                            }
                        }
                    },
                    {
                        "funcName": "a",
                        "path": "C:\\Users\\86151\\Desktoplscrcpy-master app srccli.c",
                        "info": {
                            "cyclomaticComplexity": {
                                "value": 3,
                                "label": "圈复杂度"
                            }
                        }
                    }
                ]
            },
            {
                "suggestion": "软件中48.60%函数的参数过多,建议采用结构体传递参数，或者重新审查函数的功能独立性，对于功能不够独立的函数进行拆分。",
                "details": [
                    {
                        "funcName": "b",
                        "path": "C:\\Users\\86151\\Desktoplscrcpy-master app srccli.c",
                        "info": {
                            "paramNum": {
                                "value": 5,
                                "label": "参数个数"
                            }
                        }
                    },
                    {
                        "funcName": "b",
                        "path": "C:\\Users\\86151\\Desktoplscrcpy-master app srccli.c",
                        "info": {
                            "paramNum": {
                                "value": 8,
                                "label": "参数个数"
                            }
                        }
                    },
                    {
                        "funcName": "b",
                        "path": "C:\\Users\\86151\\Desktoplscrcpy-master app srccli.c",
                        "info": {
                            "paramNum": {
                                "value": 6,
                                "label": "参数个数"
                            }
                        }
                    }
                ]
            },
            {
                "suggestion": "软件注释过少，总体注释率较低，影响对软件的理解，建议增加对软件源码的注释以提高软件的易理解性。",
                "details": [
                    {
                        "funcName": "c",
                        "path": "C:\\Users\\86151\\Desktoplscrcpy-master app srccli.c",
                        "info": {
                            "commentLine": {
                                "value": 15,
                                "label": "注释行数"
                            }
                        }
                    },
                    {
                        "funcName": "c",
                        "path": "C:\\Users\\86151\\Desktoplscrcpy-master app srccli.c",
                        "info": {
                            "commentLine": {
                                "value": 36,
                                "label": "注释行数"
                            }
                        }
                    },
                    {
                        "funcName": "c",
                        "path": "C:\\Users\\86151\\Desktoplscrcpy-master app srccli.c",
                        "info": {
                            "commentLine": {
                                "value": 6,
                                "label": "注释行数"
                            }
                        }
                    }
                ]
            }
        ]
    }
    return jsonify(data)


@app.get("/get_all_same_project/<projectname>")
def get_all_version_info(projectname):
    """
    获取与当前项目类型一致的项目
    """
    projectType = int(request.args.get("projectType"))
    projects = [
        "CUnit01",
        "CUnit02",
        "CUnit03",
        "CUnit04",
    ]
    return jsonify(projects)


@app.route("/getDesignMetric/<projectname>")
def getDesignMetric(projectname):
    '''
    设计质量评估
    '''
    data = {
        "metrix": {
            "modifiability": {
                "value": 0.8,
                "inDegree": 3,
                "outDegree": 4,
                "funcNum": 2,
                "classInDegree": 4,
                "classOutDegree": 5,
                "classNum": 10
            },
            "scalability": {
                "value": 0.6,
                "apiNum": 36,
                "funcNum": 60,
                "interfaceNum": 27,
                "classNum": 48
            },
            "testability": {
                "value": 0.8,
                "outDegree": 5,
                "funcNum": 3,
                "classOutDegree": 6,
                "classNum": 8
            },
            "refundability": {
                "value": 0.4,
                "R_sum": 5,
                "funcNum": 6,
                "Rc_sum": 7,
                "classNum": 8
            },
            "comprehensibility": {
                "value": 0.7,
                "commentFunc": 2,
                "funcNum": 3,
                "commentClass": 4,
                "classNum": 5
            },
            "funcNameList": ["test01", "test02", "test03"],
            "classNameList": ["class01", "class01", "class03"],
            "methodNameList": ["demo01", "demo02", "demo03"],
            "funcInList": [3, 4, 1],
            "funcOutList": [4, 2, 3],
            "RiList": [0.6, 0.4, 0.5],
            "classInList": [4, 5, 1],
            "classOutList": [6, 4, 3],
            "RciList": [4, 6, 3],
            "xAxis": [1, 2, 3],
            "xcAxis": [1, 2, 3]
        }
    }
    return jsonify(data)


@app.post("/metricSelected/<projectname>")
def metricSelected(projectname):
    metricTree = request.get_json().get("metricTree")
    return jsonify()


@app.get("/metricWeight/<projectname>")
def metricWeight(projectname):
    data = {
        "metricSelected": -1,  # -1表示从来没存储指标选择记录，0表示无指标字典需要设置权重，1表示需要设置指标权值，需要解析metrixTree
        "metricTree": {
            "一级指标": {
                "二级指标": {
                    "三级指标1": 0.0,
                    "三级指标2": 0.0,
                    "三级指标3": 0.0
                },
                "二级指标2": {
                    "三级指标1": 0.0,
                    "三级指标2": 0.0,
                    "三级指标3": 0.0
                }
            },
            "一级指标2": {
                "二级指标": {
                    "三级指标1": 0.0,
                    "三级指标2": 0.0,
                    "三级指标3": 0.0
                }
            },
            "一级指标3": {
                "二级指标": {
                    "三级指标1": 0.0,
                    "三级指标2": 0.0,
                    "三级指标3": 0.0
                },
                "二级指标2": {
                    "三级指标1": 0.0,
                    "三级指标2": 0.0,
                    "三级指标3": 0.0
                },
                "二级指标3": {
                    "三级指标1": 0.0,
                    "三级指标2": 0.0,
                    "三级指标3": 0.0
                }
            },
        }
    }
    return jsonify(data)


@app.post("/weightCheck/<projectname>")
def weightCheck(projectname):
    metricWeight = request.get_json().get("metricWeight")
    return jsonify({
        "weightFlag": 1,
        "data": {
        }
    })


@app.post("/getSelectedMetrics/<projectname>")
def getSelectedMetrics(projectname):
    data = {
        "data": [{"name": "软件总质量", "sub": [{"id": "可靠性", "value": 0.0, "weight": 0.3333}, {"id": "信息安全性", "value": 0.5, "weight": 0.3333}, {"id": "维护性", "value": 0.5178571428571429, "weight": 0.3333}], "subMetric": [{"name": "可靠性", "val": 0.0, "sub": [{"id": "成熟性", "value": 0.0, "weight": 0.0}, {"id": "可用性", "value": 0.0, "weight": 0.0}, {"id": "容错性", "value": 0.0, "weight": 1.0}, {"id": "易恢复性", "value": 0.0, "weight": 0.0}, {"id": "可靠性的依从性", "value": 0.0, "weight": 0.0}], "subMetric": [{"name": "成熟性", "val": 0.0, "sub": [{"id": "故障修复率", "value": None, "weight": 0.0}, {"id": "平均失效间隔时间(MTBF)", "value": None, "weight": 0.0}, {"id": "周期失效率", "value": None, "weight": 0.0}, {"id": "测试覆盖率", "value": None, "weight": 0.0}], "subMetric": [{"name": "故障修复率", "val": None, "sub": [{"id": None, "type": None, "source": None, "des": None, "val": None}, {"id": None, "type": None, "source": None, "des": None, "val": None}]}, {"name": "平均失效间隔时间(MTBF)", "val": None, "sub": [{"id": None, "type": None, "source": None, "des": None, "val": None}, {"id": None, "type": None, "source": None, "des": None, "val": None}]}, {"name": "周期失效率", "val": None, "sub": [{"id": None, "type": None, "source": None, "des": None, "val": None}, {"id": None, "type": None, "source": None, "des": None, "val": None}]}, {"name": "测试覆盖率", "val": None, "sub": [{"id": None, "type": None, "source": None, "des": None, "val": None}, {"id": None, "type": None, "source": None, "des": None, "val": None}]}]}, {"name": "可用性", "val": 0.0, "sub": [{"id": "系统可用性", "value": None, "weight": 0.0}, {"id": "平均宕机时间", "value": None, "weight": 0.0}], "subMetric": [{"name": "系统可用性", "val": None, "sub": [{"id": None, "type": None, "source": None, "des": None, "val": None}, {"id": None, "type": None, "source": None, "des": None, "val": None}]}, {"name": "平均宕机时间", "val": None, "sub": [{"id": None, "type": None, "source": None, "des": None, "val": None}, {"id": None, "type": None, "source": None, "des": None, "val": None}]}]}, {"name": "容错性", "val": 0.0, "sub": [{"id": "避免失效率", "value": None, "weight": 0.0}, {"id": "组件的冗余度", "value": 0.0, "weight": 1.0}, {"id": "平均故障通告时间", "value": None, "weight": 0.0}], "subMetric": [{"name": "避免失效率", "val": None, "sub": [{"id": None, "type": None, "source": None, "des": None, "val": None}, {"id": None, "type": None, "source": None, "des": None, "val": None}]}, {"name": "组件的冗余度", "val": 0.0, "sub": [{"id": "A", "source": "源码", "des": "冗余安装系统组件的数量", "val": 0}, {"id": "B", "source": "源码", "des": "系统组件数量", "val": 2}]}, {"name": "平均故障通告时间", "val": None, "sub": [{"id": None, "type": None, "source": None, "des": None, "val": None}, {"id": None, "type": None, "source": None, "des": None, "val": None}, {"id": None, "type": None, "source": None, "des": None, "val": None}, {"id": None, "type": None, "source": None, "des": None, "val": None}]}]}, {"name": "易恢复性", "val": 0.0, "sub": [{"id": "平均恢复时间", "value": None, "weight": 0.0}, {"id": "数据备份完整性", "value": None, "weight": 0.0}], "subMetric": [{"name": "平均恢复时间", "val": None, "sub": [{"id": None, "type": None, "source": None, "des": None, "val": None}, {"id": None, "type": None, "source": None, "des": None, "val": None}]}, {"name": "数据备份完整性", "val": None, "sub": [{"id": None, "type": None, "source": None, "des": None, "val": None}, {"id": None, "type": None, "source": None, "des": None, "val": None}]}]}, {"name": "可靠性的依从性", "val": 0.0, "sub": [{"id": "可靠性的依从性", "value": None, "weight": 0.0}], "subMetric": [{"name": "可靠性的依从性", "val": None, "sub": [{"id": None, "type": None, "source": None, "des": None, "val": None}, {"id": None, "type": None, "source": None, "des": None, "val": None}]}]}]}, {"name": "信息安全性", "val": 0.5, "sub": [{"id": "保密性", "value": 0.0, "weight": 0.0}, {"id": "完整性", "value": 0.5, "weight": 1.0}, {"id": "抗抵赖性", "value": 0.0, "weight": 0.0}, {"id": "可核查性", "value": 0.0, "weight": 0.0}, {"id": "真实性", "value": 0.0, "weight": 0.0}, {"id": "信息安全性的依从性", "value": 0.0, "weight": 0.0}], "subMetric": [{"name": "保密性", "val": 0.0, "sub": [{"id": "访问控制性", "value": None, "weight": 0.0}, {"id": "数据加密正确性", "value": None, "weight": 0.0}, {"id": "加密算法的强度", "value": None, "weight": 0.0}], "subMetric": [{"name": "访问控制性", "val": None, "sub": [{"id": None, "type": None, "source": None, "des": None, "val": None}, {"id": None, "type": None, "source": None, "des": None, "val": None}]}, {"name": "数据加密正确性", "val": None, "sub": [{"id": None, "type": None, "source": None, "des": None, "val": None}, {"id": None, "type": None, "source": None, "des": None, "val": None}]}, {"name": "加密算法的强度", "val": None, "sub": [{"id": None, "type": None, "source": None, "des": None, "val": None}, {"id": None, "type": None, "source": None, "des": None, "val": None}]}]}, {"name": "完整性", "val": 0.5, "sub": [{"id": "数据完整性", "value": None, "weight": 0.0}, {"id": "内部数据抗讹误性", "value": None, "weight": 0.0}, {"id": "缓冲区溢出防止率", "value": 0.5, "weight": 1.0}], "subMetric": [{"name": "数据完整性", "val": None, "sub": [{"id": None, "type": None, "source": None, "des": None, "val": None}, {"id": None, "type": None, "source": None, "des": None, "val": None}]}, {"name": "内部数据抗讹误性", "val": None, "sub": [{"id": None, "type": None, "source": None, "des": None, "val": None}, {"id": None, "type": None, "source": None, "des": None, "val": None}]}, {"name": "缓冲区溢出防止率", "val": 0.5, "sub": [{"id": "A", "source": "源码", "des": "在带有用户输入的内存访问中,经过边界值检查的访问数量", "val": 1}, {"id": "B", "source": "源码", "des": "软件模块中带有用户输入的内存访问数量", "val": 2}]}]}, {"name": "抗抵赖性", "val": 0.0, "sub": [{"id": "数字签名使用率", "value": None, "weight": 0.0}], "subMetric": [{"name": "数字签名使用率", "val": None, "sub": [{"id": None, "type": None, "source": None, "des": None, "val": None}, {"id": None, "type": None, "source": None, "des": None, "val": None}]}]}, {"name": "可核查性", "val": 0.0, "sub": [{"id": "用户审计跟踪的完整性", "value": None, "weight": 0.0}, {"id": "系统日志保留满足度", "value": None, "weight": 0.0}], "subMetric": [{"name": "用户审计跟踪的完整性", "val": None, "sub": [{"id": None, "type": None, "source": None, "des": None, "val": None}, {"id": None, "type": None, "source": None, "des": None, "val": None}]}, {"name": "系统日志保留满足度", "val": None, "sub": [{"id": None, "type": None, "source": None, "des": None, "val": None}, {"id": None, "type": None, "source": None, "des": None, "val": None}]}]}, {"name": "真实性", "val": 0.0, "sub": [{"id": "鉴别机制的充分性", "value": None, "weight": 0.0}, {"id": "鉴别规则的符合性", "value": None, "weight": 0.0}], "subMetric": [{"name": "鉴别机制的充分性", "val": None, "sub": [{"id": None, "type": None, "source": None, "des": None, "val": None}, {"id": None, "type": None, "source": None, "des": None, "val": None}]}, {"name": "鉴别规则的符合性", "val": None, "sub": [{"id": None, "type": None, "source": None, "des": None, "val": None}, {"id": None, "type": None, "source": None, "des": None, "val": None}]}]}, {"name": "信息安全性的依从性", "val": 0.0, "sub": [{"id": "信息安全性的依从性", "value": None, "weight": 0.0}], "subMetric": [{"name": "信息安全性的依从性", "val": None, "sub": [{"id": None, "type": None, "source": None, "des": None, "val": None}, {"id": None, "type": None, "source": None, "des": None, "val": None}]}]}]}, {"name": "维护性", "val": 0.5178571428571429, "sub": [{"id": "模块化", "value": 1.0, "weight": 0.5}, {"id": "可重用性", "value": 0.03571428571428571, "weight": 0.5}, {"id": "易分析性", "value": 0.0, "weight": 0.0}, {"id": "易修改性", "value": 0.0, "weight": 0.0}, {"id": "易测试性", "value": 0.0, "weight": 0.0}, {"id": "维护性的依从性", "value": 0.0, "weight": 0.0}], "subMetric": [{"name": "模块化", "val": 1.0, "sub": [{"id": "组件间的耦合度", "value": 1.0, "weight": 1.0}, {"id": "圈复杂度的充分性", "value": None, "weight": 0.0}], "subMetric": [{"name": "组件间的耦合度", "val": 1.0, "sub": [{"id": "A", "source": "源码", "des": "所实现的对其他组件没有产生影响的组件数量", "val": 2}, {"id": "B", "source": "源码", "des": "需要独立的组件数量", "val": 2}]}, {"name": "圈复杂度的充分性", "val": None, "sub": [{"id": "A", "source": "源码+需求文档", "des": "圈复杂度的得分超过规定阈值的软件模块数量", "val": None}, {"id": "B", "source": "源码", "des": "已实现的软件模块数量", "val": 8}]}]}, {"name": "可重用性", "val": 0.03571428571428571, "sub": [{"id": "资产的可重用性", "value": 0.07142857142857142, "weight": 0.5}, {"id": "编码规则符合性", "value": 0.0, "weight": 0.5}], "subMetric": [{"name": "资产的可重用性", "val": 0.07142857142857142, "sub": [{"id": "A", "source": "源码", "des": "为可重复使用而设计和实现的资产的数量", "val": 1}, {"id": "B", "source": "源码", "des": "系统中资产的数量", "val": 14}]}, {"name": "编码规则符合性", "val": 0.0, "sub": [{"id": "A", "source": "源码", "des": "符合特定系统编码规则的软件模块数量", "val": 0}, {"id": "B", "source": "源码", "des": "已实现的软件模功数量", "val": 8}]}]}, {"name": "易分析性", "val": 0.0, "sub": [{"id": "系统日志完整性", "value": None, "weight": 0.0}, {"id": "诊断功能有效性", "value": None, "weight": 0.0}, {"id": "诊断功能充分性", "value": None, "weight": 0.0}], "subMetric": [{"name": "系统日志完整性", "val": None, "sub": [{"id": None, "type": None, "source": None, "des": None, "val": None}, {"id": None, "type": None, "source": None, "des": None, "val": None}]}, {"name": "诊断功能有效性", "val": None, "sub": [{"id": None, "type": None, "source": None, "des": None, "val": None}, {"id": None, "type": None, "source": None, "des": None, "val": None}]}, {"name": "诊断功能充分性", "val": None, "sub": [{"id": None, "type": None, "source": None, "des": None, "val": None}, {"id": None, "type": None, "source": None, "des": None, "val": None}]}]}, {"name": "易修改性", "val": 0.0, "sub": [{"id": "修改的效率", "value": None, "weight": 0.0}, {"id": "修改的正确性", "value": None, "weight": 0.0}, {"id": "修改的能力", "value": None, "weight": 0.0}], "subMetric": [{"name": "修改的效率", "val": None, "sub": [{"id": None, "type": None, "source": None, "des": None, "val": None}, {"id": None, "type": None, "source": None, "des": None, "val": None}, {"id": None, "type": None, "source": None, "des": None, "val": None}, {"id": None, "type": None, "source": None, "des": None, "val": None}, {"id": None, "type": None, "source": None, "des": None, "val": None}, {"id": None, "type": None, "source": None, "des": None, "val": None}, {"id": None, "type": None, "source": None, "des": None, "val": None}, {"id": None, "type": None, "source": None, "des": None, "val": None}, {"id": None, "type": None, "source": None, "des": None, "val": None}]}, {"name": "修改的正确性", "val": None, "sub": [{"id": None, "type": None, "source": None, "des": None, "val": None}, {"id": None, "type": None, "source": None, "des": None, "val": None}]}, {"name": "修改的能力", "val": None, "sub": [{"id": None, "type": None, "source": None, "des": None, "val": None}, {"id": None, "type": None, "source": None, "des": None, "val": None}]}]}, {"name": "易测试性", "val": 0.0, "sub": [{"id": "测试功能的完整性", "value": None, "weight": 0.0}, {"id": "测试独立性", "value": None, "weight": 0.0}, {"id": "测试的重启动性", "value": None, "weight": 0.0}], "subMetric": [{"name": "测试功能的完整性", "val": None, "sub": [{"id": None, "type": None, "source": None, "des": None, "val": None}, {"id": None, "type": None, "source": None, "des": None, "val": None}]}, {"name": "测试独立性", "val": None, "sub": [{"id": None, "type": None, "source": None, "des": None, "val": None}, {"id": None, "type": None, "source": None, "des": None, "val": None}]}, {"name": "测试的重启动性", "val": None, "sub": [{"id": None, "type": None, "source": None, "des": None, "val": None}, {"id": None, "type": None, "source": None, "des": None, "val": None}]}]}, {"name": "维护性的依从性", "val": 0.0, "sub": [{"id": "维护性的依从性", "value": None, "weight": 0.0}], "subMetric": [{"name": "维护性的依从性", "val": None, "sub": [{"id": None, "type": None, "source": None, "des": None, "val": None}, {"id": None, "type": None, "source": None, "des": None, "val": None}]}]}]}], "val": 0.3392517857142857}],
        "metricCalculated": 1
    }
    return jsonify(data)


@app.get("/getMinMaxMetrics/<projectname>")
def getMinMaxMetrics(projectname):
    # data = {
    #     "信息安全性": {
    #         "可核查性": {
    #             "功能覆盖率": {
    #                 "val": 3.75
    #             }
    #         }
    #     },
    #     "可移植性": {
    #         "易安装性": {
    #             "功能正确性": {
    #                 "val": 1.0
    #             },
    #             "使用目标的功能适合性": {
    #                 "val": 1.6
    #             }
    #         }
    #     },
    #     "可靠性": {
    #         "可用性": {
    #             "系统的功能适合性": {
    #                 "val": 1.575
    #             },
    #             "系统可用性": {
    #                 "val": 0.517
    #             }
    #         },
    #         "容错性": {
    #             "平均故障通告时间": {
    #                 "val": 0.1
    #             },
    #             "组件的冗余度": {
    #                 "val": 0.0
    #             }
    #         },
    #         "成熟性": {
    #             "功能性的依从性": {
    #                 "val": 0.75
    #             },
    #             "平均失效间隔时间(MTBF)": {
    #                 "val": 1.85
    #             }
    #         },
    #         "易恢复性": {
    #             "平均恢复时间": {
    #                 "val": 120.05
    #             }
    #         }
    #     },
    #     "性能效率": {
    #         "容量": {
    #             "事务处理容量": {
    #                 "val": 3.5
    #             },
    #             "用户访问增长的充分性": {
    #                 "val": 4.5
    #             },
    #             "用户访问量": {
    #                 "val": 17.0
    #             }
    #         },
    #         "时间特性": {
    #             "周转时间充分性": {
    #                 "val": 1.40625
    #             },
    #             "响应时间的充分性": {
    #                 "val": 0.213898916967509
    #             },
    #             "平均吞吐量": {
    #                 "val": 1.185
    #             },
    #             "平均周转时间": {
    #                 "val": 4.5
    #             },
    #             "平均响应时间": {
    #                 "val": 1185.0
    #             }
    #         },
    #         "资源利用性": {
    #             "I/O设备平均占用率": {
    #                 "val": 0.3
    #             }
    #         }
    #     },
    #     "易用性": {
    #         "易学性": {
    #             "用户界面的自解释性": {
    #                 "val": 5.833333333333333
    #             }
    #         }
    #     },
    #     "维护性": {
    #         "可重用性": {
    #             "编码规则符合性": {
    #                 "val": 1.5
    #             }
    #         },
    #         "易修改性": {
    #             "修改的效率": {
    #                 "val": 1.3333333333333333
    #             }
    #         },
    #         "易分析性": {
    #             "系统日志完整性": {
    #                 "val": 2.3333333333333335
    #             }
    #         }
    #     }
    # }
    data = {}
    return jsonify(data)


@app.post("/setMinMax/<projectname>")
def setMinMax(projectname):
    minMaxData = request.get_json()
    return jsonify()


app.run(host="0.0.0.0", port=5001)
# if __name__ == "main":
#     app.run(host="0.0.0.0", port=5001)
