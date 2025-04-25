<template>
  <div v-loading="loading" class="container">
    <el-row>
      <el-tabs type="card" v-model="activeName1">
        <el-tab-pane label="C信息" name="c_info" v-if="projectType != 1">
            <div class="file_select">
                文件路径:
                <el-input class="el-input" placeholder="请选择文件" v-model="c_info.selectFile" clearable>
                </el-input>
                <el-button slot="trigger" class="el-button" type="primary" @click="handleSelect" plain>选择文件</el-button>
            </div>
            <div style="width: 100%;">
                <el-tabs tab-position="left">
                    <el-tab-pane label="总览信息">
                        <div>
                            <el-table
                            class="total_table"
                            :data="c_info.overviewTable"
                            :header-cell-style="()=>{return 'background: antiquewhite;color:black;'}"
                            stripe>
                                <el-table-column
                                prop="thousand_defect_num"
                                label="千行缺陷数"
                                align="center">
                                    <template slot-scope="scope">
                                        <span>{{ scope.row.thousand_defect_num }}/KLOC</span>
                                    </template>
                                </el-table-column>
                                <el-table-column
                                prop="defect_concentration"
                                label="缺陷密度"
                                align="center">
                                    <template slot-scope="scope">
                                        <span>{{ scope.row.defect_concentration }}/KLOC</span>
                                    </template>
                                </el-table-column>
                                <el-table-column
                                prop="file_defect_rate"
                                label="文件缺陷率"
                                align="center">
                                </el-table-column>
                            </el-table>
                            <el-table
                            class="total_table"
                            :data="c_info.totalTable"
                            :header-cell-style="()=>{return 'background: antiquewhite;color:black;'}"
                            stripe>
                                <el-table-column
                                prop="type"
                                align="center">
                                    <template slot-scope="scope">
                                        <span style="font-weight: bolder;">{{ scope.row.type }}</span>
                                    </template>
                                </el-table-column>
                                <el-table-column
                                prop="total_defect_num"
                                label="总缺陷数"
                                align="center">
                                </el-table-column>
                                <el-table-column
                                prop="defect_proportion"
                                label="缺陷占比"
                                align="center">
                                </el-table-column>
                                <el-table-column
                                prop="thousand_defect_num"
                                label="千行缺陷数"
                                align="center">
                                    <template slot-scope="scope">
                                        <span>{{ scope.row.thousand_defect_num }}/KLOC</span>
                                    </template>
                                </el-table-column>
                                <el-table-column
                                prop="defect_concentration"
                                label="缺陷密度"
                                align="center">
                                    <template slot-scope="scope">
                                        <span>{{ scope.row.defect_concentration }}/KLOC</span>
                                    </template>
                                </el-table-column>
                                <el-table-column
                                prop="file_defect_rate"
                                label="文件缺陷率"
                                align="center">
                                </el-table-column>
                            </el-table>
                            <div class="weight_input">
                                <span class="el-input1">权重输入:</span>
                                <el-input type="number" class="el-input1" placeholder="强制类缺陷" v-model="c_info.weights.forced_defect" :min="0" oninput="if(value < 0) value = 0">
                                </el-input>
                                <el-input type="number" class="el-input1" placeholder="可选类缺陷" v-model="c_info.weights.optional_defect" :min="0" oninput="if(value < 0) value = 0">
                                </el-input>
                                <el-input type="number" class="el-input1" placeholder="建议类缺陷" v-model="c_info.weights.suggested_defect" :min="0" oninput="if(value < 0) value = 0">
                                </el-input>
                                <el-button class="el-input1" type="primary" @click="updateWeight()">更新饼图</el-button>
                            </div>
                            <div ref="myChart1" class="my_chart"></div>
                        </div>
                    </el-tab-pane>

                    <el-tab-pane class="el-tab-pane" label="详细信息">
                        <div class="detect_class">
                            <h4>强制类缺陷</h4>
                            <el-table
                            class="total_table"
                            :data="c_info.forcedTable"
                            :header-cell-style="()=>{return 'background: rgb(182, 254, 230);color:black;'}"
                            height="30vh"
                            stripe>
                                <el-table-column
                                prop="standard"
                                label="强制标准"
                                align="center">
                                </el-table-column>
                                <el-table-column
                                prop="source"
                                label="参考来源"
                                align="center">
                                </el-table-column>
                                <el-table-column
                                prop="num"
                                label="总数"
                                align="center">
                                </el-table-column>
                            </el-table>
                        </div>

                        <div class="detect_class">
                            <h4>可选类缺陷</h4>
                            <el-table
                            class="total_table"
                            :data="c_info.optionalTable"
                            :header-cell-style="()=>{return 'background: rgb(182, 254, 230);color:black;'}"
                            height="30vh"
                            stripe>
                                <el-table-column
                                prop="standard"
                                label="可选标准"
                                align="center">
                                </el-table-column>
                                <el-table-column
                                prop="source"
                                label="参考来源"
                                align="center">
                                </el-table-column>
                                <el-table-column
                                prop="num"
                                label="总数"
                                align="center">
                                </el-table-column>
                            </el-table>
                        </div>

                        <div class="detect_class">
                            <h4>建议类缺陷</h4>
                            <el-table
                            class="total_table"
                            :data="c_info.suggestedTable"
                            :header-cell-style="()=>{return 'background: rgb(182, 254, 230);color:black;'}"
                            height="30vh"
                            stripe>
                                <el-table-column
                                prop="standard"
                                label="建议标准"
                                align="center">
                                </el-table-column>
                                <el-table-column
                                prop="source"
                                label="参考来源"
                                align="center">
                                </el-table-column>
                                <el-table-column
                                prop="num"
                                label="总数"
                                align="center">
                                </el-table-column>
                            </el-table>
                        </div>
                    </el-tab-pane>
                </el-tabs>
            </div>
        </el-tab-pane>
        <el-tab-pane label="C++信息" name="c_plus_info" v-if="projectType != 0">
            <div class="file_select">
                文件路径:
                <el-input class="el-input" placeholder="请选择文件" v-model="c_plus_info.selectFile" clearable>
                </el-input>
                <el-button slot="trigger" class="el-button" type="primary" @click="handleSelect" plain>选择文件</el-button>
            </div>
            <div style="width: 100%;">
                <el-tabs tab-position="left">
                    <el-tab-pane label="总览信息">
                        <div>
                            <el-table
                            class="total_table"
                            :data="c_plus_info.overviewTable"
                            :header-cell-style="()=>{return 'background: antiquewhite;color:black;'}"
                            stripe>
                                <el-table-column
                                prop="thousand_defect_num"
                                label="千行缺陷数"
                                align="center">
                                    <template slot-scope="scope">
                                        <span>{{ scope.row.thousand_defect_num }}/KLOC</span>
                                    </template>
                                </el-table-column>
                                <el-table-column
                                prop="defect_concentration"
                                label="缺陷密度"
                                align="center">
                                    <template slot-scope="scope">
                                        <span>{{ scope.row.defect_concentration }}/KLOC</span>
                                    </template>
                                </el-table-column>
                                <el-table-column
                                prop="file_defect_rate"
                                label="文件缺陷率"
                                align="center">
                                </el-table-column>
                            </el-table>
                            <el-table
                            class="total_table"
                            :data="c_plus_info.totalTable"
                            :header-cell-style="()=>{return 'background: antiquewhite;color:black;'}"
                            stripe>
                                <el-table-column
                                prop="type"
                                align="center">
                                    <template slot-scope="scope">
                                        <span style="font-weight: bolder;">{{ scope.row.type }}</span>
                                    </template>
                                </el-table-column>
                                <el-table-column
                                prop="total_defect_num"
                                label="总缺陷数"
                                align="center">
                                </el-table-column>
                                <el-table-column
                                prop="defect_proportion"
                                label="缺陷占比"
                                align="center">
                                </el-table-column>
                                <el-table-column
                                prop="thousand_defect_num"
                                label="千行缺陷数"
                                align="center">
                                    <template slot-scope="scope">
                                        <span>{{ scope.row.thousand_defect_num }}/KLOC</span>
                                    </template>
                                </el-table-column>
                                <el-table-column
                                prop="defect_concentration"
                                label="缺陷密度"
                                align="center">
                                    <template slot-scope="scope">
                                        <span>{{ scope.row.defect_concentration }}/KLOC</span>
                                    </template>
                                </el-table-column>
                                <el-table-column
                                prop="file_defect_rate"
                                label="文件缺陷率"
                                align="center">
                                </el-table-column>
                            </el-table>
                            <div class="weight_input">
                                <span class="el-input1">权重输入:</span>
                                <el-input type="number" class="el-input1" placeholder="强制类缺陷" v-model="c_plus_info.weights.forced_defect" :min="0" oninput="if(value < 0) value = 0">
                                </el-input>
                                <el-input type="number" class="el-input1" placeholder="可选类缺陷" v-model="c_plus_info.weights.optional_defect" :min="0" oninput="if(value < 0) value = 0">
                                </el-input>
                                <el-input type="number" class="el-input1" placeholder="建议类缺陷" v-model="c_plus_info.weights.suggested_defect" :min="0" oninput="if(value < 0) value = 0">
                                </el-input>
                                <el-button class="el-input1" type="primary" @click="updateWeight()">更新饼图</el-button>
                            </div>
                            <div ref="myChart2" class="my_chart"></div>
                        </div>
                    </el-tab-pane>

                    <el-tab-pane class="el-tab-pane" label="详细信息">
                        <div class="detect_class">
                            <h4>强制类缺陷</h4>
                            <el-table
                            class="total_table"
                            :data="c_plus_info.forcedTable"
                            :header-cell-style="()=>{return 'background: rgb(182, 254, 230);color:black;'}"
                            height="30vh"
                            stripe>
                                <el-table-column
                                prop="standard"
                                label="强制标准"
                                align="center">
                                </el-table-column>
                                <el-table-column
                                prop="source"
                                label="参考来源"
                                align="center">
                                </el-table-column>
                                <el-table-column
                                prop="num"
                                label="总数"
                                align="center">
                                </el-table-column>
                            </el-table>
                        </div>

                        <div class="detect_class">
                            <h4>可选类缺陷</h4>
                            <el-table
                            class="total_table"
                            :data="c_plus_info.optionalTable"
                            :header-cell-style="()=>{return 'background: rgb(182, 254, 230);color:black;'}"
                            height="30vh"
                            stripe>
                                <el-table-column
                                prop="standard"
                                label="可选标准"
                                align="center">
                                </el-table-column>
                                <el-table-column
                                prop="source"
                                label="参考来源"
                                align="center">
                                </el-table-column>
                                <el-table-column
                                prop="num"
                                label="总数"
                                align="center">
                                </el-table-column>
                            </el-table>
                        </div>

                        <div class="detect_class">
                            <h4>建议类缺陷</h4>
                            <el-table
                            class="total_table"
                            :data="c_plus_info.suggestedTable"
                            :header-cell-style="()=>{return 'background: rgb(182, 254, 230);color:black;'}"
                            height="30vh"
                            stripe>
                                <el-table-column
                                prop="standard"
                                label="建议标准"
                                align="center">
                                </el-table-column>
                                <el-table-column
                                prop="source"
                                label="参考来源"
                                align="center">
                                </el-table-column>
                                <el-table-column
                                prop="num"
                                label="总数"
                                align="center">
                                </el-table-column>
                            </el-table>
                        </div>
                    </el-tab-pane>
                </el-tabs>
            </div>
        </el-tab-pane>
      </el-tabs>
    </el-row>
    
  </div>
</template>

<script>
import utils from '@/utils/utils'
import config from '@/config'
export default {
    data(){
        return{
            activeName1: this.$store.state.current_project.projectType != 1 ? "c_info" : "c_plus_info",
            projectType: this.$store.state.current_project.projectType,
            c_info: {
                selectFile: "",
                // myChart: null,
                overviewTable: [],
                totalTable: [],
                forcedTable: [],
                optionalTable: [],
                suggestedTable: [],
                weights: {
                    forced_defect: null,
                    optional_defect: null,
                    suggested_defect: null
                },
                initialChartData: [
                    { value: 1, name: "强制类缺陷", key: "forced_defect" },
                    { value: 1, name: "可选类缺陷", key: "optional_defect" },
                    { value: 1, name: "建议类缺陷", key: "suggested_defect" }
                ],
                chartData: [
                    { value: 1, name: "强制类缺陷", key: "forced_defect" },
                    { value: 1, name: "可选类缺陷", key: "optional_defect" },
                    { value: 1, name: "建议类缺陷", key: "suggested_defect" }
                ],
            },
            c_plus_info: {
                selectFile: "",
                // myChart: null,
                overviewTable: [],
                totalTable: [],
                forcedTable: [],
                optionalTable: [],
                suggestedTable: [],
                weights: {
                    forced_defect: null,
                    optional_defect: null,
                    suggested_defect: null
                },
                initialChartData: [
                    { value: 1, name: "强制类缺陷", key: "forced_defect" },
                    { value: 1, name: "可选类缺陷", key: "optional_defect" },
                    { value: 1, name: "建议类缺陷", key: "suggested_defect" }
                ],
                chartData: [
                    { value: 1, name: "强制类缺陷", key: "forced_defect" },
                    { value: 1, name: "可选类缺陷", key: "optional_defect" },
                    { value: 1, name: "建议类缺陷", key: "suggested_defect" }
                ],
            },
            loading: false
        }
    },
    methods: {
        chartInit(){
            let myChart = this.activeName1 == "c_info" ? this.$echarts.init(this.$refs.myChart1) : this.$echarts.init(this.$refs.myChart2)
            let option = {
                title: {
                    text: '缺陷总览',
                    left: 'center'
                },
                tooltip: {
                    trigger: 'item'
                },
                // legend: {
                //     orient: 'vertical',
                //     left: 'left'
                // },
                series: [
                    {
                        // name: 'Access From',
                        type: 'pie',
                        radius: '50%',
                        data: this.activeName1 == "c_info" ? this.c_info.chartData : this.c_plus_info.chartData,
                        emphasis: {
                            itemStyle: {
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.5)'
                            }
                        }
                    }
                ]
            };
            myChart.setOption(option)
            // 根据窗口大小进行动态缩放
            window.addEventListener("resize", () => {
                if(myChart){
                    myChart.resize()
                }
            })
        },
        getData(data){
            if(this.activeName1 == "c_info") {
                this.c_info.overviewTable = [data.overviewData]

                let detectTypeData = data.detectTypeData
                let defect_name_map = {
                    "forced_defect": "强制类缺陷",
                    "optional_defect": "可选类缺陷",
                    "suggested_defect": "建议类缺陷"
                }
                let tableList = []
                this.c_info.chartData = []
                this.c_info.initialChartData = []
                for(let k in detectTypeData){
                    tableList.push({
                        "type": defect_name_map[k],
                        ...detectTypeData[k]
                    })
                    this.c_info.chartData.push({
                        name: defect_name_map[k],
                        value: detectTypeData[k].total_defect_num,
                        key: k
                    })
                    this.c_info.initialChartData.push({
                        name: defect_name_map[k],
                        value: detectTypeData[k].total_defect_num,
                        key: k
                    })
                }
                this.c_info.totalTable = tableList

                this.chartInit()

                this.c_info.forcedTable = data.forcedTable
                this.c_info.optionalTable = data.optionalTable
                this.c_info.suggestedTable = data.suggestedTable
                this.loading = false
            } else {
                this.c_plus_info.overviewTable = [data.overviewData]

                let detectTypeData = data.detectTypeData
                let defect_name_map = {
                    "forced_defect": "强制类缺陷",
                    "optional_defect": "可选类缺陷",
                    "suggested_defect": "建议类缺陷"
                }
                let tableList = []
                this.c_plus_info.chartData = []
                this.c_plus_info.initialChartData = []
                for(let k in detectTypeData){
                    tableList.push({
                        "type": defect_name_map[k],
                        ...detectTypeData[k]
                    })
                    this.c_plus_info.chartData.push({
                        name: defect_name_map[k],
                        value: detectTypeData[k].total_defect_num,
                        key: k
                    })
                    this.c_plus_info.initialChartData.push({
                        name: defect_name_map[k],
                        value: detectTypeData[k].total_defect_num,
                        key: k
                    })
                }
                this.c_plus_info.totalTable = tableList

                this.chartInit()

                this.c_plus_info.forcedTable = data.forcedTable
                this.c_plus_info.optionalTable = data.optionalTable
                this.c_plus_info.suggestedTable = data.suggestedTable
                this.loading = false
            }
        },
        handleSelect(){
            const _this = this
            const inputFile = document.createElement("input")
            inputFile.type = "file"
            inputFile.style.display = "none"
            inputFile.id = "fileInput"
            // inputFile.webkitdirectory = false
            // inputFile.multiple = false
            document.body.appendChild(inputFile)
            inputFile.click()
            let url = this.activeName1 == "c_info" ? "/defect_rate_calculation/C/uploadFile/" : "/defect_rate_calculation/CPP/uploadFile/"
            inputFile.addEventListener("change", function (e) {
                _this.loading = true
                // const file = e.target.files[0];
                // _this.form.codeRoot = file.webkitRelativePath.split("/")[0];
                let formData = new FormData()
                let file = inputFile.files[0]
                if(_this.activeName1 == "c_info") {
                    _this.c_info.selectFile = file.name
                } else {
                    _this.c_plus_info.selectFile = file.name
                }
                formData.append("file", file)
                utils.axiosMethod({
                    method: "POST",
                    url: window.ipConfig.baseUrl + url + _this.$store.state.current_project.name,
                    data: formData,
                    callback: (response)=>{
                        // console.log("$$$$$$", response);
                        _this.getData(response.data)
                    },
                    catch: (err) => {
                        _this.$message.error("上传文件失败")
                    }
                })
            })
        },
        updateWeight(){
            if(this.activeName1 == "c_info") {
                let chartData = this.c_info.initialChartData
                let sum = 0
                for(let index in chartData){
                    this.c_info.chartData[index].value = chartData[index].value * this.c_info.weights[chartData[index].key]
                    this.chartInit()
                    this.c_info.totalTable[index].defect_concentration = this.c_info.totalTable[index].thousand_defect_num * this.c_info.weights[chartData[index].key]
                    sum += this.c_info.totalTable[index].defect_concentration
                }
                this.c_info.overviewTable[0].defect_concentration = sum
            } else {
                let chartData = this.c_plus_info.initialChartData
                let sum = 0
                for(let index in chartData){
                    this.c_plus_info.chartData[index].value = chartData[index].value * this.c_plus_info.weights[chartData[index].key]
                    this.chartInit()
                    this.c_plus_info.totalTable[index].defect_concentration = this.c_plus_info.totalTable[index].thousand_defect_num * this.c_plus_info.weights[chartData[index].key]
                    sum += this.c_plus_info.totalTable[index].defect_concentration
                }
                this.c_plus_info.overviewTable[0].defect_concentration = sum
            }
        }
    }
}
</script>

<style scoped>
.container{
    height: 89vh;
    width: 100vw;
}
.file_select{
    display: flex;
    height: 6vh;
    justify-content: center;
    align-items: center;
}
.el-input{
    width: 15vw;
    margin-left: 2vw;
    margin-right: 2vw;
}
.el-button{
    height: 4vh;
}
.total_table{
    width: 90%;
    margin: 0 auto;
}
.weight_input{
    display: flex;
    height: 6vh;
    justify-content: center;
    align-items: center;
    margin-top: 5px;
    margin-bottom: 5px;
}
.el-input1{
    width: 8vw;
    margin-left: 3vw;
    margin-right: 3vw;
}
.my_chart{
    height: 50vh;
    width: 50vw;
    margin: 0 auto;
}
.el-tab-pane{
    height: 83vh;
    overflow-y: scroll;
}
.detect_class{
    width: 80vw;
    margin: 3vh auto;
}
</style>