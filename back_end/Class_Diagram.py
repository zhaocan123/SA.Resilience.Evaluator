'''
构造类图
作者：刘梓轩
日期：2023年7月19日
'''

import json 

def build_class_graph(class_data, func_data):
    # project_data为项目信息的字典
    # class_data为类信息的字典
    print('build class graph 1')
    class_dict = class_data
    #PLCG_dict = PLCG
    func_info_dict = func_data
    # 根据提取到的信息获得类关系
    class_relation = {}
    class_relation['Dependency'] = [] # 依赖关系
    class_relation['Association'] = [] # 关联关系
    class_relation['polymerization'] = [] # 聚合关系
    class_relation['composition'] = [] # 组合关系
    class_relation['inheritance'] = [] # 继承关系
    class_relation['realization'] = [] # 实现关系

    print('build class graph 2')

    # 依赖关系
    """
    1、类B作为类A的成员函数参数
    2、类B作为类A的成员函数的局部变量
    3、类A的成员函数调用B的静态方法
    """
    for class1, class1_info in class_dict.items():
        for mem_method in class1_info['mem_method']:
            # 类B作为类A的成员函数参数
            for param in mem_method['param_list']:
                if param['call_type'] == 'Class':
                    call_loc = param['call_loc']
                    # 删除最后一个冒号之后的字符串
                    
                    call_class_key = call_loc
                    dep = [class1, call_class_key]
                    if dep not in class_relation['Dependency'] and dep[0] != dep[1]:
                        class_relation['Dependency'].append(dep)
            # 类B作为类A的成员函数的局部变量
            for local_var in mem_method['variable_list']:
                if local_var['is_record'] == True and local_var['is_global'] == False:
                    
                    type_class_key = local_var['type_loc']
                    dep = [class1, type_class_key]
                    if dep not in class_relation['Dependency'] and dep[0] != dep[1]:
                        class_relation['Dependency'].append(dep)

            # 类A的成员函数调用B的静态方法
            mem_method_key = mem_method['this_loc'] + ':' + mem_method['name']
            called_func_list = func_info_dict[mem_method_key]['fanOut']
            for called_func in called_func_list:
                called_func_info = func_info_dict[called_func]
                if called_func_info['type'] == 'Method':
                    if 'static' in called_func_info['modify']:
                        class_key = ':'.join(called_func.split(':')[:-2]) +':'+ called_func_info["locateClass"]

                        dep = [class1, class_key]
                        if dep not in class_relation['Dependency'] and dep[0] != dep[1]:
                            class_relation['Dependency'].append(dep)

    print('build class graph 2')

    # 关联关系
    """
    被关联类B以类的属性形式出现在关联类A中
    关联类A引用了一个类型为被关联类B的全局变量
    """
    temp = []
    for class1, class1_info in class_dict.items():
        # 被关联类B以类的属性形式出现在关联类A中
        for mem_var in class1_info['mem_var']:
            call_type = mem_var['call_type']
            if 'class' in call_type:
                call_loc = mem_var['call_loc']
                # 删除最后一个冒号之后的字符串
                call_class_key = call_loc
                ass = [class1, call_class_key]
                if ass not in class_relation['Association'] and ass[0] != ass[1]:
                    class_relation['Association'].append(ass)
                if ass not in temp and ass[0] != ass[1]:
                    temp.append(ass+[call_loc.split(':')[-1]])
        
        # 关联类A引用了一个类型为被关联类B的全局变量
        for var in class1_info['variable_list']:
            if var["is_global"] == True:
                type = var["type"].replace('class ', '')
                type_loc = var["type_loc"]
                #type_loc = ':'.join(type_loc.split(':')[:-2])
                type_class_key = type_loc
                ass = [class1, type_class_key]
                if ass not in class_relation['Association'] and ass[0] != ass[1]:
                    class_relation['Association'].append(ass)

    print('build class graph 3')
    # 聚合关系和组合关系
    # 聚合关系：类A作为成员变量（指针）被类B使用，且A只被B使用
    for rel1 in temp:
        class11 = rel1[0]
        class12 = rel1[1]
        type = rel1[2]
        # 判断是否有其他类关联class2：
        find = 0
        for rel2 in temp:
            if rel2 != rel1:
                if rel2[1] == class12:
                    find = 1
                    break
        
        if find == 0:
            if '*' in type:
                # 聚合关系
                pol = [class11,class12]
                if pol not in class_relation['polymerization']:
                    class_relation['polymerization'].append(pol)
            else:
                # 组合关系
                com = [class11,class12]
                if com not in class_relation['composition']:
                    class_relation['composition'].append(com)

    print('build class graph 4')
    # 继承关系和实现关系
    for class1, class1_info in class_dict.items():
        for base_info in class1_info["baseClass"]:
            base = base_info["class_loc"].replace('class ','')
            base_class_info = class_dict[base]
            is_find = False
            # 遍历基类的成员函数
            for mem_method in base_class_info['mem_method']:
                methonline = mem_method['this_loc'].split(':')[-1]
                if methonline != base_class_info['locateLine']:
                    method_key = mem_method['this_loc'] + ':' + mem_method['name']
                    method_info = func_info_dict[method_key]
                    codetext = method_info['codeText'][-1].replace(' ','').replace('\n','').replace(';','')
                    if codetext[-2:] != '=0':
                        if 'static' not in mem_method['authority']:
                            # 如果既不是纯虚函数 也不是静态函数，则不是接口
                            is_find = True
            
            # 遍历成员遍历
            for mem_var in base_class_info['mem_var']:
                if 'static' not in mem_var['authority']:
                    is_find = False
                    
                    
                        

            rel = [class1, base]
            if is_find == False:
                # 实现关系
                if rel not in class_relation['realization']:
                    class_relation['realization'].append(rel)
            else:
                # 继承关系
                if rel not in class_relation['inheritance']:
                    class_relation['inheritance'].append(rel)

    for c,c_info in class_data.items():
        for mem_method in c_info['mem_method']:
            mem_method_key = mem_method['this_loc'] + ':' + mem_method['name']
            if mem_method_key in func_data.keys():
                mem_method['fanIn_num'] = len(func_data[mem_method_key]['fanIn'])
    print('build class graph 5')
    # 修改class_data中的fanin和fanout
    for rel_type, rel_list in class_relation.items():
        for rel in rel_list:
            class1 = rel[0]
            class2 = rel[1]
            if class2 not in class_dict[class1]['fanOut']:
                class_dict[class1]['fanOut'].append(class2)
            if class1 not in class_dict[class2]['fanIn']:
                class_dict[class2]['fanIn'].append(class1)

    print('build class graph 6')
    return class_relation, class_dict

def build_class_js(class_relation, class_data):
    # 输出到js中
    data_list = []
    link_list = []
    categories = [
                {
                    "name": "Class"
                },
                {
                    "name": "Struct"
                },
                {
                    "name": "Union"
                }
            ]
    
    for class1, class1_info in class_data.items():
        temp_dict = {}
        temp_dict['name'] = class1_info['name']
        temp_dict['id'] = class1
        temp_dict['file'] = class1_info['locateFile']
        # 类别
        if class1_info['type'] == 'Class':
            temp_dict['category'] = 0
        elif class1_info['type'] == 'Struct':
            temp_dict['category'] = 1
        elif class1_info['type'] == 'Union':
            temp_dict['category'] = 2

        # 属性
        temp_dict["symbolSize"] = 45
        temp_dict["fixed"] = False
        temp_dict["itemStyle"] = {
                        "normal": {
                            "opacity": 1
                        }
                    }
        
        # 成员变量
        mem_var_list = []
        for mem_var in class1_info['mem_var']:
            mem = mem_var['this_name'] + ' : ' + mem_var['call_type']
            if 'public' in mem_var['authority']:
                mem = '+ ' + mem
            elif 'private' in mem_var['authority']:
                mem = '- ' + mem
            elif 'protected' in mem_var['authority']:
                mem = '# ' + mem
            mem_var_list.append(mem)
        temp_dict['mem_var'] = list(set(mem_var_list))

        # 成员函数
        mem_method_list = []
        for mem_method in class1_info['mem_method']:
            mem = mem_method['name'] + '() : ' + mem_method['return_type']
            if 'public' in mem_method['authority']:
                mem = '+ ' + mem
            elif 'private' in mem_method['authority']:
                mem = '- ' + mem
            elif 'protected' in mem_method['authority']:
                mem = '# ' + mem
            mem_method_list.append(mem)
        temp_dict['mem_method'] = list(set(mem_method_list))

        # 基类
        base_list = []
        for base in class1_info['baseClass']:
            base_list.append(base['class_loc'])
        temp_dict['baseClass'] = base_list

        data_list.append(temp_dict)

    count_dict = {}
    for rel_type, rel_list in class_relation.items():
        for rel in rel_list:
            temp_dict = {}
            temp_dict['source'] = rel[0]
            temp_dict['target'] = rel[1]
            if rel[0] not in count_dict.keys():
                count_dict[rel[0]] = {}
            if rel[1] not in count_dict[rel[0]]:
                count_dict[rel[0]][rel[1]] = 1
            else:
                count_dict[rel[0]][rel[1]] += 1
            # 边的弧度
            curveness = 0.2*count_dict[rel[0]][rel[1]]
            #temp_dict['formatter'] = rel_type
            temp_dict['label'] = {
                "show": True,
                "position": "middle",
                "formatter": rel_type[:3]
            }
            
            temp_dict["symbol"] = [
                "none",
                "arrow"
            ]
            temp_dict["lineStyle"] = {
                "normal": {
                    "width": 2,
                    "curveness": curveness,
                    "type": "solid",
                            "opacity": 1
                }
            }
            link_list.append(temp_dict)

    js_data = {}
    js_data['data'] = data_list
    js_data['links'] = link_list
    js_data['categories'] = categories


    # 保存到json文件中
    with open('./static/class.js', 'w', encoding='utf-8') as f:
        f.write('var graph = ')
        json.dump(js_data, f, ensure_ascii=False, indent=4)

    return js_data
        

def CLASS_main(class_data, func_data):
    print('class 1')
    class_relation,class_dict = build_class_graph(class_data, func_data)
    print('class 2')
    js_data = build_class_js(class_relation, class_data)
    print('class 3')
    # # 保存到json文件中
    # with open('./static/class.json', 'w', encoding='utf-8') as f:
    #     json.dump(class_dict, f, ensure_ascii=False, indent=4)
    return class_dict, js_data

def get_json_data(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data
if __name__ == "__main__":
    class_file = r'E:\CPP_master\dev0815\CPP_support\back_end\project\realization\classInfo.json'
    class_data = get_json_data(class_file)
    PLCG_file = r'PLCG.json'
    PLCG = get_json_data(PLCG_file)
    func_file = r'E:\CPP_master\dev0815\CPP_support\back_end\project\realization\funcInfo.json'
    func_data = get_json_data(func_file)
    class_dict = CLASS_main(class_data, func_data)
    
