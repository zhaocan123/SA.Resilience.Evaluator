import ctypes
import inspect
import os
import threading

# import pythoncom
from flask_apscheduler import APScheduler
from CodeInfoExtract import GetInfo, build_plcg_dot, file2project, get_Buffer_overflow, get_class_anno, get_func_anno, get_info_from_func, print2json, runParsing, saveasdict
from DesignMetric import getDesignMetric

# from DocExtract import UpdataMetrix, docextract
from merge_funcInfo import merge_funcInfo
from project import query3, Project
from taskModel import *
from app import app
import BuildCG
import null25000
import call_back
import layer_graph
import pipe_filter
import sdg_new
import call_back_comp_cpp
import Class_Diagram
import traceback
import networkx as nx
import Component_recovery
import attack_surface_info
import attack_surface_uml
import attack_surface_source

Threads = {}


def _async_raise(tid, exctype):
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(pid):
    # 停止运行
    _async_raise(pid, SystemExit)


def task(task_id, a):
    # 解决win32com包的并发错误
    # pythoncom.CoInitialize()
    task_dict = {
        "done": 0,
        "runParsing": None,
        "info_ext": None,
        "merge_fun_info": None,
        "merge_pro_info": None,
        "callback_info": None,
        "layer_info": None,
        "pipe_info": None,
        "sdg_info": None,
        "cg_info": None,
        "doc_info": None,
        "metric_info": None,
    }
    Threads[task_id] = (threading.current_thread().name,
                        threading.current_thread().ident)
    project = query3(a["projectName"])
    id = project.id
    # 设计恢复
    project_name = a["projectName"]
    # 获取代码文件列表
    fileTypes = a["fileTypes"]
    file_list = []
    file_list += a["codeFiles"]['header']
    file_list += a["codeFiles"]['source']
    # file_list, fileTypes = CI.getfilelist(a["codeRoot"])
    # print(os.path.abspath(a["codeRoot"] + "/wsd_uml_folder"))
    if os.path.exists(os.path.abspath(a["codeRoot"] + "/wsd_uml_folder")):
        task_dict = {
            "done": 1,
            "runParsing": 1,
            "info_ext": 1,
            "merge_fun_info": 1,
            "merge_pro_info": 1,
            "callback_info": 1,
            "layer_info": 1,
            "pipe_info": 1,
            "sdg_info": 1,
            "cg_info": 1,
            "doc_info": 1,
            "metric_info": 1,
        }
        func_data = {}
        new_classInfo_dict = {}
        file_data = {}
        bad_smell = {}
        graph_json = {}
        design_metrics_data = {}
        projectInfo_dict = {"projectName": project_name, "projectType":1}
        update_task(task_id, task_dict)
    else:
        # 运行解析程序
        try:
            runParsing(file_list, a["codeRoot"])
            task_dict["runParsing"] = 1
            update_task(task_id, task_dict)
        except:
            traceback.print_exc()
            task_dict["runParsing"] = 0
            task_dict["done"] = -1
            update_task(task_id, task_dict)

        # # 此处的try except为测试用
        # try:

        # 获取信息
        print("源码解析完成，开始提取信息")
        try:
            codeFileInfo_dict, funcInfo_dict, classInfo_dict, global_var_list, input_locate, if_locate, matched_func_key = GetInfo(file_list, a["codeRoot"])
            task_dict["info_ext"] = 1
            update_task(task_id, task_dict)
        except:
            traceback.print_exc()
            task_dict["info_ext"] = 0
            task_dict["done"] = -1
            update_task(task_id, task_dict)
        # 保存为字典
        print("信息提取完成，开始保存信息")
        try:
            new_codeFileInfo_dict, new_funcInfo_dict, new_classInfo_dict = saveasdict(codeFileInfo_dict, funcInfo_dict, classInfo_dict, global_var_list)
            # 合并函数信息
            new_codeFileInfo_dict, new_funcInfo_dict = merge_funcInfo(new_codeFileInfo_dict, new_funcInfo_dict, matched_func_key)

            new_funcInfo_dict = get_func_anno(a["codeRoot"], new_funcInfo_dict, new_codeFileInfo_dict)
            new_classInfo_dict = get_class_anno(a["codeRoot"], new_classInfo_dict, new_codeFileInfo_dict)
            # 将plcg存到nx中
            PLCG_nx = build_plcg_dot(new_funcInfo_dict, a["codeRoot"], funcInfo_dict)
            task_dict["merge_fun_info"] = 1
            update_task(task_id, task_dict)
        except:
            traceback.print_exc()
            task_dict["merge_fun_info"] = 0
            task_dict["done"] = -1
            update_task(task_id, task_dict)
        print("合并函数信息完成")

        # 构造类图
        try:
            new_classInfo_dict, class_js_data = Class_Diagram.CLASS_main(new_classInfo_dict, new_funcInfo_dict)
            projectInfo_dict = file2project(project_name, new_codeFileInfo_dict, a["codeRoot"], fileTypes)
            print("projectInfo_dict计算完成")
            print(a["codeRoot"])
            print2json(a["codeRoot"], new_codeFileInfo_dict, new_funcInfo_dict, new_classInfo_dict, projectInfo_dict)
            print("print2json完成")

            in_degree_0, func_header_source = get_info_from_func(new_funcInfo_dict)
            task_dict["merge_pro_info"] = 1
            update_task(task_id, task_dict)
        except:
            traceback.print_exc()
            task_dict["done"] = -1
            task_dict["merge_pro_info"] = 0
            update_task(task_id, task_dict)
        print("项目级信息合并完成")
        # FOR C PROJECTS ONLY
        # TODO： CHECK if this is a C PROJECT
        # 构造调用返回和层次图
        # 构造组件依赖图
        try:
            comp_data_csv_path = call_back_comp_cpp.main(new_funcInfo_dict, new_classInfo_dict, PLCG_nx)
            call_back_json = call_back.comp2json(PLCG_nx, comp_data_csv_path)
            task_dict["callback_info"] = 1
            update_task(task_id, task_dict)
        except:
            traceback.print_exc()
            task_dict["done"] = -1
            task_dict["callback_info"] = 0
            update_task(task_id, task_dict)
        task_dict["layer_info"] = 1
        if projectInfo_dict['projectType'] == 0:
            # try:
            #     layer_graph_json = layer_graph.main(comp_data_csv_path, PLCG_nx)
            #     task_dict["layer_info"] = 1
            #     update_task(task_id, task_dict)
            # except:
            #     traceback.print_exc()
            #     task_dict["done"] = -1
            #     task_dict["layer_info"] = 0
            #     update_task(task_id, task_dict)
            # 构造管道过滤器
            try:
                pipe_filter_graph, pipe_filter_svg = pipe_filter.main(file_list, PLCG_nx, a["codeRoot"])
                task_dict["pipe_info"] = 1
                update_task(task_id, task_dict)
            except:
                traceback.print_exc()
                task_dict["pipe_info"] = 0
                task_dict["done"] = -1
                update_task(task_id, task_dict)
        else:
            task_dict["pipe_info"] = 1
            update_task(task_id, task_dict)
        # 构造SDG
        try:
            sdg_svg, sdg_nx = sdg_new.main(file_list, PLCG_nx, a["codeRoot"])
            ml_PLCG_nx = nx.MultiDiGraph(PLCG_nx)
            comp_js = Component_recovery.deal_sdg(ml_PLCG_nx, sdg_nx, func_header_source, a["projectName"])
            task_dict["sdg_info"] = 1
            update_task(task_id, task_dict)
        except:
            traceback.print_exc()
            task_dict["sdg_info"] = 0
            task_dict["done"] = -1
            update_task(task_id, task_dict)
        # 构造CG
        try:
            func_data, bad_smell, graph_json, CG, file_data, Component_redundancy, Standalone_components = BuildCG.BUILDCG_main(file_list, a["codeRoot"], a["projectName"], PLCG_nx, in_degree_0, func_header_source, call_back_json)
            task_dict["cg_info"] = 1
            update_task(task_id, task_dict)
        except:
            traceback.print_exc()
            task_dict["cg_info"] = 0
            task_dict["done"] = -1
            update_task(task_id, task_dict)
        if projectInfo_dict['projectType'] == 0:
            # graph_json['layer_js'] = layer_graph_json
            graph_json['pipe_filter_svg'] = pipe_filter_svg
            graph_json['sdg_svg'] = sdg_svg

        # graph_json['callback_js'] = call_back_json
        graph_json['class_js'] = class_js_data
        graph_json['comp_js'] = comp_js

        # except Exception as e:
        #     print(e)
        #     traceback.print_exc()
        # print(bad_smell)
        # print("bad_smell计算完成")
        design_metrics_data = {} #  getDesignMetric(func_data, new_classInfo_dict)

    try:
        if os.path.exists(os.path.abspath(a["codeRoot"] + "/wsd_uml_folder")):
            allinfos, attack_graph_str, conv_info = attack_surface_uml.deal_project(a["codeRoot"]) 
            projectInfo_dict["REL_TYPE"] = "UML"
            projectInfo_dict["uml_info"] = allinfos["uml_info"]
        else:
            allinfos, attack_graph_str, conv_info = attack_surface_source.deal_project(PLCG_nx, pipe_filter_graph, sdg_nx, a["codeRoot"])
            projectInfo_dict["REL_TYPE"] = "Source"
        resilience_info, attackSurfaceInfo = conv_info[0], conv_info[1]
        projectInfo_dict["attackSurfaceInfo"] = attackSurfaceInfo
        projectInfo_dict["resilience_report_info"] = resilience_info
        # projectInfo_dict["allrelinfo"] = allinfos
        graph_json["attack_js"] = attack_graph_str

        print("AAAAAAAAAAA")

    except:
        traceback.print_exc()

    # import pprint
    # pprint.pprint(projectInfo_dict)

    # import json
    # try:
    #     res_str_pro = json.dumps(projectInfo_dict, indent=4)
    #     with open("temp/temp.json", "w") as f:
    #         f.write(res_str_pro)
    #     print(res_str_pro)
        
    # except:
    #     traceback.print_exc()

    try:
        with app.app_context():
            project1 = Project.query.get(id)
            project1.function_info_json = str(func_data).encode()
            project1.class_info_json = str(new_classInfo_dict).encode()
            project1.project_json = str(projectInfo_dict).encode()
            project1.file_json = str(file_data).encode()
            project1.bad_smell_json = str(bad_smell).encode()
            project1.type = projectInfo_dict['projectType']
            project1.graph_info_json = str(graph_json).encode()
            print(len(project1.graph_info_json))
            print(len(project1.function_info_json))
            # project1.index_info_json = str(metric25010).encode()
            project1.design_metrics_json = str(design_metrics_data).encode()
            print(3)
            try:
                db.session.commit()
            except Exception as e:
                print(e)
            print(4)
        print("finished")
        task_dict["done"] = 1
        update_task(task_id, task_dict)
        Threads.pop(task_id)
    except:
        traceback.print_exc()
