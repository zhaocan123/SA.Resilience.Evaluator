<template>
    <div>
        <div class="el-description">
            <el-descriptions :column="4" size="mini" border>
                <el-descriptions-item label="项目名">{{ systemLevelInfo.versionSelected.name }}</el-descriptions-item>
                <el-descriptions-item label="文件数">{{ systemLevelInfo.versionSelected.fileNum }}</el-descriptions-item>
                <el-descriptions-item :label="typeName == 'c_info' ? '函数数' : '类个数'">{{ typeName == 'c_info' ?
                    systemLevelInfo.versionSelected.functionNum : systemLevelInfo.versionSelected.classNum
                }}</el-descriptions-item>
                <el-descriptions-item label="代码行数">{{ systemLevelInfo.versionSelected.codeNum }}</el-descriptions-item>
                <el-descriptions-item label="项目名">{{ systemLevelInfo.versionLatest.name }}</el-descriptions-item>
                <el-descriptions-item label="文件数">{{ systemLevelInfo.versionLatest.fileNum }}</el-descriptions-item>
                <el-descriptions-item :label="typeName == 'c_info' ? '函数数' : '类个数'">{{ typeName == 'c_info' ?
                    systemLevelInfo.versionLatest.functionNum : systemLevelInfo.versionLatest.classNum
                }}</el-descriptions-item>
                <el-descriptions-item label="代码行数">{{ systemLevelInfo.versionLatest.codeNum }}</el-descriptions-item>
            </el-descriptions>
        </div>
        <el-tabs tab-position="left" v-model="activeName">
            <el-tab-pane label="软件质量" name="software">
                <div class="el-table">
                    <el-table :data="systemLevelInfo.indexInformation"
                        :header-cell-style="() => { return 'background: rgb(176, 238, 203);color:black;' }" height="58vh"
                        stripe>
                        <el-table-column prop="indexName" label="指标" align="center">
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
                        <el-table-column label="设置标准值" align="center">
                            <template slot-scope="scope">
                                <el-button type="primary" size="mini" @click="handleEdit(scope.row)" plain>编辑</el-button>
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
            </el-tab-pane>
            <el-tab-pane label="设计质量" name="design">
                <div class="el-table">
                    <el-table :data="systemLevelInfo.designInformation"
                        :header-cell-style="() => { return 'background: rgb(176, 238, 203);color:black;' }" height="58vh"
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
                        <el-table-column label="设置标准值" align="center">
                            <template slot-scope="scope">
                                <el-button type="primary" size="mini" @click="handleEdit(scope.row)" plain>编辑</el-button>
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
            </el-tab-pane>
        </el-tabs>

        <el-dialog title="设置标准值" :visible.sync="dialogFormVisible">
            <el-form v-model="fromData">
                <el-form-item label="下界">
                    <el-input v-model="fromData.minimumValue" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="上界">
                    <el-input v-model="fromData.maximumValue" autocomplete="off"></el-input>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click="dialogFormVisible = false">取 消</el-button>
                <el-button v-if="activeName == 'software'" type="primary" @click="handleFromSub">确 定</el-button>
                <el-button v-else type="primary" @click="handleFromSubDesign">确 定</el-button>
            </div>
        </el-dialog>
    </div>
</template>

<script>
import Cache from "@/utils/cache"
export default {
    props: ["typeName"],
    watch: {
        typeName(newVal) {
            this.typeName = newVal
            this.getData()
        }
    },
    data() {
        return {
            activeName: "software",
            systemLevelInfo: null,
            dialogFormVisible: false,
            selectedRow: null,
            fromData: {
                minimumValue: 0,
                maximumValue: 1
            },
            indexMap: {
                "modifiability": "可修改性",
                "scalability": "可扩展性",
                "testability": "易测试性",
                "refundability": "可替换性",
                "comprehensibility": "易理解性"
            }
        }
    },
    mounted() {
        this.getData()
        for(let index in this.systemLevelInfo.indexInformation) {
            this.systemLevelInfo.indexInformation[index]["minimumValue"] = 0
            this.systemLevelInfo.indexInformation[index]["maximumValue"] = 1
            // this.systemLevelInfo.indexInformation[index]["standardValue"] = "(0, 1)"
        }
    },
    methods: {
        getData() {
            let data = Cache.getCache("change_information_detection_data")
            // console.log("######", data);
            if (this.typeName == "c_info") {
                this.systemLevelInfo = data.c_info.systemLevel
            }
            else {
                this.systemLevelInfo = data.c_plus_info.systemLevel
            }
        },
        handleEdit(row) {
            // console.log(row);
            this.selectedRow = row;
            this.fromData.minimumValue = row.minimumValue
            this.fromData.maximumValue = row.maximumValue
            this.dialogFormVisible = true
        },
        handleFromSub() {
            this.dialogFormVisible = false
            let minimumValue = parseFloat(this.fromData.minimumValue)
            let maximumValue = parseFloat(this.fromData.maximumValue)
            if (!(!isNaN(minimumValue) && isFinite(this.fromData.minimumValue)) || !(!isNaN(maximumValue) && isFinite(this.fromData.maximumValue))) {
                this.$message.error("输入值非法")
                return
            }
            if (minimumValue >= maximumValue) {
                this.$message.error("输入值非法")
                return
            }
            if (this.selectedRow != null) {
                let minimumValue = this.fromData.minimumValue
                let maximumValue = this.fromData.maximumValue
                for (let index in this.systemLevelInfo.indexInformation) {
                    if (this.systemLevelInfo.indexInformation[index].indexName == this.selectedRow.indexName) {
                        this.systemLevelInfo.indexInformation[index].minimumValue = minimumValue
                        this.systemLevelInfo.indexInformation[index].maximumValue = maximumValue
                        if (this.systemLevelInfo.indexInformation[index].versionSelected > minimumValue
                            && this.systemLevelInfo.indexInformation[index].versionSelected < maximumValue
                            && this.systemLevelInfo.indexInformation[index].versionLatest > minimumValue
                            && this.systemLevelInfo.indexInformation[index].versionLatest < maximumValue) {
                            this.systemLevelInfo.indexInformation[index]["result"] = 1
                        } else {
                            this.systemLevelInfo.indexInformation[index]["result"] = 0
                        }
                        return
                    }
                }
            }
        },
        handleFromSubDesign() {
            this.dialogFormVisible = false
            let minimumValue = parseFloat(this.fromData.minimumValue)
            let maximumValue = parseFloat(this.fromData.maximumValue)
            if (!(!isNaN(minimumValue) && isFinite(this.fromData.minimumValue)) || !(!isNaN(maximumValue) && isFinite(this.fromData.maximumValue))) {
                this.$message.error("输入值非法")
                return
            }
            if (minimumValue >= maximumValue) {
                this.$message.error("输入值非法")
                return
            }
            if (this.selectedRow != null) {
                let minimumValue = this.fromData.minimumValue
                let maximumValue = this.fromData.maximumValue
                for (let index in this.systemLevelInfo.designInformation) {
                    if (this.systemLevelInfo.designInformation[index].indexName == this.selectedRow.indexName) {
                        this.systemLevelInfo.designInformation[index].minimumValue = minimumValue
                        this.systemLevelInfo.designInformation[index].maximumValue = maximumValue
                        if (this.systemLevelInfo.designInformation[index].versionSelected > minimumValue
                            && this.systemLevelInfo.designInformation[index].versionSelected < maximumValue
                            && this.systemLevelInfo.designInformation[index].versionLatest > minimumValue
                            && this.systemLevelInfo.designInformation[index].versionLatest < maximumValue) {
                            this.systemLevelInfo.designInformation[index]["result"] = 1
                        } else {
                            this.systemLevelInfo.designInformation[index]["result"] = 0
                        }
                        return
                    }
                }
            }
        }
    }
}
</script>

<style scoped>
.el-description {
    padding-left: 5vw;
    padding-right: 5vw;
    margin-top: 5vh;
    margin-bottom: 5vh;
}

.el-table {
    width: 98%;
    margin: 0 auto;
}
</style>