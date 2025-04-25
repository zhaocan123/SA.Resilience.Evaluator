# 层析分析法
import numpy as np
RILIST = [0, 0, 0.58, 0.9, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49, 1.52, 1.54, 1.56, 1.58, 1.59]
np.seterr(divide='ignore', invalid='ignore')


class AHD:
    # 层次分析法
    def __init__(self, matrix):
        self.matrix = matrix
        # 矩阵大小
        self.n = len(matrix)

        # 初始化RI，用于一致性检验
        self.RI = RILIST[self.n]

        # 获取矩阵的特征值和特征向量
        self.eigenvalue, self.eigenvector = np.linalg.eig(self.matrix)

        # 获取最大特征值
        self.maxEigenvalue = np.max(self.eigenvalue)

        # 获取最大特征值对应的特征向量
        self.maxEigenvector = self.eigenvector[:, self.eigenvalue.argmax()]

        # 计算矩阵的一致性指标CI
        self.CI = (self.maxEigenvalue - self.n) / (self.n - 1)

        # 计算矩阵的一致性比率CR
        self.CR = self.CI / self.RI

    # 一致性检验
    def isConsistent(self):
        if self.n <= 2:
            return True
        else:
            if self.CR < 0.1:
                return True
            else:
                return False

    # 特征值法计算权重
    def getWeight(self):
        return self.maxEigenvector / np.sum(self.maxEigenvector)


def cal_weight(matrix):
    ahd = AHD(matrix)
    if ahd.isConsistent():
        return ahd.getWeight().real.round(4)
    else:
        return None


def cal_values(value_dict, weight_dict):
    res_value = {}
    for k, v in value_dict.items():
        for k2, v2 in v.items():
            for k3, v3 in v2.items():
                res_value[k3] = v3
    for k, v in value_dict.items():
        for k2, v2 in v.items():
            weights = weight_dict[k2]
            if len(weights["data"]) == 1:
                res_value[k2] = res_value[weights["index"][0]]
                continue
            res_weights = cal_weight(np.array(weights["data"]))
            if res_weights is None:
                return k2
            res = sum([res_value[weights["index"][i]] * res_weights[i] for i in range(len(res_weights))])
            res_value[k2] = res
    for k, v in value_dict.items():
        weights = weight_dict[k]
        if len(weights["data"]) == 1:
            res_value[k] = res_value[weights["index"][0]]
            continue
        res_weights = cal_weight(np.array(weights["data"]))
        if res_weights is None:
            return k
        res = sum([res_value[weights["index"][i]] * res_weights[i] for i in range(len(res_weights))])
        res_value[k] = res
    return res_value


if __name__ == "__main__":
    value_dict = {
        "性能效率": {
            "容量": {
                "事务处理容量": 1,
                "用户访问量": 2,
                "用户访问增长的充分性": 3
            }
        }
    }
    weight_dict = {
        "性能效率": {
            "index": ["容量"],
            "data": [[1]]
        },
        "容量": {
            "index": ["事务处理容量", "用户访问量", "用户访问增长的充分性"],
            "data": [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
        }
    }
    # print(cal_values(value_dict, weight_dict))
