import json
import re


class Advice:
    def __init__(self, threshold, function_Info):
        self.advice_out = []
        self.function_Info = function_Info
        self.threshold = threshold
        self.filterFault()

    def filterFault(self):
        functions = self.function_Info
        self.funcs = []
        for key in functions.keys():
            match = re.match("(.*):(\d+):(.*)", key)
            if match is not None:
                # print("--------")
                # print(functions[key])
                self.funcs.append((match[3],
                                   match[1],
                                   functions[key]["variableNum"],
                                   len(functions[key]["paramList"]),
                                   functions[key]["cyclComplexity"],
                                   len(functions[key]["fanIn"]),
                                   len(functions[key]["fanOut"]),
                                   functions[key]["codeInfo"]["codeLine"],
                                   functions[key]["codeInfo"]["commentLine"]))

        if self.threshold["par"] is not None:
            p = float(self.threshold["par"][0]) / 100
            num = float(self.threshold["par"][1])
            self.par = [item for item in self.funcs if item[3] > num]
            if len(self.par) / len(self.funcs) >= p:
                self.advice_out.append({
                    "num": len(self.par),
                    "suggestion": "软件中" + str(round(len(self.par) / len(self.funcs) * 100,
                                                    2)) + "%函数的参数过多,建议采用结构体传递参数，或者重新审查函数的功能独立性，对于功能不够独立的函数进行拆分。",
                    "details": [{"funcName": item[0],
                                 "info": {
                                     "paramNum": {
                                         "value": item[3],
                                         "label": "参数个数"
                                     }
                    },
                        "path": item[1]} for item in self.par]
                })
        if self.threshold["var"] is not None:
            p = float(self.threshold["var"][0]) / 100
            num = float(self.threshold["var"][1])
            self.var = [item for item in self.funcs if item[2] > num]
            if len(self.var) / len(self.funcs) >= p:
                self.advice_out.append({
                    "num": len(self.var),
                    "suggestion": "软件中" + str(round(len(self.var) / len(self.funcs) * 100,
                                                    2)) + "%函数的变量过多,建议重新审查函数的功能独立性，对于功能不够独立的函数进行拆分。",
                    "details": [{"funcName": item[0],
                                 "info": {
                                     "varNum": {
                                         "value": item[2],
                                         "label": "变量个数"
                                     }
                    },
                        "path": item[1]} for item in self.var]
                })

        if self.threshold["cir"] is not None:
            p = float(self.threshold["cir"][0]) / 100
            num = float(self.threshold["cir"][1])
            self.cir = [item for item in self.funcs if item[4] > num]
            if len(self.cir) / len(self.funcs) > p:
                self.advice_out.append({
                    "num": len(self.cir),
                    "suggestion": "易理解性和函数的圈复杂度负相关，函数圈复杂度越高则越难理解。建议降低当前软件版本中函数的复杂度以提高软件的易理解性。",
                    "details": [{"funcName": item[0],
                                 "info": {
                                     "cyclomaticComplexity": {
                                         "value": item[4],
                                         "label": "圈复杂度"
                                     }
                    }, "path": item[1]} for item in self.cir]
                })
        flag = True
        if self.threshold["out"] is not None:
            p = float(self.threshold["out"][0]) / 100
            num = float(self.threshold["out"][1])
            self.fanout = [item for item in self.funcs if item[6] > num]
            if len(self.fanout) / len(self.funcs) > p:
                flag = False
                self.advice_out.append({
                    "num": len(self.fanout),
                    "suggestion": "易测试性和函数的出度负相关，函数出度越大，测试中需要的桩模块越多，测试成本越高。建议减少函数对外调用以提高软件的易测试性。",
                    "details": [{"funcName": item[0],
                                 "info": {
                                     "fanOut": {
                                         "value": item[6],
                                         "label": "出度"
                                     }
                    }, "path": item[1]} for item in self.fanout]
                })
        if self.threshold["in"] is not None:
            p = float(self.threshold["in"][0]) / 100
            num = float(self.threshold["in"][1])
            self.fanin = [item for item in self.funcs if item[5] > num]
            if len(self.fanin) / len(self.funcs) > p:
                self.advice_out.append({
                    "num": len(self.fanin),
                    "suggestion": "可替换性和函数的入度负相关，函数入度越大，说明修改或替换该函数的难度越大。建议减少函数被调用的次数以提高软件可替换性。",
                    "details": [{"funcName": item[0],
                                 "info": {
                                     "fanIn": {
                                         "value": item[5],
                                         "label": "入度"
                                     }
                    }, "path": item[1]} for item in self.fanin]
                })
                if not flag:
                    self.advice_out.append({
                        "num": len(self.fanout) + len(self.fanout),
                        "suggestion": "可修改性和函数的出入度负相关，函数出入度越大，可修改性越差。建议通过减少函数调用及被调的次数来提高软件的可修改性。",
                        "details": [{"funcName": item[0], "info": {
                            "fanInAndOut": {
                                "value": item[5],
                                "label": "入度"
                            }
                        }, "path": item[1]} for item in self.fanin]
                        +
                        [{"funcName": item[0],
                          "info": {
                            "fanInAndOut": {
                                "value": item[6],
                                "label": "出度"
                            }
                        }, "path": item[1]} for item in self.fanout]
                    })
        self.avg_code = sum([item[7] for item in self.funcs]) / len(self.funcs)
        self.avg_over_200 = [item for item in self.funcs if item[7] > 200]
        if self.avg_code > 200:
            self.advice_out.append({
                "num": len(self.avg_over_200),
                "suggestion": "软件函数的平均规模超过200，建议合并函数中重复的代码片段或将函数依照功能进行拆分。",
                "details": [{"funcName": item[0], "info": {
                    "funcLength": {
                        "value": item[7],
                        "label": "函数规模"
                    }
                }, "path": item[1]} for item in self.avg_over_200]
            })
        self.avg_cyc = sum([item[4] for item in self.funcs]) / len(self.funcs)
        self.cyc_over80 = [item for item in self.funcs if item[4] > 80]
        self.cyc_over20 = [item for item in self.funcs if item[4] > 20]
        cyc_advice = ""
        if self.avg_cyc > 10:
            cyc_advice += "软件中函数的平均圈复杂度已超过10,"
        if len(self.cyc_over80) > 0:
            cyc_advice += "部分函数圈复杂度大于80,"
        if len(self.cyc_over20) / len(self.funcs) > 0.2:
            cyc_advice += "圈复杂度大于20的函数占比超过了函数总量的20%,"
        if len(cyc_advice) > 1:
            cyc_advice += "建议降低以下圈复杂度过高的函数的复杂度。"
            self.advice_out.append({
                "num": len(self.cyc_over80),
                "suggestion": cyc_advice,
                "details": [{"funcName": item[0],
                             "info": {
                                 "cyclomaticComplexity": {
                                     "value": item[4],
                                     "label": "圈复杂度"
                                 }
                },
                    "path": item[1]} for item in self.cyc_over80]
            })
        self.avg_comment = sum([item[8] for item in self.funcs]) / len(self.funcs)
        self.comment_below_20 = [item for item in self.funcs if item[8] < 20]
        if self.avg_comment < 20:
            self.advice_out.append({
                "num": len(self.comment_below_20),
                "suggestion": "软件注释过少，总体注释率较低，影响对软件的理解，建议增加对软件源码的注释以提高软件的易理解性。",
                "details": [{"funcName": item[0],
                             "info": {
                                 "commentLine": {
                                     "value": item[8],
                                     "label": "注释行数"
                                 }
                },
                    "path": item[1]} for item in
                    self.comment_below_20]
            })

    def getAdvice(self):
        return self.advice_out
#
