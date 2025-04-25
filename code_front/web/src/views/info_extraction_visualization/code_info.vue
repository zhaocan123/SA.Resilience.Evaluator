<template>
    <div>
        <el-button style="position: absolute; right: 2vw; z-index: 3;" type="primary" @click="dialogPdfVisible = true">打印</el-button>

        <el-tabs type="card" v-model="activeName" @tab-click="handleClick">
            <el-tab-pane label="C信息" name="c_info"
                v-if="this.$store.state.current_project.projectType == 0 || this.$store.state.current_project.projectType == 2">
            </el-tab-pane>
            <el-tab-pane label="C++信息" name="c_plus_info"
                v-if="this.$store.state.current_project.projectType == 1 || this.$store.state.current_project.projectType == 2">
            </el-tab-pane>
            <div>
                <div class="cards">
                    <el-card class="card" shadow="hover">
                        <div slot="header" style="font-weight: bolder;font-size:calc(100vw * 16 / 1920);">
                            <span>{{ mainInfo.fileType }}</span>
                        </div>
                        <div class="card-item">
                            <el-row style="font-size:calc(100vw * 13 / 1920); color: rgb(244, 70, 163);">
                                <el-col :span="12">
                                    <div style="text-align: left;">{{ mainInfo.fileProp_k }}</div>
                                </el-col>
                                <el-col :span="12">
                                    <div style="text-align: right;">{{ mainInfo.fileProp }}</div>
                                </el-col>
                            </el-row>
                        </div>
                        <div class="card-item">
                            <el-row style="font-size:calc(100vw * 13 / 1920); color: rgb(244, 70, 163);">
                                <el-col :span="12">
                                    <div style="text-align: left;">{{ mainInfo.totalNum_k }}</div>
                                </el-col>
                                <el-col :span="12">
                                    <div style="text-align: right;">{{ mainInfo.totalNum }}</div>
                                </el-col>
                            </el-row>
                        </div>
                    </el-card>
                    <el-card class="card" shadow="hover" v-for="(card, index) in cardInfo" :key="index">
                        <div slot="header" style="font-weight: bolder;font-size:calc(100vw * 16 / 1920);">
                            <span>{{ card.title }}</span>
                        </div>
                        <div class="card-item">
                            <el-row style="font-size:calc(100vw * 13 / 1920); color: rgb(244, 70, 163);">
                                <el-col :span="12">
                                    <div style="text-align: left;">{{ card.key1 }}</div>
                                </el-col>
                                <!--    <el-col :span="12">
                                    <div style="text-align: right;">{{ card.val1 }}</div>
                                </el-col> -->
                            </el-row>
                        </div>
                        <div class="card-item">
                            <el-row style="font-size:calc(100vw * 13 / 1920); color: rgb(244, 70, 163);">
                                <el-col :span="12">
                                    <div style="text-align: left;">{{ card.msg }}</div>
                                </el-col>
                                <el-col :span="12">
                                    <div style="text-align: right;">{{ card.val1 }}</div>
                                </el-col>
                            </el-row>
                        </div>
                        <div class="card-item">
                            <el-row style="font-size:calc(100vw * 13 / 1920);">
                                <el-col :span="12">
                                    <div>{{ card.key2 }}</div>
                                </el-col>
                                <el-col :span="12">
                                    <div style="text-align: right;">{{ card.val2 }}</div>
                                </el-col>
                            </el-row>
                        </div>
                        <div class="card-item" style="font-size:calc(100vw * 13 / 1920);">
                            <el-row>
                                <el-col :span="12">
                                    <div>{{ card.key3 }}</div>
                                </el-col>
                                <el-col :span="12">
                                    <div style="text-align: right;">{{ card.val3 }}</div>
                                </el-col>
                            </el-row>
                        </div>
                    </el-card>
                </div>
                <div style="padding: 0 1vw 0 1vw">
                    <span style="margin-left: 1vw; margin-right: 1vw;">文件选择</span>
                    <el-select v-if="activeName == 'c_info'" v-model="selectedFilePath1" @change="selectFile"
                        placeholder="请选择文件">
                        <el-option v-for="item in filePathList" :key="item" :label="item" :value="item">
                        </el-option>
                    </el-select>
                    <el-select v-else v-model="selectedFilePath2" @change="selectFile" placeholder="请选择文件">
                        <el-option v-for="item in filePathList" :key="item" :label="item" :value="item">
                        </el-option>
                    </el-select>
                    <el-table v-loading="loading" style="margin-top: 2vh;" height="50vh" :data="tableData" border
                        :header-cell-style="()=>{return 'background: rgb(182, 254, 230);color:black;'}">
                        <el-table-column v-for="(item, index) in tableHeader" :key="index" :prop="item.prop"
                            :label="item.label" align="center">
                        </el-table-column>
                    </el-table>
                </div>
            </div>
        </el-tabs>

        <el-dialog class="scroll_none" title="打印预览" top="2vh" :visible.sync="dialogPdfVisible" width="60vw" center>
            <pdf_project_info v-if="dialogPdfVisible" ref="print" style="height: 70vh; margin: 0 auto; overflow-y: scroll;"></pdf_project_info>
            <span slot="footer" class="dialog-footer">
                <el-button @click="dialogPdfVisible = false">取 消</el-button>
                <el-button type="primary" @click="goPrint">打 印</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
import utils from '@/utils/utils'
import Cache from "@/utils/cache"
import pdf_project_info from "@/views/pdf_template/pdf_project_info.vue"

export default {
    components: {
        pdf_project_info
    },
    data() {
        return {
            activeName: this.$store.state.current_project.projectType != 1 ? "c_info" : "c_plus_info",
            mainInfo: {
                fileType: ".c",
                fileProp_k: "C文件占比",
                fileProp: "",
                totalNum_k: "函数总数",
                totalNum: ""
            },
            cardInfo: [],
            filePathList: [],
            selectedFilePath1: null,
            selectedFilePath2: null,
            tableHeader: [],
            tableData: [],
            loading: false,
            dialogPdfVisible: false
        }
    },
    mounted() {
        this.getData()
    },
    methods: {
        getData() {
            let _this = this
            utils.axiosMethod({
                method: "GET",
                url: window.ipConfig.baseUrl + "/codeInfo/" + _this.$store.state.current_project.name,
                callback: (response)=>{
                    let data = response.data
                    Cache.setCache("project_code_info", data)
                    if(_this.activeName == "c_info") {
                        _this.mainInfo = {
                            fileType: ".c",
                            fileProp_k: "C文件占比",
                            fileProp: data[_this.activeName].cFileProp,
                            totalNum_k: "函数总数",
                            totalNum: data[_this.activeName].funcTotal
                        }
                        _this.filePathList = data[_this.activeName].filePathList
                        _this.cardInfo = []
                        _this.cardInfo.push({
                            title: "最大行数函数",
                            key1: data[_this.activeName].functionLine.maxLineFunc,
                            msg: "行数",
                            val1: data[_this.activeName].functionLine.maxLine + "行",
                            key2: "平均行数",
                            val2: data[_this.activeName].functionLine.avgLine.toFixed(2) + "行",
                            key3: "最小行数",
                            val3: data[_this.activeName].functionLine.minLine + "行"
                        })
                        _this.cardInfo.push({
                            title: "最大行数文件",
                            key1: data[_this.activeName].fileLine.maxLineFile,
                            msg: "行数",
                            val1: data[_this.activeName].fileLine.maxLine + "行",
                            key2: "平均行数",
                            val2: data[_this.activeName].fileLine.avgLine.toFixed(2) + "行",
                            key3: "最小行数",
                            val3: data[_this.activeName].fileLine.minLine + "行"
                        })
                        _this.cardInfo.push({
                            title: "包含函数最多的文件",
                            key1: data[_this.activeName].defineFuncFile.maxFuncFile,
                            msg: "包含函数",
                            val1: data[_this.activeName].defineFuncFile.maxFunc + "个",
                            key2: "平均包含函数",
                            val2: data[_this.activeName].defineFuncFile.avgFunc.toFixed(2) + "个",
                            key3: "最小包含函数",
                            val3: data[_this.activeName].defineFuncFile.minFunc + "个"
                        })

                        _this.tableHeader = [
                            {
                                prop: "funcName",
                                label: "函数名"
                            },
                            {
                                prop: "returnVal",
                                label: "返回值"
                            },
                            {
                                prop: "params",
                                label: "参数"
                            },
                            {
                                prop: "outDegree",
                                label: "出度"
                            },
                            {
                                prop: "inDegree",
                                label: "入度"
                            },
                            {
                                prop: "filePath",
                                label: "文件位置"
                            },
                        ]
                        _this.filePathList = data[_this.activeName].filePathList
                    }
                    else {
                        _this.mainInfo = {
                            fileType: ".cpp",
                            fileProp_k: "Cpp文件占比",
                            fileProp: data[_this.activeName].cppFileProp,
                            totalNum_k: "类总数",
                            totalNum: data[_this.activeName].classTotal
                        }
                        _this.filePathList = data[_this.activeName].filePathList
                        _this.cardInfo = []
                        _this.cardInfo.push({
                            title: "包含最多成员的类",
                            key1: data[_this.activeName].classMember.maxMemberClass,
                            msg: "包含成员数",
                            val1: data[_this.activeName].classMember.maxMember + "个",
                            key2: "平均包含成员数",
                            val2: data[_this.activeName].classMember.avgMember.toFixed(2) + "个",
                            key3: "最小包含成员数",
                            val3: data[_this.activeName].classMember.minMember + "个"
                        })
                        _this.cardInfo.push({
                            title: "最大行数文件",
                            key1: data[_this.activeName].fileLine.maxLineFile,
                            msg: "行数",
                            val1: data[_this.activeName].fileLine.maxLine + "行",
                            key2: "平均行数",
                            val2: data[_this.activeName].fileLine.avgLine.toFixed(2) + "行",
                            key3: "最小行数",
                            val3: data[_this.activeName].fileLine.minLine + "行"
                        })
                        _this.cardInfo.push({
                            title: "包含类最多的文件",
                            key1: data[_this.activeName].defineClassFile.maxClassFile,
                            msg: "包含类数",
                            val1: data[_this.activeName].defineClassFile.maxClass + "个",
                            key2: "平均包含类数",
                            val2: data[_this.activeName].defineClassFile.avgClass.toFixed(2) + "个",
                            key3: "最小包含类数",
                            val3: data[_this.activeName].defineClassFile.minClass + "个"
                        })

                        _this.tableHeader = [
                            {
                                prop: "className",
                                label: "类名"
                            },
                            {
                                prop: "memberVariable",
                                label: "成员变量"
                            },
                            {
                                prop: "memberFunc",
                                label: "成员方法"
                            },
                            {
                                prop: "superClass",
                                label: "父类"
                            },
                            {
                                prop: "outDegree",
                                label: "出度"
                            },
                            {
                                prop: "inDegree",
                                label: "入度"
                            },
                            {
                                prop: "filePath",
                                label: "文件位置"
                            },
                        ]
                        _this.filePathList = data[_this.activeName].filePathList
                    }
                },
                catch: (err) => {
                    _this.$message.error("获取异常")
                }
            })
            
        },
        handleClick(){
            this.getData()
        },
        selectFile(file){
            this.loading = true
            let _this = this
            utils.axiosMethod({
                method: "GET",
                url: window.ipConfig.baseUrl + "/codeInfo/fileAnalyse/" + _this.$store.state.current_project.name,
                params: {
                    "selectFile": file,
                    "type": _this.activeName
                },
                callback: (response)=>{
                    _this.tableData = response.data
                    _this.loading = false
                }
            })
        },
        goPrint() {
            this.$print(this.$refs.print)
            this.dialogPdfVisible = false
        }
    }
}
</script>

<style scoped>
.cards {
    height: 40%;
    width: 100%;
    display: flex;
    flex-flow: wrap;
}

.card {
    /* height: 40%; */
    width: 23%;
    margin-left: 1%;
    margin-right: 1%;
    margin-bottom: 1%;
}

.card-item {
    font-size: calc(100vw * 15 / 1920);
    margin-bottom: 2%;
}
</style>