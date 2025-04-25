from Extract_info_from_list import *
import numpy as np


# 计算X=1-A/B，A、B可以是列表，可以是float等，返回的是列表
def template_A_over_B_list(A, B):
    if isinstance(A,list) and A:
        if isinstance(A[0],dict):
            tmp = []
            for each_one in A:
                tmp.append(each_one['val'])
            A = tmp
    if isinstance(B,list) and B:
        if isinstance(B[0],dict):
            tmp = []
            for each_one in B:
                tmp.append(each_one['val'])
            B = tmp
    if isinstance(A,dict):
        A = A['val']
    if isinstance(B,dict):
        B = B['val']
    X = None
    if A is not None and B is not None:
        if isinstance(A, list) and isinstance(B, list):
            if A and B:
                X = []
                for i in range(len(A)):
                    X.append(1-float(A[i])/float(B[i]))
        else:
            if B > 0:
                X = []
                X.append(1 - A/B)
    return X  # 返回的是列表


# 计算列表A的平均值
def template_avg_Ai_n(A):
    X = None
    if isinstance(A,list) and A:
        if isinstance(A[0],dict):
            tmp = []
            for each_one in A:
                tmp.append(each_one['val'])
            A = tmp
    if isinstance(A,dict):
        A = A['val']
        X = None
        if A:
            X = np.mean(A)
    elif isinstance(A,list) and A:
        if isinstance(A[0],dict):
            L = []
            for dic in A:
                L.append(dic['val'])
            X = None
            if L:
                X = np.mean(L)
        else:
            X = None
            if A:
                X = np.mean(A)
    return X


# 计算列表A除以n的平均值
def template_Ai_cover_n(A, n):
    if isinstance(A,list) and A:
        if isinstance(A[0],dict):
            tmp = []
            for each_one in A:
                tmp.append(each_one['val'])
            A = tmp
    if isinstance(A,dict):
        A = A['val']
    if isinstance(n, dict):
        n = n['val']
    X = None
    if A and n != 0:
        X = np.sum(A)
        X = X/n
    return X


# 计算X=1-A/B，但B是列表（阈值相关内容）
def template_one_A_over_B_Threshold(A, B, template):
    if isinstance(A,list) and A:
        if isinstance(A[0],dict):
            tmp = []
            for each_one in A:
                tmp.append(each_one['val'])
            A = tmp
    if isinstance(B,list) and B:
        if isinstance(B[0],dict):
            tmp = []
            for each_one in B:
                tmp.append(each_one['val'])
            B = tmp
    if isinstance(A,dict):
        A = A['val']
    if isinstance(B,dict):
        B = B['val']
    X = None
    if B:
        if A is not None and template != 0:
            if is_number(A):
                if template == 1 and is_number(B[0]):
                    X = 1 - A/B[0]
                elif template == 2 and is_number(B[0]):
                    X = 1 - B[0]/A
                elif template == 3 and is_number(B[0]) and is_number(B[1]):
                    X = [1 - A/B[0], 1 - B[0]/A]
    return X


# 计算X=A/B，但B是列表（阈值相关内容）
def template_A_over_B_Threshold(A, B, template):
    if isinstance(A,list) and A:
        if isinstance(A[0],dict):
            tmp = []
            for each_one in A:
                tmp.append(each_one['val'])
            A = tmp
    if isinstance(B,list) and B:
        if isinstance(B[0],dict):
            tmp = []
            for each_one in B:
                tmp.append(each_one['val'])
            B = tmp
    if isinstance(A,dict):
        A = A['val']
    if isinstance(B,dict):
        B = B['val']
    X = None
    if B:
        if B[0] == 0:
            X = 0
        elif A is not None and template != 0:
            if is_number(A):
                if template == 1 and is_number(B[0]):
                    X = A/B[0]
                elif template == 2 and is_number(B[0]):
                    X = A/B[0]
                elif template == 3 and is_number(B[0]) and is_number(B[1]):
                    X = [1 - A/B[0], 1 - B[0]/A]
    return X


# B-A再求平均的模板，如果有Xi则直接求Xi平均，否则求Bi-Ai的平均
def template_B_minus_A(Ai, Bi, Xi):
    if isinstance(Ai,list) and Ai:
        if isinstance(Ai[0],dict):
            tmp = []
            for each_one in Ai:
                tmp.append(each_one['val'])
            Ai = tmp
    if isinstance(Bi,list) and Bi:
        if isinstance(Bi[0],dict):
            tmp = []
            for each_one in Bi:
                tmp.append(each_one['val'])
            Bi = tmp
    if isinstance(Xi,list) and Xi:
        if isinstance(Xi[0],dict):
            tmp = []
            for each_one in Xi:
                tmp.append(each_one['val'])
            Xi = tmp
    if isinstance(Ai,dict):
        Ai = Ai['val']
    if isinstance(Bi,dict):
        Bi = Bi['val']
    if isinstance(Xi,dict):
        Xi = Xi['val']
    Ti = []
    if Xi:
        Ti = Ti + Xi
    if Ai is not None and Bi is not None:
        LAi = len(Ai)
        LBi = len(Bi)
        if Ai and Bi and (LAi == LBi):
            for i in range(LAi):
                Ti.append(Bi[i] - Ai[i])
    X = template_avg_Ai_n(Ti)
    return X


# A/B再求平均的模板，如果有Xi则直接求Xi平均，否则求Ai/Bi的平均
def template_A_over_B_avg(Ai, Bi, Xi):
    if isinstance(Ai,list) and Ai:
        if isinstance(Ai[0],dict):
            tmp = []
            for each_one in Ai:
                tmp.append(each_one['val'])
            Ai = tmp
    if isinstance(Bi,list) and Bi:
        if isinstance(Bi[0],dict):
            tmp = []
            for each_one in Bi:
                tmp.append(each_one['val'])
            Bi = tmp
    if isinstance(Xi,list) and Xi:
        if isinstance(Xi[0],dict):
            tmp = []
            for each_one in Xi:
                tmp.append(each_one['val'])
            Xi = tmp
    if isinstance(Ai,dict):
        Ai = Ai['val']
    if isinstance(Bi,dict):
        Bi = Bi['val']
    if isinstance(Xi,dict):
        Xi = Xi['val']
    Ti = []
    if Xi:
        Ti = Ti + Xi
    if Ai is not None and Bi is not None:
        LAi = len(Ai)
        LBi = len(Bi)
        if Ai and Bi and (LAi == LBi):
            for i in range(LAi):
                Ti.append(Ai[i] / Bi[i])
    X = template_avg_Ai_n(Ti)
    return X


# A/B再除以n的模板
def template_A_over_B_over_n(Ai, Bi, n):
    if isinstance(Ai,list) and Ai:
        if isinstance(Ai[0],dict):
            tmp = []
            for each_one in Ai:
                tmp.append(each_one['val'])
            Ai = tmp
    if isinstance(Bi,list) and Bi:
        if isinstance(Bi[0],dict):
            tmp = []
            for each_one in Bi:
                tmp.append(each_one['val'])
            Bi = tmp
    if isinstance(Ai,dict):
        Ai = Ai['val']
    if isinstance(Bi,dict):
        Bi = Bi['val']
    Ti = []
    if Ai and Bi:
        for i in range(len(Ai)):
            Ti.append(Ai[i]/Bi[i])
    X = template_Ai_cover_n(Ti, n)
    return X


# A/B的模板，A和B均为对应列表的长度，计算结果为一个值
def template_A_over_B_num(A, B):
    if isinstance(A,list) and A:
        if isinstance(A[0],dict):
            tmp = []
            for each_one in A:
                tmp.append(each_one['val'])
            A = tmp
    if isinstance(B,list) and B:
        if isinstance(B[0],dict):
            tmp = []
            for each_one in B:
                tmp.append(each_one['val'])
            B = tmp
    if isinstance(A,dict):
        A = A['val']
    if isinstance(B,dict):
        B = B['val']
    X = None
    if A is not None and B is not None:
        if B > 0:
            X = A/B
        else:
            X = 0
    return X


# A*B的模板，A和B均为对应列表的长度，计算结果为一个值
def template_A_times_B_num(A, B):
    if isinstance(A,list) and A:
        if isinstance(A[0],dict):
            tmp = []
            for each_one in A:
                tmp.append(each_one['val'])
            A = tmp
    if isinstance(B,list) and B:
        if isinstance(B[0],dict):
            tmp = []
            for each_one in B:
                tmp.append(each_one['val'])
            B = tmp
    if isinstance(A,dict):
        A = A['val']
    if isinstance(B,dict):
        B = B['val']
    X = None
    if A is not None and B is not None:
        X = A * B
    return X


# 1-A/B的模板，A和B均为对应列表的长度，计算结果为一个值
def template_one_A_over_B_num(A, B):
    if isinstance(A,list) and A:
        if isinstance(A[0],dict):
            A = A[0]['val']
    if isinstance(B,list) and B:
        if isinstance(B[0],dict):
            B = B[0]['val']
    if isinstance(A,dict):
        A = A['val']
    if isinstance(B,dict):
        B = B['val']

    X = None
    if A is not None and B is not None:
        try:
            if B > 0:
                X = 1 - A/B
        except:
            X = None
    return X


def template_ms_to_other(X, C):
    T = []
    if isinstance(X, dict):
        T = X['val']
    if isinstance(X, list) and X:
        if isinstance(X[0], dict):
            for each_one in X:
                T.append(each_one['val'])
            if C == 's':  # 转为秒
                if T:
                    for i in range(len(T)):
                        T[i] = T[i] / 1000  # 毫秒转为秒
            elif C == 'm':  # 转为分钟
                if T:
                    for i in range(len(T)):
                        T[i] = T[i] / (1000 * 60)  # 毫秒转为分钟
            elif C == 'h':  # 转为小时
                if T:
                    for i in range(len(T)):
                        T[i] = T[i] / (1000 * 3600)  # 毫秒转为小时
            elif C == 'd':  # 转为天
                if T:
                    for i in range(len(T)):
                        T[i] = T[i] / (1000 * 3600 * 24)  # 毫秒转为天
            for i, each_one in enumerate(X):
                each_one['val'] = T[i]
    elif X:
        if C == 's':  # 转为秒
            if T:
                for i in range(len(T)):
                    T[i] = T[i] / 1000  # 毫秒转为秒
        elif C == 'm':  # 转为分钟
            if T:
                for i in range(len(T)):
                    T[i] = T[i] / (1000 * 60)  # 毫秒转为分钟
        elif C == 'h':  # 转为小时
            if T:
                for i in range(len(T)):
                    T[i] = T[i] / (1000 * 3600)  # 毫秒转为小时
        elif C == 'd':  # 转为天
            if T:
                for i in range(len(T)):
                    T[i] = T[i] / (1000 * 3600 * 24)  # 毫秒转为天
        X['val'] = T
    return X


def fcr1g_cd(require_document_list, use_case_document_list):
    A = fcr1g_cd_A(require_document_list, use_case_document_list)
    B = fcr1g_cd_B(require_document_list)
    X = template_A_over_B_list(A, B)
    if X:
        X = np.mean(X)
    else:
        X = -1
    metric = {'val':X, 'sub':[A,B]}
    return metric


def fcp1g_cd(require_document_list):
    A = fcp1g_cd_A(require_document_list)
    B = fcp1g_cd_B(require_document_list)
    X = template_A_over_B_list(A, B)
    if X:
        X = np.mean(X)
    else:
        X = -1
    metric = {'val': X, 'sub': [A, B]}
    return metric


def fap1g_cd(require_document_list, use_case_document_list):
    A = fap1g_cd_A(require_document_list, use_case_document_list)
    B = fap1g_cd_B(require_document_list)
    X = template_A_over_B_list(A, B)
    if X:
        X = np.mean(X)
    else:
        X = -1
    metric = {'val': X, 'sub': [A, B]}
    return metric


def fap2g_cd(require_document_list, use_case_document_list):
    A = fap1g_cd(require_document_list, use_case_document_list)
    X = template_avg_Ai_n(A)
    metric = {'val': X, 'sub': A['sub']}
    return metric


def ptb1g_cd(require_document_list, use_case_document_list):
    A = ptb1g_cd_Ai(require_document_list, use_case_document_list)
    X = template_avg_Ai_n(A)
    metric = {'val': X, 'sub': A}
    return metric


def ptb2g_cd(require_document_list, use_case_document_list):
    A = ptb1g_cd(require_document_list, use_case_document_list)
    B, template, development_value = ptb2g_cd_B(require_document_list)
    X = template_A_over_B_Threshold(A, B, template)
    tmp = deepcopy(A["sub"])
    tmp.append(B)
    metric = {'val': X, 'sub': tmp}
    return metric


def ptb3g_cd(require_document_list, use_case_document_list):
    Ai = ptb3g_cd_Ai(require_document_list, use_case_document_list)
    Bi = ptb3g_cd_Bi(require_document_list, use_case_document_list)
    Xi = ptb3g_cd_Xi(require_document_list, use_case_document_list)

    X = template_B_minus_A(Ai, Bi, Xi)
    metric = {'val': X, 'sub': Ai + Bi + Xi}
    return metric


def ptb4g_cd(require_document_list, use_case_document_list):
    A = ptb3g_cd(require_document_list, use_case_document_list)
    B, template, development_value = ptb4g_cd_B(require_document_list)
    X = template_A_over_B_Threshold(A, B, template)
    tmp = A["sub"]
    tmp.append(B)
    metric = {'val': X, 'sub': tmp}
    return metric


def ptb5g_cd(require_document_list, use_case_document_list):
    Ai = ptb5g_cd_Ai(require_document_list, use_case_document_list)
    Bi = ptb5g_cd_Bi(require_document_list, use_case_document_list)
    Xi = ptb5g_cd_Xi(require_document_list, use_case_document_list)

    Bi = template_ms_to_other(Bi, 's')
    X = template_A_over_B_avg(Ai, Bi, Xi)
    metric = {'val': X, 'sub': Ai + Bi + Xi}
    return metric


def pru1g_cd(require_document_list, use_case_document_list):
    Ai = pru1g_cd_Ai(require_document_list, use_case_document_list)
    Bi = pru1g_cd_Bi(require_document_list, use_case_document_list)
    Xi = pru1g_cd_Xi(require_document_list, use_case_document_list)

    X = template_A_over_B_avg(Ai, Bi, Xi)

    metric = {'val': X, 'sub': Ai + Bi + Xi}
    return metric


def pru2g_cd(require_document_list, use_case_document_list):
    Ai = pru2g_cd_Ai(require_document_list, use_case_document_list)
    Bi = pru2g_cd_Bi(require_document_list, use_case_document_list)
    Xi = pru2g_cd_Xi(require_document_list, use_case_document_list)

    X = template_A_over_B_avg(Ai, Bi, Xi)
    metric = {'val': X, 'sub': Ai + Bi + Xi}
    return metric


def pru3g_cd(require_document_list, use_case_document_list):
    Ai = pru3g_cd_Ai(require_document_list, use_case_document_list)
    Bi = pru3g_cd_Bi(require_document_list, use_case_document_list)
    Xi = pru3g_cd_Xi(require_document_list, use_case_document_list)

    X = template_A_over_B_avg(Ai, Bi, Xi)
    metric = {'val': X, 'sub': Ai + Bi + Xi}
    return metric


def pru4s_cd(require_document_list, use_case_document_list):
    Ai = pru4s_cd_A(require_document_list, use_case_document_list)
    Bi = pru4s_cd_B(require_document_list, use_case_document_list)
    Xi = pru4s_cd_X(require_document_list, use_case_document_list)

    X = template_A_over_B_avg(Ai, Bi, Xi)
    metric = {'val': X, 'sub': Ai + Bi + Xi}
    return metric


def pca1g_cd(require_document_list, use_case_document_list):
    Ai = pca1g_cd_A(require_document_list, use_case_document_list)
    Bi = pca1g_cd_B(require_document_list, use_case_document_list)
    Xi = pca1g_cd_X(require_document_list, use_case_document_list)

    Bi = template_ms_to_other(Bi, 's')
    X = template_A_over_B_avg(Ai, Bi, Xi)
    metric = {'val': X, 'sub': Ai + Bi + Xi}
    return metric


def pca2g_cd(require_document_list, use_case_document_list):
    Ai = pca2g_cd_Ai(require_document_list, use_case_document_list)

    X = template_avg_Ai_n(Ai)
    metric = {'val': X, 'sub': Ai}
    return metric


def pca3s_cd(require_document_list, use_case_document_list):
    Ai = pca3s_cd_A(require_document_list, use_case_document_list)
    Bi = pca3s_cd_B(require_document_list, use_case_document_list)
    Xi = pca3s_cd_X(require_document_list, use_case_document_list)

    Bi = template_ms_to_other(Bi, 's')
    X = template_A_over_B_avg(Ai, Bi, Xi)
    metric = {'val': X, 'sub': Ai + Bi + Xi}
    return metric


def cco1g_cd(require_document_list, use_case_document_list):
    A = cco1g_cd_A(require_document_list, use_case_document_list)
    B = cco1g_cd_B(require_document_list)

    X = template_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric


def cin1g_cd(require_document_list, use_case_document_list):
    A = cin1g_cd_A(require_document_list, use_case_document_list)
    B = cin1g_cd_B(require_document_list)

    X = template_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric


def cin2g_cd(require_document_list, use_case_document_list):
    A = cin2g_cd_A(require_document_list, use_case_document_list)
    B = cin2g_cd_B(require_document_list)

    X = template_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric


def cin3s_cd(require_document_list, use_case_document_list):
    A = cin3s_cd_A(require_document_list, use_case_document_list)
    B = cin3s_cd_B(require_document_list)

    X = template_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric


def uap1g_cd(require_document_list, use_case_document_list):
    A = uap1g_cd_A(require_document_list, use_case_document_list)
    B = uap1g_cd_B(require_document_list)

    X = template_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric


def uap2s_cd(require_document_list, use_case_document_list):
    A = uap2s_cd_A(require_document_list, use_case_document_list)
    B = uap2s_cd_B(require_document_list)

    X = template_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric


def uap3s_cd(require_document_list, use_case_document_list):
    A = uap3s_cd_A(require_document_list, use_case_document_list)
    B, template, development_value = uap3s_cd_B(require_document_list)

    X = None
    if A:
        X = template_A_over_B_Threshold(A[0]['val'], B, template)
    metric = {'val': X, 'sub': A + [B]}
    return metric


def ule1g_cd(require_document_list, use_case_document_list):
    A = ule1g_cd_A(require_document_list, use_case_document_list)
    B = ule1g_cd_B(require_document_list)

    X = template_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric


def ule2s_cd(require_document_list, use_case_document_list):
    A = ule2s_cd_A(require_document_list, use_case_document_list)
    B = ule2s_cd_B(require_document_list)

    X = template_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric


def ule3s_cd(require_document_list, use_case_document_list):
    A = ule3s_cd_A(require_document_list, use_case_document_list)
    B = ule3s_cd_B(require_document_list)

    X = template_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric


def ule4s_cd(require_document_list, use_case_document_list):
    A = ule4s_cd_A(require_document_list, use_case_document_list)
    B, template, development_value = ule4s_cd_B(require_document_list)

    X = None
    if A:
        X = template_A_over_B_Threshold(A[0]['val'], B, template)
    metric = {'val': X, 'sub': A+ [B]}
    return metric


def uop1g_cd(require_document_list, use_case_document_list):
    A = uop1g_cd_A(require_document_list, use_case_document_list)
    B = uop1g_cd_B(require_document_list)

    X = template_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric


def uop2g_cd(require_document_list, use_case_document_list):
    A = uop2g_cd_A(require_document_list, use_case_document_list)
    B = uop2g_cd_B(require_document_list)

    X = template_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric


def uop3s_cd(require_document_list, use_case_document_list):
    A = uop3s_cd_A(require_document_list, use_case_document_list)
    B = uop3s_cd_B(require_document_list)

    X = template_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric


def uop4s_cd(require_document_list, use_case_document_list):
    A = uop4s_cd_A(require_document_list, use_case_document_list)
    B = uop4s_cd_B(require_document_list)

    X = template_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric


def uop5s_cd(require_document_list, use_case_document_list):
    A = uop5s_cd_A(require_document_list, use_case_document_list)
    B = uop5s_cd_B(require_document_list)

    X = template_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric


def uop6s_cd(require_document_list, use_case_document_list):
    A = uop6s_cd_A(require_document_list, use_case_document_list)
    B = uop6s_cd_B(require_document_list)

    X = template_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric


def uop7s_cd(require_document_list, use_case_document_list):
    A = uop7s_cd_A(require_document_list, use_case_document_list)
    B = uop7s_cd_B(require_document_list)

    X = template_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric


def uop8s_cd(require_document_list, use_case_document_list):
    A = uop8s_cd_A(require_document_list, use_case_document_list)
    B = uop8s_cd_B(require_document_list, use_case_document_list)

    X = None
    X = template_one_A_over_B_num(A, B)  # 计算1-A/B
    metric = {'val': X, 'sub': A + B}
    return metric


def uop9s_cd(require_document_list, use_case_document_list):
    A = uop9s_cd_A(require_document_list, use_case_document_list)
    B = uop9s_cd_B(require_document_list)

    X = template_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric


def uep1g_cd(require_document_list, use_case_document_list):
    A = uep1g_cd_A(require_document_list, use_case_document_list)
    B = uep1g_cd_B(require_document_list)

    X = template_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric


def uep2s_cd(require_document_list, use_case_document_list):
    A = uep2s_cd_A(require_document_list, use_case_document_list)
    B = uep2s_cd_B(require_document_list)

    X = template_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric


def uep3s_cd(require_document_list, use_case_document_list):
    A = uep3s_cd_A(require_document_list, use_case_document_list)
    B = uep3s_cd_B(require_document_list, use_case_document_list)

    X = template_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric


def uin1s_cd(require_document_list, use_case_document_list):
    A = uin1s_cd_A(require_document_list, use_case_document_list)
    B = uin1s_cd_B(require_document_list, use_case_document_list)

    X = template_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric


def uac1g_cd(require_document_list, use_case_document_list):
    A = uac1g_cd_A(require_document_list, use_case_document_list)
    B = uac1g_cd_B(require_document_list)

    X = template_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric


def uac2s_cd(require_document_list, use_case_document_list):
    A = uac2s_cd_A(require_document_list, use_case_document_list)
    B = uac2s_cd_B(require_document_list)

    X = template_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric


def rma1g_cd(require_document_list, bug_document_list):
    A = rma1g_cd_A(require_document_list, bug_document_list)
    B = rma1g_cd_B(require_document_list, bug_document_list)

    X = template_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric


def rma2g_cd(require_document_list, use_case_document_list):
    Ai = rma2g_cd_A(require_document_list, use_case_document_list)
    Bi = rma2g_cd_B(require_document_list, use_case_document_list)
    Xi = rma2g_cd_X(require_document_list, use_case_document_list)

    Ai = template_ms_to_other(Ai, 'h')
    Xi = template_ms_to_other(Xi, 'h')
    X = template_A_over_B_avg(Ai, Bi, Xi)
    metric = {'val': X, 'sub': Ai + Bi + Xi}
    return metric


def rma3g_cd(require_document_list, use_case_document_list):
    Ai = rma3g_cd_A(require_document_list, use_case_document_list)
    Bi = rma3g_cd_B(require_document_list, use_case_document_list)
    Xi = rma3g_cd_X(require_document_list, use_case_document_list)

    Bi = template_ms_to_other(Bi, 'h')
    X = template_A_over_B_avg(Ai, Bi, Xi)
    metric = {'val': X, 'sub': Ai + Bi + Xi}
    return metric


def rma4s_cd(require_document_list, use_case_document_list):
    A = rma4s_cd_A(require_document_list, use_case_document_list)
    B = rma4s_cd_B(require_document_list, use_case_document_list)

    X = template_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric


def rav1g_cd(require_document_list, use_case_document_list):
    A = rav1g_cd_A(require_document_list, use_case_document_list)
    B, template, development_value = rav1g_cd_B(require_document_list)

    X = None
    if A:
        X = template_A_over_B_Threshold(A[0]['val'], B, template)
    metric = {'val': X, 'sub': A + [B]}
    return metric


def rav2g_cd(require_document_list, use_case_document_list):
    Ai = rav2g_cd_A(require_document_list, use_case_document_list)
    Bi = rav2g_cd_B(require_document_list, use_case_document_list)
    Xi = rav2g_cd_X(require_document_list, use_case_document_list)

    Ai = template_ms_to_other(Ai, 'd')
    Xi = template_ms_to_other(Xi, 'd')
    X = template_A_over_B_avg(Ai, Bi, Xi)
    metric = {'val': X, 'sub': Ai+ Bi+ Xi}
    return metric


def rft1g_cd(require_document_list, use_case_document_list):
    A = rft1g_cd_A(require_document_list, use_case_document_list)
    B = rft1g_cd_B(require_document_list)

    X = template_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric


def rft2s_cd():
    A = rft2s_cd_A()
    B = rft2s_cd_B()

    X = template_A_times_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric


def rft3s_cd(require_document_list, use_case_document_list):
    Ai = rft3s_cd_Ai(require_document_list, use_case_document_list)
    Bi = rft3s_cd_Bi(require_document_list, use_case_document_list)
    Xi = rft3s_cd_Xi(require_document_list, use_case_document_list)

    X = template_B_minus_A(Ai, Bi, Xi)
    if X is not None:
        X = X / 1000  # 转化为秒
    metric = {'val': X, 'sub': Ai+ Bi+ Xi}
    return metric


def rre1g_cd(require_document_list, use_case_document_list):
    A = rre1g_cd_Ai(require_document_list, use_case_document_list)
    X = template_avg_Ai_n(A)
    if X is not None:
        X = X / 1000  # 转化为秒
    metric = {'val': X, 'sub': A}
    return metric


def rre2s_cd(require_document_list, use_case_document_list):
    A = rre2s_cd_A(require_document_list, use_case_document_list)
    B = rre2s_cd_B(require_document_list)

    X = template_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric


def sco1g_cd(require_document_list, use_case_document_list):
    A = sco1g_cd_A(require_document_list, use_case_document_list)
    B = sco1g_cd_B(require_document_list)

    X = template_one_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric


def sco2g_cd(require_document_list, use_case_document_list):
    A = sco2g_cd_A(require_document_list, use_case_document_list)
    B = sco2g_cd_B(require_document_list)

    X = template_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric


def sco3s_cd(require_document_list, use_case_document_list):
    A = sco3s_cd_A(require_document_list, use_case_document_list)
    B = sco3s_cd_B(require_document_list)

    X = template_one_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric

def sin1g_cd(require_document_list, use_case_document_list):
    A = sin1g_cd_A(require_document_list, use_case_document_list)
    B = sin1g_cd_B(require_document_list)

    X = template_one_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric


def sin2g_cd(require_document_list, use_case_document_list):
    A = sin2g_cd_A(require_document_list, use_case_document_list)
    B = sin2g_cd_B(require_document_list)

    X = template_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric


def sin3s_cd():
    A = sin3s_cd_A()
    B = sin3s_cd_B()

    X = template_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric


def sno1g_cd(require_document_list, use_case_document_list):
    A = sno1g_cd_A(require_document_list, use_case_document_list)
    B = sno1g_cd_B(require_document_list)

    X = template_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric


def sac1g_cd(require_document_list, use_case_document_list):
    Ai = sac1g_cd_A(require_document_list, use_case_document_list)
    Bi = sac1g_cd_B(require_document_list, use_case_document_list)

    X = template_A_over_B_avg(Ai, Bi, [])
    metric = {'val': X, 'sub': Ai + Bi}
    return metric


def sac2s_cd(require_document_list, use_case_document_list):
    A = sac2s_cd_A(require_document_list, use_case_document_list)
    B, template, development_value = sac2s_cd_B(require_document_list)

    A = template_ms_to_other(A, 'd')
    B = template_ms_to_other(B, 'd')
    X = None
    if A:
        X = template_A_over_B_Threshold(A[0]['val'], B, template)
    metric = {'val': X, 'sub': A + [B]}
    return metric


def sau1g_cd(require_document_list, use_case_document_list):
    A = sau1g_cd_A(require_document_list, use_case_document_list)
    B = sau1g_cd_B(require_document_list)

    X = template_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric


def sau2s_cd(require_document_list, use_case_document_list):
    A = sau2s_cd_A(require_document_list, use_case_document_list)
    B = sau2s_cd_B(require_document_list)

    X = template_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric


def mmo1g_cd():
    A = mmo1g_cd_A()
    B = mmo1g_cd_B()

    X = template_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric


def mmo2s_cd(require_document_list):
    Xi, template, development_value = mmo2s_cd_Xi(require_document_list)  # 提取阈值
    A = mmo2s_cd_A()
    B = mmo2s_cd_B()

    X = template_one_A_over_B_num(A, B)
    try:
        metric = {'val': Xi['val'][0], 'sub': [A, B]}
    except:
        metric = {'val': None, 'sub': [A, B]}
    return metric


def mre1g_cd():
    A = mre1g_cd_A()
    B = mre1g_cd_B()

    X = template_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric


def mre2s_cd(require_document_list, use_case_document_list):
    A = mre2s_cd_A(require_document_list, use_case_document_list)
    B = mre2s_cd_B()

    X = template_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric


def man1g_cd(require_document_list, use_case_document_list):
    A = man1g_cd_A(require_document_list, use_case_document_list)
    B = man1g_cd_B(require_document_list, use_case_document_list)

    X = template_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric


def man2s_cd(require_document_list, use_case_document_list):
    A = man2s_cd_A(require_document_list, use_case_document_list)
    B = man2s_cd_B(require_document_list)

    X = template_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric


def man3s_cd(require_document_list, use_case_document_list):
    A = man3s_cd_A(require_document_list, use_case_document_list)
    B = man3s_cd_B(require_document_list)

    X = template_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric


def mmd1g_cd(require_document_list, mission_document_list):
    Ai = mmd1g_cd_Ai(require_document_list, mission_document_list)
    Bi = mmd1g_cd_Bi(require_document_list, mission_document_list)
    n = mmd1g_cd_n(require_document_list)

    X = template_A_over_B_over_n(Ai, Bi, n)
    metric = {'val': X, 'sub': Ai + Bi + [n]}
    return metric


def mmd2g_cd(require_document_list, use_case_document_list):
    A = mmd2g_cd_A(require_document_list, use_case_document_list)
    B = mmd2g_cd_B(require_document_list)

    X = template_one_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric


def mmd3s_cd(require_document_list):
    A = mmd3s_cd_A(require_document_list)
    B = mmd3s_cd_B(require_document_list)

    X = template_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric


def mte1g_cd(require_document_list, use_case_document_list):
    A = mte1g_cd_A(require_document_list, use_case_document_list)
    B, template, development_value = mte1g_cd_B(require_document_list)

    X = None
    if A:
        X = template_A_over_B_Threshold(A[0]['val'], B, template)
    metric = {'val': X, 'sub': A + [B]}
    return metric


def mte2s_cd(use_case_document_list):
    A = mte2s_cd_A(use_case_document_list)
    B = mte2s_cd_B(use_case_document_list)

    X = template_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric


def mte3s_cd(use_case_document_list):
    A = mte3s_cd_A(use_case_document_list)
    B = mte3s_cd_B(use_case_document_list)

    X = template_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric


def pad1g_cd(require_document_list, use_case_document_list):
    A = pad1g_cd_A(require_document_list, use_case_document_list)
    B = pad1g_cd_B(require_document_list, use_case_document_list)

    X = template_one_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric


def pad2g_cd(require_document_list, use_case_document_list):
    A = pad2g_cd_A(require_document_list, use_case_document_list)
    B = pad2g_cd_B(require_document_list, use_case_document_list)

    X = template_one_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric


def pad3s_cd(require_document_list, use_case_document_list):
    A = pad3s_cd_A(require_document_list, use_case_document_list)
    B = pad3s_cd_B(require_document_list, use_case_document_list)

    X = template_one_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric


def pin1g_cd(require_document_list, use_case_document_list):
    Ai = pin1g_cd_Ai(require_document_list, use_case_document_list)
    Bi = pin1g_cd_Bi(require_document_list, use_case_document_list)
    n = pin1g_cd_n(require_document_list)

    X = template_A_over_B_over_n(Ai, Bi, n)
    Ai.extend(Bi)
    Ai.append(n)
    metric = {'val': X, 'sub': Ai}
    return metric


def pin2g_cd(require_document_list, use_case_document_list):
    A = pin2g_cd_A(require_document_list, use_case_document_list)
    B, template, development_value = pin2g_cd_B(require_document_list)

    X = None
    if A:
        X = template_A_over_B_Threshold(A[0]['val'], B, template)
    metric = {'val': X, 'sub': A + [B]}
    return metric


def pre1g_cd(require_document_list, use_case_document_list):
    A = pre1g_cd_A(require_document_list, use_case_document_list)
    B = pre1g_cd_B(require_document_list)

    X = template_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric


def pre2s_cd(require_document_list, use_case_document_list):
    A = pre2s_cd_A(require_document_list, use_case_document_list)
    B = pre2s_cd_B(require_document_list)

    X = template_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric


def pre3s_cd(require_document_list, use_case_document_list):
    A = pre3s_cd_A(require_document_list, use_case_document_list)
    B = pre3s_cd_B(require_document_list)

    X = template_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric

def pre4s_cd(require_document_list, use_case_document_list):
    A = pre4s_cd_A(require_document_list, use_case_document_list)
    B = pre4s_cd_B(require_document_list)

    X = template_A_over_B_num(A, B)
    metric = {'val': X, 'sub': [A, B]}
    return metric