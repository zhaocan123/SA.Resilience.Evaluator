"""
代码解析+设计恢复
"""
import CodeInfoExtract
import BuildCG


def codeParse(path):
    """
    测试代码解析+设计恢复
    """
    # 代码解析
    CodeInfoExtract.main(path)

    # 调用图，控制流图，计算坏味
    BuildCG.BUILDCG_main(path)


if __name__ == "__main__":

    project_path = r"E:/CPP_master/dev0807/CPP_support/uploads/2222222222/code/code/"
    codeParse(project_path)
