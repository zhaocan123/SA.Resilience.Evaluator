import os
import shutil
import subprocess
import zipfile

from flask import jsonify, request, Blueprint

from app import executor
from badsmell import del_bad_smell
from my_utils import add_micro_define, get_pro_files, rewrite_file, walk_floder
from project import *
from service import *
from metric import *
from app import app

project_api = Blueprint('project_api', __name__)


@project_api.route('/createProject', methods=['POST'])
def create_task():
    a = dict(request.get_json())
    upload_path = app.config.get("UPLOADS_DEFAULT_DEST")
    a['codeRoot'] = (upload_path + "/" + a["projectName"] +
                     "/code").replace("\\", "/").replace("//", "/")
    if a["fileSelect"]:
        for i in a["fileSelect"]:
            i["path"] = upload_path + "/" + \
                a["projectName"] + "/docs/" + i["path"]
            i["path"].replace("\\", "/").replace("//", "/")
    elif a['pdocs']:
        tmp = []
        for i in a['pdocs']:
            i = upload_path + "/" + a["projectName"] + "/docs/" + i
            i = i.replace("\\", "/").replace("//", "/")
            tmp.append(i)
        a['pdocs'] = tmp
    else:
        tmp = []
        for i in a['cddocs']:
            i = upload_path + "/" + a["projectName"] + "/docs/" + i
            i = i.replace("\\", "/").replace("//", "/")
            tmp.append(i)
        a["cddocs"] = tmp
    if query2(a["projectName"]) is not None:
        return jsonify({"createFlag": 1, "msg": a["projectName"] + "创建失败，存在同名项目！"}), 201
    task_id = add_task()
    a["task_id"] = str(task_id)
    a["codeFiles"] = {"header": [], "source": []}
    ctypelist = (".c")
    cpptypelist = (".C", ".cc", ".CC", ".cp", ".c++", ".C++", ".cxx", ".cpp", ".CPP", ".CXX")
    headertypelist = (".h", ".H", ".hh", ".hpp", ".hxx")
    fileTypes = {
        "c": [],
        "cpp": [],
        "header": [],
        # "other": []
    }
    for file_path in a["selectCodeFiles"]:
        if file_path.endswith(ctypelist):
            a["codeFiles"]["source"].append(file_path.replace("\\", "/").replace("./", a['codeRoot']+"/"))
            fileTypes['c'].append(file_path.replace("\\", "/").replace("./", a['codeRoot']+"/"))
        elif file_path.endswith(cpptypelist):
            a["codeFiles"]["source"].append(file_path.replace("\\", "/").replace("./", a['codeRoot']+"/"))
            fileTypes['cpp'].append(file_path.replace("\\", "/").replace("./", a['codeRoot']+"/"))
        elif file_path.endswith(headertypelist):
            a["codeFiles"]["header"].append(file_path.replace("\\", "/").replace("./", a['codeRoot']+"/"))
            fileTypes['header'].append(file_path.replace("\\", "/").replace("./", a['codeRoot']+"/"))
    # for root, dirs, files in os.walk(a['codeRoot']):
    #     for file in files:
    #         if file.endswith(ctypelist):
    #             fileTypes['c'].append(os.path.join(root, file).replace('\\', '/'))
    #         elif file.endswith(cpptypelist):
    #             fileTypes['cpp'].append(os.path.join(root, file).replace('\\', '/'))
    #         elif file.endswith(headertypelist):
    #             fileTypes['header'].append(os.path.join(root, file).replace('\\', '/'))
    #         else:
    #             fileTypes['other'].append(os.path.join(root, file).replace('\\', '/'))
    with open(upload_path + "/" + a["projectName"] + "/analyze_files.json", "w", encoding="utf-8") as f:
        json.dump(a["codeFiles"], f, ensure_ascii=False, indent=4)
    if fileTypes['c']:
        if fileTypes['cpp']:
            projectType = 2
        else:
            projectType = 0
    else:
        projectType = 1
    project = Project(
        name=a["projectName"],
        path=app.config.get("UPLOADS_DEFAULT_DEST")+"/"+a["projectName"],
        task_id=task_id,
        type=projectType
    )
    add_project(project)
    a["fileTypes"] = fileTypes
    executor.submit(task, task_id, a)
    return jsonify({"createFlag": 0, "msg": a["projectName"] + "项目创建成功!"}), 201


@app.route("/queryProjectName/<projectName>", methods=['POST', "GET"])
def queryProjectName(projectName):
    if query2(projectName) is not None:
        return jsonify({"createFlag": 1, "msg": projectName + "创建失败，存在同名项目！"}), 201
    else:
        return jsonify({"createFlag": 0, "msg": "新项目创建成功"}), 200


@project_api.route("/uploadProjectZip/<projectName>", methods=['POST'])
def uploadProjectZip(projectName):
    zip_file = request.files.get("projectZip")
    project_path = app.config.get("UPLOADS_DEFAULT_DEST") + "/" + projectName
    project_path = project_path.replace("\\", "/").replace("//", "/")
    if os.path.exists(project_path):
        shutil.rmtree(project_path)
        # tmp = f"rm -r {project_path}"
        # t = subprocess.Popen(["Powershell.exe", tmp])
        # if t.communicate()[0] != b'':
        #     raise Exception("删除文件夹失败！")
        # else:
        #     os.mkdir(project_path)
    else:
        os.mkdir(project_path)
    zip_file_name = zip_file.filename
    zip_file_path = project_path + "/" + zip_file_name
    zip_file.save(zip_file_path)
    code_path = project_path + "/code"
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        # 解压后如果是文件直接在code目录，如果是文件夹则在code目录下一个文件夹展开
        zip_ref.extractall(code_path)
    # 解析文件夹目录树并返回，如果是一个一个文件则返回"."

    includes_list = set()
    if os.path.exists(code_path+"/excluded_path.txt"):
        replace_dir = []
        for item in os.scandir(code_path):
            if item.is_dir():
                replace_dir.append(item.name)
        if len(replace_dir) > 1:
            raise Exception("压缩包中存在多个项目文件夹，不符合要求！")
        with open(code_path+"/excluded_path.txt", "r") as f:
            while True:
                line = f.readline()
                if not line:
                    break
                line = line.strip().strip("\n")
                if line != "":
                    if len(replace_dir) == 1:
                        line = line.replace("\\", "/")
                        line = line.replace(".", "./" + replace_dir[0])
                    else:
                        line = line.replace("\\", "/")
                    if line[-1] == "/":
                        line = line[:-1]
                    # 直接删除该文件夹下所有的文件
                    del_path = os.path.abspath(os.path.join(code_path, line))
                    if os.path.exists(del_path):
                        shutil.rmtree(del_path)
                    # includes_list.add(line)
                    # for root, dir, files in os.walk(line):
                    #     for dir_name in dir:
                    #         includes_list.add(os.path.join(root, dir_name).replace("\\", "/"))
    uvprojx_path = []
    pro_files = []
    floder_tree = walk_floder(code_path, code_path, uvprojx_path)
    code_dict = rewrite_file(code_path, project_path, includes_list)
    add_micro_define(code_path, project_path)
    if uvprojx_path != []:
        pro_files = get_pro_files(uvprojx_path[0], code_path, code_dict)
    return jsonify({"floder_tree": [{"id": 0, "path": "/", "label": "/", "children": floder_tree}], "uvprojx": pro_files}), 200
    # return jsonify([{"id": 0, "path": "/", "label": "/", "children": floder_tree}]), 200


@project_api.get("/get_project_percentage/<project_task_id>")
def get_project_percentage(project_task_id):
    res = get_task_from_mysql(project_task_id)
    data = {
        "ready": False,
        "failed": False,
        "percentage": 0.0
    }
    if len(res) == 0:
        raise Exception("检索task_id失败")
    count = 0.0
    if res["done"] == 1:
        data["ready"] = True
    elif res["done"] == -1:
        data["failed"] = True
    for key, value in res.items():
        if key == "done":
            continue
        if value == 1:
            count += 1
    data["percentage"] = round(count / (len(res) - 1) * 100, 2)

    return jsonify(data)


@project_api.route("/uploadProjectFile/<projectName>", methods=['POST'])
def uploadProjectFile(projectName):
    docs = request.files.getlist("docs")
    for doc in docs:
        file_name = doc.filename.split("/")
        file_path = app.config.get("UPLOADS_DEFAULT_DEST") + "/" + projectName
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        file_path += "/docs/"
        # print(file_path)
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        for i in range(len(file_name) - 1):
            file_path += file_name[i] + "/"
            # print(file_path)
            if not os.path.exists(file_path):
                os.mkdir(file_path)
        file_path += file_name[-1]
        if os.path.exists(file_path):
            continue
        else:
            doc.save(file_path)
    return jsonify({"createFlag": 0, "msg": "success"}), 200


@project_api.route('/remove_project/<projectname>/<task_id>', methods=['delete'])
def remove_project(projectname, task_id):
    if (task_id in Threads.keys()):
        stop_thread(Threads[task_id][1])
    updir = app.config.get("UPLOADS_DEFAULT_DEST") + "/" + projectname
    if os.path.exists(updir):
        shutil.rmtree(updir)
    if os.path.exists(app.config.get("EXE_PATH") + "/temp/" + projectname):
        shutil.rmtree(app.config.get("EXE_PATH") + "/temp/" + projectname)
    delete_project(projectname)
    delete_metric(projectname)
    del_bad_smell(projectname)
    # cpath = WEB_PATH + "/" + projectname
    # tmp = f"rm -r {cpath}"
    # subprocess.Popen(["Powershell.exe", tmp])
    # subprocess.Popen(["Powershell.exe", 'rm '+path+'/data/tmp/'+projectname+'filedata.bak '+path+'/data/tmp/'+projectname+'filedata.dat '+path+'/data/tmp/'+projectname+'filedata.dir '+path+'/data/tmp/' +
    #                  projectname+'fun_comment.bak '+path+'/data/tmp/'+projectname+'fun_comment.dat '+path+'/data/tmp/'+projectname+'fun_comment.dir '+path+'/data/tmp/'+projectname+'funcNumber.json'])
    return "ok"
