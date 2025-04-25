<template>
    <div class="pdf_main" style="width: 21cm">
        <h1 style="text-align: center;">{{ projectName }} 项目变更信息检测</h1>
        <h2>1. 系统级别变更</h2>
        <h3>1.1 软件质量指标变更详情</h3>
        <div>
            <el-table
                :data="systemLevelInfo.indexInformation"
                :header-cell-style="
                () => {return 'background: rgb(176, 238, 203);color:black;';}"
                stripe>
                <el-table-column prop="indexName" label="指标" align="center">
                </el-table-column>
                <el-table-column
                prop="versionSelected"
                :label="systemLevelInfo.versionSelected.name"
                align="center"
                >
                </el-table-column>
                <el-table-column
                prop="versionLatest"
                :label="systemLevelInfo.versionLatest.name"
                align="center"
                >
                </el-table-column>
                <el-table-column label="趋势" align="center">
                <template slot-scope="scope">
                    <span style="color: green" v-if="scope.row.trend == 1"> ⬆ </span>
                    <span style="color: red" v-else-if="scope.row.trend == 0"> ⬇ </span>
                    <span v-else> - </span>
                </template>
                </el-table-column>
                <el-table-column label="标准值" align="center">
                <template slot-scope="scope">
                    <span>
                    ({{ scope.row.minimumValue }}, {{ scope.row.maximumValue }})
                    </span>
                </template>
                </el-table-column>
                <el-table-column label="检测结果" align="center">
                <template slot-scope="scope">
                    <span v-if="scope.row.result == 1" style="color: rgb(49, 197, 76)"
                    >合格</span
                    >
                    <span v-else style="color: rgb(234, 47, 109)">不合格</span>
                </template>
                </el-table-column>
            </el-table>
        </div>
        <h3>1.2 设计质量指标变更详情</h3>
        <div>
            <el-table :data="systemLevelInfo.designInformation"
                :header-cell-style="() => { return 'background: rgb(176, 238, 203);color:black;' }"
                stripe>
                <el-table-column label="指标" align="center">
                    <template slot-scope="scope">
                        <span>{{ indexMap[scope.row.indexName] }}</span>
                    </template>
                </el-table-column>
                <el-table-column prop="versionSelected" :label="systemLevelInfo.versionSelected.name"
                    align="center">
                </el-table-column>
                <el-table-column prop="versionLatest" :label="systemLevelInfo.versionLatest.name" align="center">
                </el-table-column>
                <el-table-column label="趋势" align="center">
                    <template slot-scope="scope">
                        <span style="color: green;" v-if="scope.row.trend == 1">
                            ⬆
                        </span>
                        <span style="color: red;" v-else-if="scope.row.trend == 0">
                            ⬇
                        </span>
                        <span v-else>
                            -
                        </span>
                    </template>
                </el-table-column>
                <el-table-column label="标准值" align="center">
                    <template slot-scope="scope">
                        <span>
                            ({{ scope.row.minimumValue }}, {{ scope.row.maximumValue }})
                        </span>
                    </template>
                </el-table-column>
                <el-table-column label="检测结果" align="center">
                    <template slot-scope="scope">
                        <span v-if="scope.row.result == 1" style="color: rgb(49, 197, 76);">合格</span>
                        <span v-else style="color: rgb(234, 47, 109);">不合格</span>
                    </template>
                </el-table-column>
            </el-table>
        </div>
        <div v-if="projectType != 1">
        <h2>2. 函数级别变更</h2>
            <h3>2.1 变更概况</h3>
            <el-descriptions :column="4" size="mini" border>
                <el-descriptions-item label="项目名">{{ systemLevelCInfo.versionSelected.name }}</el-descriptions-item>
                <el-descriptions-item label="文件数">{{ systemLevelCInfo.versionSelected.fileNum }}</el-descriptions-item>
                <el-descriptions-item label="函数数">{{systemLevelCInfo.versionSelected.functionNum}}</el-descriptions-item>
                <el-descriptions-item label="代码行数">{{ systemLevelCInfo.versionSelected.codeNum }}</el-descriptions-item>
                <el-descriptions-item label="项目名">{{ systemLevelCInfo.versionLatest.name }}</el-descriptions-item>
                <el-descriptions-item label="文件数">{{ systemLevelCInfo.versionLatest.fileNum }}</el-descriptions-item>
                <el-descriptions-item label="函数数">{{ systemLevelCInfo.versionLatest.functionNum }}</el-descriptions-item>
                <el-descriptions-item label="代码行数">{{ systemLevelCInfo.versionLatest.codeNum }}</el-descriptions-item>
            </el-descriptions>
            <h3>2.2 变更详情</h3>
            <div v-for="(item, index) in Object.keys(funcMap)" :key="index">
                <h4>2.2.{{ index + 1 }} {{ funcMap[item] }} 变更</h4>
                <h5>2.2.{{ index + 1 }}.1 {{ funcMap[item] }} 变更概况</h5>
                <el-descriptions :column="6" size="mini" border>
                    <el-descriptions-item :label="`${funcMap[item]}变化的函数个数`">{{ functionLevelInfo[item].totalNum }}</el-descriptions-item>
                    <el-descriptions-item label="占比">{{ functionLevelInfo[item].totalProp }}</el-descriptions-item>
                    <el-descriptions-item :label="`${funcMap[item]}增加的函数个数`" :labelStyle="{'background': '#E1F3D8'}">{{ functionLevelInfo[item].increaseNum }}</el-descriptions-item>
                    <el-descriptions-item label="占比" :labelStyle="{'background': '#E1F3D8'}">{{ functionLevelInfo[item].increaseProp }}</el-descriptions-item>
                    <el-descriptions-item :label="`${funcMap[item]}降低的函数个数`" :labelStyle="{'background': '#FDE2E2'}">{{ functionLevelInfo[item].decreaseNum }}</el-descriptions-item>
                    <el-descriptions-item label="占比" :labelStyle="{'background': '#FDE2E2'}">{{ functionLevelInfo[item].decreaseProp }}</el-descriptions-item>
                </el-descriptions>
                <h5>2.2.{{ index + 1 }}.2 {{ funcMap[item] }} 变更详情</h5>
                <el-table
                :data="functionLevelInfo[item].changeinfoList"
                :header-cell-style="()=>{return 'background: rgb(176, 238, 203);color:black;'}"
                stripe>
                    <el-table-column
                    type="index"
                    label="序号"
                    align="center">
                    </el-table-column>
                    <el-table-column
                    prop="functionPath"
                    label="函数路径"
                    align="center">
                    </el-table-column>
                </el-table>
            </div>
        </div>
        <div v-if="projectType == 1">
            <h2>2. 类级别变更</h2>
                <h3>2.1 变更概况</h3>
                <el-descriptions :column="4" size="mini" border>
                    <el-descriptions-item label="项目名">{{ systemLevelCplusInfo.versionSelected.name }}</el-descriptions-item>
                    <el-descriptions-item label="文件数">{{ systemLevelCplusInfo.versionSelected.fileNum }}</el-descriptions-item>
                    <el-descriptions-item label="类个数">{{ systemLevelCplusInfo.versionSelected.classNum }}</el-descriptions-item>
                    <el-descriptions-item label="代码行数">{{ systemLevelCplusInfo.versionSelected.codeNum }}</el-descriptions-item>
                    <el-descriptions-item label="项目名">{{ systemLevelCplusInfo.versionLatest.name }}</el-descriptions-item>
                    <el-descriptions-item label="文件数">{{ systemLevelCplusInfo.versionLatest.fileNum }}</el-descriptions-item>
                    <el-descriptions-item label="类个数">{{ systemLevelCplusInfo.versionLatest.classNum }}</el-descriptions-item>
                    <el-descriptions-item label="代码行数">{{ systemLevelCplusInfo.versionLatest.codeNum }}</el-descriptions-item>
                </el-descriptions>
                <h3>2.2 变更详情</h3>
                <div v-for="(item, index) in Object.keys(classMap)" :key="index">
                    <h4>2.2.{{ index + 1 }} {{ classMap[item] }} 变更</h4>
                    <h5>2.2.{{ index + 1 }}.1 {{ classMap[item] }} 变更概况</h5>
                    <el-descriptions :column="6" size="mini" border>
                        <el-descriptions-item :label="`${classMap[item]}变化的类个数`">{{ classLevelInfo[item].totalNum }}</el-descriptions-item>
                        <el-descriptions-item label="占比">{{ classLevelInfo[item].totalProp }}</el-descriptions-item>
                        <el-descriptions-item :label="`${classMap[item]}增加的类个数`" :labelStyle="{ 'background': '#E1F3D8' }">{{ classLevelInfo[item].increaseNum }}</el-descriptions-item>
                        <el-descriptions-item label="占比" :labelStyle="{ 'background': '#E1F3D8' }">{{ classLevelInfo[item].increaseProp }}</el-descriptions-item>
                        <el-descriptions-item :label="`${classMap[item]}降低的类个数`" :labelStyle="{ 'background': '#FDE2E2' }">{{ classLevelInfo[item].decreaseNum }}</el-descriptions-item>
                        <el-descriptions-item label="占比" :labelStyle="{ 'background': '#FDE2E2' }">{{ classLevelInfo[item].decreaseProp }}</el-descriptions-item>
                    </el-descriptions>
                    <h5>2.2.{{ index + 1 }}.2 {{ classMap[item] }} 变更详情</h5>
                    <el-table
                    :data="classLevelInfo[item].changeinfoList"
                    :header-cell-style="() => { return 'background: rgb(176, 238, 203);color:black;' }"
                    stripe>
                        <el-table-column
                        type="index"
                        label="序号"
                        align="center">
                        </el-table-column>
                        <el-table-column
                        prop="classPath"
                        label="类路径"
                        align="center">
                        </el-table-column>
                    </el-table>
                </div>
            </div>
        <div v-if="projectType == 2">
        <h2>3. 类级别变更</h2>
            <h3>3.1 变更概况</h3>
            <el-descriptions :column="4" size="mini" border>
                <el-descriptions-item label="项目名">{{ systemLevelCplusInfo.versionSelected.name }}</el-descriptions-item>
                <el-descriptions-item label="文件数">{{ systemLevelCplusInfo.versionSelected.fileNum }}</el-descriptions-item>
                <el-descriptions-item label="类个数">{{systemLevelCplusInfo.versionSelected.classNum}}</el-descriptions-item>
                <el-descriptions-item label="代码行数">{{ systemLevelCplusInfo.versionSelected.codeNum }}</el-descriptions-item>
                <el-descriptions-item label="项目名">{{ systemLevelCplusInfo.versionLatest.name }}</el-descriptions-item>
                <el-descriptions-item label="文件数">{{ systemLevelCplusInfo.versionLatest.fileNum }}</el-descriptions-item>
                <el-descriptions-item label="类个数">{{ systemLevelCplusInfo.versionLatest.classNum }}</el-descriptions-item>
                <el-descriptions-item label="代码行数">{{ systemLevelCplusInfo.versionLatest.codeNum }}</el-descriptions-item>
            </el-descriptions>
            <h3>3.2 变更详情</h3>
            <div v-for="(item, index) in Object.keys(classMap)" :key="index">
                <h4>3.2.{{ index + 1}} {{ classMap[item] }} 变更</h4>
                <h5>3.2.{{ index + 1 }}.1 {{ classMap[item] }} 变更概况</h5>
                <el-descriptions :column="6" size="mini" border>
                    <el-descriptions-item :label="`${classMap[item]}变化的类个数`">{{ classLevelInfo[item].totalNum }}</el-descriptions-item>
                    <el-descriptions-item label="占比">{{ classLevelInfo[item].totalProp }}</el-descriptions-item>
                    <el-descriptions-item :label="`${classMap[item]}增加的类个数`" :labelStyle="{'background': '#E1F3D8'}">{{ classLevelInfo[item].increaseNum }}</el-descriptions-item>
                    <el-descriptions-item label="占比" :labelStyle="{'background': '#E1F3D8'}">{{ classLevelInfo[item].increaseProp }}</el-descriptions-item>
                    <el-descriptions-item :label="`${classMap[item]}降低的类个数`" :labelStyle="{'background': '#FDE2E2'}">{{ classLevelInfo[item].decreaseNum }}</el-descriptions-item>
                    <el-descriptions-item label="占比" :labelStyle="{'background': '#FDE2E2'}">{{ classLevelInfo[item].decreaseProp }}</el-descriptions-item>
                </el-descriptions>
                <h5>3.2.{{ index + 1 }}.2 {{ classMap[item] }} 变更详情</h5>
                <el-table
                :data="classLevelInfo[item].changeinfoList"
                :header-cell-style="()=>{return 'background: rgb(176, 238, 203);color:black;'}"
                stripe>
                    <el-table-column
                    type="index"
                    label="序号"
                    align="center">
                    </el-table-column>
                    <el-table-column
                    prop="classPath"
                    label="类路径"
                    align="center">
                    </el-table-column>
                </el-table>
            </div>
        </div>
        <el-backtop target=".pdf_main" :right="250" :bottom="60"></el-backtop>
    </div>
</template>

<script>
import Cache from '@/utils/cache';
export default {
    data() {
        return {
            projectName: this.$store.state.current_project.name,
            projectType: this.$store.state.current_project.projectType,
            systemLevelInfo: null,
            systemLevelCInfo: null,
            systemLevelCplusInfo: null,
            indexMap: {
                "modifiability": "可修改性",
                "scalability": "可扩展性",
                "testability": "易测试性",
                "refundability": "可替换性",
                "comprehensibility": "易理解性"
            },
            functionLevelInfo: null,
            funcMap: {
                "paramNum": "参数个数",
                "variableNum": "变量个数",
                "cyclomaticComplexity": "圈复杂度",
                "codeNum": "代码行",
                "outDegree": "出度",
                "inDegree": "入度"
            },
            classLevelInfo: null,
            classMap: {
                "memberVariableNum": "成员变量个数",
                "memberFunctionNum": "成员方法个数",
                "classNum":"基类个数", 
                "outDegree":"出度",
                "inDegree":"入度"
            }
        }
    },
    mounted() {
        let data = Cache.getCache("change_information_detection_data")
        console.log("data", data);

        if(this.projectType != 1) {
            this.systemLevelInfo = data.c_info.systemLevel
            this.systemLevelCInfo = data.c_info.systemLevel
            this.functionLevelInfo = data.c_info.functionLevel

        }
        if (this.projectType != 0) {
            this.systemLevelInfo = data.c_plus_info.systemLevel
            this.systemLevelCplusInfo = data.c_plus_info.systemLevel
            this.classLevelInfo = data.c_plus_info.classLevel
        }
    }
};
</script>

<style scoped>

</style>