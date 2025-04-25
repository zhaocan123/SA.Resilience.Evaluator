<template>
    <div>
        <el-tabs type="border-card" v-model="activeName" @tab-click="handleClick">
            <el-tab-pane label="参数个数" name="paramNum"></el-tab-pane>
            <el-tab-pane label="变量个数" name="variableNum"></el-tab-pane>
            <el-tab-pane label="圈复杂度" name="cyclomaticComplexity"></el-tab-pane>
            <el-tab-pane label="代码行" name="codeNum"></el-tab-pane>
            <el-tab-pane label="出度" name="outDegree"></el-tab-pane>
            <el-tab-pane label="入度" name="inDegree"></el-tab-pane>
            <div>
                <el-descriptions :column="6" size="mini" border>
                    <el-descriptions-item :label="`${this.labelName}变化的函数个数`">{{ functionLevelInfo[activeName].totalNum }}</el-descriptions-item>
                    <el-descriptions-item label="占比">{{ functionLevelInfo[activeName].totalProp }}</el-descriptions-item>
                    <el-descriptions-item :label="`${this.labelName}增加的函数个数`" :labelStyle="{'background': '#E1F3D8'}">{{ functionLevelInfo[activeName].increaseNum }}</el-descriptions-item>
                    <el-descriptions-item label="占比" :labelStyle="{'background': '#E1F3D8'}">{{ functionLevelInfo[activeName].increaseProp }}</el-descriptions-item>
                    <el-descriptions-item :label="`${this.labelName}降低的函数个数`" :labelStyle="{'background': '#FDE2E2'}">{{ functionLevelInfo[activeName].decreaseNum }}</el-descriptions-item>
                    <el-descriptions-item label="占比" :labelStyle="{'background': '#FDE2E2'}">{{ functionLevelInfo[activeName].decreaseProp }}</el-descriptions-item>
                </el-descriptions>
                <div class="box">
                    <div ref="myChart" class="my_chart"></div>
                    <el-table
                    :data="functionLevelInfo[activeName].changeinfoList"
                    :header-cell-style="()=>{return 'background: rgb(176, 238, 203);color:black;'}"
                    height="100%"
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
        </el-tabs>
    </div>
</template>

<script>
import Cache from '@/utils/cache'
export default {
    props: ["typeName"],
    watch: {
        typeName(newVal) {
            this.typeName = newVal
            this.getData()
        }
    },
    data(){
        return {
            functionLevelInfo: null,
            activeName: "paramNum",
            labelName: "参数个数",
            myChart: null,
            selectedVersion: null,
            latestVersion: null
        }
    },    
    mounted(){
        this.getData()
        // setTimeout(this.chartInit, 1000)
    },
    methods:{
        getData() {
            let data = Cache.getCache("change_information_detection_data")
            this.selectedVersion = data[this.typeName].systemLevel.versionSelected.name
            this.latestVersion = data[this.typeName].systemLevel.versionLatest.name
            this.functionLevelInfo = data.c_info.functionLevel
            // this.chartInit()
            setTimeout(this.chartInit, 500)
        },
        chartInit() {
            // console.log("===================", this.functionLevelInfo);
            let totalNum = parseInt(this.functionLevelInfo[this.activeName].totalNum)
            let xAxis = new Array(totalNum).fill(1).map((v, i) => ++i)
            // console.log("xAxis", xAxis);
            let selectedValues = []
            let latestValues = []
            let changeinfoList = this.functionLevelInfo[this.activeName].changeinfoList
            for(let index in changeinfoList) {
                selectedValues.push(changeinfoList[index].selectedValue)
                latestValues.push(changeinfoList[index].latestValue)
            }
            // console.log("selectedValues", selectedValues);

            this.myChart = this.$echarts.init(this.$refs.myChart)
            let option = {
                title: {
                    text: `函数${this.labelName}变更统计图`,
                    left: 'center'
                },
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                    type: 'shadow'
                    }
                },
                legend: {
                    left: "5%"
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                yAxis: {
                    type: 'value',
                    boundaryGap: [0, 0.01]
                },
                xAxis: {
                    type: 'category',
                    data: xAxis
                },
                series: [
                    {
                        name: this.selectedVersion,
                        type: 'bar',
                        data: selectedValues,
                        itemStyle: {
                            color: 'red'
                        }
                    },
                    {
                        name: this.latestVersion,
                        type: 'bar',
                        data: latestValues,
                        itemStyle: {
                            color: 'orange'
                        }
                    }
                ]
            };
            this.myChart.setOption(option)
            let myChart = this.myChart
            // 根据窗口大小进行动态缩放
            window.addEventListener("resize", () => {
                if(myChart){
                    myChart.resize()
                }
            })
        },
        handleClick(tap){
            // console.log("############", tap);
            this.labelName = tap.label
            this.chartInit()
        }
    }
}
</script>

<style>
    .box{
        /* height: 60vh; */
        width: 100vw;
        display: flex;
        padding-top: 2%;
        padding-right: 4vw;
    }
    .my_chart{
        width: 60vw;
        /* height: 60vh; */
    }
</style>