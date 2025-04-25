<template>
    <div class="container">
        <div class="main-left">
            <el-card class="box-card">
                <div slot="header" class="clearfix">
                    <span style="font-weight: bold; font-size: 18px;">设置阈值</span>
                    <el-button style="float: right; padding: 3px 0" type="text" @click="generSugesstion">生成建议</el-button>
                </div>
                <div class="file_opt">
                    <el-button slot="trigger" class="el-button" type="success" @click="importFile" plain>导入模板</el-button>
                    <el-button slot="trigger" class="el-button" type="primary" @click="exportFile" plain>导出数据</el-button>
                </div>

                <div class="title">参数个数：</div>
                <el-form :inline="true">
                    <el-form-item size="small">
                        <el-input type="number" v-model="threshold.par[0]" style="width: 5vw;"
                        oninput="if(value < 0 || value > 100) {value = 0}"
                        onblur="if(value == '' || value == null) {value = 0}"></el-input>
                        <span style="margin-left: 5px;">%</span>
                    </el-form-item>
                    <el-form-item label="函数的参数个数不超过" size="small">
                        <el-input type="number" v-model="threshold.par[1]" style="width: 5vw;"
                        oninput="value = Number(value) || 0"
                        :min="0"></el-input>
                    </el-form-item>
                </el-form>

                <div class="title">变量个数：</div>
                <el-form :inline="true">
                    <el-form-item size="small">
                        <el-input type="number" v-model="threshold.var[0]" style="width: 5vw;"
                        oninput="if(value < 0 || value > 100) {value = 0}"
                        onblur="if(value == '' || value == null) {value = 0}"></el-input>
                        <span style="margin-left: 5px;">%</span>
                    </el-form-item>
                    <el-form-item label="函数的局部变量个数不超过" size="small">
                        <el-input type="number" v-model="threshold.var[1]" style="width: 5vw;"
                        oninput="value = Number(value) || 0"
                        :min="0"></el-input>
                    </el-form-item>
                </el-form>

                <div class="title">圈复杂度：</div>
                <el-form :inline="true">
                    <el-form-item size="small">
                        <el-input type="number" v-model="threshold.cir[0]" style="width: 5vw;"
                        oninput="if(value < 0 || value > 100) {value = 0}"
                        onblur="if(value == '' || value == null) {value = 0}"></el-input>
                        <span style="margin-left: 5px;">%</span>
                    </el-form-item>
                    <el-form-item label="函数的圈复杂度不超过" size="small">
                        <el-input type="number" v-model="threshold.cir[1]" style="width: 5vw;"
                        oninput="value = Number(value) || 0"
                        :min="0"></el-input>
                    </el-form-item>
                </el-form>

                <div class="title">出度：</div>
                <el-form :inline="true">
                    <el-form-item size="small">
                        <el-input type="number" v-model="threshold.out[0]" style="width: 5vw;"
                        oninput="if(value < 0 || value > 100) {value = 0}"
                        onblur="if(value == '' || value == null) {value = 0}"></el-input>
                        <span style="margin-left: 5px;">%</span>
                    </el-form-item>
                    <el-form-item label="函数的出度不超过" size="small">
                        <el-input type="number" v-model="threshold.out[1]" style="width: 5vw;"
                        oninput="value = Number(value) || 0"
                        :min="0"></el-input>
                    </el-form-item>
                </el-form>

                <div class="title">入度：</div>
                <el-form :inline="true">
                    <el-form-item size="small">
                        <el-input type="number" v-model="threshold.in[0]" style="width: 5vw;"
                        oninput="if(value < 0 || value > 100) {value = 0}"
                        onblur="if(value == '' || value == null) {value = 0}"></el-input>
                        <span style="margin-left: 5px;">%</span>
                    </el-form-item>
                    <el-form-item label="函数的入度不超过" size="small">
                        <el-input type="number" v-model="threshold.in[1]" style="width: 5vw;"
                        oninput="value = Number(value) || 0"
                        :min="0"></el-input>
                    </el-form-item>
                </el-form>
            </el-card>
        </div>
        <div v-loading="loading" class="main-right">
            <el-button @click="dialogPdfVisible = true" type="primary" style="float: right;margin-bottom: 2%;">打印</el-button>
            <el-table height="83vh" class="total_table" :data="suggestionTable"
                :header-cell-style="() => { return 'background: antiquewhite;color:black;' }" stripe>
                <el-table-column prop="num" label="序号" type="index" align="center">
                </el-table-column>
                <el-table-column prop="suggestion" label="具体建议" align="center">
                </el-table-column>
                <el-table-column prop="details" label="详细信息" align="center">
                    <template slot-scope="scope">
                        <el-button size="mini" @click="showDetail(scope)" type="primary">详情</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </div>
        <el-dialog title="详细信息" :visible.sync="dialogFormVisible">
            <el-table class="total_table" :data="showDetails"
                :header-cell-style="() => { return 'background: rgb(240,249,235);color:black;' }" stripe>
                <el-table-column prop="funcName" label="函数名" align="center">
                </el-table-column>
                <el-table-column label="信息" align="center">
                    <template slot-scope="scope">
                        <el-tag type="warning" style="margin-right: 1px;"
                            v-for="(item, index) in Object.keys(scope.row.info)" :key="index">
                            {{ scope.row.info[item].label }} : {{ scope.row.info[item].value }}
                        </el-tag>
                    </template>
                </el-table-column>
                <el-table-column prop="path" label="所在路径" align="center">
                </el-table-column>
            </el-table>
            <div slot="footer" class="dialog-footer">
                <el-button @click="dialogFormVisible = false">取 消</el-button>
            </div>
        </el-dialog>
        <el-dialog class="scroll_none" media="print" title="打印预览" top="2vh" :visible.sync="dialogPdfVisible" width="60vw" center>
            <pdf_design_refactor_suggestion v-if="dialogPdfVisible" ref="print" style="height: 70vh; margin: 0 auto; overflow-y: scroll;"></pdf_design_refactor_suggestion>
            <span slot="footer" class="dialog-footer">
                <el-button @click="dialogPdfVisible = false">取 消</el-button>
                <el-button type="primary" @click="goPrint">打 印</el-button>
            </span>
        </el-dialog>
    </div>
</template>


<script>
import utils from '@/utils/utils';
import FileSaver from "file-saver"
import Cache from "@/utils/cache"
import pdf_design_refactor_suggestion from "@/views/pdf_template/pdf_design_refactor_suggestion.vue"
export default {
    components:{
        pdf_design_refactor_suggestion
    },
    data() {
        return {
            dialogFormVisible: false,
            suggestionTable: [],
            details: [],
            showDetails: [],
            // threshold: {
            //     paraNum: 0,
            //     paraNumMax: 0,
            //     varNum: 0,
            //     varNumMax: 0,
            //     cyclomaticComplexity: 0,
            //     cyclomaticComplexityMax: 0,
            //     outDegree: 0,
            //     outDegreeMax: 0,
            //     inDegree: 0,
            //     inDegreeMax: 0
            // },
            threshold: {
                "par":[0,0],
                "var":[0,0],
                "cir":[0,0],
                "out":[0,0],
                "in":[0,0]
            },
            loading: false,
            dialogPdfVisible: false
        }
    },
    methods: {
        goPrint() {
            this.$print(this.$refs.print)
            this.dialogPdfVisible = false
        },
        // goPdfDesignRefactorSuggestion() {
        //     this.$router.push({name:"pdf_design_refactor_suggestion"});
        // },
        getData(data) {
            this.suggestionTable = []
            this.details = []
            for (let index in data.suggestionTable) {
                let item = data.suggestionTable[index];
                this.suggestionTable.push(item);
                this.details.push(item.details);
            }
            this.loading = false
            Cache.setCache("design_refactor_suggestion_data_suggestionTable",this.suggestionTable)
            // Cache.setCache("design_refactor_suggestion_data_details",this.details)
        },
        generSugesstion(){
            this.loading = true
            let _this = this
            utils.axiosMethod({
                method: "POST",
                url: window.ipConfig.baseUrl + "/design_refactor_suggestion/" + _this.$store.state.current_project.name,
                data: _this.threshold,
                callback: (response)=>{
                    _this.getData(response.data)
                    // console.log(response.data)
                    // Cache.setCache("design_refactor_suggestion_data", response.data);
                    Cache.setCache("design_refactor_suggestion_threshold",_this.threshold)

                },
                catch: (err) => {
                    _this.$message.error("获取异常")
                }
            })
        },
        showDetail(scope) {
            this.dialogFormVisible = true;
            this.showDetails = this.details[scope.$index];
        },
        importFile(){
            let _this = this
            const inputFile = document.createElement("input")
            inputFile.type = "file"
            inputFile.style.display = "none"
            inputFile.id = "fileInput"
            // inputFile.webkitdirectory = false
            // inputFile.multiple = false
            document.body.appendChild(inputFile)
            inputFile.click()
            inputFile.addEventListener("change", function (e) {         
                let file = inputFile.files[0]
                // console.log("#########", file)
                if(file.type != "application/json") {
                    _this.$message.error("上传文件要求为json格式")
                    return
                }
                const reader = new FileReader()
                reader.readAsText(file)
                reader.onload = ()=>{
                    // console.log("文件内容", JSON.parse(reader.result))
                    let data = null
                    try {
                        data = JSON.parse(reader.result)
                    } catch(e) {
                        _this.$message.error("上传文件解析错误")
                    return
                    }
                    // 逐个字段赋值，防止json格式非法
                    for(let k in _this.threshold){
                        if(k in data){
                            _this.threshold[k] = data[k]
                        }
                    }
                }
            })
        },
        exportFile(){
            let blob = new Blob([JSON.stringify(this.threshold)], {
                type: "application/json",
            })
            let downloadName = "threshold_design_refactor_suggestion_" + new Date().getTime() + ".json";
            FileSaver.saveAs(blob, downloadName);
        }
    }
}

</script>


<style scoped>
.container {
    display: flex;
    margin-top: 25px;
}

.main-left {
    width: 32vw;
    margin-left: 15px;
}

.file_opt {
    margin-bottom: 2vh;
}

.box-card {
    width: 100%;
    height: 100%;
}

.title {
    font-size: medium;
    font-weight: bold;
    margin-bottom: 8px;
}

.main-right {
    width: 78vw;
    margin-left: 40px;
}

.item {
    display: flex;
    margin-bottom: 18px;
    align-items: center;
}

.clearfix:before,
.clearfix:after {
    display: table;
    content: "";
    clear: both;
}

/* 隐藏滚动条 */
/* .scroll_none ::-webkit-scrollbar{
    display:none;
} */
</style>