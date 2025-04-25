<template>
    <div class="main">
        <!-- <el-button style="position: absolute; right: 2vw;" type="primary" @click="dialogPdfVisible = true">打印</el-button> -->
        <div class="main-left">
            <div class="tables">
                <div class="table1">
                    <el-table :data="tableData1" border
                        :header-cell-style="()=>{return 'background: lightgreen;color:black;'}">
                        <!-- <el-table-column
                            prop="dirNumber"
                            label="文件夹"
                            align="center">
                        </el-table-column> -->
                        <el-table-column prop="fileNumber" label="文件" align="center">
                        </el-table-column>
                        <el-table-column prop="functionNumber" label="函数" align="center">
                        </el-table-column>
                        <el-table-column prop="codeLine" label="总代码行数" align="center">
                        </el-table-column>
                    </el-table>
                </div>
                <!-- <div class="table2">
                    <el-table :data="tableData2" border
                        :header-cell-style="()=>{return 'background: antiquewhite;color:black;'}">
                        <el-table-column prop="codeLine" label="总代码行数" align="center">
                        </el-table-column>
                        <el-table-column prop="codeLineExp" label="有效代码行" align="center">
                        </el-table-column>
                        <el-table-column prop="commentLine" label="注释行" align="center">
                        </el-table-column>
                        <el-table-column prop="commentLineExp" label="有效注释行" align="center">
                        </el-table-column>
                    </el-table>
                </div> -->
                <div class="table4">
                    <el-table :data="tableData4" border
                        :header-cell-style="()=>{return 'background: lightgreen;color:black;'}">
                        <el-table-column prop="codeLineExpProp" label="有效代码行占比" align="center">
                        </el-table-column>
                        <el-table-column prop="emptyLineProp" label="空行占比" align="center">
                        </el-table-column>
                        <el-table-column prop="libraryCount" label="外部库依赖个数" align="center">
                        </el-table-column>
                    </el-table>
                </div>

                <div class="table5">
                    <el-table :data="tableData5" border
                        :header-cell-style="()=>{return 'background: lightgreen;color:black;'}">
                        <el-table-column prop="dataInCount" label="数据入口个数" align="center">
                        </el-table-column>
                        <el-table-column prop="dataOutCount" label="数据出口个数" align="center">
                        </el-table-column>
                        <el-table-column prop="unTrustedDataCount" label="不可信数据元素个数" align="center">
                        </el-table-column>
                    </el-table>
                </div>

                <div class="table6">
                    <el-table :data="tableData6" border
                        :header-cell-style="()=>{return 'background: lightgreen;color:black;'}">
                        <el-table-column prop="attackSetSize" label="潜在攻击集合大小" align="center">
                        </el-table-column>
                        <el-table-column prop="attackSetCat" label="潜在攻击种类" align="center">
                        </el-table-column>
                        <el-table-column prop="resilienceResult" label="韧性评估结果" align="center">
                        </el-table-column>
                    </el-table>
                </div>

            </div>
        </div>
        <div ref="myChart" class="main-right"></div>

        

        <!-- <el-dialog class="scroll_none" title="打印预览" top="2vh" :visible.sync="dialogPdfVisible" width="60vw" center>
            <pdf_project_info v-if="dialogPdfVisible" ref="print" style="height: 70vh; margin: 0 auto; overflow-y: scroll;"></pdf_project_info>
            <span slot="footer" class="dialog-footer">
                <el-button @click="dialogPdfVisible = false">取 消</el-button>
                <el-button type="primary" @click="goPrint">打 印</el-button>
            </span>
        </el-dialog> -->
    </div>
</template>

<script>
import utils from "@/utils/utils"
import Cache from "@/utils/cache"
import pdf_project_info from "@/views/pdf_template/pdf_project_info.vue"

export default {
    components: {
        pdf_project_info
    },
    data(){
        return {
            myChart: null,
            option: {
                title: {
                    text: this.$store.state.current_project.name + '文件种类',
                    left: 'center',
                    top: '5%'
                },
                tooltip: {
                    trigger: 'item'
                },
                legend: {
                    orient: 'vertical',
                    left: 'left',
                    top: '5%'
                },
                series: [
                    {
                        // name: 'Access From',
                        type: 'pie',
                        radius: '50%',
                        data: [
                            { value: 1048, name: 'header' },
                            { value: 735, name: 'c_source' },
                            { value: 580, name: 'c++_source' },
                            // { value: 484, name: 'other_file' }
                        ],
                        emphasis: {
                            itemStyle: {
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.5)'
                            }
                        }
                    }
                ]
            },
            tableData1: [],
            tableData2: [],
            tableData3: [],
            tableData4: [],
            tableData5: [],
            tableData6: [],
            dialogPdfVisible: false
        }
    },
    mounted(){
        this.getData()
    },
    methods: {
        chartInit(){
            this.myChart = this.$echarts.init(this.$refs.myChart)
            this.myChart.setOption(this.option)
            let myChart = this.myChart
            // 根据窗口大小进行动态缩放
            window.addEventListener("resize", () => {
                if(myChart){
                    myChart.resize()
                }
            })
        },
        getData() {
            utils.axiosMethod({
                method: "GET",
                url: window.ipConfig.baseUrl + "/projectInfo/" + this.$store.state.current_project.name,
                callback: (response)=>{
                    let data = response.data
                    Cache.setCache("project_info", data)
                    this.option = {
                        title: {
                            text: this.$store.state.current_project.name + '文件种类',
                            left: 'center',
                            top: '5%'
                        },
                        tooltip: {
                            trigger: 'item'
                        },
                        legend: {
                            orient: 'vertical',
                            left: 'left',
                            top: '5%'
                        },
                        series: [
                            {
                                // name: 'Access From',
                                type: 'pie',
                                radius: '50%',
                                data: data.fileProp,
                                emphasis: {
                                    itemStyle: {
                                        shadowBlur: 10,
                                        shadowOffsetX: 0,
                                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                                    }
                                }
                            }
                        ]
                    }
                    this.chartInit()

                    this.tableData1 = [{
                        functionNumber: data.functionNumber + "个",
                        fileNumber: data.fileNumber + "个",
                        codeLine: data.codeLine + "行"
                    }]
                    this.tableData2 = [{
                        codeLine: data.codeLine + "行",
                        codeLineExp: data.codeLineExp + "行",
                        commentLine: data.commentLine + "行",
                        commentLineExp: data.commentLineExp + "行"
                    }]
                    this.tableData3 = [{
                        codeLineExpProp: data.codeLineExpProp,
                        emptyLineProp: data.emptyLineProp,
                        commentLineExpProp: data.commentLineExpProp
                    }]
                    this.tableData4 = [
                        {
                            codeLineExpProp: data.codeLineExpProp,
                            emptyLineProp: data.emptyLineProp,
                            libraryCount: data.libraryCount
                        }
                    ]
                    this.tableData5 = [
                        {   
                            dataInCount: data.dataInCount,
                            dataOutCount: data.dataOutCount,
                            unTrustedDataCount: data.unTrustedDataCount
                        }
                    ]
                    this.tableData6 = [
                        {
                            attackSetSize: data.attackSetSize,
                            attackSetCat: data.attackSetCat,
                            resilienceResult: data.resilienceResult
                        }
                    ]

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
.main {
    display: flex;
    flex-direction: row;
}

.main-left {
    height: 89vh;
    width: 50vw;
    padding-left: 3%;
}

.main-right {
    height: 89vh;
    width: 50%;
    padding: 3% 3% 3% 3%;
}

.tables {
    height: 100%;
    width: 100%;
    padding-top: 5%;
}

.table1 {
    width: 90%;
    margin-bottom: 10%;
}

.table2 {
    width: 90%;
    margin-bottom: 10%;
}

.table3 {
    width: 90%;
    margin-bottom: 10%;
}
.table4 {
    width: 90%;
    margin-bottom: 10%;
}

.table5 {
    width: 90%;
    margin-bottom: 10%;
}

.table6 {
    width: 90%;
}
</style>