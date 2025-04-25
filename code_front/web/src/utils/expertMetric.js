export default {
    data: [{
        "des": "这是设计指标的描述和公式",
        "metrics": [
            {
                "name": "可修改性",
                "des": "该指标用于描述对设计进行修改的难度，特指对设计改正和改进活动实施的难度，指标值越高，实施难度越低。",
                "formula": "\\begin{equation} \\begin{aligned} X = 1- \\frac{\\sum_{i=1}^N \\frac{FOD_i + FID_i}{N} + \\sum_{j=1}^M \\frac{COD_j + CID_j}{M}}{N + M} \\end{aligned} \\end{equation}",
                "factors": [
                    "`FOD_i=函数i的出度`",
                    "`FID_i=函数i的入度`",
                    "`N=设计中函数的数量`",
                    "`COD_j=类j的出度`",
                    "`CID_j=类j的入度`",
                    "`M=设计中类的数量`"
                ]
            },
            {
                "name": "可扩展性",
                "des": "该指标度量的是对设计进行扩展的难度，指标值越高，扩展难度越低。",
                "formula": "\\begin{equation} \\begin{aligned} X = \\frac{N_{API} + M_{API}}{N + M} \\end{aligned} \\end{equation}",
                "factors": [
                    "`N_{API}=设计中函数接口的数量`",
                    "`N=设计中函数的数量`",
                    "`M_{API}=设计中接口类的数量`",
                    "`M=设计中类的数量`"
                ]
            },
            {
                "name": "易测试性",
                "des": "该指标度量对该软件设计进行测试的难度，指标值越高，测试难度越小。",
                "formula": "\\begin{equation} \\begin{aligned} X = 1- \\frac{\\sum_{i=1}^N \\frac{FOD_i}{N} + \\sum_{j=1}^M \\frac{COD_j}{M}}{N + M} \\end{aligned} \\end{equation}",
                "factors": [
                    "`FOD_i=函数i的出度`",
                    "`N=设计中函数的数量`",
                    "`COD_j=类j的出度`",
                    "`M=设计中类的数量`"
                ]
            },
            {
                "name": "可替换性",
                "des": "该指标度量设计中的函数和类被具有相似功能的函数和类替换的难度，以及删除特定功能函数和类的难度，指标值越高，替换/删除难度越小。",
                "formula": "\\begin{equation} \\begin{aligned} X &= \\frac{\\sum_{i=1}^N{R_i} + \\sum_{j=1}^M{Rc_j}}{N + M} \\\\ R_i &= \\frac{1}{1 + FID_i} \\\\ Rc_j &= \\frac{1}{1 + CID_j} \\end{aligned} \\end{equation}",
                "factors": [
                    "`R_i=函数i的可替换性`",
                    "`FID_i=函数i的入度`",
                    "`N=设计中函数的数量`",
                    "`Rc_j=类j的可替换性`",
                    "`CID_j=类j的入度`",
                    "`M=设计中类的数量`"
                ]
            },
            {
                "name": "易理解性",
                "des": "该指标度量的是开发人员对于设计和现有工程文件理解的难易程度，指标值越高，设计和工程文件越易于理解，越利于开发人员开展演进活动。",
                "formula": "\\begin{equation} \\begin{aligned} X = \\frac{N_{comment} + M_{comment}}{N + M} \\end{aligned} \\end{equation}",
                "factors": [
                    "`N_{comment}=包含注释的函数的数量`",
                    "`N=设计中函数的数量`",
                    "`M_{comment}=包含注释的类的数量`",
                    "`M=设计中类的数量`"
                ]
            },
            // {
            //     "name": "坏味道率",
            //     "des": "该指标度量的是设计和实现过程中出现坏味道的频率，指标值越高，因设计缺陷或不良编码习惯而引入程序的、导致深层次质量问题越少。",
            //     "formula": "\\begin{equation} \\begin{aligned} X = 1 - \\frac{N_{bad}}{N} \\end{aligned} \\end{equation}",
            //     "factors": [
            //         "`N_{bad}=存在坏味道的函数数量`",
            //         "`N=设计中函数的数量`"
            //     ]
            // }
        ]
    }]
}